from fastapi import APIRouter

from ..responses import HttpResponse
from .model import ImageModel
from .service import ImageService


class ImageRouter(APIRouter):
    def __init__(self, *, service: ImageService) -> None:
        self._service = service

        super().__init__(prefix="/images", tags=["Images"])
        self.add_api_route(path="", endpoint=self.list(), methods=["GET"], response_model=list[ImageModel], summary="List all stored image URLs")
        self.add_api_route(path="", endpoint=self.create(), methods=["POST"], response_model=HttpResponse, summary="Store image URLs")

    def list(self):
        def route():
            return self._service.list()

        return route

    def create(self):
        def route():
            self._service.search_urls("dogs")
            return {"message": "ok"}

        return route
