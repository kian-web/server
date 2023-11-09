from fastapi import APIRouter, Depends, Path, HTTPException, status
from typing import Annotated
from uuid import UUID
from app.models import schema
from app.models.docs import Teacher, Course
from app.deps import get_current_user
from beanie.operators import All

router = APIRouter(prefix="/{course_id}/students", tags=["Students"])


@router.get("/", response_model=schema.Students)
async def get_course_students(
    user: Annotated[Teacher, Depends(get_current_user)],
    course_id: Annotated[UUID, Path()],
) -> schema.Students:
    course = await Course.find_one(
        Course.id == course_id, All(Course.teachers, [user.id])
    )
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await course.fetch_link(course.students)
    return course.students
