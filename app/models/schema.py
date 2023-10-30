from pydantic import BaseModel as __BaseModel
from uuid import UUID


def to_camel(string: str) -> str:
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


class BaseModel(__BaseModel):
    class config:
        alias_generator = to_camel


...


class ClientRegister(BaseModel):
    student_id: int
    course_id: UUID


class ClientRegisterResult(BaseModel):
    name: str
    course_name: str
    id: UUID


class AttendanceRequest(BaseModel):
    session_id: UUID
    client_id: UUID
