from datetime import datetime
from datetime import timedelta
from fastapi import HTTPException
from fastapi import status
from jose import JWTError
from jose import jwt
from sqlalchemy.orm import Session

from src.core.settings import SECRET_KEY
from src.core.settings import JWT as JWTSettings  # noqa N811
from src.helpers.jwt.models import AccessTokenModel
from src.helpers.jwt.schemas import JWTTokenSchema
from fastapi_babel import _


class JWT:
    """
    JWT (JSON Web Token) utility class for handling access and refresh tokens.

    This class provides methods to create, verify, update, and expire JWT tokens used for authentication and authorization.

    Methods:
        create_access_token(user_id, session): Create an access token and return it as a JWTTokenSchema.
        is_token_expired(token): Check if a JWT token has expired.
        verify_token(token): Verify a JWT token and return the user_id if valid.
        update_token(user_id, refresh_token, session): Update a token using a refresh token and return a new access token.
        expire_token(user_id, session): Expire (delete) tokens associated with a user.

    Example usage:

    ```python
    jwt_util = JWT()

    access_token = jwt_util.create_access_token(user_id, session)
    user_id = jwt_util.verify_token(token)
    new_access_token = jwt_util.update_token(user_id, refresh_token, session)
    jwt_util.expire_token(user_id, session)
    ```

    """

    @classmethod
    def create_access_token(cls, user_id: int, session: Session) -> JWTTokenSchema:
        """
        Create an access token for a user.

        Args:
            user_id (int): The user's ID.
            session (Session): The SQLAlchemy database session.

        Returns:
            JWTTokenSchema: The JWT access and refresh tokens.

        """
        to_encode = {"sub": str(user_id)}

        access_token_expire = datetime.utcnow() + timedelta(minutes=JWTSettings.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
        to_encode.update({"exp": access_token_expire})

        refresh_token_expire = datetime.utcnow() + timedelta(minutes=JWTSettings.get("REFRESH_TOKEN_EXPIRE_MINUTES"))
        refresh_token = jwt.encode({"exp": refresh_token_expire}, SECRET_KEY, algorithm=JWTSettings.get("ALGORITHM"))

        to_encode["refresh_token"] = refresh_token

        access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=JWTSettings.get("ALGORITHM"))

        record = AccessTokenModel(user_id=user_id, refresh_token=refresh_token, refresh_token_expiration=refresh_token_expire)

        session.add(record)
        session.commit()

        return JWTTokenSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="JWT",
        )

    @classmethod
    def is_token_expired(cls, token: str) -> bool:
        """
        Check if a JWT token has expired.

        Args:
            token (str): The JWT token to check.

        Returns:
            bool: True if the token has expired, False otherwise.

        Raises:
            HTTPException: If there is an issue decoding or checking the token.

        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWTSettings.get("ALGORITHM")])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_("Invalid Credentials."))

        current_time = datetime.utcnow()
        expiration_time = datetime.fromtimestamp(payload.get("exp", 0))
        return current_time > expiration_time

    @classmethod
    def verify_token(cls, token: str) -> int | Exception:
        """
        Verify a JWT token and return the user_id if valid.

        Args:
            token (str): The JWT token to verify.

        Returns:
            int | Exception: The user's ID if the token is valid, or an Exception if invalid.

        Raises:
            HTTPException: If there is an issue decoding, checking, or handling the token.

        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWTSettings.get("ALGORITHM")])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_("Invalid Credentials."))
        else:
            if cls.is_token_expired(token):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_("Token Expired."))

            user_id = int(payload["sub"])
            return user_id

    @classmethod
    def update_token(cls, user_id: int, refresh_token: str, session: Session) -> JWTTokenSchema:
        """
        Update a token using a refresh token and return a new access token.

        Args:
            user_id (int): The user's ID.
            refresh_token (str): The refresh token to use for updating.
            session (Session): The SQLAlchemy database session.

        Returns:
            JWTTokenSchema: The updated JWT access and refresh tokens.

        Raises:
            HTTPException: If there is an issue decoding, checking, or handling the tokens.

        """
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[JWTSettings.get("ALGORITHM")])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_("Invalid refresh token"))
        else:
            current_time = datetime.utcnow()
            if current_time > datetime.fromtimestamp(payload["exp"]):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=_("Could not validate timestamps"))

            session.query(AccessTokenModel).filter(AccessTokenModel.refresh_token == refresh_token).delete()
            session.commit()
            return cls.create_access_token(user_id=user_id, session=session)

    @classmethod
    def expire_token(cls, user_id: int, session: Session) -> bool:
        """
        Expire (delete) tokens associated with a user.

        Args:
            user_id (int): The user's ID.
            session (Session): The SQLAlchemy database session.

        Returns:
            bool: True if the tokens were successfully expired (deleted), False otherwise.

        """
        session.query(AccessTokenModel).filter(AccessTokenModel.user_id == user_id).delete()
        session.commit()
        return True
