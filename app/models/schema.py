from pydantic import (
    BaseModel as BaseModel,
    EmailStr,
    SecretStr,
    RootModel,
    MongoDsn,
    Field,
)
from fastapi import Form
from uuid import UUID
from typing import Literal, Annotated


class ConfigModel(BaseModel):
    db: MongoDsn = Field(
        examples=["mongodb://user:pass@mongodb.example.com:27017"],
        description="mongodb link to your database",
    )


def to_camel(string: str) -> str:
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


class CustomBaseModel(BaseModel):
    class config:
        alias_generator = to_camel


class ClientRegister(CustomBaseModel):
    student_id: int
    course_id: UUID


class ClientRegisterResult(CustomBaseModel):
    name: str
    course_name: str
    id: UUID


class AttendanceRequest(CustomBaseModel):
    session_id: UUID
    client_id: UUID


class TeacherLogin:
    def __init__(
        self,
        *,
        username: Annotated[EmailStr, Form()],
        password: Annotated[SecretStr, Form()]
    ):
        self.username = username
        self.password = password


class LoginResult(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


class Teacher(CustomBaseModel):
    name: str


class Course(CustomBaseModel):
    id: UUID
    name: str
    owner: Teacher


Courses = RootModel[list[Course]]


class Student(CustomBaseModel):
    id: UUID
    name: str


Students = RootModel[list[Student]]
