from fastapi import APIRouter, Depends
from app.deps import from_local
from app.models.schema import NewTeacher
from app.models.docs import Teacher
from app.utils import generate_pass_hash

router = APIRouter(prefix="/admin", dependencies=[Depends(from_local)])


@router.post("/new-teacher")
async def add_new_teacher(data: NewTeacher):
    new_teacher = Teacher(
        email=data.email, name=data.name, pass_hash=generate_pass_hash(data.password)
    )
    await new_teacher.create()
