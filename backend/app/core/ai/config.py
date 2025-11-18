from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class AISettings(BaseSettings):
    """AI and LangChain configuration settings."""

    # LLM Provider Settings
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API key")
    ANTHROPIC_API_KEY: str = Field(default="", description="Anthropic API key")
    LLM_PROVIDER: str = Field(
        default="openai", description="LLM provider: openai or anthropic"
    )
    LLM_MODEL: str = Field(
        default="gpt-4-turbo-preview",
        description="Model name for the LLM",
    )
    LLM_TEMPERATURE: float = Field(
        default=0.7, description="Temperature for LLM responses"
    )

    # ChromaDB Settings
    CHROMADB_HOST: str = Field(default="chromadb", description="ChromaDB host")
    CHROMADB_PORT: int = Field(default=8001, description="ChromaDB port")
    CHROMADB_COLLECTION_NAME: str = Field(
        default="gym_knowledge", description="ChromaDB collection name"
    )

    # LangSmith Settings (for monitoring)
    LANGSMITH_API_KEY: str = Field(default="", description="LangSmith API key")
    LANGSMITH_PROJECT: str = Field(
        default="ai-gym-management", description="LangSmith project name"
    )
    LANGSMITH_TRACING: bool = Field(
        default=False, description="Enable LangSmith tracing"
    )

    # Agent Settings
    AGENT_MAX_ITERATIONS: int = Field(
        default=10, description="Maximum iterations for agent execution"
    )
    AGENT_TIMEOUT: int = Field(
        default=300, description="Agent execution timeout in seconds"
    )

    # Churn Prediction Settings
    CHURN_PREDICTION_THRESHOLD: float = Field(
        default=0.7,
        description="Probability threshold for churn risk classification",
    )
    CHURN_LOOKBACK_DAYS: int = Field(
        default=30, description="Days to look back for churn analysis"
    )

    # Equipment Maintenance Settings
    MAINTENANCE_PREDICTION_DAYS: int = Field(
        default=14,
        description="Days ahead to predict maintenance needs",
    )
    EQUIPMENT_USAGE_THRESHOLD: int = Field(
        default=1000,
        description="Usage count threshold for maintenance alert",
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global AI settings instance
ai_settings = AISettings()
