import uuid
import datetime
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TEXT
from sqlalchemy import Enum
from sqlalchemy import event
from sqlalchemy import Table
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import or_

from src.core.database import Basemodel
from src.resources.recipes.enums import TAGEnum
from src.resources.recipes.fixtures import tag_fixtures

recipe_tag_association = Table(
    "recipe_tag_association", Basemodel.metadata, Column("recipe_id", Integer, ForeignKey("recipes.id")), Column("tag_id", Integer, ForeignKey("tags.id"))
)


class TagModel(Basemodel):
    __tablename__ = "tags"

    title = Column(Enum(TAGEnum), nullable=False)


class RecipeModel(Basemodel):
    __tablename__ = "recipes"

    uuid = Column(String(36), unique=True, nullable=False, default=lambda x: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    content = Column(TEXT, nullable=False)
    is_active = Column(Boolean, default=True)

    __created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("UserModel", back_populates="recipes")
    tags = relationship("TagModel", secondary=recipe_tag_association)

    def __repr__(self):
        return self.uuid

    @hybrid_property
    def created_at(self):
        return self.__created_at.isoformat()

    @classmethod
    def search(cls, session, query_string=None):
        if query_string:
            filters = [
                cls.title.ilike(f"%{query_string}%"),
                cls.content.ilike(f"%{query_string}%"),
            ]

            return session.query(cls).filter(or_(*filters))
        else:
            return session.query(cls)


event.listen(TagModel.__table__, "after_create", tag_fixtures)
