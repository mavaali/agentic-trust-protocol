# Irreversibility Bounds Agent Autonomy, Not Verification Quality

*Working note — ATP. Drafted Jul 2026; revised Jul 22 after a full read of the source essay and a cross-check against repo state. Revision log at the bottom.*

**Source under discussion:** Taber, *Who Verifies the Agents?* (Jul 2026), <https://commentary.dev/blog/who-verifies-the-agents>.

**Repo anchors:** the two-way/one-way door composition thesis ([README.md](../README.md) §Thesis), the A3 premise-drift failure ([NEXT_STEPS.md](../NEXT_STEPS.md), "A3 deep dive"), Structural Gaming ([docs/paper/draft.md](../docs/paper/draft.md) §6.6), and the compensation program ([docs/paper2_outline.md](../docs/paper2_outline.md)).

## 1. The claim this note attacks

The prevailing argument for autonomous agent verification (Taber, above) runs: verification was always a stack of procedures — lint, compile, test, deploy, end-to-end, exploratory — and the human was merely invoking them. Hand the invocation to the agent, keep the human at the top of the loop for standard-setting, and quality is preserved. The human step is expected to fade as the codebase accumulates its own rules.

The essay is honest about its evidence base ("all I have is my own experience so far") — the generalization is flagged, not silent. But it misdiagnoses the *shape* of its own caveat: it treats the risk as insufficient long-run data, curable by time and better models, when the structural risks (§3, §5 below) are exactly the ones neither time nor model quality repairs.

The argument is stronger than its critics allow and weaker than it appears, but not for the reason usually given.

## 2. Why the standard objection is insufficient

[HYPOTHESIS] The common objection — "the agent authored the tests, so the loop only proves self-consistency" — is correct but not decisive. Every layer except compilation is a derived artifact of the same generator: tests, coverage rules, E2E scripts, and the brief for the exploratory pass. The loop converges on internal coherence rather than correctness.

This is real, and it is not fixed by better models: a stronger generator produces a *more* coherent misreading, not a less likely one. The essay's closing bet — "the whole thing rides on how good the models are, and they keep getting better" — is aimed at the wrong failure mode; model improvement strengthens per-step verification while making drifted artifacts *harder* to catch.

But the objection is only fatal if intent verification is expensive. Where a single owner can confirm intent in five minutes against a running deployment, the self-consistency gap is cheaply closed — *provided the owner is in the usage loop at high frequency.* The argument therefore survives under two conditions it treats as incidental: (a) failures are cheap (see §5), and (b) the intent-holder re-anchors the spec by continuous use. Drift accumulates in proportion to the interval between intent-holder contacts, not in proportion to hops. Taber's own setting — sole owner, dogfooding nightly output every morning — maximizes contact frequency, which is why his loop genuinely works *there*.

## 3. Intent drift through composed two-way doors

[HYPOTHESIS] The sharper failure mode is drift, and it does not require multiple humans or teams.

