import re
from typing import Optional, List
from typing_extensions import Annotated
from pydantic import Field, BaseModel, field_validator
from fastapi.param_functions import Form

from src.resources.images.schemas import ImageSchema
from src.resources.users.enums import GenderEnum
from fastapi_babel.core import make_gettext as _


class UserSchema(BaseModel):
    phone_number: str = Field(alias="username", description="The phone number or username of the user.")
    password: str = Field(description="The password of the user.")
    email: Optional[str] = Field(None, description="The email address of the user.")
    gender: Optional[GenderEnum] = Field(None, description="The gender of the user.")
    avatar: Optional[ImageSchema] = Field(None, description="The user's avatar image.")

    def manual_all_validations(self, *args, **kwargs):
        """
        Manually validate user data using a list of validation functions.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            bool: True if all validations pass, otherwise raises ValueError.
        """
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
        """
        Validate the user's phone number or username.

        Args:
            phone_number (str): The phone number or username of the user.

        Returns:
            str: The validated phone number or username.

        Raises:
            ValueError: If the phone number or username is not valid.
        """
        if phone_number:
            pattern = r"^\+(?:[0-9] ?){6,14}[0-9]$"
            match = re.match(pattern, phone_number)
            if not match:
                raise ValueError(_("Invalid phone number"))
        return phone_number

    @field_validator("password")
    def validate_password(cls, password):
        """
        Validate the user's password.

        Args:
            password (str): The password of the user.

        Returns:
            str: The validated password.

        Raises:
            ValueError: If the password does not meet the requirements.
        """
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
        """
        Validate the user's email address.

        Args:
            email (str): The email address of the user.

        Returns:
            str: The validated email address.

        Raises:
            ValueError: If the email address is not valid.
        """
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
    phone_number: str = Field(description="The phone number or username of the user.")
    email: str = Field(description="The email address of the user.")

    class Config:
        from_attributes = True


class UserQuerySchema(BaseModel):
    phone_number: str = Field(description="The phone number or username of the user.")
    email: str = Field(description="The email address of the user.")
    gender: str = Field("", description="The gender of the user")
    is_online: bool = Field(description="Indicates whether the user is online or not.")
    recipes: List[str] = Field([], description="A list of recipe IDs associated with the user.")
    avatars: List[str] = Field([], description="A list of avatar image URLs associated with the user.")

    class Config:
        from_attributes = True


class UserFilterSchema(BaseModel):
    gender: Optional[GenderEnum] = Field(None, description="Filter by user's gender.")
    is_online: Optional[bool] = Field(None, description="Filter by user's online status.")


class UserEditSchema(BaseModel):
    username: Optional[str] = Field(None, description="The updated phone number or username of the user.")
    password: Optional[str] = Field(None, description="The updated password of the user.")
    email: Optional[str] = Field(None, description="The updated email address of the user.")
    gender: Optional[GenderEnum] = Field(None, description="The updated gender of the user.")
    avatar: Optional[ImageSchema] = Field(None, description="The updated user's avatar image.")
