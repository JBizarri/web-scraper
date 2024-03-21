import sqlite3
from contextlib import contextmanager
from typing import Optional


class Database:
    def __init__(self, path: Optional[str] = None) -> None:
        self._path = path

    @property
    @contextmanager
    def connection(self):
        connection = sqlite3.connect(self._path or ":memory:", check_same_thread=False)
        connection.row_factory = sqlite3.Row

        try:
            yield connection
        except Exception:
            connection.rollback()
            connection.close()
        else:
            connection.commit()
        finally:
            connection.close()
