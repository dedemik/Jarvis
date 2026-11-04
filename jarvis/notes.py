import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


class NoteStore:
    def __init__(self, database_path: str | Path | None = None):
        self.database_path = (
            Path(database_path)
            if database_path is not None
            else Path.home() / ".jarvis" / "jarvis.sqlite3"
        )

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database_path)
        try:
            with connection:
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL
                    )
                    """
                )
                yield connection
        finally:
            connection.close()

    def add(self, content: str) -> int:
        with self._connection() as connection:
            cursor = connection.execute(
                "INSERT INTO notes (content) VALUES (?)",
                (content,),
            )
            note_id = cursor.lastrowid
            if note_id is None:
                raise sqlite3.DatabaseError("Not kimliği oluşturulamadı.")
            return note_id

    def list_all(self) -> list[tuple[int, str]]:
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT id, content FROM notes ORDER BY id"
            ).fetchall()
        return [(int(note_id), content) for note_id, content in rows]

    def delete(self, note_id: int) -> bool:
        with self._connection() as connection:
            cursor = connection.execute(
                "DELETE FROM notes WHERE id = ?",
                (note_id,),
            )
            return cursor.rowcount > 0
