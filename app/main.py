from fastapi import FastAPI, HTTPException, status
from app.models.schema import ClientRegister, ClientRegisterResult, AttendanceRequest
from app.models.docs import *
from uuid import uuid1

app = FastAPI()


@app.post("/register")
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


@app.post("/attendance")
async def attendance(data: AttendanceRequest):
    if (student := await Student.find_one(Student.client_id == data.client_id)) is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    if (session := await Session.get(data.session_id)) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if student.course_id != session.course:
        ...
    # get student by client_id
    # check session_id
    # check course_id
    # check student is in class
