from .admin import router
from . import course

router.include_router(course.router)
