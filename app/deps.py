from fastapi import Depends, HTTPException, status, Path, Request
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from typing import Annotated
from jose import jwt, JWTError
from pydantic import ValidationError
from app.utils import AccessTokenData, JWT_ACCESS_SECRET_KEY, ALGORITHM
from app.models.docs import Teacher, Course
from datetime import datetime
from uuid import UUID
from beanie.operators import All

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/admin/login",
    scheme_name="JWT",
)


async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
) -> Teacher:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, JWT_ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = AccessTokenData.model_validate(payload)
        timezone = token_data.exp.tzinfo
        if (user := await Teacher.get(token_data.id)) is None:
            raise credentials_exception
        if token_data.exp < datetime.now(timezone):
            raise credentials_exception
        if user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user
    except (JWTError, ValidationError):
        raise credentials_exception


async def from_local(req: Request):
    if req.client.host not in ("127.0.0.1", "localhost"):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
