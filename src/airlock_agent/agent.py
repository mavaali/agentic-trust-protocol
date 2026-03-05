"""Airlock agent — CQRS architecture with read/write path separation."""

from __future__ import annotations

from rich.console import Console

from src.mock_email.backend import EmailBackend
from src.mock_email.fixtures import AGENT_USER, seed_backend
from src.shared.llm import LLMClient
from src.shared.logging import ActionTrace, get_logger

from .checkpoint import Checkpoint, EvalCheckpoint
from .read_path import ReadPath
from .staging import StagingArea
from .trust_budget import TrustBudget
from .write_path import WritePath

console = Console()
logger = get_logger("airlock_agent")


class AirlockAgent:
    """CQRS-based agent: read path observes and stages, write path gates and executes."""

    def __init__(
        self,
        backend: EmailBackend | None = None,
        agent_email: str = AGENT_USER,
        llm: LLMClient | None = None,
        checkpoint: Checkpoint | None = None,
        initial_budget: float = 3.0,
        max_steps: int = 10,
    ) -> None:
        self.backend = backend or seed_backend()
        self.agent_email = agent_email
        self.staging = StagingArea()
        self.trust_budget = TrustBudget(initial_budget=initial_budget)
        self.checkpoint = checkpoint or EvalCheckpoint()

        self.read_path = ReadPath(
            backend=self.backend,
            staging=self.staging,
            agent_email=agent_email,
            llm=llm,
            max_steps=max_steps,
        )
        self.write_path = WritePath(
            backend=self.backend,
            staging=self.staging,
            trust_budget=self.trust_budget,
            agent_email=agent_email,
            checkpoint=self.checkpoint,
        )

    def run(self, task: str, scenario_id: str = "interactive") -> list[ActionTrace]:
        """Run the full airlock pipeline: read path -> staging -> write path."""
        console.print(f"\n[bold]{'='*60}[/bold]")
        console.print(f"[bold]Airlock Agent — Scenario: {scenario_id}[/bold]")
        console.print(f"[bold]Trust Budget: {self.trust_budget.remaining:.1f}[/bold]")
        console.print(f"[bold]{'='*60}[/bold]\n")

        # Phase 1: Read path observes and proposes actions
        console.print("[bold cyan]--- READ PATH ---[/bold cyan]")
        staged_actions = self.read_path.process(task)

        if not staged_actions:
            console.print("[dim]No actions proposed (read-only task).[/dim]")
            return []

        # Phase 2: Write path evaluates and executes staged actions
        console.print(f"\n[bold magenta]--- WRITE PATH ({len(staged_actions)} staged) ---[/bold magenta]")
        traces = self.write_path.process_staged(scenario_id=scenario_id)

        # Summary
        approved = sum(1 for t in traces if t.checkpoint_approved is not False)
        rejected = sum(1 for t in traces if t.checkpoint_approved is False)
        console.print(f"\n[bold]Results: {approved} approved, {rejected} rejected[/bold]")
        console.print(f"[bold]Budget remaining: {self.trust_budget.remaining:.1f}[/bold]")

        return traces


def main() -> None:
    """CLI entry point for interactive use."""
    console.print("[bold]Airlock Email Agent[/bold] (CQRS architecture)")
    console.print("Type a task or 'quit' to exit.\n")

    agent = AirlockAgent(checkpoint=Checkpoint(auto_approve=False))

    while True:
        task = console.input("[bold blue]Task:[/bold blue] ")
        if task.lower() in ("quit", "exit", "q"):
            break
        agent.run(task)
        agent.staging.clear()
        agent.trust_budget.reset()
        console.print()


if __name__ == "__main__":
    main()
