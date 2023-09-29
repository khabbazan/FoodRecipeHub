import datetime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property

from src.core.database import Basemodel


class RelationModel(Basemodel):
    __tablename__ = "relations"

    follower_id = Column(Integer, ForeignKey("users.id"))
    following_id = Column(Integer, ForeignKey("users.id"))

    __followed_on = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"{self.follower_id} follows {self.following_id}"

    @hybrid_property
    def created_at(self):
        return self.__followed_on.isoformat()
