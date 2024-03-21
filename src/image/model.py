from pydantic import BaseModel


class ImageModel(BaseModel):
    search_term: str
    url: str
