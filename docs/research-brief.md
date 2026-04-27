# Research Brief

## Problem

AI agents are increasingly granted the ability to take real-world actions — sending emails, executing code, managing infrastructure. Per-call alignment in contemporary frontier models has progressed substantially: a well-aligned 2026 model refuses the canonical agent-safety failure modes (CEO-fraud wires, blast-radius reply-alls, crude prompt injection in primary content) on its own merits, without any architectural intervention. This is good. It is also misleading. The failures that survive a well-aligned per-call model are precisely the ones a single forward pass cannot see: failures that live in the *path* the agent walks across multiple calls, not in any individual call.

## Framing

**A series of two-way doors composes into a one-way door.**

Per-call safety classifies individual doors. Each forward pass evaluates one action against its inputs and returns a judgment. But the agent is walking a path, and the world moves between steps — because the agent is moving it. By the time the agent has passed through several doors, the trajectory has crossed into a region from which retreat is no longer available, even though no single door it walked was one-way at the moment it walked through.

Per-call alignment cannot, by construction, observe paths. The path lives in state outside any single forward pass: prior actions taken, premises now in flight, recipients now informed, calendars now changed, audit logs now written. Architectural primitives that observe state outside the model — a trust budget that approximates path-irreversibility, a staging area that exposes the proposed trajectory before it is walked, an irreversibility classifier whose output feeds the path-level computation — are the layer at which path-level safety can be enforced.

## Contribution

This is a synthesis-and-framing paper, not a theorem paper. The mathematical core (locally-reversible decisions composing into globally-irreversible trajectories) has been formalized in economics (Arthur 1989), safe RL (Krakovna et al. 2018), and distributed systems (Garcia-Molina & Salem 1987). The path-level safety claim for LLM agents specifically has been made in SafetyDrift (Dhodapkar & Pishori 2026). The architectural separation has been proposed under "Plan-then-Execute" (Del Rosario et al. 2025).

What this paper contributes is the **conceptual scaffolding** the field can use to think about path-level agent safety:

1. The **door-composition framing** applied specifically to LLM agents in the post-aligned-model era. The math has antecedents; the framing applied to this domain, with the right metaphor, is sticky in a way that prior framings are not.
2. The **four composition modes** — accumulation, premise, classification, iteration — as an analytic taxonomy of the mechanisms by which two-way doors compose into one-way doors. None of the prior work decomposes the failure surface this way. This is the analytic contribution practitioners can use as a checklist.
3. A **trace-free, preventive architectural operationalization** — trust budget + staging area + irreversibility classifier — sitting inside the Plan-then-Execute skeleton (Del Rosario et al. 2025). Contrasts with SafetyDrift's empirical learned monitor by requiring no per-task training traces; trades empirical accuracy for operational simplicity.
4. An **empirical demonstration** that aligned 2026 frontier models (Sonnet 4) produce path-level failures across all four composition modes, despite refusing each step's stand-alone harmful variant — and that the architecture catches them as the framing predicts.

We do not claim a novel theorem. We do not claim a novel architecture. We claim the framing, the taxonomy, and the minimal trace-free operationalization for LLM agents in 2026.

## Strategic positioning

Goal: **thought leadership in the agent-safety space**. The thought-leadership lever in a crowded technical field is *naming and organizing*, not theorem novelty. Influential AI-safety papers (ReAct, Constitutional AI, Chain of Thought) often combined or named existing ideas; the framing made them citable. We aim for that.

Two-month execution timeline targets arXiv preprint plus companion blog post (LessWrong, LinkedIn) plus open-source repo as the deliverable bundle. Workshop submission deferred to whatever cycle aligns naturally; arXiv preprint is the primary public artifact.

## Scope

- **In scope:** Email-agent prototype, mock backend, 10 evaluation scenarios spanning four composition modes plus one defense-in-depth case, qualitative naive-vs-airlock comparison on harmful-trajectory rate. Companion blog essay and Github implementation.
- **Out of scope:** Real email integration; learned irreversibility classifiers; multi-agent coordination; head-to-head benchmark comparison against SafetyDrift's 357-trace dataset (deferred to future work); formal proof of path-irreversibility detection completeness (cited from prior work, not re-proven).

## Status

- [x] Failure catalog (10 cases under composition-mode taxonomy) — [failure-catalog.md](failure-catalog.md)
- [x] Thesis and framing locked (door composition / path-irreversibility, synthesis positioning) — this doc + [paper/draft.md](paper/draft.md)
- [x] Literature review with grounded citations — [literature-map.md](literature-map.md)
- [x] Formal model with light sketch and citation of prior formal work — [formal-model.md](formal-model.md)
- [x] Paper outline drafted — [paper/draft.md](paper/draft.md)
- [x] Architecture implemented; smoke tests pass on naive and airlock agents
- [ ] Scenario fixtures for the new composition-mode scenarios — needs new mock-email content
- [ ] Parameter retuning for path-level rather than per-action gating
- [ ] Evaluation across 10 scenarios with N≥10 replicates per scenario
- [ ] Empirical results section
- [ ] Companion blog post
- [ ] Github repo cleanup and documentation
- [ ] arXiv preprint submission

## Note on prior framings

The project began as a "CQRS-based trust architecture" defense against canonical agent-safety attacks (prompt injection, social engineering, blast radius). Smoke tests in 2026-04 confirmed contemporary models refuse those scenarios on their own, collapsing the harmful-action gap that framing depended on. We then briefly pursued a stronger theoretical framing ("we prove a structural theorem about path irreversibility") before a literature review found the theorem held by Arthur (1989), Krakovna (2018), and Garcia-Molina & Salem (1987), and the LLM-specific version held by SafetyDrift (2026). The current synthesis-and-framing positioning is the honest contribution that survives the literature.
