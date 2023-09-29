from typing import Any
from pydantic import BaseModel

class ResponseSchema(BaseModel):
    message: str
    metadata: dict | None = None

class ResponseWithTokenSchema(BaseModel):
    message: str
    access_token: str
    refresh_token: str
    token_type: str
    metadata: dict | None = None

class Page(BaseModel):
    page_size: int = 10
    page_number: int = 1

class ResponseListQuery(BaseModel):
    data: Any
    page_count: int
    count: int

class ResponseQuery(BaseModel):
    data: Any
