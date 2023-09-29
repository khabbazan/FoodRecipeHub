
import re
from typing import Optional
from typing import Any
from pydantic import BaseModel
from pydantic import field_validator

from src.resources.recipes.enums import TAGEnum
from fastapi_babel.core import make_gettext as _

class RecipeSchema(BaseModel):
    title: str
    content: str
    tags: list[TAGEnum]
    is_active: bool = True

    def manual_all_validations(self, *args, **kwargs):
        validation_functions = [
            {"name": self.validate_title, "args": [self.title]},
            {"name": self.validate_content, "args": [self.content]},
        ]
        for func in validation_functions:
            func["name"](*func["args"])
        return True

    @field_validator('title')
    def validate_title(cls, title):
        len_ptr = re.compile(r'^\w.{8,}\w$')
        if not re.match(len_ptr, title):
            raise ValueError(_('Recipe title must contain at least 8 characters'))
        return title

    @field_validator('content')
    def validate_content(cls, content):
        len_ptr = re.compile(r'^\w.{8,}\w$')  # todo: update for 50 chars
        if not re.match(len_ptr, content):
            raise ValueError(_('Recipe content must contain at least 50 characters'))
        return content


class TagQuerySchema(BaseModel):
    title: str
    display_title: str

    class Config:
        from_attributes = True


class RecipeQuerySchemaSimple(BaseModel):
    uuid: str
    title: str
    user: Any

    class Config:
        from_attributes = True


class RecipeQuerySchema(BaseModel):
    uuid: str
    title: str
    content: str
    is_active: bool
    user: Any
    created_at: str
    tags: list[TagQuerySchema] = []

    class Config:
        from_attributes = True


class RecipeFilterSchema(BaseModel):
    is_active: Optional[bool] = None


class RecipeEditSchema(BaseModel):
    uuid: str
    title: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = True
    tags: Optional[list[TAGEnum]] = None
