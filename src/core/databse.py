from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import sessionmaker

from src.core.settings import DATABASE


engine = create_engine(DATABASE["URL"], **DATABASE["PARAMS"])

local_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@as_declarative()
class Basemodel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


def get_db_session():
    db_session = local_session()
    try:
        yield db_session
    finally:
        db_session.close()


######### Order of Models ###########
from src.resources.images.models import ImageModel
from src.resources.relations.models import RelationModel
from src.resources.recipes.models import RecipeModel
from src.resources.recipes.models import TagModel
from src.resources.users.models import UserModel
