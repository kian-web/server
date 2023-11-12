from fastapi import APIRouter, Depends
from app.deps import from_local

router = APIRouter(prefix="/admin", dependencies=[Depends(from_local)])
