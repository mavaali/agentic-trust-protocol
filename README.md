# The Agentic Trust Protocol

Research prototype: path-level safety architecture for AI agents.

> **Status:** Active research prototype. Single-replicate scenario data so far; multi-replicate evaluation in progress. See [STATUS.md](STATUS.md) for what's working and what isn't. Expect rough edges. Pre-publication feedback welcome.

## The Thesis

**A series of two-way doors composes into a one-way door.**

Per-call alignment in contemporary frontier models has progressed substantially — well-aligned 2026 models refuse the canonical agent-safety failures (CEO fraud, prompt injection, blast-radius reply-all) on their own merits. The residual failure surface for agents lives one layer up: in the *path* the agent walks across multiple calls, where individually-reversible actions compose into cumulatively irreversible trajectories.

A single forward pass evaluates one action at a time. It cannot, by construction, observe paths. Architectural primitives — a trust budget that approximates path-irreversibility, a staging area that exposes the proposed trajectory before it is walked, an irreversibility classifier whose output feeds the path-level computation — are the only layer at which path-level safety can be enforced. This project demonstrates and evaluates that claim.

## What's Here

- **Naive Agent:** Standard ReAct-style email agent. Single reasoning chain from observation to action. No guardrails.
- **Airlock Agent:** Same tool surface, CQRS-style architecture inside a Plan-then-Execute structure. Read path (observe/reason/draft) separated from write path (act), with a trust budget that approximates the path integral of irreversibility, a staging area for proposed actions, and a per-action irreversibility classifier.
- **Mock email backend** with seeded fixtures designed to exercise specific composition modes (quantity, premise, classification, iteration) plus an auto-responder hook for testing iteration-mode failures.
- **Evaluation harness:** five scenarios complete (A1, B1, B2, C1, D1); five more planned. See [eval/scenarios/](eval/scenarios/) and [docs/failure-catalog.md](docs/failure-catalog.md).

## Quick Start

```bash
# Clone (replace with your fork URL)
git clone <repo-url>
cd agentic-trust-protocol

# Install
pip install -e ".[dev]"

# Set up your API key
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# Reproduce the headline finding (single command, ~30 seconds)
python scripts/reproduce_a1.py

# Run an agent interactively
naive-agent      # naive ReAct baseline
airlock-agent    # CQRS-style architecture

# Run the full evaluation across all available scenarios
run-eval
```

## Reproducing the headline finding

`python scripts/reproduce_a1.py` runs the A1 (accumulator) scenario against both agents and prints the contrast. Expected pattern: naive agent fires ~8 outbound emails in one chain (each individually reasonable; cumulative count is the harm); airlock agent's trust budget caps execution at ~3 sends with the rest checkpointed. ~62% reduction in unsupervised actions.

This is the canonical example of a *quantity-mode* path-level failure — invisible to any single forward pass because catching it requires observing the count of write actions across the session, which is structurally external to the model's input. See [docs/paper/draft.md](docs/paper/draft.md) Section 3.6 for the structural argument.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  Airlock Agent                   │
│                                                  │
│  ┌──────────────┐    ┌─────────┐    ┌─────────┐ │
│  │  Read Path    │───▶│ Staging │───▶│  Write  │ │
│  │  (observe,    │    │  Area   │    │  Path   │ │
│  │   reason,     │    │         │    │         │ │
│  │   draft)      │    │         │    │  ┌────┐ │ │
│  └──────────────┘    └─────────┘    │  │Gate│ │ │
│                                      │  └────┘ │ │
│  Tools: read, search, list           │    │     │ │
│                                      │    ▼     │ │
│                               ┌──────┴────────┐ │
│                               │ Trust Budget   │ │
│                               │ Irreversibility│ │
│                               │ Checkpoint     │ │
│                               └───────────────┘ │
└─────────────────────────────────────────────────┘
```

## Results

Run `run-eval` to generate results across the available scenarios, or see [eval/results/](eval/results/) after evaluation. Single-replicate results discussed in [docs/paper/draft.md](docs/paper/draft.md) Section 6.4.

## Documentation

- [docs/research-brief.md](docs/research-brief.md) — what the project is and isn't, current scope
- [docs/paper/draft.md](docs/paper/draft.md) — paper outline under door-composition framing
- [docs/formal-model.md](docs/formal-model.md) — light formal sketch with citations to prior formal work
- [docs/failure-catalog.md](docs/failure-catalog.md) — ten cases organized by composition mode
- [docs/literature-map.md](docs/literature-map.md) — annotated bibliography across eight relevant areas
- [STATUS.md](STATUS.md) — current state, known limitations, what's not done yet
- [AUTHORS.md](AUTHORS.md) — current authorship and forthcoming attribution
- [CITATION.cff](CITATION.cff) — software citation metadata

## Contributing

This is research code; the priority is getting the framing and empirical claims right. If you find a sharp counter to the framing, an issue with the empirical methodology, or prior art the literature map missed, open an issue. PRs welcome for: additional scenario YAMLs, new failure modes, irreversibility-classifier alternatives, executor extensions for new action types.

## License

MIT