Each agent decision in a long-running loop is individually reversible, so no single step trips a review gate. But reversibility is not composable. N reversible choices, each conditioned on its predecessor, produce a state exitable only by discarding the entire run. The door remains open; the room behind it no longer exists. The two-way/one-way taxonomy assumes decisions are separable enough to be un-made one at a time — an assumption that fails at agent throughput. (This is the intent-layer generalization of the repo's action-layer thesis: a series of two-way doors composes into a one-way door.)

Intent degrades along the same path. It is re-read at every hop, each read conditioned on the last, so the specification drifts by interpolation rather than by detectable error. Nothing fails. The resulting artifact satisfies intent-as-most-recently-understood, and detecting this requires diffing against intent-as-written — precisely the review being eliminated.

[DATA] A4 is the action-layer miniature of this failure: the naive agent hallucinated `contact@baolabs.com` in 10/10 replicates and sent 30 confidential messages to it ([NEXT_STEPS.md](../NEXT_STEPS.md)). Any test the same generator wrote for that flow would have asserted delivery *to the hallucinated address* — Taber's entire pyramid would have been green. A3 (wrong codename propagating across action types, 0/10 checkpoints) is the drift case the Airlock itself does not see; this section is A3's theory.

**Consequence for end-of-loop human checks:** using the running feature tests whether it does something coherent, not whether it does the thing specified N hops ago. The check is at the wrong layer — *unless* the checker is the intent-holder at high contact frequency (§2), in which case their use is itself the diff against intent-as-written.

## 4. Why agent-authored intent checkpoints are theater

[HYPOTHESIS] The natural repair — have the agent restate its working intent at each hop — fails, because the same drifting process authors the restatement.

[COUNTER — from the full text of the essay] Taber's actual mechanism is better than the summary version of his argument: the human reviews the **test plan** — what the agent intends to verify — *before* execution. That is an intent-layer artifact diffed early, before drift compounds; structurally it is closer to the pinned-spec repair below than to the end-of-loop check §3 attacks. The correct critique targets its **fading** ("the system starts holding its own standard"): the accumulated standard is authored by the same drifting process, so codified drift becomes the precedent the next change is verified against. The fading is only safe if the standard is pinned to something outside the generator's write path.

The candidate independent fix is an adversarial challenger (jugalbandi-style dialogue). This helps less than expected, and the reason is worth stating precisely:

> **Adversarial dialogue supplies independence of *reasoning*. Drift detection requires independence of *reference*.**

The Challenger reads the artifact the Resolver produced at hop N, with no privileged access to intent at hop 0. Two navigators check each other's arithmetic while both work from the same erroneous star fix; the arithmetic is sound.

Worse, coherence is the attack surface. A well-drifted artifact is internally consistent by construction — every hop was a locally reasonable read of its predecessor — which is the artifact an assumption-surfacing challenger finds *least* to say about.

[DATA — needs anchoring] The jugalbandi ablation supports assumption surfacing (25.4 vs 9.4 vs 14.2 avg) and says nothing about drift detection. Assumptions surfaced at hop N are assumptions about the current frame. *(These numbers are quoted from the jugalbandi working doc and are not yet anchored to a reproducible run; anchor or strike before anything citable.)*

**Structural repair:** pin the original specification as immutable and define the Challenger's brief as a *diff against it*, not a critique of current state. This converts a judgment task into a comparison task, where correlated priors between model instances hurt least.

[COUNTER] The repair does not yield an oracle. Divergence from a written spec is frequently *correct* — legitimate envelope-filling of an underdetermined specification. The diff flags drift and desirable adaptation identically; separating them requires the intent-holder. Jugalbandi makes drift visible and cheap to inspect. It cannot adjudicate it. Instrument, not oracle.

## 5. The bounding constraint is irreversibility, not verification quality

[HYPOTHESIS] This is the load-bearing claim of the note.

A fully event-sourced, append-only, replayable system has no one-way doors. Every bad state is a rebuild away, so the try/fail/fix/redeploy loop genuinely converges and the autonomy argument holds. (Terminology guard: "replay-limited" here means event-sourced and rebuildable — *not* the repo's "CQRS-style" read/write-path separation, which is an orthogonal architectural property the Airlock already has.)

Real codebases are not replay-limited. They mutate in place: destructive schema migrations, captured payments, sent mail, mutated third-party state, poisoned downstream caches. At each such transition the loop's core mechanic is unavailable. A refund cannot be retried. Every layer of Taber's stack — lint, compile, test, deploy clean, deploy as upgrade, E2E, exploratory, "fixing and redeploying until it all passes" — assumes a failed attempt costs one more loop iteration. The essay contains no irreversible effect anywhere; its loop works partly because its gate count is near zero, a condition it does not identify as load-bearing.

**Therefore the governing metric is accumulated irreversibility, not confidence in the verification stack.** Required non-agent involvement scales with the irreversibility the path accrues, not with trust in the agent.

[COUNTER — self-inflicted, and the fix is already in this repo] Stated as "gate count over discrete irreversible transitions," the metric contradicts §3. §3's point is that irreversibility can be *emergent*: a path of individually reversible steps whose composition is irreversible has a gate count of zero and is exactly the case that matters. The general form is a **threshold on the path integral of irreversibility** — the trust budget. A discrete gate is the special case where one step carries the whole integral (migration, payment); the budget is what catches the C2 case, where five individually-scored deletes compose into the harm and no single transition would trip a per-step gate. Restated: *gates where the integral concentrates, budget where it diffuses.*

This reframes where the investment goes, in two ways:

1. **Autonomy is bought by converting one-way doors into two-way doors** — expand/contract migrations, idempotency keys, transactional outbox, shadow writes, sandboxed external effects, and *compensating transactions*. This is precisely the Paper 2 program ([docs/paper2_outline.md](../docs/paper2_outline.md)): compensation converts a one-way door into a decaying two-way door. The source argument optimizes the verification axis; the door-conversion axis is where autonomy actually comes from.
2. **The scarce human look should be allocated by irreversibility, not by size.** Taber's rule — one last manual pass "before the biggest changes ship" — uses feature size as the risk proxy. Size is a bad proxy: a one-line destructive migration is small; a major feature can be entirely reversible. His own scarcity argument (human review no longer scales) is correct and implies the better allocation rule he doesn't draw.

[COUNTER] "Human" is the default implementation at a gate, not the requirement. What the gate requires is an authority the agent cannot grant itself. A policy engine holding capability tokens satisfies the constraint with no person in the loop. The live question is how many gates can be delegated to a non-human authority genuinely outside the agent's write path — which is the ATP claim.

## 6. Separation is falsifiable, not confirmable

[HYPOTHESIS] The separation property splits asymmetrically, and any eventual formal statement should say so explicitly.

**Syntactic separation is testable.** Can the agent's credentials mutate the policy, its rules, or its evaluation configuration? This is a reachability question over the permission graph, falsifiable by direct attempt — a red team whose sole objective is obtaining the gate. Failure disproves separation cleanly. (This is Sibling B from [docs/paper2_outline.md](../docs/paper2_outline.md) — the agent gaming its own irreversibility classifier — stated as a security objective.)

**Semantic separation is not testable.** The policy evaluates artifacts the agent authored: diffs, test plans, migration metadata, PR text. The agent shapes the decision without touching the decider. No write-path violation, identical outcome. The absence of this channel cannot be established by inspection, because the channel *is* the intended input. A fence can be shown to have a hole by walking through it; it cannot be shown to have none by failing to find one.

Consequence: separation is a security property, not a theorem. Evidence accumulates as failed attacks, never as proof.

[COUNTER — and this likely improves the paper] Semantic influence may not constitute a separation failure at all. The gate is *supposed* to read agent output. What must be agent-independent is the **criteria**, not the inputs. If the criteria can be stated as functions of properties the agent cannot fake without performing the underlying work — migration reversibility, idempotency of an external call, blast radius, rollback path existence — then influence over inputs is harmless.

This narrows the verification target from **"no influence"** to **"no cheap forgery."** Tractable, testable, and a materially weaker claim than any "Separation Theorem" — and probably the true one.

[DATA] The paper's Structural Gaming result (draft §6.6: N=10 across 9 scenarios, no observed mode-shifting under budget pressure) is weak-but-real early evidence on the cheap-forgery frontier: under mild pressure, this agent did not find forgeries. It is not evidence that forgeries are expensive — only that they weren't sought.

## 7. Open items

- **Pin the "Separation Theorem" statement.** No document in this repo states such a theorem; the nearest artifacts are the CQRS read/write separation (architectural, not a theorem) and the structural-input-availability argument (paper §3.6). §6 currently narrows a claim that exists only in conversation. Either write the statement down (likely as a security property per §6, not a theorem) or retitle the target.
- Formalize *cheap forgery*: cost ratio between faking a gate-relevant property and satisfying it. Where is the ratio unfavourable enough to be load-bearing? Sibling B is the natural empirical vehicle.
- Enumerate gate-relevant properties that resist cheap forgery. Reversibility and idempotency are candidates; test coverage and spec conformance are not.
- Anchor the jugalbandi ablation numbers (§4) to a reproducible run, or strike them.
- Empirical: measure gate count *and* budget-threshold crossings across a sample of real repositories. If irreversible transitions are rare and path-accrual stays under plausible budgets in practice, the bounding claim weakens considerably. **This is the kill condition for §5, and it is not obviously hard to hit** — mature systems with disciplined migration practice may already approximate replay-limited behaviour.

---

## Revision log (Jul 22)

- Added source link; read the full essay (prior draft worked from a summary). Corrections that came out of the full read: the essay flags its own novelty caveat (§1); its test-plan review is an early intent anchor, so the §4 critique now targets its fading rather than its layer; added the size-vs-irreversibility allocation point (§5).
- Fixed the internal §3/§5 tension: "gate count" over discrete transitions undercounts emergent (compositional) irreversibility; generalized to a path-integral threshold, i.e. the trust budget, with discrete gates as the concentrated special case.
- Cross-linked repo anchors: README thesis (§3), A3/A4 findings (§3), Structural Gaming §6.6 (§6), Paper 2 compensation program (§5, §6).
- Added the intent-holder contact-frequency condition (§2, §3).
- Renamed "CQRS-limited" to "replay-limited" to avoid colliding with the repo's "CQRS-style" read/write separation (§5).
- Flagged the jugalbandi ablation numbers as unanchored (§4) and the missing Separation Theorem statement (§7).
