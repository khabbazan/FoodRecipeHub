# flake8: NOQA

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import sessionmaker

from src.core.settings import DATABASE

# Create a SQLAlchemy database engine based on the specified URL and parameters.
engine = create_engine(DATABASE["URL"], **DATABASE["PARAMS"])

# Create a session factory that binds to the database engine.
local_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@as_declarative()
class Basemodel:
    """
    Base class for SQLAlchemy models.

    This class provides common attributes and configuration for SQLAlchemy models.

    Attributes:
        __tablename__ (str): The name of the database table, derived from the class name.
        id (Column): The primary key column for the model.

    Example usage:

    ```python
    class MyModel(Basemodel):
        # Your model's columns and relationships go here.
    ```
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


def get_db_session():
    """
    A generator function that yields a database session.

    This function creates a database session using the session factory and yields it to the caller.
    The caller should use this session and ensure it is closed properly.

    Example usage:

    ```python
    with get_db_session() as db_session:
        # Use the database session to perform database operations.
    # The database session is automatically closed when exiting the context.
    ```
    """
    db_session = local_session()
    try:
        yield db_session
    finally:
        db_session.close()


# Import order of models (if any) goes here.
from src.resources.images.models import ImageModel
from src.resources.relations.models import RelationModel
from src.resources.recipes.models import RecipeModel
from src.resources.recipes.models import TagModel
from src.resources.users.models import UserModel
