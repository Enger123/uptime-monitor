from pydantic import BaseModel, HttpUrl

class UrlGiven(BaseModel):
    name: str | None = None
    url: HttpUrl

class MonitorResponse(BaseModel):
    id: int
    name: str | None = None
    url: str
    model_config={'from_attributes': True}

class MonitorUpdateSchema(BaseModel):
    name: str | None = None
    url: HttpUrl | None = None


    

