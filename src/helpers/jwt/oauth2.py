from typing import Optional
from starlette.requests import Request
from sqlalchemy.orm import Session
from fastapi import status
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param

from src.helpers.jwt import JWT
from src.core.databse import get_db_session
from src.resources.users.models import UserModel
from fastapi_babel import _

class OAuth2PasswordJWT(OAuth2PasswordBearer):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict] = None,
        auto_error: bool = True,
    ):
        super().__init__(
            tokenUrl=tokenUrl,
            scopes=scopes,
            scheme_name=scheme_name,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
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

oauth2_scheme = OAuth2PasswordJWT(scheme_name="JWT", tokenUrl="/user/login")

def get_current_user(token: str = Depends(oauth2_scheme), db_session: Session = Depends(get_db_session)):
    user_id = JWT.verify_token(token)
    user = db_session.query(UserModel).filter_by(id=user_id).first()
    return user
