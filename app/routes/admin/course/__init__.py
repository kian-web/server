from .course import router
from . import students

router.include_router(students.router)
