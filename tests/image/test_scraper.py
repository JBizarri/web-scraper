from typing import Any

import pytest

from src.image.scraper import ImageScraper


@pytest.fixture
def image_scraper_fixture():
    return ImageScraper()


@pytest.mark.parametrize(
    "data", [{"search": "dogs", "size": 1}, {"search": "dogs", "size": 5}, {"search": "dogs", "size": 10}]
)
def test_get_urls(data: dict[str, Any], image_scraper_fixture: ImageScraper):
    result = image_scraper_fixture.get_urls(data["search"], data["size"])

    assert isinstance(result, list)
    assert len(result) == data["size"]
    for r in result:
        assert r.startswith("https://") or r.startswith("http://")
