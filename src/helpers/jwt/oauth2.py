from typing import Optional
from starlette.requests import Request
from sqlalchemy.orm import Session
from fastapi import status
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param

from src.helpers.jwt import JWT
from src.core.database import get_db_session
from src.resources.users.models import UserModel
from fastapi_babel import _


class OAuth2PasswordJWT(OAuth2PasswordBearer):
    """
    OAuth2PasswordJWT is a custom OAuth2 password bearer scheme for JWT-based authentication.

    This class extends the OAuth2PasswordBearer class to support JWT-based authentication using the "JWT" scheme.

    Attributes:
        token_url (str): The URL where the token can be obtained.
        scheme_name (str): The name of the authentication scheme (default is "Bearer").
        scopes (Optional[dict]): Optional OAuth2 scopes.
        auto_error (bool): Whether to raise an HTTPException on authentication failure (default is True).

    Example usage:

    ```python
    oauth2_scheme = OAuth2PasswordJWT(scheme_name="JWT", token_url="/user/login")
    ```

    """

    def __init__(
        self,
        token_url: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict] = None,
        auto_error: bool = True,
    ):
        super().__init__(
            tokenUrl=token_url,
            scopes=scopes,
            scheme_name=scheme_name,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        """
        Authenticate a request and return the JWT token if valid.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            Optional[str]: The JWT token if valid, or None if authentication fails.

        Raises:
            HTTPException: If authentication fails and auto_error is set to True.

        """
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "jwt":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=_("Not authenticated"),
                    headers={"WWW-Authenticate": "JWT"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordJWT(scheme_name="JWT", token_url="/user/login")


def get_current_user(token: str = Depends(oauth2_scheme), db_session: Session = Depends(get_db_session)):
    """
    Get the current user based on the provided JWT token.

    Args:
        token (str): The JWT token obtained from the request.
        db_session (Session): The SQLAlchemy database session.

    Returns:
        UserModel: The user associated with the provided token.

    ```

    """
    user_id = JWT.verify_token(token)
    user = db_session.query(UserModel).filter_by(id=user_id).first()
    return user
