# Paper 2 — Outline

*Working title: "Compensating Transactions for LLM Agents: A Saga-Pattern Approach to Path-Level Safety after the Gate"*

This is the natural follow-up to the current preventive-side paper. The current paper argues that path-level safety requires architectural primitives that observe what no forward pass can; this paper argues that a *complete* path-level safety architecture also requires compensation primitives that operate after irreversible actions have fired. Together they form the persistence-layer story.

---

## Conceptual frame: completing the supply-chain lifecycle

The current paper [Wagle 2026] introduces a **logistics framing** for path-level agent safety: agentic execution as just-in-time supply chain, where the staging area is an inspection buffer, the trust budget is a shelf-life monitor on cumulative state, and the irreversibility classifier ensures only "fresh" inputs flow to the write-path. Under this metaphor, the current paper's architecture handles **prevention of data spoilage** — gating actions before unsafe state propagates.

The metaphor exposes what is missing: **logistical recovery.** Real supply chains have recall and return mechanisms for goods that have already shipped and turned out to be defective. LLM agent architectures have no analogue. Once an action fires — and the budget gate later proves to have under-counted the cost, or a downstream consequence reveals the action as a mistake — the current architecture is silent.

This paper completes the supply-chain lifecycle by adding the recall/return primitive. The Saga pattern (Garcia-Molina & Salem 1987) is the formal antecedent: every forward action paired with a *compensating action* whose role is semantic, not state-restoring. *"You cannot un-send an email; you can mail an apology."* The compensation literature is mature for distributed databases and has been ported to microservices (Richardson 2018). It has *not* been seriously developed for LLM agents.

This second paper closes that gap.

---

## Positioning relative to the current paper

The current paper's architecture is **preventive**: trust budget + staging area + irreversibility classifier gate actions before they fire. This addresses the structural-input-availability gap on the *forward* path. It does not address what happens once an action *has* fired and the cumulative budget is later found to have been crossed — by underestimation, parallelism, or downstream consequence.

The current paper labels this scope explicitly (§4.7, §7.8) and forecasts the present paper as the natural completion: *"a complete persistence-layer architecture for LLM agents would also include compensating-transaction primitives."* The supply-chain frame in §7.2 of the current paper makes the gap concrete — recall/return is what's missing — and this paper fills it.

The CaMeL parallel from §7.6 is worth noting: CaMeL secures the information-flow *perimeter*; the Airlock governs the path-level *trajectory*; this paper's compensation layer governs *post-action recovery*. The three primitives are non-overlapping and combinable in a complete defense stack.

## What this paper claims

1. A complete path-level safety architecture for LLM agents requires both preventive and compensating primitives. The supply-chain metaphor introduced in [Wagle 2026] makes this concrete: prevention is shelf-life monitoring; compensation is recall/return.
2. Compensation in the LLM-agent setting is *itself* subject to door composition: the time-decay of compensation effectiveness, and the compensability of compensating actions, must be modeled. This is the natural extension of the door-composition framing — compensating actions are themselves doors that close over time.
3. A taxonomy of compensability (compensable / partially compensable / non-compensable) plus a compensation-cost integral give a tractable architectural primitive that practitioners can deploy.
4. Empirically, an LLM agent equipped with compensation primitives recovers from budget-overrun scenarios at higher rates than one without, *and* the cost of compensation can be quantified.
5. **The cooperative-safety extension.** The current paper's §7.9 phase diagram (Visibility × Enforcement) hypothesizes "cooperative agent-environment safety" — an agent that sees its budget and self-limits. The compensation primitive opens a third axis: an agent that sees its *compensation cost* in advance can reason about whether a planned action is worth its forward + recovery cost together. We sketch this as future work but do not test it in this paper.

## Outline (provisional, ~9000 words)

### 1. Introduction
- The preventive surface (recap of current paper, brief). Lead with the supply-chain framing: prevention as shelf-life monitoring at the staging area.
- The post-action surface — actions that fire despite preventive gates. The recall/return gap.
- The Saga antecedent: 30 years of compositional-safety practice in distributed systems, never applied to LLM agents.
- This paper's claim: compensation is the missing half.

