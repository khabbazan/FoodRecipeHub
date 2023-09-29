import re
from pydantic import BaseModel
from pydantic import field_validator

from fastapi_babel import _


class ImageSchema(BaseModel):
    name: str
    base64_image: str

    def manual_all_validations(self, *args, **kwargs):
        validation_functions = [
            {"name": self.validate_image_name, "args": [self.name]},
            {"name": self.validate_base64_string, "args": [self.image_base64]},
        ]
        for func in validation_functions:
            func["name"](*func["args"])
        return True

    @field_validator("name")
    def validate_image_name(cls, image_name):
        if image_name:
            pattern = r"^[a-zA-Z0-9_-]+\.(jpg|jpeg|png|gif|bmp|svg|webp)$"

            if not re.match(pattern, image_name):
                raise ValueError(_("Image name is not valid. there is no file extension."))
        return image_name

    @field_validator("base64_image")
    def validate_base64_string(cls, base64_image):
        if base64_image:
            pattern = r"^data:image/(png|jpeg|jpg|gif|bmp|webp);base64,([A-Za-z0-9+/]+={0,2})$"

            if not re.match(pattern, base64_image):
                raise ValueError(_("Base64 content is not valid"))
        return base64_image


class ImageQuerySchema(BaseModel):
    url: str
    created_at: str

    class Config:
        from_attributes = True
