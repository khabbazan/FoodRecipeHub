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
        return self.__created_at.isoformat()

    @classmethod
    def search(cls, session, query_string=None):
        if query_string:
            filters = [
                cls.phone_number.ilike(f"%{query_string}%"),
                cls.email.ilike(f"%{query_string}%"),
            ]

            return session.query(cls).filter(or_(*filters))
        else:
            return session.query(cls)

    def get_avatars(self, session):
        avatars = session.query(ImageModel).filter_by(object=self).all()
        return [avatar.url for avatar in avatars]

    async def set_avatar(self, name, base64_image, session):
        avatars = session.query(ImageModel).filter_by(object=self).all()

        for avatar in avatars:
            await avatar.delete(session=session)

        if name and base64_image:
            image = ImageModel(filename=name, base64_image=base64_image, object=self)
            await image.save(session=session)

        return True
