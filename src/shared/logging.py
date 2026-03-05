"""Structured logging for evaluation traces."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import structlog
from pydantic import BaseModel, Field


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance."""
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    return structlog.get_logger(name)


class ActionTrace(BaseModel):
    """A single traced action from an agent run, used for evaluation."""

    timestamp: datetime = Field(default_factory=datetime.now)
    agent_type: str  # "naive" or "airlock"
    scenario_id: str
    step: int
    action_type: str  # "read_email", "send_email", "draft_email", etc.
    action_params: dict[str, Any] = Field(default_factory=dict)
    reasoning: str = ""
    irreversibility_score: float | None = None
    trust_budget_before: float | None = None
    trust_budget_after: float | None = None
    checkpoint_triggered: bool = False
    checkpoint_approved: bool | None = None
    was_harmful: bool | None = None  # set during evaluation

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
