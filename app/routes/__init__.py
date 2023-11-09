from .root import router
from . import teacher
from . import admin

router.include_router(teacher.router)
router.include_router(admin.router)
