from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src.core.database import Basemodel


class AccessTokenModel(Basemodel):
    """
    AccessTokenModel represents access tokens associated with users in the database.

    This model stores information about access tokens, including the user ID, refresh token, and refresh token expiration.

    Attributes:
        id (int): The primary key for the access token record.
        user_id (int): The ID of the user associated with the access token.
        refresh_token (str): The refresh token used for token refreshing.
        refresh_token_expiration (DateTime): The expiration date and time of the refresh token.

    Relationships:
        user (UserModel): A relationship to the UserModel representing the user associated with this access token.

    Example usage:

    ```python
    access_token = AccessTokenModel(user_id=1, refresh_token="some_token", refresh_token_expiration=datetime.utcnow())
    session.add(access_token)
    session.commit()
    ```

    """

    __tablename__ = "access_tokens"

    user_id = Column(Integer, ForeignKey("users.id"))
    refresh_token = Column(String)
    refresh_token_expiration = Column(DateTime)

    user = relationship("UserModel", back_populates="access_tokens")
