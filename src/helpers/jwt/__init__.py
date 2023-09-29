from datetime import datetime
from datetime import timedelta
from fastapi import HTTPException
from fastapi import status
from jose import JWTError
from jose import jwt
from sqlalchemy.orm import Session

from src.core.settings import SECRET_KEY
from src.core.settings import JWT as JWTSettings
from src.helpers.jwt.models import AccessTokenModel
from src.helpers.jwt.schemas import JWTTokenSchema
from fastapi_babel import _

class JWT:

    @classmethod
    def create_access_token(cls, user_id: int, session: Session) -> JWTTokenSchema:
        to_encode = {"sub": str(user_id)}

        access_token_expire = datetime.utcnow() + timedelta(minutes=JWTSettings.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
        to_encode.update({"exp": access_token_expire})

        refresh_token_expire = datetime.utcnow() + timedelta(minutes=JWTSettings.get("REFRESH_TOKEN_EXPIRE_MINUTES"))
        refresh_token = jwt.encode({"exp": refresh_token_expire}, SECRET_KEY, algorithm=JWTSettings.get("ALGORITHM"))

        to_encode["refresh_token"] = refresh_token

        access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=JWTSettings.get("ALGORITHM"))

        record = AccessTokenModel(
            user_id=user_id,
            refresh_token=refresh_token,
            refresh_token_expiration=refresh_token_expire
        )

        session.add(record)
        session.commit()

        return JWTTokenSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="JWT",
        )

    @classmethod
    def is_token_expired(cls, token: str) -> bool:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWTSettings.get("ALGORITHM")])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="_(Invalid Credentials.")

        # Check if the token has expired
        current_time = datetime.utcnow()
        expiration_time = datetime.fromtimestamp(payload.get("exp", 0))
        return current_time > expiration_time


    @classmethod
    def verify_token(cls, token: str) -> int | Exception:
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
        session.query(AccessTokenModel).filter(AccessTokenModel.user_id == user_id).delete()
        session.commit()
        return True
