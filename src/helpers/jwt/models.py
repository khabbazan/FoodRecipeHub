from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src.core.database import Basemodel


class AccessTokenModel(Basemodel):
    __tablename__ = "access_tokens"

    user_id = Column(Integer, ForeignKey("users.id"))
    refresh_token = Column(String)
    refresh_token_expiration = Column(DateTime)

    user = relationship("UserModel", back_populates="access_tokens")
