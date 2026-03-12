import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

from app.core.config import settings
import jwt

from app.core.database import SessionDep

from pwdlib import PasswordHash

from app.models import AuthSessions

password_hash = PasswordHash.recommended()

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=10)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt



# def create_refresh_token(db: SessionDep, expires_delta: timedelta | None = None) -> AuthSessions:
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(days=5)
#     jti = uuid.uuid4().hex
#
#     payload = {
#         "sub":user.username,
#         "jti":jti,
#         "type": "refresh",
#         "exp": expire,
#         "iat": datetime.now(timezone.utc),
#     }
#
#     token = jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)
#
#     data = AuthSessions(user_id= user_id, jti= jti, expires_at= expire, revoked=False)
#
#     db.add(data)
#     db.commit()
#     db.refresh(data)
#
#     return token + data








def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password,hashed_password)

def get_password_hash(password: str):
    return password_hash.hash(password)
