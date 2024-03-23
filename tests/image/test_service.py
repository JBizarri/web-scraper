from unittest.mock import MagicMock

from fastapi import HTTPException
import pytest

from src.image.schema import ImageSchema
from src.image.service import ImageService


@pytest.fixture
def image_service_fixture():
    return ImageService(scraper=MagicMock(), repository=MagicMock())


def test_search_urls_success(image_service_fixture: ImageService):
    search = "dogs"
    size = 10

    image_service_fixture._scraper.get_urls = MagicMock(return_value=["url"] * size)

    result = image_service_fixture.search_urls(search, size)

    assert isinstance(result, list)
    assert len(result) == size
    for r in result:
        assert isinstance(r, ImageSchema)
        assert r.search_term == search
        assert isinstance(r.url, str)

    image_service_fixture._scraper.get_urls.assert_called_once_with(search, size)
    image_service_fixture._repository.save_urls.assert_called_once_with(result)


def test_search_urls_error(image_service_fixture: ImageService):
    search = "dogs"
    size = 10

    image_service_fixture._scraper.get_urls = MagicMock(return_value=[])

    with pytest.raises(HTTPException) as exc:
        image_service_fixture.search_urls(search, size)

    assert exc.value.status_code == 500
    assert exc.value.detail == "Could not find the URLs"
    image_service_fixture._scraper.get_urls.assert_called_once_with(search, size)
    image_service_fixture._repository.save_urls.assert_not_called()
