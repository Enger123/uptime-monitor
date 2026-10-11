from pydantic import BaseModel

class UrlGiven(BaseModel):
    name: str | None = None
    url: str

