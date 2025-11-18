from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from langchain.schema import HumanMessage, SystemMessage

from app.agents.base.agent import BaseAgent
from app.agents.base.state import AgentType, AgentResult, AgentStatus
from app.core.ai.config import ai_settings
from app.models.member import Member, MembershipStatus
from app.models.check_in import CheckIn
from app.models.user import User


class MemberEngagementAgent(BaseAgent):
    """
    AI Agent for member engagement, retention, and churn prediction.

    Capabilities:
    - Predict member churn risk
    - Identify at-risk members
    - Generate personalized retention campaigns
    - Analyze engagement patterns
    """

    def __init__(self, db: AsyncSession):
        super().__init__(agent_type=AgentType.MEMBER_ENGAGEMENT, db=db)

    async def execute(self, context: Dict[str, Any]) -> AgentResult:
        """Execute member engagement analysis."""
        start_time = datetime.utcnow()

        try:
            # Analyze all active members
            at_risk_members = await self.identify_at_risk_members()

            # Generate retention strategies
            retention_strategies = await self.generate_retention_strategies(
                at_risk_members
            )

            # Calculate engagement metrics
            engagement_metrics = await self.calculate_engagement_metrics()

            execution_time = (datetime.utcnow() - start_time).total_seconds()

            return AgentResult(
                agent_type=self.agent_type,
                status=AgentStatus.COMPLETED,
                success=True,
                results={
                    "at_risk_members": at_risk_members,
                    "retention_strategies": retention_strategies,
                    "engagement_metrics": engagement_metrics,
                    "total_analyzed": len(at_risk_members),
                },
                execution_time=execution_time,
            )

        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            return AgentResult(
                agent_type=self.agent_type,
                status=AgentStatus.FAILED,
                success=False,
                errors=[str(e)],
                execution_time=execution_time,
            )

    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze member engagement data."""
        member_id = data.get("member_id")

        if not member_id:
            return {"error": "member_id is required"}

        # Get member data
        member = await self._get_member_with_stats(member_id)

        if not member:
            return {"error": "Member not found"}

        # Calculate churn risk
        churn_risk = await self.predict_churn_risk(member)

        # Get engagement insights
        insights = await self._generate_member_insights(member)

        return {
            "member_id": member_id,
            "churn_risk": churn_risk,
            "insights": insights,
            "recommendation": self._get_retention_recommendation(churn_risk),
        }

    async def identify_at_risk_members(self) -> List[Dict[str, Any]]:
        """Identify members at risk of churning."""
        await self.log_message("system", "Identifying at-risk members...")

        lookback_date = datetime.utcnow() - timedelta(
            days=ai_settings.CHURN_LOOKBACK_DAYS
        )

        # Get active members
        result = await self.db.execute(
            select(Member, User)
            .join(User, Member.user_id == User.id)
            .where(Member.membership_status == MembershipStatus.ACTIVE)
        )
        members = result.all()

        at_risk = []

        for member, user in members:
            # Calculate churn risk
            risk_score = await self.predict_churn_risk(member)

            if risk_score >= ai_settings.CHURN_PREDICTION_THRESHOLD:
                at_risk.append(
                    {
                        "member_id": member.id,
                        "user_id": user.id,
                        "name": user.full_name,
                        "email": user.email,
                        "risk_score": risk_score,
                        "last_check_in": (
                            member.last_check_in.isoformat()
                            if member.last_check_in
                            else None
                        ),
                        "total_check_ins": member.total_check_ins,
                    }
                )

        self.add_action(
            "identify_at_risk_members",
            {"count": len(at_risk), "threshold": ai_settings.CHURN_PREDICTION_THRESHOLD},
        )

        return at_risk

    async def predict_churn_risk(self, member: Member) -> float:
        """
        Predict churn risk for a member.

        TODO: Implement ML model for more accurate predictions.
        Current implementation uses heuristics.
        """
        risk_score = 0.0

        # Factor 1: Days since last check-in (40% weight)
        if member.last_check_in:
            days_since_checkin = (
                datetime.utcnow() - member.last_check_in
            ).days
            if days_since_checkin > 14:
                risk_score += 0.4
            elif days_since_checkin > 7:
                risk_score += 0.2
        else:
            risk_score += 0.4  # Never checked in

        # Factor 2: Check-in frequency (30% weight)
        if member.total_check_ins < 5:
            risk_score += 0.3
        elif member.total_check_ins < 10:
            risk_score += 0.15

        # Factor 3: Membership approaching end (30% weight)
        if member.membership_end_date:
            days_until_expiry = (
                member.membership_end_date - datetime.utcnow().date()
            ).days
            if days_until_expiry < 7:
                risk_score += 0.3
            elif days_until_expiry < 14:
                risk_score += 0.15

        # TODO: Add more sophisticated factors:
        # - Class participation rate
        # - Social engagement (workout buddy interactions)
        # - Goal achievement progress
        # - Equipment usage patterns
        # - Response to previous communications

        return min(risk_score, 1.0)

    async def generate_retention_strategies(
        self, at_risk_members: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate personalized retention strategies using AI."""
        strategies = []

        for member_data in at_risk_members[:5]:  # Limit to top 5 for API costs
            try:
                # Use LLM to generate personalized strategy
                system_prompt = """You are a gym retention specialist AI.
                Generate a personalized retention strategy for at-risk gym members.
                Be specific, actionable, and empathetic."""

                user_prompt = f"""
                Member Profile:
                - Name: {member_data['name']}
                - Risk Score: {member_data['risk_score']:.2f}
                - Total Check-ins: {member_data['total_check_ins']}
                - Last Check-in: {member_data['last_check_in'] or 'Never'}

                Generate a retention strategy with:
                1. Personalized outreach message (2-3 sentences)
                2. Specific incentive or offer
                3. Recommended follow-up action
                """

                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_prompt),
                ]

                response = await self.llm.ainvoke(messages)

                strategies.append(
                    {
                        "member_id": member_data["member_id"],
                        "strategy": response.content,
                        "risk_score": member_data["risk_score"],
                    }
                )

                self.add_action(
                    "generate_retention_strategy",
                    {"member_id": member_data["member_id"]},
                )

            except Exception as e:
                # TODO: Implement fallback strategy templates
                strategies.append(
                    {
                        "member_id": member_data["member_id"],
                        "strategy": "Generic retention offer: 20% off next month + free personal training session",
                        "error": str(e),
                    }
                )

        return strategies

    async def calculate_engagement_metrics(self) -> Dict[str, Any]:
        """Calculate overall engagement metrics."""
        # Total active members
        active_count = await self.db.execute(
            select(func.count(Member.id)).where(
                Member.membership_status == MembershipStatus.ACTIVE
            )
        )
        total_active = active_count.scalar()

        # Members who checked in this week
        week_ago = datetime.utcnow() - timedelta(days=7)
        weekly_active = await self.db.execute(
            select(func.count(Member.id.distinct())).where(
                Member.last_check_in >= week_ago
            )
        )
        weekly_active_count = weekly_active.scalar()

        # Calculate engagement rate
        engagement_rate = (
            (weekly_active_count / total_active * 100) if total_active > 0 else 0
        )

        return {
            "total_active_members": total_active,
            "weekly_active_members": weekly_active_count,
            "engagement_rate": round(engagement_rate, 2),
            "calculated_at": datetime.utcnow().isoformat(),
        }

    async def _get_member_with_stats(self, member_id: int) -> Member:
        """Get member with additional statistics."""
        result = await self.db.execute(
            select(Member).where(Member.id == member_id)
        )
        return result.scalar_one_or_none()

    async def _generate_member_insights(self, member: Member) -> List[str]:
        """Generate insights about a specific member."""
        insights = []

        # TODO: Use AI to generate more sophisticated insights

        if member.total_check_ins < 5:
            insights.append("Low engagement: Member has minimal gym visits")

        if member.last_check_in:
            days_since = (datetime.utcnow() - member.last_check_in).days
            if days_since > 14:
                insights.append(f"Inactive: No visits in {days_since} days")

        if member.membership_end_date:
            days_left = (member.membership_end_date - datetime.utcnow().date()).days
            if days_left < 14:
                insights.append(f"Membership expiring in {days_left} days")

        return insights

    def _get_retention_recommendation(self, risk_score: float) -> str:
        """Get retention recommendation based on risk score."""
        if risk_score >= 0.8:
            return "URGENT: Immediate personal outreach required"
        elif risk_score >= 0.6:
            return "HIGH: Send personalized retention offer"
        elif risk_score >= 0.4:
            return "MEDIUM: Automated engagement campaign"
        else:
            return "LOW: Standard member nurturing"
