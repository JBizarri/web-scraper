from ..database import Database
from .schema import ImageSchema


class ImageRepository:
    __table_name__ = "image"

    def __init__(self, *, database: Database) -> None:
        self._database = database
        self.init()

    def init(self):
        with self._database.cursor as cursor:
            table_exists = cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name = ?", (ImageRepository.__table_name__,)
            ).fetchone()
            if not table_exists:
                cursor.execute(
                    f"CREATE TABLE {ImageRepository.__table_name__}(search_term VARCHAR, url TEXT, UNIQUE(search_term, url))"
                )

    def save_urls(self, urls: list[ImageSchema]):
        with self._database.cursor as cursor:
            data = [url.model_dump() for url in urls]
            cursor.executemany(
                f"INSERT OR IGNORE INTO {ImageRepository.__table_name__} (search_term, url) VALUES(:search_term, :url)",
                data,
            )

    def list(self) -> list[ImageSchema]:
        with self._database.cursor as cursor:
            rows = cursor.execute(f"SELECT * FROM {ImageRepository.__table_name__}").fetchall()
            return [ImageSchema.model_validate(dict(row)) for row in rows]
