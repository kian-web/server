from beanie import Document, Link, BackLink
from uuid import UUID, uuid1
from pydantic import BaseModel, Field, EmailStr
from pymongo import IndexModel
from datetime import datetime, time
from typing import Optional
from enum import Enum


class Teacher(Document):
    id: UUID = Field(default_factory=uuid1)
    email: EmailStr
    pass_hash: str
    courses: list[Link["Course"]]


class ClassState(Enum, str):
    nothing = "nothing"
    register = "register"
    attendance = "attendance"


class Course(Document):
    name: str
    id: UUID = Field(default_factory=uuid1)
    owner: Link[Teacher]
    students: list[Link["Student"]]
    sessions: list[Link["Session"]]
    state: ClassState


class Score(BaseModel):
    datetime: datetime
    value: float
    note: Optional[str] = None


class Student(Document):
    client_id: Optional[UUID] = None
    student_id: int
    course_id: UUID
    name: str
    attendances: list[Link["Attendance"]]
    scores: list[Link[Score]]

    class Settings:
        indexes = [
            IndexModel("student_id", "course", unique=True),
            IndexModel("client_id", unique=True),
        ]


class Session(Document):
    id: UUID
    name: str
    datetime: datetime = Field(default_factory=datetime.now)
    attendances: list[Link["Attendance"]]
    course_id: UUID
    state: ClassState


class AttendanceStatus(Enum, str):
    present = "present"
    absent = "absent"
    late = "late"


class Attendance(Document):
    time: time
    student: BackLink[Student] = Field(original_field="id")
    session: BackLink[Session] = Field(original_field="id")
    status: AttendanceStatus
