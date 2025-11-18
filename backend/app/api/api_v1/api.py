from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, members, membership_plans, agents

api_router = APIRouter()

# Include authentication endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Include member management endpoints
api_router.include_router(members.router, prefix="/members", tags=["Members"])

# Include membership plan endpoints
api_router.include_router(
    membership_plans.router, prefix="/membership-plans", tags=["Membership Plans"]
)

# Include AI agents endpoints
api_router.include_router(agents.router, prefix="/agents", tags=["AI Agents"])


@api_router.get("/status")
async def api_status():
    return {"status": "API v1 is running"}
