"""Evaluation metrics: harmful-action count, trust-budget usage, multi-replicate aggregation."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from statistics import mean, stdev
from typing import Any

from src.shared.logging import ActionTrace


@dataclass
class ScenarioResult:
    """Results from running one scenario with one agent (single replicate)."""

    scenario_id: str
    agent_type: str  # "naive" or "airlock"
    traces: list[ActionTrace] = field(default_factory=list)
    harmful_action_count: int = 0
    total_actions: int = 0
    write_action_count: int = 0
    checkpoints_triggered: int = 0
    checkpoints_rejected: int = 0
    final_trust_budget: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "agent_type": self.agent_type,
            "harmful_action_count": self.harmful_action_count,
            "total_actions": self.total_actions,
            "write_action_count": self.write_action_count,
            "checkpoints_triggered": self.checkpoints_triggered,
            "checkpoints_rejected": self.checkpoints_rejected,
            "final_trust_budget": self.final_trust_budget,
        }


@dataclass
class MultiReplicateResult:
    """N replicates of a single (scenario_id, agent_type) combination, with aggregates.

    Holds the raw replicate-level results and computes mean / std / bootstrap CI
    for the headline metrics (harmful_action_count, write_action_count,
    checkpoints_triggered).
    """

    scenario_id: str
    agent_type: str
    replicates: list[ScenarioResult] = field(default_factory=list)

    @property
    def n(self) -> int:
        return len(self.replicates)

    def _values(self, attr: str) -> list[float]:
        return [float(getattr(r, attr)) for r in self.replicates]

    def mean_of(self, attr: str) -> float:
        vals = self._values(attr)
        return mean(vals) if vals else 0.0

    def std_of(self, attr: str) -> float:
        vals = self._values(attr)
        return stdev(vals) if len(vals) > 1 else 0.0

    def bootstrap_ci(
        self, attr: str, confidence: float = 0.95, n_resamples: int = 1000
    ) -> tuple[float, float]:
        """Percentile bootstrap CI for the mean of `attr` across replicates.

        Returns (lower, upper). Uses Python stdlib only — no scipy dependency.
        For N < 3 replicates, returns (mean, mean) since CIs are not meaningful.
        """
        vals = self._values(attr)
        if len(vals) < 3:
            m = mean(vals) if vals else 0.0
            return (m, m)
        rng = random.Random(0xA1)  # seeded for reproducibility
        means: list[float] = []
        for _ in range(n_resamples):
            sample = [rng.choice(vals) for _ in vals]
            means.append(mean(sample))
        means.sort()
        alpha = 1.0 - confidence
        lo_idx = int(n_resamples * (alpha / 2))
        hi_idx = int(n_resamples * (1 - alpha / 2)) - 1
        return (means[lo_idx], means[hi_idx])

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "scenario_id": self.scenario_id,
            "agent_type": self.agent_type,
            "n_replicates": self.n,
            "replicates": [r.to_dict() for r in self.replicates],
        }
        for attr in ("harmful_action_count", "write_action_count", "checkpoints_triggered"):
            lo, hi = self.bootstrap_ci(attr)
            out[f"{attr}_mean"] = self.mean_of(attr)
            out[f"{attr}_std"] = self.std_of(attr)
            out[f"{attr}_ci95"] = [lo, hi]
        return out


def paired_bootstrap_diff(
    naive: MultiReplicateResult,
    airlock: MultiReplicateResult,
    attr: str = "write_action_count",
    n_resamples: int = 1000,
) -> dict[str, float]:
    """Bootstrap distribution of the mean difference (naive - airlock) on `attr`.

    Replicates are unpaired (different runs), so we resample each independently
    and compute the difference of means. Returns mean_diff, ci_lower, ci_upper,
    and a one-sided p-value-equivalent (fraction of bootstrap samples where
    naive <= airlock — small means strong evidence naive > airlock).
    """
    n_vals = [float(getattr(r, attr)) for r in naive.replicates]
    a_vals = [float(getattr(r, attr)) for r in airlock.replicates]
    if len(n_vals) < 3 or len(a_vals) < 3:
        diff = (mean(n_vals) if n_vals else 0.0) - (mean(a_vals) if a_vals else 0.0)
        return {"mean_diff": diff, "ci_lower": diff, "ci_upper": diff, "p_naive_le_airlock": -1.0}
    rng = random.Random(0xB2)
    diffs: list[float] = []
    for _ in range(n_resamples):
        n_sample = [rng.choice(n_vals) for _ in n_vals]
        a_sample = [rng.choice(a_vals) for _ in a_vals]
        diffs.append(mean(n_sample) - mean(a_sample))
    diffs.sort()
    p = sum(1 for d in diffs if d <= 0) / n_resamples
    return {
        "mean_diff": mean(diffs),
        "ci_lower": diffs[int(n_resamples * 0.025)],
        "ci_upper": diffs[int(n_resamples * 0.975) - 1],
        "p_naive_le_airlock": p,
    }


@dataclass
class EvalResults:
    """Aggregated results across all scenarios for both agents.

    In single-replicate mode, holds raw ScenarioResult objects.
    In multi-replicate mode, also holds MultiReplicateResult aggregates.
    """

    scenario_results: list[ScenarioResult] = field(default_factory=list)
    aggregates: list[MultiReplicateResult] = field(default_factory=list)

    def add(self, result: ScenarioResult) -> None:
        self.scenario_results.append(result)

    def add_aggregate(self, agg: MultiReplicateResult) -> None:
        self.aggregates.append(agg)

    def summary(self) -> dict[str, Any]:
        naive = [r for r in self.scenario_results if r.agent_type == "naive"]
        airlock = [r for r in self.scenario_results if r.agent_type == "airlock"]

        return {
            "naive": {
                "total_runs": len(naive),
                "total_harmful_actions": sum(r.harmful_action_count for r in naive),
                "total_actions": sum(r.total_actions for r in naive),
                "total_write_actions": sum(r.write_action_count for r in naive),
            },
            "airlock": {
                "total_runs": len(airlock),
                "total_harmful_actions": sum(r.harmful_action_count for r in airlock),
                "total_actions": sum(r.total_actions for r in airlock),
                "total_write_actions": sum(r.write_action_count for r in airlock),
                "total_checkpoints_triggered": sum(r.checkpoints_triggered for r in airlock),
                "total_checkpoints_rejected": sum(r.checkpoints_rejected for r in airlock),
            },
        }

    def print_table(self) -> None:
        from rich.console import Console
        from rich.table import Table

        console = Console()

        if self.aggregates:
            # Multi-replicate display: per-scenario means with CIs and paired diff
            table = Table(title=f"Multi-Replicate Evaluation Results")
            table.add_column("Scenario", style="bold")
            table.add_column("Naive writes (mean [95% CI])", justify="right")
            table.add_column("Airlock writes (mean [95% CI])", justify="right")
            table.add_column("Diff (naive - airlock)", justify="right")
            table.add_column("p(N≤A)", justify="right")

            scenarios = sorted({a.scenario_id for a in self.aggregates})
            for sid in scenarios:
                naive_agg = next(
                    (a for a in self.aggregates if a.scenario_id == sid and a.agent_type == "naive"),
                    None,
                )
                airlock_agg = next(
                    (a for a in self.aggregates if a.scenario_id == sid and a.agent_type == "airlock"),
                    None,
                )
                if not naive_agg or not airlock_agg:
                    continue
                n_mean = naive_agg.mean_of("write_action_count")
                n_lo, n_hi = naive_agg.bootstrap_ci("write_action_count")
                a_mean = airlock_agg.mean_of("write_action_count")
                a_lo, a_hi = airlock_agg.bootstrap_ci("write_action_count")
                diff_stats = paired_bootstrap_diff(
                    naive_agg, airlock_agg, attr="write_action_count"
                )
                table.add_row(
                    sid,
                    f"[red]{n_mean:.1f}[/red] [{n_lo:.1f}, {n_hi:.1f}]",
                    f"[green]{a_mean:.1f}[/green] [{a_lo:.1f}, {a_hi:.1f}]",
                    f"{diff_stats['mean_diff']:+.1f} [{diff_stats['ci_lower']:+.1f}, {diff_stats['ci_upper']:+.1f}]",
                    f"{diff_stats['p_naive_le_airlock']:.3f}"
                    if diff_stats["p_naive_le_airlock"] >= 0
                    else "n/a",
                )
            console.print(table)
            return

        # Single-replicate fallback
        summary = self.summary()
        table = Table(title="Evaluation Results (single replicate)")
        table.add_column("Metric", style="bold")
        table.add_column("Naive Agent", justify="right")
        table.add_column("Airlock Agent", justify="right")

        table.add_row(
            "Runs", str(summary["naive"]["total_runs"]), str(summary["airlock"]["total_runs"])
        )
        table.add_row(
            "Total Actions",
            str(summary["naive"]["total_actions"]),
            str(summary["airlock"]["total_actions"]),
        )
        table.add_row(
            "Write Actions",
            str(summary["naive"]["total_write_actions"]),
            str(summary["airlock"]["total_write_actions"]),
        )
        table.add_row(
            "Harmful Actions",
            f"[red]{summary['naive']['total_harmful_actions']}[/red]",
            f"[green]{summary['airlock']['total_harmful_actions']}[/green]",
        )
        table.add_row(
            "Checkpoints Triggered",
            "N/A",
            str(summary["airlock"]["total_checkpoints_triggered"]),
        )
        table.add_row(
            "Checkpoints Rejected",
            "N/A",
            str(summary["airlock"]["total_checkpoints_rejected"]),
        )

        console.print(table)
