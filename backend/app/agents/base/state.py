from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class AgentStatus(str, Enum):
    """Agent execution status."""

    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class AgentType(str, Enum):
    """Types of AI agents in the system."""

    MEMBER_ENGAGEMENT = "member_engagement"
    OPERATIONS = "operations"
    FINANCIAL = "financial"
    HEALTH_WELLNESS = "health_wellness"
    BUSINESS_INTELLIGENCE = "business_intelligence"


class AgentState(BaseModel):
    """State model for agent execution."""

    agent_type: AgentType
    status: AgentStatus = AgentStatus.IDLE
    current_iteration: int = 0
    max_iterations: int = 10
    context: Dict[str, Any] = Field(default_factory=dict)
    messages: List[Dict[str, str]] = Field(default_factory=list)
    results: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True


class AgentAction(BaseModel):
    """Agent action model."""

    action_type: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentResult(BaseModel):
    """Agent execution result."""

    agent_type: AgentType
    status: AgentStatus
    success: bool
    results: Dict[str, Any] = Field(default_factory=dict)
    actions_taken: List[AgentAction] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    execution_time: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True
