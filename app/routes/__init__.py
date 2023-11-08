from .root import router
from . import admin

router.include_router(admin.router)
