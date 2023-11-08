from pydantic import BaseModel, SecretStr
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256
from jose import jwt
import os

from app.models.docs import Teacher

ACCESS_TOKEN_EXPIRE_TIME = timedelta(hours=12)
ALGORITHM = "HS256"
JWT_ACCESS_SECRET_KEY = os.environ.get(
    "JWT_ACCESS_SECRET_KEY", "a secret key for access token"
)  # should be kept secret


def generate_pass_hash(password: SecretStr) -> str:
    return pbkdf2_sha256.using(rounds=8000, salt_size=10).hash(
        password.get_secret_value()
    )


def check_password(password: SecretStr, hash: str) -> bool:
    return pbkdf2_sha256.using(rounds=8000, salt_size=10).verify(
        password.get_secret_value(), hash
    )


class AccessTokenData(BaseModel):
    id: str
    exp: datetime


class RefreshTokenData(BaseModel):
    id: str
    exp: datetime


def create_access_token(user: Teacher, expires_delta: timedelta = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + ACCESS_TOKEN_EXPIRE_TIME
    encoded_jwt = jwt.encode(
        AccessTokenData(
            id=user.id,
            exp=expires_delta,
        ).model_dump(),
        JWT_ACCESS_SECRET_KEY,
        ALGORITHM,
    )
    return encoded_jwt
