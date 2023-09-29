from pydantic import BaseModel
from pydantic import field_validator
from pydantic import Field
from typing import Optional
from typing import List
from typing_extensions import Annotated
from fastapi.param_functions import Form

from src.resources.images.schemas import ImageSchema
from src.resources.users.enums import GenderEnum
from fastapi_babel.core import make_gettext as _

import re


class UserSchema(BaseModel):
    phone_number: str = Field(alias="username")
    password: str
    email: Optional[str] = None
    gender: Optional[GenderEnum] = None
    avatar: Optional[ImageSchema] = None

    def manual_all_validations(self, *args, **kwargs):
        validation_functions = [
            {"name": self.validate_phone_number, "args": [self.phone_number]},
            {"name": self.validate_password, "args": [self.password]},
            {"name": self.validate_email, "args": [self.email]},
        ]
        for func in validation_functions:
            func["name"](*func["args"])
        return True

    @field_validator("phone_number")
    def validate_phone_number(cls, phone_number):
        if phone_number:
            pattern = r"^\+(?:[0-9] ?){6,14}[0-9]$"
            match = re.match(pattern, phone_number)
            if not match:
                raise ValueError(_("Invalid phone number"))
        return phone_number

    @field_validator("password")
    def validate_password(cls, password):
        if password:
            len_ptr = re.compile(r"[\w$./]+")  # Check if password has at least 8 characters  # Todo: Edit regular exp
            if not re.match(len_ptr, password):
                raise ValueError(_("Password must contain at least 8 characters"))

            lower_ptr = re.compile(r"[a-z]+")  # Check if at least one lowercase letter
            if not re.findall(lower_ptr, password):
                raise ValueError(_("Password must contain at least one lowercase character"))

            upper_ptr = re.compile(r"[A-Z]+")  # Check if at least one uppercase letter
            if not re.findall(upper_ptr, password):
                raise ValueError(_("Password must contain at least one uppercase character"))

            digit_ptr = re.compile(r"[0-9]+")  # Check if at least one digit.
            if not re.findall(digit_ptr, password):
                raise ValueError(_("Password must contain at least one digit character"))

        return password

    @field_validator("email")
    def validate_email(cls, email):
        if email:
            pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            match = re.match(pattern, email)
            if not match:
                raise ValueError(_("Invalid email address"))
        return email


class UserLoginForm:
    def __init__(
        self,
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
    ):
        self.username = username
        self.password = password
        self.email = ""

    def to_schema(self):
        return UserSchema(username=self.username, email=self.email, password=self.password)


class UserQuerySchemaSimple(BaseModel):
    phone_number: str
    email: str

    class Config:
        from_attributes = True


class UserQuerySchema(BaseModel):
    phone_number: str
    email: str
    is_online: bool
    recipes: List[str] = []
    avatars: List[str] = []

    class Config:
        from_attributes = True


class UserFilterSchema(BaseModel):
    gender: Optional[GenderEnum] = None
    is_online: Optional[bool] = None


class UserEditSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[GenderEnum] = None
    avatar: Optional[ImageSchema] = None