### 2. Background and Related Work
- The current paper [Wagle 2026 — preprint] as the immediate predecessor. The supply-chain frame, the four-mode taxonomy, the variance-asymmetry signal, and the explicit out-of-scope flag for compensation (§4.7, §7.8 of [Wagle 2026]).
- Garcia-Molina & Salem 1987 (Sagas) — the foundational compositional-reversibility result.
- Lynch & Merritt 1988 (TCS journal version; original tech report 1986); Weikum & Vossen 2001 — formal nested-transactions theory.
- Richardson 2018 — modern microservices Saga practice.
- Compensating transactions in agent literature: largely absent. (We position this as the gap we're filling.)
- Parallel: SafetyDrift's reversibility dimension (Dhodapkar & Pishori 2026) — they detect drift but do not address recovery.
- Adjacent: the rollback / undo literature in HCI and version-controlled systems (cite a representative sample).
- Adjacent: A3-style premise-WRONG-AS-FACT failures from [Wagle 2026] — the architecture's known failure mode is a natural compensation target. When the wrong codename propagates across three actions, retraction-and-correction is the recovery primitive.

### 3. Compensation as a Door-Composition Phenomenon
This is the conceptual core. Compensation is itself subject to path-irreversibility composition:
- A compensating action consumes budget like any other action.
- Compensation effectiveness decays with time — a retraction sent at $t = 30s$ is far more effective than one at $t = 30m$. The compensation surface is itself a one-way door that opens narrower over time.
- Composed compensations are not commutative: if you must compensate $a_1$ and $a_2$ where $a_2$ conditioned on $a_1$, the order matters and the joint cost is super-additive.

Light formal sketch: extend the path-irreversibility model from the current paper to include compensation. $I^*(\pi, W_0)$ becomes $I^*(\pi, W_0) - C(\sigma, W_n)$ where $\sigma$ is the compensation trajectory and $C$ is a (decaying-with-time) compensation effectiveness function.

### 4. A Taxonomy of Compensability
Three primary categories, each with subcases:

- **Compensable** — semantic compensator exists and is reasonably effective.
  - Email: `send_email` ↔ `send_retraction_email` (effective if recipient hasn't acted on original).
  - Calendar: `schedule_meeting` ↔ `send_cancellation` (effective if attendees haven't planned travel).
  - Document share: `share_document` ↔ `revoke_share + notify_recipient`.
- **Partially compensable** — compensator exists but its effectiveness window is narrow or its cost is comparable to the original action.
  - Wire transfer: clawback within bank's reversal window; non-compensable after.
  - Public post: `delete_post` ↔ original viewers may have screenshotted.
  - Multi-recipient email: compensator effectiveness scales inversely with recipient count.
- **Non-compensable** — no semantic compensator exists.
  - File deletion (without backup).
  - Information leak that cannot be retracted (e.g., to a competitor).
  - Action triggering downstream automated processes that cannot be unwound.

Each entry in the taxonomy has structured metadata: time-decay constant, compensation cost (in irreversibility units), and dependency on world state (e.g., "has any recipient replied?").

### 5. Architecture: Sagas for Agents
- A `compensator` registry mapping each forward action type to one or more compensating actions plus their cost. (The recall mechanism in supply-chain terms.)
- A `compensation log` that records executed forward actions with their irreversibility cost and whether they have been compensated. (The shipment manifest.)
- A `compensate` operation invocable when budget is found to have been crossed: walks the log in reverse-LIFO order, executing compensators where applicable, accumulating compensation cost into an extended budget.
- Integration with the preventive architecture: compensation is the recovery primitive when the preventive gate fails or the irreversibility classifier underestimates. The two layers form a complete supply-chain lifecycle: prevention upstream of the write-path, recovery downstream of it.

Diagram: Plan-then-Execute architecture extended with a Compensation channel, parallel to the Read path and Write path. The figure should mirror Figure 5 of [Wagle 2026] with the Compensation layer added below the email backend.

### 6. Implementation
- Email backend extended with mock compensators (retraction email, calendar cancellation, etc.).
- The trust budget extended to include "post-action recoverable" and "post-action non-recoverable" tracks.
- Three new scenarios designed to trigger compensation:
  - **R1: Late-discovered overrun.** Agent processes 8 emails; on review (simulated by an external check after the fact), 2 of those sends turn out to have been wrong-recipient. Compensator: send retraction-and-correction.
  - **R2: Cascading retraction.** Agent sends emails A, B, C where B and C reference content from A. A is found wrong. Compensation requires retracting all three in reverse order. Tests joint cost.
  - **R3: Time-decay degradation.** Same as R1 but compensation is delayed (simulated by adding a "time elapsed" parameter). Tests effectiveness decay.

### 7. Empirical Evaluation
- For each of R1, R2, R3 across $N \geq 10$ replicates, compare:
  - Naive ReAct (no compensation): forward harm only, no recovery.
  - Preventive-only architecture (current paper): preventive gate triggers but no recovery from already-fired actions.
  - Preventive + Compensation architecture (this paper): both gating and compensation.
- Metrics: total irreversibility cost (forward + compensation), recovery rate (fraction of harmful actions semantically recovered), compensation-cost-to-original-action-cost ratio, time-to-recovery.
- Analysis: where is compensation worth its cost, and where does the time-decay function dominate?

### 8. Discussion
- Compensation is not a substitute for prevention; the two are complementary.
- The compensation-cost integral is a deployable design tool: it tells you when to spend budget on prevention vs. when to leave it for compensation.
- Limitations: compensation is *semantic* — our model treats "effectiveness" as a real number on $[0,1]$ but the actual social/operational meaning of effectiveness is messy.
- The taxonomy will need extension as new agent-tool surfaces emerge (e.g., physical-world actuators have very different compensability profiles than communication actions).

### 9. Conclusion
- The supply-chain lifecycle for LLM agents has two halves: shelf-life monitoring upstream of the write-path (prevention) and recall/return downstream of it (compensation).
- The current paper [Wagle 2026] addresses prevention; this paper addresses compensation.
- Together they form a deployable architectural template. The complete defense stack also includes orthogonal primitives: runtime monitors (SafetyDrift), capability defenses (CaMeL — perimeter), and the trajectory-level Airlock primitives. None of these substitute for any of the others.

### Appendices
- A: Compensation taxonomy in full (likely 30-50 entries spanning common agent action types).
- B: Compensation-cost integral derivation.
- C: Mock-backend compensation implementation details.
- D: Per-scenario compensation walkthrough with traces.

---

## Empirical scope (smaller than current paper)

- 3 new scenarios (R1, R2, R3), $N \geq 10$ replicates.
- 3 conditions: Naive, Preventive-only, Preventive+Compensation.
- Total runs: 90, ~$15-25 in Sonnet API.
- Single-author session can probably build the compensators in a week, run the eval in ~1 hour.

## Anticipated reviewer pushback

1. *"Sagas are 30 years old; what's new?"* — same response as current paper: the math is old; the application to LLM agents is new, and the time-decay-as-door-composition treatment is the conceptual contribution.
2. *"How is this different from runtime monitors with auto-rollback?"* — runtime monitors detect; compensation acts. We argue the pairing is necessary, not redundant.
3. *"Compensation effectiveness is subjective; your numbers are made up."* — partly true. We honest-up about this in Section 8 and treat the compensation-cost integral as a *design tool* rather than a ground-truth measurement.
4. *"Why not just use database-style transactions if you want rollback?"* — because the agent's actions affect the world (recipients' attention, social capital) which is not transactional. Saga's whole point is precisely this: semantic compensation, not state restoration.
5. *"Isn't the supply-chain metaphor overextended?"* — the metaphor is load-bearing in the conceptual frame but not in the math. Reviewers who object to the metaphor can read the paper as a Saga-pattern application without losing technical content. The supply-chain frame is a way of telling the story, not a hidden assumption.

## Timeline

If the current paper lands in arXiv in ~6 weeks, this follow-up could realistically land another ~8-10 weeks after that. So total timeline from project start to v2 preprint: ~4-5 months.

## Possible alternative framings / sibling papers

If the compensation work proves too large for one paper, natural splits:

- **Sibling A: "The full phase diagram"** — Visibility × Enforcement × Feedback-Timing, 8-condition factorial. Shorter empirical paper, lower theoretical contribution, but completes the empirical map of the current paper's preventive architecture.
- **Sibling B: "Adversarial agents in budget-constrained environments"** — extends Structural Gaming finding into a security paper. What happens when the agent is incentivized to game its own irreversibility classifier? Threat model + defenses. Different audience (security venues).
- **Sibling C: "Path-level safety benchmark"** — generalizes the scenario design into a public benchmark suite. Compares against ToolEmu, AgentDojo, AgentHarm. Methodological contribution rather than theoretical.

The compensation paper is the most natural single follow-up. Siblings A, B, C are workshop-track or longer-tail.
