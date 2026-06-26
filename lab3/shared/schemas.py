from pydantic import BaseModel, HttpUrl


class ParseRequest(BaseModel):
    url: HttpUrl


class ParseResult(BaseModel):
    url: str
    title: str
    saved_id: int
    saved_to: str = "tag"
