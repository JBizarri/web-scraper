import pytest

from src.image.scraper import ImageScraper


@pytest.fixture
def image_scraper_fixture():
    return ImageScraper()


def test_get_urls(image_scraper_fixture: ImageScraper):
    search = "dogs"
    size = 1

    result = image_scraper_fixture.get_urls(search, size)

    assert len(result) == size
    assert result[0].startswith("https://")
