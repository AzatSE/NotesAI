from datetime import timedelta
from typing import Annotated
from fastapi import  Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.schemas import Token

from sqlalchemy.orm import Session

from app.schemas import Token, TokenData
from app.models import User
from app.core.database import get_db, SessionDep

from jwt.exceptions import InvalidTokenError
import jwt

from app.core.config import settings
from app.core.security import verify_password, create_access_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)


def get_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user



async def get_current_user(
    access_token: str | None = Cookie(None),
    db: Session = Depends(get_db)
):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token"
        )

    try:
        payload = jwt.decode(
            access_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

async def get_current_active_user(
        current_user: CurrentUser
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

