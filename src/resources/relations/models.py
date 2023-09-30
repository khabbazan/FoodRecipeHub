import datetime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property

from src.core.database import Basemodel


class RelationModel(Basemodel):
    """
    Represents a user relationship model in the database.

    This model tracks the relationships between users, specifically who is following whom.

    Attributes:
        follower_id (int): The ID of the user who is following another user.
        following_id (int): The ID of the user who is being followed.
        created_at (str): The timestamp when the relationship was created in ISO format.

    Methods:
        __repr__: Get a string representation of the relationship.

    """

    __tablename__ = "relations"

    follower_id = Column(Integer, ForeignKey("users.id"))
    following_id = Column(Integer, ForeignKey("users.id"))

    __followed_on = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        """Returns a string representation of the relationship."""
        return f"{self.follower_id} follows {self.following_id}"

    @hybrid_property
    def created_at(self):
        """Hybrid Property: Get the creation timestamp in ISO format."""
        return self.__followed_on.isoformat()
