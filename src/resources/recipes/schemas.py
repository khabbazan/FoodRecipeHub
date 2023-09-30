import re
from typing import Optional, Any
from pydantic import Field, BaseModel, field_validator

from src.resources.recipes.enums import TAGEnum
from fastapi_babel.core import make_gettext as _


class RecipeSchema(BaseModel):
    title: str = Field(description="The title of the recipe.")
    content: str = Field(description="The content or description of the recipe.")
    tags: list[TAGEnum] = Field(description="A list of tags associated with the recipe.")
    is_active: bool = Field(True, description="Indicates whether the recipe is active or not.")

    def manual_all_validations(self, *args, **kwargs):
        """
        Manually validate recipe data using a list of validation functions.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            bool: True if all validations pass, otherwise raises ValueError.
        """
        validation_functions = [
            {"name": self.validate_title, "args": [self.title]},
            {"name": self.validate_content, "args": [self.content]},
        ]
        for func in validation_functions:
            func["name"](*func["args"])
        return True

    @field_validator("title")
    def validate_title(cls, title):
        """
        Validate the recipe title to ensure it has at least 8 characters.

        Args:
            title (str): The title of the recipe.

        Returns:
            str: The validated recipe title.

        Raises:
            ValueError: If the title does not meet the length requirement.
        """
        len_ptr = re.compile(r"^\w.{8,}\w$")
        if not re.match(len_ptr, title):
            raise ValueError(_("Recipe title must contain at least 8 characters"))
        return title

    @field_validator("content")
    def validate_content(cls, content):
        """
        Validate the recipe content to ensure it has at least 50 characters.

        Args:
            content (str): The content or description of the recipe.

        Returns:
            str: The validated recipe content.

        Raises:
            ValueError: If the content does not meet the length requirement.
        """
        len_ptr = re.compile(r"^\w.{8,}\w$")  # todo: update for 50 chars
        if not re.match(len_ptr, content):
            raise ValueError(_("Recipe content must contain at least 50 characters"))
        return content


class TagQuerySchema(BaseModel):
    title: str = Field(description="The title of the tag.")
    display_title: str = Field(description="The display title of the tag.")

    class Config:
        from_attributes = True


class RecipeQuerySchemaSimple(BaseModel):
    uuid: str = Field(description="The UUID of the recipe.")
    title: str = Field(description="The title of the recipe.")
    user: Any = Field(description="Information about the user associated with the recipe.")

    class Config:
        from_attributes = True


class RecipeQuerySchema(BaseModel):
    uuid: str = Field(description="The UUID of the recipe.")
    title: str = Field(description="The title of the recipe.")
    content: str = Field(description="The content or description of the recipe.")
    is_active: bool = Field(description="Indicates whether the recipe is active or not.")
    user: Any = Field(description="Information about the user associated with the recipe.")
    created_at: str = Field(description="The timestamp indicating when the recipe was created.")
    tags: list[TagQuerySchema] = Field([], description="A list of tags associated with the recipe.")

    class Config:
        from_attributes = True


class RecipeFilterSchema(BaseModel):
    is_active: Optional[bool] = Field(None, description="Filter by recipe's active status.")


class RecipeEditSchema(BaseModel):
    uuid: str = Field(description="The UUID of the recipe.")
    title: Optional[str] = Field(None, description="The updated title of the recipe.")
    content: Optional[str] = Field(None, description="The updated content or description of the recipe.")
    is_active: Optional[bool] = Field(None, description="The updated active status of the recipe.")
    tags: Optional[list[TAGEnum]] = Field(None, description="The updated list of tags associated with the recipe.")
