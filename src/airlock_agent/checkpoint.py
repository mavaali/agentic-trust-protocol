"""Human-in-the-loop gate for actions above the trust budget threshold."""

from __future__ import annotations

from rich.console import Console

from .staging import StagedAction

console = Console()


class Checkpoint:
    """Gate that pauses execution for human approval on high-risk actions."""

    def __init__(self, auto_approve: bool = False) -> None:
        self.auto_approve = auto_approve
        self.decisions: list[dict] = []

    def request_approval(self, action: StagedAction) -> bool:
        """Ask for human approval. Returns True if approved.

        In eval mode (auto_approve=False), this simulates a human rejecting
        high-risk actions that exceed the trust budget. In interactive mode,
        it prompts the user.
        """
        if self.auto_approve:
            self.decisions.append({"action_id": action.id, "approved": True, "mode": "auto"})
            return True

        console.print("\n[bold red]--- CHECKPOINT ---[/bold red]")
        console.print(f"Action: [bold]{action.action_type}[/bold]")
        console.print(f"Irreversibility: [bold]{action.irreversibility_score:.1f}[/bold]")
        console.print(f"Reasoning: {action.reasoning}")
        console.print(f"Params: {action.params}")

        response = console.input("\n[bold]Approve? (y/n): [/bold]").strip().lower()
        approved = response in ("y", "yes")
        self.decisions.append({"action_id": action.id, "approved": approved, "mode": "interactive"})
        return approved


class EvalCheckpoint(Checkpoint):
    """Checkpoint for evaluation: rejects all actions that trigger it.

    This simulates a cautious human who always denies requests that
    exceed the trust budget — the ideal behavior the airlock enables.
    """

    def __init__(self) -> None:
        super().__init__(auto_approve=False)

    def request_approval(self, action: StagedAction) -> bool:
        self.decisions.append({"action_id": action.id, "approved": False, "mode": "eval_reject"})
        return False
