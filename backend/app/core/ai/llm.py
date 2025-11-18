from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import BaseMessage
from app.core.ai.config import ai_settings


class LLMProvider:
    """Wrapper for LLM provider management."""

    _instance: Optional["LLMProvider"] = None

    def __init__(self):
        self.provider = ai_settings.LLM_PROVIDER
        self.model = ai_settings.LLM_MODEL
        self.temperature = ai_settings.LLM_TEMPERATURE
        self._llm = None

    @classmethod
    def get_instance(cls) -> "LLMProvider":
        """Get singleton instance of LLM provider."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_llm(self):
        """Get the configured LLM instance."""
        if self._llm is None:
            if self.provider == "openai":
                self._llm = ChatOpenAI(
                    model=self.model,
                    temperature=self.temperature,
                    api_key=ai_settings.OPENAI_API_KEY,
                )
            elif self.provider == "anthropic":
                self._llm = ChatAnthropic(
                    model=self.model,
                    temperature=self.temperature,
                    api_key=ai_settings.ANTHROPIC_API_KEY,
                )
            else:
                raise ValueError(f"Unsupported LLM provider: {self.provider}")

        return self._llm

    async def ainvoke(self, messages: list[BaseMessage]) -> str:
        """Async invoke the LLM with messages."""
        llm = self.get_llm()
        response = await llm.ainvoke(messages)
        return response.content


# Global LLM provider instance
llm_provider = LLMProvider.get_instance()
