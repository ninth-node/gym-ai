from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from langchain.schema import HumanMessage, SystemMessage

from app.agents.base.agent import BaseAgent
from app.agents.base.state import AgentType, AgentResult, AgentStatus
from app.core.ai.config import ai_settings
from app.models.equipment import Equipment, EquipmentStatus
from app.models.check_in import CheckIn


class OperationsAgent(BaseAgent):
    """
    AI Agent for facility operations and equipment management.

    Capabilities:
    - Predict equipment maintenance needs
    - Optimize facility capacity
    - Monitor equipment health
    - Generate maintenance schedules
    - Analyze facility usage patterns
    """

    def __init__(self, db: AsyncSession):
        super().__init__(agent_type=AgentType.OPERATIONS, db=db)

    async def execute(self, context: Dict[str, Any]) -> AgentResult:
        """Execute operations analysis."""
        start_time = datetime.utcnow()

        try:
            # Predict maintenance needs
            maintenance_needed = await self.predict_maintenance_needs()

            # Analyze capacity
            capacity_analysis = await self.analyze_facility_capacity()

            # Get equipment health report
            equipment_health = await self.get_equipment_health_report()

            execution_time = (datetime.utcnow() - start_time).total_seconds()

            return AgentResult(
                agent_type=self.agent_type,
                status=AgentStatus.COMPLETED,
                success=True,
                results={
                    "maintenance_needed": maintenance_needed,
                    "capacity_analysis": capacity_analysis,
                    "equipment_health": equipment_health,
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
        """Analyze equipment or facility data."""
        analysis_type = data.get("type", "equipment")

        if analysis_type == "equipment":
            equipment_id = data.get("equipment_id")
            if equipment_id:
                return await self._analyze_equipment(equipment_id)

        elif analysis_type == "capacity":
            return await self.analyze_facility_capacity()

        return {"error": "Invalid analysis type"}

    async def predict_maintenance_needs(self) -> List[Dict[str, Any]]:
        """Predict equipment maintenance needs."""
        await self.log_message("system", "Predicting maintenance needs...")

        prediction_date = datetime.utcnow() + timedelta(
            days=ai_settings.MAINTENANCE_PREDICTION_DAYS
        )

        # Get all equipment
        result = await self.db.execute(select(Equipment))
        equipment_list = result.scalars().all()

        maintenance_needed = []

        for equipment in equipment_list:
            # Predict if maintenance is needed
            prediction = await self._predict_equipment_maintenance(equipment)

            if prediction["needs_maintenance"]:
                maintenance_needed.append(
                    {
                        "equipment_id": equipment.id,
                        "name": equipment.name,
                        "category": equipment.category.value,
                        "current_status": equipment.status.value,
                        "prediction": prediction,
                        "priority": self._calculate_maintenance_priority(
                            equipment, prediction
                        ),
                    }
                )

        # Sort by priority
        maintenance_needed.sort(key=lambda x: x["priority"], reverse=True)

        self.add_action(
            "predict_maintenance",
            {"count": len(maintenance_needed), "total_equipment": len(equipment_list)},
        )

        return maintenance_needed

    async def _predict_equipment_maintenance(
        self, equipment: Equipment
    ) -> Dict[str, Any]:
        """
        Predict if equipment needs maintenance.

        TODO: Implement ML model for more accurate predictions using:
        - IoT sensor data
        - Usage patterns
        - Historical maintenance records
        - Manufacturer recommendations
        """
        needs_maintenance = False
        reasons = []
        confidence = 0.0

        # Factor 1: Usage count threshold
        if equipment.total_usage_count > ai_settings.EQUIPMENT_USAGE_THRESHOLD:
            needs_maintenance = True
            reasons.append(
                f"High usage count: {equipment.total_usage_count} uses"
            )
            confidence += 0.3

        # Factor 2: Time since last maintenance
        if equipment.last_maintenance_date:
            days_since_maintenance = (
                datetime.utcnow() - equipment.last_maintenance_date
            ).days
            if days_since_maintenance > 90:  # 3 months
                needs_maintenance = True
                reasons.append(
                    f"Last maintenance {days_since_maintenance} days ago"
                )
                confidence += 0.4
        else:
            # Never maintained
            if equipment.purchase_date:
                days_since_purchase = (
                    datetime.utcnow() - equipment.purchase_date
                ).days
                if days_since_purchase > 180:  # 6 months
                    needs_maintenance = True
                    reasons.append("Never maintained")
                    confidence += 0.5

        # Factor 3: Current status
        if equipment.status == EquipmentStatus.MAINTENANCE_NEEDED:
            needs_maintenance = True
            reasons.append("Already marked for maintenance")
            confidence += 0.3

        # TODO: Add IoT sensor data analysis
        # TODO: Add predictive failure detection based on usage patterns

        return {
            "needs_maintenance": needs_maintenance,
            "confidence": min(confidence, 1.0),
            "reasons": reasons,
            "estimated_days_until_failure": self._estimate_days_until_failure(
                equipment
            ),
        }

    def _calculate_maintenance_priority(
        self, equipment: Equipment, prediction: Dict[str, Any]
    ) -> float:
        """Calculate maintenance priority score (0-1)."""
        priority = 0.0

        # Base on confidence
        priority += prediction["confidence"] * 0.5

        # Add urgency based on estimated failure time
        days_until_failure = prediction.get("estimated_days_until_failure", 30)
        if days_until_failure < 7:
            priority += 0.3
        elif days_until_failure < 14:
            priority += 0.2

        # Add category importance (cardio equipment is higher priority)
        if equipment.category.value == "cardio":
            priority += 0.2

        return min(priority, 1.0)

    def _estimate_days_until_failure(self, equipment: Equipment) -> int:
        """
        Estimate days until equipment failure.

        TODO: Use ML model for accurate prediction
        """
        # Simple heuristic for now
        if equipment.total_usage_count > ai_settings.EQUIPMENT_USAGE_THRESHOLD * 1.5:
            return 7
        elif equipment.total_usage_count > ai_settings.EQUIPMENT_USAGE_THRESHOLD:
            return 14
        else:
            return 30

    async def analyze_facility_capacity(self) -> Dict[str, Any]:
        """Analyze facility capacity and usage patterns."""
        # Get check-ins for the last 7 days
        week_ago = datetime.utcnow() - timedelta(days=7)

        # Daily check-in counts
        result = await self.db.execute(
            select(
                func.date(CheckIn.check_in_time).label("date"),
                func.count(CheckIn.id).label("count"),
            )
            .where(CheckIn.check_in_time >= week_ago)
            .group_by(func.date(CheckIn.check_in_time))
        )

        daily_counts = [
            {"date": str(row.date), "count": row.count} for row in result.all()
        ]

        # Peak hours analysis (by hour of day)
        result = await self.db.execute(
            select(
                func.extract("hour", CheckIn.check_in_time).label("hour"),
                func.count(CheckIn.id).label("count"),
            )
            .where(CheckIn.check_in_time >= week_ago)
            .group_by(func.extract("hour", CheckIn.check_in_time))
            .order_by(func.count(CheckIn.id).desc())
        )

        peak_hours = [
            {"hour": int(row.hour), "count": row.count} for row in result.all()
        ]

        # Current occupancy
        current_occupancy = await self.db.execute(
            select(func.count(CheckIn.id)).where(CheckIn.check_out_time.is_(None))
        )
        current_count = current_occupancy.scalar()

        # TODO: Add capacity recommendations based on patterns
        # TODO: Integrate with HVAC and climate control
        # TODO: Add peak time predictions

        return {
            "current_occupancy": current_count,
            "daily_trends": daily_counts,
            "peak_hours": peak_hours[:5],  # Top 5 peak hours
            "capacity_utilization": self._calculate_capacity_utilization(
                daily_counts
            ),
            "recommendations": await self._generate_capacity_recommendations(
                peak_hours
            ),
        }

    def _calculate_capacity_utilization(
        self, daily_counts: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate facility capacity utilization.

        TODO: Get actual facility capacity from configuration
        """
        assumed_capacity = 100  # TODO: Make this configurable
        if not daily_counts:
            return 0.0

        avg_daily = sum(d["count"] for d in daily_counts) / len(daily_counts)
        return round((avg_daily / assumed_capacity) * 100, 2)

    async def _generate_capacity_recommendations(
        self, peak_hours: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate recommendations for capacity management."""
        recommendations = []

        if peak_hours:
            top_hour = peak_hours[0]
            recommendations.append(
                f"Peak hour is {top_hour['hour']}:00 with {top_hour['count']} check-ins. Consider additional staff during this time."
            )

        # TODO: Use AI to generate more sophisticated recommendations

        return recommendations

    async def get_equipment_health_report(self) -> Dict[str, Any]:
        """Get overall equipment health report."""
        # Count by status
        result = await self.db.execute(
            select(
                Equipment.status, func.count(Equipment.id).label("count")
            ).group_by(Equipment.status)
        )

        status_counts = {row.status.value: row.count for row in result.all()}

        # Total equipment
        total = sum(status_counts.values())

        # Calculate health score
        operational = status_counts.get("operational", 0)
        health_score = (operational / total * 100) if total > 0 else 0

        return {
            "total_equipment": total,
            "status_breakdown": status_counts,
            "health_score": round(health_score, 2),
            "operational_percentage": round(health_score, 2),
        }

    async def _analyze_equipment(self, equipment_id: int) -> Dict[str, Any]:
        """Analyze specific equipment."""
        result = await self.db.execute(
            select(Equipment).where(Equipment.id == equipment_id)
        )
        equipment = result.scalar_one_or_none()

        if not equipment:
            return {"error": "Equipment not found"}

        prediction = await self._predict_equipment_maintenance(equipment)

        return {
            "equipment_id": equipment_id,
            "name": equipment.name,
            "status": equipment.status.value,
            "total_usage": equipment.total_usage_count,
            "maintenance_prediction": prediction,
        }
