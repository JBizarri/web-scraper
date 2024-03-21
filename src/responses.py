from pydantic import BaseModel

class HttpResponse(BaseModel):
    message: str
