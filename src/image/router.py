from fastapi import APIRouter

from ..responses import HttpResponse
from .schema import ImageSchema, SearchImageSchema
from .service import ImageService


class ImageRouter(APIRouter):
    def __init__(self, *, service: ImageService) -> None:
        self._service = service

        super().__init__(prefix="/images", tags=["Images"])
        self.add_api_route(path="", endpoint=self.list(), methods=["GET"], response_model=list[ImageSchema], summary="List all stored image URLs")
        self.add_api_route(path="", endpoint=self.create(), methods=["POST"], response_model=HttpResponse, summary="Store image URLs")

    def list(self):
        def route():
            return self._service.list()

        return route

    def create(self):
        def route(data: SearchImageSchema):
            self._service.search_urls(data.search_term, data.size)
            return {"message": "ok"}

        return route
