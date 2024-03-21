import sqlite3
from typing import Optional


class Database:
    def __init__(self, path: Optional[str] = None) -> None:
        self._connection = sqlite3.connect(path or ":memory:", check_same_thread=False)
        self._connection.row_factory = sqlite3.Row

    @property
    def connection(self):
        return self._connection
