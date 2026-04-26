"""Reproduce the headline A1 (accumulator) contrast in one command.

Runs the naive ReAct agent and the airlock (CQRS-style) agent against
the same scenario — eight unread emails warranting small write actions —
and prints the contrast in unsupervised outbound communications.

Usage:
    python scripts/reproduce_a1.py

Requires ANTHROPIC_API_KEY in environment or .env. Uses Sonnet 4 by default
(see src/shared/llm.py).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml

# Make 'src' importable when running from repo root
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Lightweight .env loader so users don't need python-dotenv. Treats unset and
# empty existing env vars equivalently — both get filled from .env.
env_path = ROOT / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip()
            if not os.environ.get(k):
                os.environ[k] = v

from src.airlock_agent.agent import AirlockAgent
from src.airlock_agent.checkpoint import EvalCheckpoint
from src.naive_agent.agent import NaiveAgent


SCENARIO_PATH = ROOT / "eval" / "scenarios" / "A1_accumulator.yaml"


def main() -> None:
    with SCENARIO_PATH.open() as f:
        scenario = yaml.safe_load(f)

    print("\n" + "=" * 70)
    print(f"REPRODUCING: {scenario['name']}")
    print("=" * 70)
    print(f"\n{scenario['description'].strip()}\n")
    print("=" * 70)

    print("\n--- NAIVE AGENT ---")
    naive = NaiveAgent(max_steps=20)
    naive_traces = naive.run(scenario["task"], scenario_id=scenario["id"])
    naive_writes = [
        t for t in naive_traces
        if t.action_type in ("send_email", "reply_all", "draft_email")
    ]

    print("\n--- AIRLOCK AGENT ---")
    airlock = AirlockAgent(checkpoint=EvalCheckpoint(), max_steps=20)
    airlock_traces = airlock.run(scenario["task"], scenario_id=scenario["id"])
    airlock_executed = airlock.backend.sent_log
    airlock_rejected = sum(1 for t in airlock_traces if t.checkpoint_approved is False)

    print("\n" + "=" * 70)
    print("CONTRAST")
    print("=" * 70)
    print(f"  Naive write actions executed:     {len(naive_writes)}")
    print(f"  Airlock write actions executed:   {len(airlock_executed)}")
    print(f"  Airlock checkpoints triggered:    {airlock_rejected}")
    print(f"  Airlock final trust budget:       {airlock.trust_budget.remaining:.2f}")
    if naive_writes:
        reduction = (1 - len(airlock_executed) / len(naive_writes)) * 100
        print(
            f"  Reduction in unsupervised actions: {reduction:.1f}% "
            f"({len(naive_writes)} -> {len(airlock_executed)})"
        )
    print("=" * 70)
    print(
        "\nExpected pattern: ~8 naive writes vs. ~3 airlock writes. The trust "
        "budget gates additional sends after ~3, demonstrating that the "
        "architecture catches the cumulative-quantity failure mode that no "
        "single forward pass can observe.\n"
    )


if __name__ == "__main__":
    main()
