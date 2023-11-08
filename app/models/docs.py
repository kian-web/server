from typing_extensions import Unpack
from beanie import Document, Link, BackLink
from uuid import UUID, uuid1
from pydantic import BaseModel, Field, EmailStr
from pymongo import IndexModel
from datetime import datetime, time
from typing import Optional
from enum import Enum


def to_camel(string: str) -> str:
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


class MyBaseModel(BaseModel):
    class config:
        alias_generator = to_camel


DOCUMENTS_LIST = []


class MyDocument(Document):
    class config:
        alias_generator = to_camel

    def __init_subclass__(cls, **kwargs):
        DOCUMENTS_LIST.append(cls)
        return super().__init_subclass__(**kwargs)


class Teacher(MyDocument):
    id: UUID = Field(default_factory=uuid1)
    name: str
    email: EmailStr
    pass_hash: str
    courses: list[Link["Course"]]
    disabled: bool = False


class ClassState(str, Enum):
    nothing = "nothing"
    register = "register"
    attendance = "attendance"


class Course(MyDocument):
    id: UUID = Field(default_factory=uuid1)
    name: str
    owner: BackLink[Teacher] = Field(original_field="id")
    teachers: list[Link[Teacher]]
    students: list[Link["Student"]]
    sessions: list[Link["Session"]]


class Score(MyBaseModel):
    datetime: datetime
    value: float
    note: Optional[str] = None


class Student(MyDocument):
    client_id: Optional[UUID] = None
    student_id: int
    course: Link[Course]
    name: str
    attendances: list[Link["Attendance"]]
    scores: list[Score]
    state: ClassState

    class Settings:
        indexes = [
            IndexModel(("student_id", "course"), unique=True),
            IndexModel("client_id", unique=True),
        ]


class Session(MyDocument):
    id: UUID
    name: str
    start_datetime: datetime = Field(default_factory=datetime.now)
    attendances: list[Link["Attendance"]]
    course: BackLink[Course] = Field(original_field="id")
    state: ClassState


class Attendance(MyDocument):
    attendance_time: time = Field(default_factory=lambda: datetime.now().time())
