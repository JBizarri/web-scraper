from .scraper import ImageScraper
from .repository import ImageRepository


class ImageService:
    def __init__(self, *, scraper: ImageScraper, repository: ImageRepository):
        self._scraper = scraper
        self._repository = repository

    def search_urls(self, search: str):
        urls = self._scraper.get_urls(search)
        self._repository.save_urls(search, urls)

    def list(self):
        return self._repository.list()
