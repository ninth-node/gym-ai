from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.session import get_db
from app.core.dependencies import require_role
from app.models.user import User, UserRole

from app.agents.engagement.member_engagement_agent import MemberEngagementAgent
from app.agents.operations.operations_agent import OperationsAgent
from app.agents.financial.financial_agent import FinancialAgent

router = APIRouter()


class AgentExecutionRequest(BaseModel):
    context: Dict[str, Any] = {}


class AgentAnalysisRequest(BaseModel):
    data: Dict[str, Any]


# ===== Member Engagement Agent Endpoints =====


@router.post("/engagement/execute")
async def execute_engagement_agent(
    request: AgentExecutionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STAFF)),
):
    """Execute Member Engagement Agent to analyze churn risk and generate retention strategies."""
    agent = MemberEngagementAgent(db)
    result = await agent.run(request.context)
    return result.model_dump()


@router.post("/engagement/analyze")
async def analyze_member_engagement(
    request: AgentAnalysisRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STAFF)),
):
    """Analyze specific member's engagement and churn risk."""
    agent = MemberEngagementAgent(db)
    result = await agent.analyze(request.data)
    return result


@router.get("/engagement/at-risk-members")
async def get_at_risk_members(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STAFF)),
):
    """Get list of members at risk of churning."""
    agent = MemberEngagementAgent(db)
    members = await agent.identify_at_risk_members()
    return {"at_risk_members": members, "count": len(members)}


# ===== Operations Agent Endpoints =====


@router.post("/operations/execute")
async def execute_operations_agent(
    request: AgentExecutionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STAFF)),
):
    """Execute Operations Agent for equipment and facility management."""
    agent = OperationsAgent(db)
    result = await agent.run(request.context)
    return result.model_dump()


@router.post("/operations/analyze")
async def analyze_operations(
    request: AgentAnalysisRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STAFF)),
):
    """Analyze equipment or facility capacity."""
    agent = OperationsAgent(db)
    result = await agent.analyze(request.data)
    return result


@router.get("/operations/maintenance-predictions")
async def get_maintenance_predictions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STAFF)),
):
    """Get equipment maintenance predictions."""
    agent = OperationsAgent(db)
    predictions = await agent.predict_maintenance_needs()
    return {"maintenance_needed": predictions, "count": len(predictions)}


@router.get("/operations/capacity-analysis")
async def get_capacity_analysis(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.STAFF)),
):
    """Get facility capacity analysis."""
    agent = OperationsAgent(db)
    analysis = await agent.analyze_facility_capacity()
    return analysis


# ===== Financial Agent Endpoints =====


@router.post("/financial/execute")
async def execute_financial_agent(
    request: AgentExecutionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    """Execute Financial Agent for revenue optimization and forecasting."""
    agent = FinancialAgent(db)
    result = await agent.run(request.context)
    return result.model_dump()


@router.post("/financial/analyze")
async def analyze_financial(
    request: AgentAnalysisRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    """Analyze financial metrics and forecasts."""
    agent = FinancialAgent(db)
    result = await agent.analyze(request.data)
    return result


@router.get("/financial/revenue-forecast")
async def get_revenue_forecast(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    """Get revenue forecast for next 30/60/90 days."""
    agent = FinancialAgent(db)
    forecast = await agent.forecast_revenue()
    return forecast


@router.get("/financial/expiring-memberships")
async def get_expiring_memberships(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    """Get memberships expiring soon for renewal campaigns."""
    agent = FinancialAgent(db)
    expiring = await agent.identify_expiring_memberships()
    return {"expiring_memberships": expiring, "count": len(expiring)}


@router.get("/financial/pricing-recommendations")
async def get_pricing_recommendations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    """Get AI-powered pricing optimization recommendations."""
    agent = FinancialAgent(db)
    recommendations = await agent.analyze_pricing_optimization()
    return recommendations


# ===== General Agent Status =====


@router.get("/status")
async def get_agents_status(
    current_user: User = Depends(require_role(UserRole.STAFF)),
):
    """Get status of all AI agents."""
    return {
        "agents": [
            {
                "name": "Member Engagement Agent",
                "type": "member_engagement",
                "status": "operational",
                "capabilities": [
                    "Churn prediction",
                    "Retention strategies",
                    "Engagement analysis",
                ],
            },
            {
                "name": "Operations Agent",
                "type": "operations",
                "status": "operational",
                "capabilities": [
                    "Equipment maintenance prediction",
                    "Capacity analysis",
                    "Facility optimization",
                ],
            },
            {
                "name": "Financial Agent",
                "type": "financial",
                "status": "operational",
                "capabilities": [
                    "Revenue forecasting",
                    "Pricing optimization",
                    "Renewal management",
                ],
            },
        ],
        "total_agents": 3,
    }
