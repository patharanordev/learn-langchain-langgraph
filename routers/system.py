from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["system"])

@router.get("/")
async def healthcheck():
    return {"message": "ok"}