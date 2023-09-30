import re
from pydantic import Field
from pydantic import BaseModel
from pydantic import field_validator

from fastapi_babel import _


class ImageSchema(BaseModel):
    name: str = Field(description="The name of the image.")
    base64_image: str = Field(description="The base64-encoded content of the image.")

    def manual_all_validations(self, *args, **kwargs):
        """
        Manually validate image data using a list of validation functions.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            bool: True if all validations pass, otherwise raises ValueError.
        """
        validation_functions = [
            {"name": self.validate_image_name, "args": [self.name]},
            {"name": self.validate_base64_string, "args": [self.image_base64]},
        ]
        for func in validation_functions:
            func["name"](*func["args"])
        return True

    @field_validator("name")
    def validate_image_name(cls, image_name):
        """
        Validate the image name to ensure it has a valid file extension.

        Args:
            image_name (str): The name of the image.

        Returns:
            str: The validated image name.

        Raises:
            ValueError: If the image name is not valid.
        """
        if image_name:
            pattern = r"^[a-zA-Z0-9_-]+\.(jpg|jpeg|png|gif|bmp|svg|webp)$"

            if not re.match(pattern, image_name):
                raise ValueError(_("Image name is not valid. There is no file extension."))
        return image_name

    @field_validator("base64_image")
    def validate_base64_string(cls, base64_image):
        """
        Validate the base64-encoded image content.

        Args:
            base64_image (str): The base64-encoded content of the image.

        Returns:
            str: The validated base64-encoded image content.

        Raises:
            ValueError: If the base64 content is not valid.
        """
        if base64_image:
            pattern = r"^data:image/(png|jpeg|jpg|gif|bmp|webp);base64,([A-Za-z0-9+/]+={0,2})$"

            if not re.match(pattern, base64_image):
                raise ValueError(_("Base64 content is not valid"))
        return base64_image


class ImageQuerySchema(BaseModel):
    url: str = Field(description="The URL of the image.")
    created_at: str = Field(description="The timestamp indicating when the image was created.")

    class Config:
        from_attributes = True
