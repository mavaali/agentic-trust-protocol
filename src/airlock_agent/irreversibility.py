"""Rule-based irreversibility classifier (ADR-002)."""

from __future__ import annotations

IRREVERSIBILITY_RULES: dict[str, float] = {
    "send_email": 0.9,
    "reply_all": 1.0,
    "schedule_meeting": 0.7,
    "draft_email": 0.1,
    "read_email": 0.0,
    "list_inbox": 0.0,
    "list_unread": 0.0,
    "search_inbox": 0.0,
}


def classify(action_type: str) -> float:
    """Return the irreversibility score for an action type.

    Returns 0.5 for unknown actions (conservative default).
    """
    return IRREVERSIBILITY_RULES.get(action_type, 0.5)


def is_read_only(action_type: str) -> bool:
    """Check if an action is purely observational (no side effects)."""
    return classify(action_type) == 0.0


def is_high_risk(action_type: str, threshold: float = 0.7) -> bool:
    """Check if an action is above the high-risk threshold."""
    return classify(action_type) >= threshold
