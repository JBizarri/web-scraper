from pydantic import BaseModel, Field


class ImageSchema(BaseModel):
    search_term: str
    url: str


class SearchImageSchema(BaseModel):
    search_term: str = Field(default="dogs")
    size: int = Field(default=1000)
