import datetime
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Enum
from sqlalchemy import DateTime
from sqlalchemy_utils.types.password import PasswordType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import or_

from src.core.database import Basemodel
from src.resources.images.models import ImageModel

from src.resources.users.enums import GenderEnum


class UserModel(Basemodel):
    """
    Represents a user model in the database.

    This class defines the structure and relationships of the user model in the database.

    Args:
        Basemodel (Base): The base model class for SQLAlchemy.

    Attributes:
        phone_number (str): The phone number of the user.
        email (str, optional): The email address of the user.
        gender (GenderEnum, optional): The gender of the user.
        is_online (bool): Indicates whether the user is online.
        password (PasswordType): The hashed password of the user.
        __created_at (DateTime): The timestamp when the user was created.
        access_tokens (relationship): Relationship with access tokens.
        following (relationship): Relationship with users being followed.
        followers (relationship): Relationship with followers.
        recipes (relationship): Relationship with user's recipes.

    Methods:
        created_at: Get the creation timestamp in ISO format.
        search: Search for users based on query string.
        get_avatars: Get user's avatar URLs.
        set_avatar: Set the user's avatar.

    """

    __tablename__ = "users"

    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=True)
    gender = Column(Enum(GenderEnum), nullable=True)
    is_online = Column(Boolean, default=False)
    password = Column(PasswordType(schemes=["pbkdf2_sha512"]), nullable=False)

    __created_at = Column(DateTime, default=datetime.datetime.utcnow)

    access_tokens = relationship("AccessTokenModel", back_populates="user")
    following = relationship("RelationModel", foreign_keys="[RelationModel.follower_id]")
    followers = relationship("RelationModel", foreign_keys="[RelationModel.following_id]")
    recipes = relationship("RecipeModel", back_populates="user", foreign_keys="[RecipeModel.user_id]")

    def __repr__(self):
        return self.phone_number

    @hybrid_property
    def created_at(self):
        """Get the creation timestamp in ISO format."""
        return self.__created_at.isoformat()

    @classmethod
    def search(cls, session, query_string=None):
        """
        Search for users based on query string.

        Args:
            session (Session): SQLAlchemy session.
            query_string (str, optional): The query string for searching users.

        Returns:
            Query: SQLAlchemy query for searching users.
        """
        if query_string:
            filters = [
                cls.phone_number.ilike(f"%{query_string}%"),
                cls.email.ilike(f"%{query_string}%"),
            ]

            return session.query(cls).filter(or_(*filters))
        else:
            return session.query(cls)

    def get_avatars(self, session):
        """
        Get user's avatar URLs.

        Args:
            session (Session): SQLAlchemy session.

        Returns:
            list: List of avatar URLs for the user.
        """
        avatars = session.query(ImageModel).filter_by(object=self).all()
        return [avatar.url for avatar in avatars]

    async def set_avatar(self, name, base64_image, session):
        """
        Set the user's avatar.

        Args:
            name (str): The name of the avatar image.
            base64_image (str): The base64-encoded image data.
            session (Session): SQLAlchemy session.

        Returns:
            bool: True if the avatar is set successfully.
        """
        avatars = session.query(ImageModel).filter_by(object=self).all()

        for avatar in avatars:
            await avatar.delete(session=session)

        if name and base64_image:
            image = ImageModel(filename=name, base64_image=base64_image, object=self)
            await image.save(session=session)

        return True
