"""LLM client wrapper — defaults to Anthropic Claude, swappable."""

from __future__ import annotations

import os
from dataclasses import dataclass, field

import anthropic


@dataclass
class LLMClient:
    """Thin wrapper around the Anthropic SDK for agent use."""

    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096
    _client: anthropic.Anthropic | None = field(default=None, repr=False)
    chat_count: int = 0

    def __post_init__(self) -> None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set. Copy .env.example to .env and fill it in.")
        self._client = anthropic.Anthropic(api_key=api_key)

    def chat(
        self,
        messages: list[dict],
        system: str | None = None,
        tools: list[dict] | None = None,
    ) -> anthropic.types.Message:
        """Single-turn chat completion with optional tool use."""
        kwargs: dict = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": messages,
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = tools
        self.chat_count += 1
        return self._client.messages.create(**kwargs)

    def complete(self, prompt: str, system: str | None = None) -> str:
        """Simple text completion — returns assistant text."""
        messages = [{"role": "user", "content": prompt}]
        response = self.chat(messages, system=system)
        return response.content[0].text
