"""
LLM client abstraction for multiple providers.

Supports OpenAI and Anthropic with a unified interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from src.config import settings


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters

        Returns:
            Generated text response
        """
        pass

    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ):
        """
        Generate a streaming response from the LLM.

        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters

        Yields:
            Text chunks as they are generated
        """
        pass


class OpenAILLMClient(LLMClient):
    """OpenAI LLM client implementation."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ):
        """
        Initialize OpenAI client.

        Args:
            api_key: OpenAI API key (defaults to settings)
            model: Model name (default: gpt-4)
            temperature: Default temperature
            max_tokens: Default max tokens
        """
        self.api_key = api_key or settings.openai_api_key
        if not self.api_key:
            raise ValueError("OpenAI API key is required")

        self.model = model
        self.default_temperature = temperature
        self.default_max_tokens = max_tokens

        self.client = ChatOpenAI(
            model=self.model,
            temperature=self.default_temperature,
            max_tokens=self.default_max_tokens,
            openai_api_key=self.api_key,
        )

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> str:
        """Generate a response using OpenAI."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Create a temporary client with custom parameters
        client = ChatOpenAI(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens or self.default_max_tokens,
            openai_api_key=self.api_key,
            **kwargs
        )

        response = await client.ainvoke(messages)
        return response.content

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ):
        """Generate a streaming response using OpenAI."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        client = ChatOpenAI(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens or self.default_max_tokens,
            openai_api_key=self.api_key,
            **kwargs
        )

        async for chunk in client.astream(messages):
            if chunk.content:
                yield chunk.content


class AnthropicLLMClient(LLMClient):
    """Anthropic Claude LLM client implementation."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-opus-20240229",
        temperature: float = 0.7,
        max_tokens: Optional[int] = 1024,
    ):
        """
        Initialize Anthropic client.

        Args:
            api_key: Anthropic API key (defaults to settings)
            model: Model name (default: claude-3-opus-20240229)
            temperature: Default temperature
            max_tokens: Default max tokens
        """
        self.api_key = api_key or settings.anthropic_api_key
        if not self.api_key:
            raise ValueError("Anthropic API key is required")

        self.model = model
        self.default_temperature = temperature
        self.default_max_tokens = max_tokens or 1024

        self.client = ChatAnthropic(
            model=self.model,
            temperature=self.default_temperature,
            max_tokens=self.default_max_tokens,
            anthropic_api_key=self.api_key,
        )

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> str:
        """Generate a response using Anthropic."""
        messages = [{"role": "user", "content": prompt}]

        client = ChatAnthropic(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens or self.default_max_tokens,
            anthropic_api_key=self.api_key,
            system=system_prompt,
            **kwargs
        )

        response = await client.ainvoke(messages)
        return response.content

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ):
        """Generate a streaming response using Anthropic."""
        messages = [{"role": "user", "content": prompt}]

        client = ChatAnthropic(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens or self.default_max_tokens,
            anthropic_api_key=self.api_key,
            system=system_prompt,
            **kwargs
        )

        async for chunk in client.astream(messages):
            if chunk.content:
                yield chunk.content


def create_llm_client(
    provider: str = "openai",
    model: Optional[str] = None,
    **kwargs: Any
) -> LLMClient:
    """
    Factory function to create an LLM client.

    Args:
        provider: LLM provider ("openai" or "anthropic")
        model: Model name (optional, uses defaults)
        **kwargs: Additional client parameters

    Returns:
        LLMClient instance

    Raises:
        ValueError: If provider is not supported
    """
    if provider.lower() == "openai":
        model = model or "gpt-4"
        return OpenAILLMClient(model=model, **kwargs)
    elif provider.lower() == "anthropic":
        model = model or "claude-3-opus-20240229"
        return AnthropicLLMClient(model=model, **kwargs)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
