"""Evaluation metrics: harmful-action count, trust-budget usage, latency."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.shared.logging import ActionTrace


@dataclass
class ScenarioResult:
    """Results from running one scenario with one agent."""

    scenario_id: str
    agent_type: str  # "naive" or "airlock"
    traces: list[ActionTrace] = field(default_factory=list)
    harmful_action_count: int = 0
    total_actions: int = 0
    checkpoints_triggered: int = 0
    checkpoints_rejected: int = 0
    final_trust_budget: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "agent_type": self.agent_type,
            "harmful_action_count": self.harmful_action_count,
            "total_actions": self.total_actions,
            "checkpoints_triggered": self.checkpoints_triggered,
            "checkpoints_rejected": self.checkpoints_rejected,
            "final_trust_budget": self.final_trust_budget,
        }


@dataclass
class EvalResults:
    """Aggregated results across all scenarios for both agents."""

    scenario_results: list[ScenarioResult] = field(default_factory=list)

    def add(self, result: ScenarioResult) -> None:
        self.scenario_results.append(result)

    def summary(self) -> dict[str, Any]:
        naive = [r for r in self.scenario_results if r.agent_type == "naive"]
        airlock = [r for r in self.scenario_results if r.agent_type == "airlock"]

        return {
            "naive": {
                "total_scenarios": len(naive),
                "total_harmful_actions": sum(r.harmful_action_count for r in naive),
                "total_actions": sum(r.total_actions for r in naive),
                "harmful_rate": (
                    sum(r.harmful_action_count for r in naive) / max(sum(r.total_actions for r in naive), 1)
                ),
            },
            "airlock": {
                "total_scenarios": len(airlock),
                "total_harmful_actions": sum(r.harmful_action_count for r in airlock),
                "total_actions": sum(r.total_actions for r in airlock),
                "harmful_rate": (
                    sum(r.harmful_action_count for r in airlock) / max(sum(r.total_actions for r in airlock), 1)
                ),
                "total_checkpoints_triggered": sum(r.checkpoints_triggered for r in airlock),
                "total_checkpoints_rejected": sum(r.checkpoints_rejected for r in airlock),
            },
        }

    def print_table(self) -> None:
        from rich.console import Console
        from rich.table import Table

        console = Console()
        summary = self.summary()

        table = Table(title="Evaluation Results")
        table.add_column("Metric", style="bold")
        table.add_column("Naive Agent", justify="right")
        table.add_column("Airlock Agent", justify="right")

        table.add_row("Scenarios", str(summary["naive"]["total_scenarios"]), str(summary["airlock"]["total_scenarios"]))
        table.add_row("Total Actions", str(summary["naive"]["total_actions"]), str(summary["airlock"]["total_actions"]))
        table.add_row(
            "Harmful Actions",
            f"[red]{summary['naive']['total_harmful_actions']}[/red]",
            f"[green]{summary['airlock']['total_harmful_actions']}[/green]",
        )
        table.add_row(
            "Harmful Rate",
            f"[red]{summary['naive']['harmful_rate']:.1%}[/red]",
            f"[green]{summary['airlock']['harmful_rate']:.1%}[/green]",
        )
        table.add_row(
            "Checkpoints Triggered", "N/A", str(summary["airlock"]["total_checkpoints_triggered"])
        )
        table.add_row(
            "Checkpoints Rejected", "N/A", str(summary["airlock"]["total_checkpoints_rejected"])
        )

        console.print(table)
