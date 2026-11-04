import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


class TaskStore:
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
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        completed INTEGER NOT NULL DEFAULT 0
                    )
                    """
                )
                yield connection
        finally:
            connection.close()

    def add(self, content: str) -> int:
        with self._connection() as connection:
            cursor = connection.execute(
                "INSERT INTO tasks (content) VALUES (?)",
                (content,),
            )
            task_id = cursor.lastrowid
            if task_id is None:
                raise sqlite3.DatabaseError("Görev kimliği oluşturulamadı.")
            return task_id

    def list_all(self) -> list[tuple[int, str, bool]]:
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT id, content, completed FROM tasks ORDER BY id"
            ).fetchall()
        return [
            (int(task_id), content, bool(completed))
            for task_id, content, completed in rows
        ]

    def complete(self, task_id: int) -> bool:
        with self._connection() as connection:
            cursor = connection.execute(
                "UPDATE tasks SET completed = 1 "
                "WHERE id = ? AND completed = 0",
                (task_id,),
            )
            return cursor.rowcount > 0

    def delete(self, task_id: int) -> bool:
        with self._connection() as connection:
            cursor = connection.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,),
            )
            return cursor.rowcount > 0
