from fastapi import APIRouter, Depends, Path, HTTPException, status
from typing import Annotated
from uuid import UUID
from app.models import schema
from app.models.docs import Teacher, Course
from app.deps import get_current_user
from beanie.operators import All
from beanie import WriteRules

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=schema.Courses)
async def courses(
    user: Annotated[Teacher, Depends(get_current_user)]
) -> schema.Courses:
    return [course.fetch() for course in user.courses]


@router.get("/{id}", response_model=schema.Course)
async def get_course(
    user: Annotated[Teacher, Depends(get_current_user)],
    id: Annotated[UUID, Path()],
) -> schema.Course:
    course = await Course.find_one(Course.id == id, All(Course.teachers, [user.id]))
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await course.fetch_link(Course.owner)
    return course


@router.post("/new-course")
async def create_new_course(
    user: Annotated[Teacher, Depends(get_current_user)], data: schema.NewCourse
):
    new_course = Course(name=data.name, teachers=[user])
    user.courses.append(new_course)
    await user.save(link_rule=WriteRules.WRITE)
