import sqlite3
from contextlib import contextmanager


class Database:
    def __init__(self, path: str | None = None) -> None:
        self._path = path
        self._connection = sqlite3.connect(self._path or ":memory:", check_same_thread=False)
        self._connection.row_factory = sqlite3.Row

    @property
    @contextmanager
    def cursor(self):
        cursor = self._connection.cursor()
        try:
            yield cursor
        except Exception as exc:
            self._connection.rollback()
            raise exc
        else:
            self._connection.commit()
        finally:
            cursor.close()
