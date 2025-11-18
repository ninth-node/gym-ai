from fastapi import APIRouter
from app.api.api_v1.endpoints import auth

api_router = APIRouter()

# Include authentication endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])


@api_router.get("/status")
async def api_status():
    return {"status": "API v1 is running"}
