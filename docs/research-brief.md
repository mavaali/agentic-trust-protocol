# Research Brief

## Problem

AI agents are increasingly granted the ability to take real-world actions — sending emails, executing code, managing infrastructure. Current agent architectures (ReAct, chain-of-thought + tools) treat observation and action as a single reasoning chain. This means a hallucination or prompt injection at the reasoning stage can flow directly into an irreversible action.

## Thesis

Trust in agentic AI is an architecture problem, not a model problem. By applying CQRS (Command Query Responsibility Segregation) patterns from distributed systems to agent design, we can create an "airlock" that separates observation from action. This architectural intervention prevents the class of failures where bad reasoning leads to bad actions, without requiring a better model.

## Key Claims

1. The single-chain ReAct pattern is structurally vulnerable to cascading failures
2. Separating read (observe/reason) from write (act) paths creates a natural checkpoint
3. An irreversibility classifier + trust budget can automate low-risk actions while gating high-risk ones
4. This architecture trades latency for safety — and the trade-off is quantifiable

## Scope

- **In scope:** Email agent prototype, mock backend, 10 evaluation scenarios, quantitative comparison
- **Out of scope:** Real email integration, learned irreversibility classifiers, multi-agent coordination

## Status

- [ ] Failure catalog (8-10 cases)
- [ ] Literature map (4 domains)
- [ ] Formal model
- [ ] Prototype implementation
- [ ] Evaluation
- [ ] Paper draft
