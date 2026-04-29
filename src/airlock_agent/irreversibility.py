"""Rule-based irreversibility classifier (ADR-002)."""

from __future__ import annotations

from typing import Any

IRREVERSIBILITY_RULES: dict[str, float] = {
    "send_email": 0.9,
    "reply_all": 1.0,
    "schedule_meeting": 0.9,
    "draft_email": 0.1,
    "archive_email": 0.2,
    "delete_email": 1.0,
    "read_email": 0.0,
    "list_inbox": 0.0,
    "list_unread": 0.0,
    "search_inbox": 0.0,
}


def classify(action_type: str, params: dict[str, Any] | None = None) -> float:
    """Return the irreversibility score for an action type.

    Returns 0.5 for unknown actions (conservative default).

    Params-aware scaling: for actions that fan out to multiple recipients,
    the score scales with audience size (each additional recipient beyond
    two adds 0.05, capped at 1.0). This captures the intuition that a
    12-person calendar invite is more irreversible than a 1:1.
    """
    base = IRREVERSIBILITY_RULES.get(action_type, 0.5)
    if params is None:
        return base

    n_audience = 0
    if action_type == "schedule_meeting":
        n_audience = len(params.get("attendees", []) or [])
    elif action_type in ("send_email", "reply_all"):
        recipients = params.get("recipients", []) or []
        cc = params.get("cc", []) or []
        n_audience = len(recipients) + len(cc)

    if n_audience >= 2:
        scaled = base + 0.05 * min(n_audience - 2, 10)
        return min(scaled, 1.0)
    return base


def is_read_only(action_type: str) -> bool:
    """Check if an action is purely observational (no side effects)."""
    return classify(action_type) == 0.0


def is_high_risk(action_type: str, threshold: float = 0.7) -> bool:
    """Check if an action is above the high-risk threshold."""
    return classify(action_type) >= threshold
