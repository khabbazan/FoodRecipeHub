from typing import Any
from pydantic import Field, BaseModel


class ResponseSchema(BaseModel):
    message: str = Field(None, description="A message included in the response.")
    metadata: dict | None = Field(None, description="Optional metadata included in the response.")


class ResponseWithTokenSchema(BaseModel):
    message: str = Field(description="A message included in the response.")
    access_token: str = Field(description="An access token included in the response.")
    refresh_token: str = Field(description="A refresh token included in the response.")
    token_type: str = Field(description="The type of the token included in the response.")
    metadata: dict | None = Field(None, description="Optional metadata included in the response.")


class Page(BaseModel):
    page_size: int = Field(10, description="The number of items per page in a paged response.")
    page_number: int = Field(1, description="The current page number in a paged response.")


class ResponseListQuery(BaseModel):
    data: Any = Field(description="The data included in the response.")
    page_count: int = Field(description="The total number of pages in a paged response.")
    count: int = Field(description="The total count of items in a paged response.")


class ResponseQuery(BaseModel):
    data: Any = Field(description="The data included in the response.")
