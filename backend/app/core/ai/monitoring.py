import os
import time
from typing import Optional, Dict, Any
from datetime import datetime
from app.core.ai.config import ai_settings
from app.core.logging import StructuredLogger


class AgentMonitor:
    """
    Monitor and log AI agent activities.
    Integrates with LangSmith for production monitoring.
    """

    def __init__(self):
        self.enabled = ai_settings.LANGSMITH_TRACING
        self.logger = StructuredLogger('agents.monitor')
        self.langsmith_client = None

        if self.enabled:
            # Initialize LangSmith client via environment variables
            # LangChain automatically picks up these environment variables
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_API_KEY"] = ai_settings.LANGSMITH_API_KEY or ""
            os.environ["LANGCHAIN_PROJECT"] = ai_settings.LANGSMITH_PROJECT or "gym-ai"
            os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

            self.logger.info(
                "LangSmith monitoring enabled",
                project=ai_settings.LANGSMITH_PROJECT
            )
        else:
            self.logger.info("LangSmith monitoring disabled - using local logging only")

    def log_agent_execution(
        self,
        agent_type: str,
        execution_time: float,
        success: bool,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Log agent execution metrics."""
        log_data = {
            "agent_type": agent_type,
            "execution_time_seconds": execution_time,
            "success": success,
            **(metadata or {})
        }

        if success:
            self.logger.info(
                f"Agent execution completed: {agent_type}",
                **log_data
            )
        else:
            self.logger.error(
                f"Agent execution failed: {agent_type}",
                **log_data
            )

        # LangSmith tracing is automatic via environment variables when using LangChain
        # No manual sending needed - traces are captured automatically

    def log_llm_call(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        cost: float,
        latency: float,
    ):
        """Log LLM API call metrics."""
        total_tokens = prompt_tokens + completion_tokens

        self.logger.info(
            f"LLM API call completed: {model}",
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost_usd=cost,
            latency_seconds=latency,
            cost_per_1k_tokens=cost / (total_tokens / 1000) if total_tokens > 0 else 0
        )

        # LangSmith automatically captures LLM calls when tracing is enabled

    def log_agent_action(
        self,
        agent_type: str,
        action_type: str,
        parameters: Dict[str, Any],
        result: Any,
    ):
        """Log specific agent actions."""
        self.logger.info(
            f"Agent action: {agent_type} - {action_type}",
            agent_type=agent_type,
            action_type=action_type,
            parameters=parameters,
            result=str(result)[:200]  # Truncate long results
        )

    def log_agent_error(
        self,
        agent_type: str,
        error_type: str,
        error_message: str,
        stack_trace: Optional[str] = None,
    ):
        """Log agent errors."""
        self.logger.error(
            f"Agent error: {agent_type} - {error_type}",
            agent_type=agent_type,
            error_type=error_type,
            error_message=error_message,
            stack_trace=stack_trace
        )

    def track_metrics(
        self,
        metric_name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None
    ):
        """Track custom metrics."""
        self.logger.info(
            f"Metric tracked: {metric_name}",
            metric_name=metric_name,
            value=value,
            tags=tags or {}
        )


# Global monitor instance
agent_monitor = AgentMonitor()
