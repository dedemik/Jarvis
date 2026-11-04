import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator


class ReminderStore:
    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS reminders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        due_at TEXT NOT NULL,
                        notified INTEGER NOT NULL DEFAULT 0
                    )
                    """
                )
                yield connection
        finally:
            connection.close()

    def add(self, content: str, due_at: datetime) -> int:
        with self._connection() as connection:
            cursor = connection.execute(
                "INSERT INTO reminders (content, due_at) VALUES (?, ?)",
                (content, due_at.isoformat(timespec="minutes")),
            )
            reminder_id = cursor.lastrowid
            if reminder_id is None:
                raise sqlite3.DatabaseError("Hatırlatıcı kimliği oluşturulamadı.")
            return reminder_id

    def list_all(self) -> list[tuple[int, str, datetime, bool]]:
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT id, content, due_at, notified FROM reminders ORDER BY due_at, id"
            ).fetchall()
        return [
            (int(reminder_id), content, datetime.fromisoformat(due_at), bool(notified))
            for reminder_id, content, due_at, notified in rows
        ]

    def notify_due(self, now: datetime | None = None) -> list[tuple[int, str]]:
        if not self.database_path.exists():
            return []
        current_time = now or datetime.now()
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT id, content, due_at FROM reminders WHERE notified = 0"
            ).fetchall()
            due_reminders = [
                (int(reminder_id), content)
                for reminder_id, content, due_at in rows
                if datetime.fromisoformat(due_at) <= current_time
            ]
            connection.executemany(
                "UPDATE reminders SET notified = 1 WHERE id = ?",
                [(reminder_id,) for reminder_id, _ in due_reminders],
            )
        return due_reminders

    def delete(self, reminder_id: int) -> bool:
        with self._connection() as connection:
            cursor = connection.execute(
                "DELETE FROM reminders WHERE id = ?",
                (reminder_id,),
            )
            return cursor.rowcount > 0
