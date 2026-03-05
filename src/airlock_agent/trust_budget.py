"""Trust budget: depletes on high-irreversibility actions, resets per session (ADR-003)."""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from src.shared.logging import get_logger

logger = get_logger("trust_budget")


@dataclass
class TrustBudget:
    """Manages a per-session trust budget.

    - Each session starts with a budget (default 3.0 points).
    - Each action deducts its irreversibility score.
    - Actions within budget proceed automatically.
    - Actions that would exceed remaining budget trigger a checkpoint.
    """

    initial_budget: float = field(
        default_factory=lambda: float(os.environ.get("TRUST_BUDGET_DEFAULT", "3.0"))
    )
    remaining: float = field(init=False)
    history: list[dict] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.remaining = self.initial_budget

    def can_afford(self, cost: float) -> bool:
        """Check if the action fits within the remaining budget."""
        return cost <= self.remaining

    def deduct(self, action_type: str, cost: float) -> None:
        """Deduct the cost from the budget."""
        self.remaining -= cost
        self.history.append({
            "action": action_type,
            "cost": cost,
            "remaining_after": self.remaining,
        })
        logger.info(
            "budget_deduction",
            action=action_type,
            cost=cost,
            remaining=self.remaining,
        )

    def reset(self) -> None:
        """Reset budget for a new session."""
        self.remaining = self.initial_budget
        self.history.clear()

    @property
    def spent(self) -> float:
        return self.initial_budget - self.remaining
