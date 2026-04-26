"""Write path: action channel with irreversibility gate and trust budget."""

from __future__ import annotations

from rich.console import Console

from src.mock_email.backend import EmailBackend
from src.shared.logging import ActionTrace, get_logger

from .checkpoint import Checkpoint, EvalCheckpoint
from .staging import StagedAction, StagingArea
from .trust_budget import TrustBudget

console = Console()
logger = get_logger("write_path")


class WritePath:
    """Processes staged actions: checks budget, gates high-risk actions, executes."""

    def __init__(
        self,
        backend: EmailBackend,
        staging: StagingArea,
        trust_budget: TrustBudget,
        agent_email: str,
        checkpoint: Checkpoint | None = None,
    ) -> None:
        self.backend = backend
        self.staging = staging
        self.trust_budget = trust_budget
        self.agent_email = agent_email
        self.checkpoint = checkpoint or EvalCheckpoint()

    def process_staged(self, scenario_id: str = "interactive") -> list[ActionTrace]:
        """Process all pending staged actions through the write path."""
        traces: list[ActionTrace] = []

        for i, action in enumerate(self.staging.pending):
            trace = self._process_one(action, step=i, scenario_id=scenario_id)
            traces.append(trace)

        return traces

    def _process_one(self, action: StagedAction, step: int, scenario_id: str) -> ActionTrace:
        score = action.irreversibility_score
        budget_before = self.trust_budget.remaining
        checkpoint_triggered = False
        checkpoint_approved = None

        console.print(f"\n[bold magenta]Write Path:[/bold magenta] {action.summary()}")

        if action.irreversibility_score == 0.0:
            # Read-only actions pass through (shouldn't normally be staged)
            action.approved = True
            console.print("[green]Approved (read-only)[/green]")

        elif self.trust_budget.can_afford(score):
            # Within budget — auto-approve
            self.trust_budget.deduct(action.action_type, score)
            action.approved = True
            console.print(
                f"[green]Approved (budget: {budget_before:.1f} -> {self.trust_budget.remaining:.1f})[/green]"
            )

        else:
            # Over budget — checkpoint
            checkpoint_triggered = True
            console.print(
                f"[red]Over budget! (need {score:.1f}, have {self.trust_budget.remaining:.1f})[/red]"
            )
            approved = self.checkpoint.request_approval(action)
            checkpoint_approved = approved
            if approved:
                self.trust_budget.deduct(action.action_type, score)
                action.approved = True
                self.staging.approve(action.id)
                console.print("[yellow]Checkpoint approved[/yellow]")
            else:
                action.approved = False
                self.staging.reject(action.id)
                console.print("[red]Checkpoint rejected[/red]")

        # Execute if approved
        if action.approved:
            self._execute(action)

        return ActionTrace(
            agent_type="airlock",
            scenario_id=scenario_id,
            step=step,
            action_type=action.action_type,
            action_params=action.params,
            reasoning=action.reasoning,
            irreversibility_score=score,
            trust_budget_before=budget_before,
            trust_budget_after=self.trust_budget.remaining,
            checkpoint_triggered=checkpoint_triggered,
            checkpoint_approved=checkpoint_approved,
        )

    def _execute(self, action: StagedAction) -> None:
        """Execute an approved action against the backend."""
        params = action.params

        if action.action_type == "send_email":
            self.backend.send_email(
                sender=self.agent_email,
                recipients=params.get("recipients", []),
                subject=params.get("subject", ""),
                body=params.get("body", ""),
                cc=params.get("cc"),
                reply_to_id=params.get("reply_to_id"),
            )
            console.print("[green]Email sent.[/green]")

        elif action.action_type == "reply_all":
            original = self.backend.read_email(self.agent_email, params.get("email_id", ""))
            if original:
                all_recipients = list(
                    set([original.sender] + original.recipients + original.cc) - {self.agent_email}
                )
                self.backend.send_email(
                    sender=self.agent_email,
                    recipients=all_recipients,
                    subject=f"Re: {original.subject}",
                    body=params.get("body", ""),
                    reply_to_id=original.id,
                )
                console.print(f"[green]Reply-all sent to {len(all_recipients)} recipients.[/green]")

        elif action.action_type == "draft_email":
            self.backend.draft_email(
                sender=self.agent_email,
                recipients=params.get("recipients", []),
                subject=params.get("subject", ""),
                body=params.get("body", ""),
            )
            console.print("[green]Draft created.[/green]")

        elif action.action_type == "schedule_meeting":
            attendees = params.get("attendees", [])
            self.backend.send_email(
                sender=self.agent_email,
                recipients=attendees,
                subject=f"Calendar invite: {params.get('subject', '')}",
                body=(
                    f"Date: {params.get('date', '')}\n"
                    f"Time: {params.get('start_time', '')} - {params.get('end_time', '')}\n"
                    f"Location: {params.get('location', '')}\n\n"
                    f"{params.get('description', '')}"
                ),
            )
            console.print(f"[green]Calendar invite sent to {len(attendees)} attendees.[/green]")

        else:
            logger.warning("unknown_action", action_type=action.action_type)
