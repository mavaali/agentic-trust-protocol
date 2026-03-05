# The Agentic Trust Protocol

Research prototype: CQRS-based trust architecture for AI agents.

## The Thesis

Trust in agentic AI is an architecture problem, not a model problem. Separating observation from action — like CQRS in distributed systems — prevents the class of failures where a hallucinated premise leads directly to an irreversible action. This project demonstrates and evaluates that claim.

## What's Here

- **Naive Agent (Version A):** Standard ReAct-style email agent. Single reasoning chain from observation to action. No guardrails.
- **Airlock Agent (Version B):** Same capabilities, CQRS architecture. Read path (observe/reason/draft) separated from write path (act). Includes irreversibility classifier, trust budget, and human checkpoint.
- **Evaluation harness:** 10 scenarios (benign, adversarial, edge cases) comparing both agents on harmful-action rate.

## Quick Start

```bash
# Clone and install
git clone https://github.com/your-username/agentic-trust-protocol.git
cd agentic-trust-protocol
pip install -e ".[dev]"

# Set up your API key
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# Run the naive agent interactively
naive-agent

# Run the airlock agent interactively
airlock-agent

# Run the full evaluation
run-eval
```

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

Run `run-eval` to generate results, or see `eval/results/` after evaluation.

## Paper

See `docs/paper/draft.md` (in progress).

## Contributing

- Branch per feature: `feat/*` for prototype, `docs/*` for research, `eval/*` for evaluation
- Weekly sync notes in `docs/sync/`
- Design decisions as ADRs in code comments and docs

## License

MIT
