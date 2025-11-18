from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio
from app.agents.base.state import (
    AgentState,
    AgentStatus,
    AgentType,
    AgentResult,
    AgentAction,
)
from app.core.ai.llm import llm_provider
from app.core.ai.config import ai_settings
from sqlalchemy.ext.asyncio import AsyncSession


class BaseAgent(ABC):
    """Base class for all AI agents."""

    def __init__(
        self,
        agent_type: AgentType,
        db: Optional[AsyncSession] = None,
    ):
        self.agent_type = agent_type
        self.db = db
        self.llm = llm_provider.get_llm()
        self.state = AgentState(
            agent_type=agent_type,
            max_iterations=ai_settings.AGENT_MAX_ITERATIONS,
        )

    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> AgentResult:
        """Execute the agent's main logic."""
        pass

    @abstractmethod
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data and provide insights."""
        pass

    async def run(self, context: Dict[str, Any]) -> AgentResult:
        """Run the agent with proper state management."""
        self.state.status = AgentStatus.RUNNING
        self.state.started_at = datetime.utcnow()
        self.state.context = context

        try:
            # Execute with timeout
            result = await asyncio.wait_for(
                self.execute(context),
                timeout=ai_settings.AGENT_TIMEOUT,
            )

            self.state.status = AgentStatus.COMPLETED
            self.state.completed_at = datetime.utcnow()

            return result

        except asyncio.TimeoutError:
            self.state.status = AgentStatus.FAILED
            self.state.errors.append("Agent execution timed out")

            return AgentResult(
                agent_type=self.agent_type,
                status=AgentStatus.FAILED,
                success=False,
                errors=["Execution timed out"],
            )

        except Exception as e:
            self.state.status = AgentStatus.FAILED
            self.state.errors.append(str(e))

            return AgentResult(
                agent_type=self.agent_type,
                status=AgentStatus.FAILED,
                success=False,
                errors=[str(e)],
            )

    def add_action(self, action_type: str, parameters: Dict[str, Any]):
        """Record an action taken by the agent."""
        action = AgentAction(
            action_type=action_type,
            parameters=parameters,
        )
        # Store in state for tracking
        if "actions" not in self.state.metadata:
            self.state.metadata["actions"] = []
        self.state.metadata["actions"].append(action.model_dump())

    async def log_message(self, role: str, content: str):
        """Log a message in the agent's conversation."""
        self.state.messages.append(
            {
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    def update_context(self, key: str, value: Any):
        """Update agent context."""
        self.state.context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """Get value from agent context."""
        return self.state.context.get(key, default)
