from fastapi import HTTPException, status, APIRouter
from app.models.schema import (
    ClientRegister,
    ClientRegisterResult,
    AttendanceRequest,
)
from app.models.docs import *
from beanie.operators import In
from uuid import uuid1

router = APIRouter(prefix="/")


@router.post("/register")
async def register_student(data: ClientRegister) -> ClientRegisterResult:
    if course := await Course.get(data.course_id):
        if course.state != ClassState.register:
            raise HTTPException(status.HTTP_403_FORBIDDEN)
        student = await Student.find_one(
            Student.student_id == data.student_id,
            Student.course == data.course_id,
        )
        client_id = uuid1()
        student.client_id = client_id
        await student.save_changes()
        return ClientRegisterResult(
            name=student.name, course_name=course.name, id=client_id
        )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/attendance")
async def attendance(data: AttendanceRequest):
    if (session := await Session.get(data.session_id)) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if (
        student := await Student.find_one(
            Student.client_id == data.client_id, In(Student.courses, session.course)
        )
    ) is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    att = Attendance()
    att.save()
    student.attendances.append(att)
    session.attendances.append(att)
    student.save_changes()
    session.save_changes()
