"""Evaluation harness: runs both agents against all scenarios, collects metrics."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from rich.console import Console

from src.mock_email.fixtures import AGENT_USER, seed_backend
from src.naive_agent.agent import NaiveAgent
from src.airlock_agent.agent import AirlockAgent
from src.airlock_agent.checkpoint import EvalCheckpoint
from src.shared.llm import LLMClient
from src.shared.logging import ActionTrace

from .metrics import EvalResults, ScenarioResult

console = Console()
SCENARIOS_DIR = Path(__file__).parent / "scenarios"
RESULTS_DIR = Path(__file__).parent / "results"


def load_scenarios() -> list[dict[str, Any]]:
    """Load all scenario YAML files."""
    scenarios = []
    for path in sorted(SCENARIOS_DIR.glob("*.yaml")):
        with open(path) as f:
            scenarios.append(yaml.safe_load(f))
    return scenarios


def is_harmful(trace: ActionTrace, scenario: dict[str, Any]) -> bool:
    """Check if a traced action is harmful according to the scenario definition."""
    harmful_actions = scenario.get("harmful_actions", [])
    disallowed = scenario.get("expected_behavior", {}).get("disallowed_actions", [])

    # Check explicit disallowed actions
    if trace.action_type in disallowed:
        return True

    # Check harmful action conditions
    for harmful in harmful_actions:
        if trace.action_type == harmful.get("action_type"):
            return True

    return False


def run_scenario_naive(
    scenario: dict[str, Any], llm: LLMClient
) -> ScenarioResult:
    """Run a single scenario with the naive agent."""
    backend = seed_backend()
    agent = NaiveAgent(backend=backend, llm=llm)
    traces = agent.run(scenario["task"], scenario_id=scenario["id"])

    harmful_count = 0
    for trace in traces:
        trace.was_harmful = is_harmful(trace, scenario)
        if trace.was_harmful:
            harmful_count += 1

    return ScenarioResult(
        scenario_id=scenario["id"],
        agent_type="naive",
        traces=traces,
        harmful_action_count=harmful_count,
        total_actions=len(traces),
    )


def run_scenario_airlock(
    scenario: dict[str, Any], llm: LLMClient
) -> ScenarioResult:
    """Run a single scenario with the airlock agent."""
    backend = seed_backend()
    checkpoint = EvalCheckpoint()
    agent = AirlockAgent(backend=backend, llm=llm, checkpoint=checkpoint)
    traces = agent.run(scenario["task"], scenario_id=scenario["id"])

    harmful_count = 0
    for trace in traces:
        trace.was_harmful = is_harmful(trace, scenario)
        if trace.was_harmful:
            harmful_count += 1

    return ScenarioResult(
        scenario_id=scenario["id"],
        agent_type="airlock",
        traces=traces,
        harmful_action_count=harmful_count,
        total_actions=len(traces),
        checkpoints_triggered=sum(1 for t in traces if t.checkpoint_triggered),
        checkpoints_rejected=sum(1 for t in traces if t.checkpoint_approved is False),
        final_trust_budget=agent.trust_budget.remaining,
    )


def run_eval() -> EvalResults:
    """Run full evaluation: both agents against all scenarios."""
    scenarios = load_scenarios()
    llm = LLMClient()
    results = EvalResults()

    console.print(f"\n[bold]Running evaluation: {len(scenarios)} scenarios x 2 agents[/bold]\n")

    for scenario in scenarios:
        console.print(f"\n[bold]{'='*60}[/bold]")
        console.print(f"[bold]Scenario: {scenario['name']}[/bold]")
        console.print(f"[bold]Type: {scenario['type']}[/bold]")
        console.print(f"[bold]{'='*60}[/bold]")

        # Run naive agent
        console.print("\n[bold yellow]--- Naive Agent ---[/bold yellow]")
        naive_result = run_scenario_naive(scenario, llm)
        results.add(naive_result)

        # Run airlock agent
        console.print("\n[bold cyan]--- Airlock Agent ---[/bold cyan]")
        airlock_result = run_scenario_airlock(scenario, llm)
        results.add(airlock_result)

    return results


def save_results(results: EvalResults) -> None:
    """Save results to JSON."""
    output = {
        "summary": results.summary(),
        "scenarios": [r.to_dict() for r in results.scenario_results],
    }
    output_path = RESULTS_DIR / "eval_results.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    console.print(f"\n[bold]Results saved to {output_path}[/bold]")


def main() -> None:
    """CLI entry point for running the full evaluation."""
    results = run_eval()
    results.print_table()
    save_results(results)


if __name__ == "__main__":
    main()
