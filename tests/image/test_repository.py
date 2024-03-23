import pytest

from src.database.database import Database
from src.image.repository import ImageRepository
from src.image.schema import ImageSchema


@pytest.fixture(scope="function")
def image_repository_fixture():
    return ImageRepository(database=Database(":memory:"))


def test_image_table_exists(image_repository_fixture: ImageRepository):
    with image_repository_fixture._database.cursor as cursor:
        table = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'image'").fetchone()
        assert table is not None


def test_save_urls_one_url(image_repository_fixture: ImageRepository):
    images = [ImageSchema(search_term="term", url="url")]

    image_repository_fixture.save_urls(images)

    with image_repository_fixture._database.cursor as cursor:
        rows = cursor.execute(f"SELECT * FROM image").fetchall()
        assert len(rows) == 1


def test_save_urls_two_different_urls(image_repository_fixture: ImageRepository):
    images = [ImageSchema(search_term="term", url="url"), ImageSchema(search_term="term", url="url_2")]

    image_repository_fixture.save_urls(images)

    with image_repository_fixture._database.cursor as cursor:
        rows = cursor.execute(f"SELECT * FROM image").fetchall()
        assert len(rows) == 2


def test_save_urls_duplicate_urls(image_repository_fixture: ImageRepository):
    images = [ImageSchema(search_term="term", url="url")] * 2

    image_repository_fixture.save_urls(images)

    with image_repository_fixture._database.cursor as cursor:
        rows = cursor.execute(f"SELECT * FROM image").fetchall()
        assert len(rows) == 1


def test_list(image_repository_fixture: ImageRepository):
    urls = [{"search_term": "term", "url": "url"}]
    with image_repository_fixture._database.cursor as cursor:
        cursor.executemany(
            f"INSERT OR IGNORE INTO image (search_term, url) VALUES(:search_term, :url)",
            urls,
        )

    result = image_repository_fixture.list()
    assert len(result) == 1
    assert isinstance(result[0], ImageSchema)
