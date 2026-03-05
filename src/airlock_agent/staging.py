"""Staging area: holds drafted actions before they are committed to the write path."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from src.shared.logging import get_logger

logger = get_logger("staging")


@dataclass
class StagedAction:
    """An action proposed by the read path, pending write-path approval."""

    id: str = field(default_factory=lambda: uuid4().hex[:8])
    action_type: str = ""
    params: dict[str, Any] = field(default_factory=dict)
    reasoning: str = ""
    irreversibility_score: float = 0.0
    approved: bool | None = None  # None = pending, True = approved, False = rejected

    def summary(self) -> str:
        status = "pending" if self.approved is None else ("approved" if self.approved else "rejected")
        return f"[{self.id}] {self.action_type} (irreversibility={self.irreversibility_score:.1f}) [{status}]"


class StagingArea:
    """Holds actions between the read path and write path."""

    def __init__(self) -> None:
        self._staged: list[StagedAction] = []

    def stage(
        self,
        action_type: str,
        params: dict[str, Any],
        reasoning: str,
        irreversibility_score: float,
    ) -> StagedAction:
        """Stage an action proposed by the read path."""
        action = StagedAction(
            action_type=action_type,
            params=params,
            reasoning=reasoning,
            irreversibility_score=irreversibility_score,
        )
        self._staged.append(action)
        logger.info("action_staged", action_id=action.id, type=action_type, score=irreversibility_score)
        return action

    @property
    def pending(self) -> list[StagedAction]:
        return [a for a in self._staged if a.approved is None]

    @property
    def all_actions(self) -> list[StagedAction]:
        return list(self._staged)

    def approve(self, action_id: str) -> StagedAction | None:
        for action in self._staged:
            if action.id == action_id:
                action.approved = True
                return action
        return None

    def reject(self, action_id: str) -> StagedAction | None:
        for action in self._staged:
            if action.id == action_id:
                action.approved = False
                return action
        return None

    def clear(self) -> None:
        self._staged.clear()
