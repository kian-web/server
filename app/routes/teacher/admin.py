from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models import schema
from app.models.docs import Teacher
from app.utils import check_password, create_access_token
from typing import Annotated

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/login")
async def login(
    login_info: Annotated[schema.TeacherLogin, Depends()]
) -> schema.LoginResult:
    if (
        teacher := await Teacher.find_one(Teacher.email == login_info.username)
    ) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if not check_password(login_info.password, teacher.pass_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return create_access_token(teacher)
