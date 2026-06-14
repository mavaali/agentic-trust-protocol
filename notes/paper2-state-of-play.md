# Paper 2 — state of play

**Compiled:** 2026-06-14 (read-only synthesis)
**Sources:** [docs/paper2_outline.md](../docs/paper2_outline.md) (151 lines), [notes/omnigent-governance-plan.md](omnigent-governance-plan.md), [docs/literature-map.md](../docs/literature-map.md), `docs/paper/references.bib`, `STATUS.md`, `NEXT_STEPS.md`.
**Not read:** `docs/paper/draft.tex` (v1) except where the outline/governance plan cross-reference it.

---

## 1. Current thesis (verbatim)

**Working title** (`paper2_outline.md:3`):
> "Compensating Transactions for LLM Agents: A Saga-Pattern Approach to Path-Level Safety after the Gate"

**Headline** (`:5`):
> "the current paper argues that path-level safety requires architectural primitives that observe what no forward pass can; this paper argues that a *complete* path-level safety architecture also requires compensation primitives that operate after irreversible actions have fired. Together they form the persistence-layer story."

**Five sub-claims** ("What this paper claims," `:31–35`), verbatim:
1. "A complete path-level safety architecture for LLM agents requires both preventive and compensating primitives. The supply-chain metaphor … makes this concrete: prevention is shelf-life monitoring; compensation is recall/return."
2. "Compensation in the LLM-agent setting is *itself* subject to door composition: the time-decay of compensation effectiveness, and the compensability of compensating actions, must be modeled."
3. "A taxonomy of compensability (compensable / partially compensable / non-compensable) plus a compensation-cost integral give a tractable architectural primitive that practitioners can deploy."
4. "Empirically, an LLM agent equipped with compensation primitives recovers from budget-overrun scenarios at higher rates than one without, *and* the cost of compensation can be quantified."
5. "**The cooperative-safety extension.** … an agent that sees its *compensation cost* in advance can reason about whether a planned action is worth its forward + recovery cost together. We sketch this as future work but do not test it in this paper."

The load-bearing conceptual move (`:61`): extend the v1 path-irreversibility model so `I*(π, W₀)` becomes `I*(π, W₀) − C(σ, Wₙ)`, where σ is the compensation trajectory and C is a (time-decaying) effectiveness function.

---

## 2. Outline structure (≤2 sentences each)

Provisional ~9000 words, §1–9 + 4 appendices (`:37–120`).

- **§1 Introduction** — recap preventive surface, name the post-action/recall gap, Saga antecedent. *Skeleton (bullets).*
- **§2 Background & Related Work** — v1 as predecessor; Sagas, nested-transactions, microservices; "Compensating transactions in agent literature: largely absent." *Skeleton; this is where the Omnigent foil + matrix land (§4 below).*
- **§3 Compensation as a Door-Composition Phenomenon** — the conceptual core: compensators consume budget, decay with time, compose non-commutatively. Has the one real equation (`:61`). *Semi-developed: prose-ish bullets + formal sketch, no full prose.*
- **§4 A Taxonomy of Compensability** — three categories (compensable / partial / non-compensable) with worked examples (email↔retraction, wire-transfer clawback window, file deletion). *Detailed skeleton — the most fleshed-out outline section.*
- **§5 Architecture: Sagas for Agents** — `compensator` registry, `compensation log`, reverse-LIFO `compensate` op, integration with the preventive stack. Figure mirrors v1 Fig 5 + compensation channel. *Skeleton.*
- **§6 Implementation** — mock compensators; budget split into recoverable/non-recoverable tracks; three new scenarios R1/R2/R3 (late-discovered overrun, cascading retraction, time-decay). *Skeleton, but scenarios are concretely specified.*
- **§7 Empirical Evaluation** — R1–R3 × N≥10 × 3 conditions (Naive / Preventive-only / Preventive+Compensation); metrics: total irreversibility cost, recovery rate, cost ratio, time-to-recovery. *Skeleton; design specified, no data.*
- **§8 Discussion** — complementarity, compensation-cost integral as a design tool, limitations (effectiveness is semantic/fuzzy). *Skeleton.*
- **§9 Conclusion** — two-halves supply-chain lifecycle. *Skeleton.*
- **Appendices A–D** — full taxonomy (30–50 entries), cost-integral derivation, mock impl, per-scenario traces. *Placeholder.*

---

## 3. What's already written (prose vs skeleton)

Of 151 lines: **~40–45 lines of genuine connected prose**, the rest headings/bullets/blank.

**Actual prose (publishable-adjacent):**
- "Conceptual frame: completing the supply-chain lifecycle" (`:9–17`) — ~4 paragraphs, the strongest written passage.
- "Positioning relative to the current paper" (`:21–27`) — ~3 paragraphs.
- "What this paper claims" (`:29–35`) — 5 full-sentence claims.
- "Anticipated reviewer pushback" (`:131–137`) — 5 Q&A pairs, fully written.
- "Timeline" (`:139–141`) and "sibling papers" (`:143–151`) — prose + bullets.

**Skeleton only (bullets/TBD):** the entire §1–9 body (`:37–120`) and all appendices. **No section of the paper proper exists as drafted prose** — the prose lives in the framing/positioning/meta sections, not the paper body.

---

## 4. Scaffolding that feeds in (from the governance plan)

**Prevent / accumulate / compensate matrix** (verbatim, → Paper 2 §2/positioning):

| System | Prevent (perimeter) | Accumulate (trajectory) | Compensate (post-action) |
|---|---|---|---|
| CaMeL | ✓ information-flow | — | — |
| Omnigent policy layer | ✓ per-action gate | ✓ `risk_score` / budgets | — |
| Airlock (this work) | ✓ staging gate | ✓ trust budget | Paper 2: saga / compensation |

> "Omnigent closing the accumulate column is *evidence for* Paper 2's thesis, not against it — accumulation is becoming table stakes; compensation is the frontier."

**§2 Omnigent placement** (verbatim framing): "a production agent framework (Databricks Omnigent, Apache-2.0, June 2026) whose policy layer already accumulates non-fungible path state … yet still has no compensation primitive once an action has fired. This **sharpens** Paper 2's central gap: the missing half is not accumulation … but recovery."

**Defensible claim #1 (paper-bearing for Paper 2):** "**No compensation / saga primitive.** Omnigent's policy layer is a synchronous per-action `ALLOW`/`ASK`/`DENY` gate … There is no construct to stage reversible steps, commit atomically at a boundary, or compensate/roll back after an action has fired. *This is the gap Paper 2 fills* — and it is unrefuted."

**Do-NOT-claim list constrains Paper 2 framing too** — five forbidden claims, notably: don't say Omnigent "can only accumulate fungible scalars," "evaluates only the pending action," has state that "can't persist across a path," "no seam for a path-level measure," or "can't express a path-level irreversibility budget." Each is code-refuted. **Implication for Paper 2:** position Omnigent as *accumulate-but-can't-compensate*, never as *can't-accumulate*.

**Literature already mapped** ([literature-map.md:36–44](../docs/literature-map.md)): Garcia-Molina & Salem 1987 (Sagas, the systems origin), Lynch & Merritt 1986, Weikum & Vossen 2001, Richardson 2018. In `references.bib`: **`garcia1987sagas` and `lynch1988` exist** (shared with v1); **Weikum 2001 and Richardson 2018 are not yet in the bib** — need adding.

---

## 5. Open decisions (what the outline punts on)

1. **Empirical scope — real or structural-only?** The outline commits to experiments (R1/R2/R3 × N≥10 × 3 conditions, ~90 runs, `:124–129`) but none are built or run. Open: does compensation produce a clean headline signal comparable to v1's variance result, or is the recovery-rate metric softer? (See Risk B.)
2. **The saga primitive in LLM-agent terms.** §5 names a `compensator` registry + `compensation log` + reverse-LIFO `compensate`, but the semantics of "effectiveness ∈ [0,1]" are unspecified and the outline itself flags this as fuzzy (`:108`). The C(σ, Wₙ) effectiveness function is asserted, not defined.
3. **Scope vs v2's §3.6.** The outline predates the v2 cross-session work. Paper 1 v2 (PR #3) now owns the **cross-session boundary** (scope-and-reset of the accumulator). Paper 2's axis must stay **post-action compensation, within-session** — but the outline's claim 5 (cooperative-safety / seeing compensation cost in advance) flirts with the visibility axis v2 also touches. Needs an explicit boundary statement.
4. **Lit-framing freshness.** The claim "compensating transactions in agent literature is largely absent" (`:50`) was written months ago. **Worth a fresh check** before it becomes a load-bearing novelty claim — the agent-safety literature moves fast (Omnigent itself shipped June 2026).
5. **Cross-ref drift.** The outline cites v1 sections by stale numbers (`§4.7`, `§7.6`, `§7.8`, `§7.9`, "Figure 5") that won't match the current `draft.tex`. Mechanical but must be reconciled.

---

## 6. Natural starting points (3–5)

1. **Re-run the literature check on "compensation in agent frameworks."** *Why first:* the entire novelty claim rests on absence; cheapest thing to falsify, highest blast radius if wrong. *Unblocks:* a defensible §2 and the framing for the whole paper.
2. **Define the compensation-effectiveness function C(σ, Wₙ) precisely.** *Why first:* it is the one piece of real theory and everything (taxonomy, cost integral, metrics) depends on it. *Unblocks:* §3 prose, §4 metadata fields, §7 metrics.
3. **Draft §3 (Compensation as Door-Composition) as full prose.** *Why first:* it is the conceptual core and the part least dependent on experiments; can be written now. *Unblocks:* the paper's identity as a structural contribution even if experiments slip.
4. **Build R1 (late-discovered overrun) end-to-end as a vertical slice.** *Why first:* smallest real experiment; proves the compensator/registry/log machinery works before committing to R2/R3. *Unblocks:* the empirical claim 4 and a go/no-go on whether the signal is clean.
5. **Write the explicit Paper-1-v2 / Paper-2 boundary paragraph.** *Why first:* cheap, and prevents both papers drifting into each other's territory (see Risk A). *Unblocks:* clean scoping for §1 and §2.

---

## 7. Risks worth flagging early

**A. The v2 §3.6 / Paper 2 boundary.** v1 v2 (PR #3) now carries the **cross-session / scope-and-reset axis**; Paper 2 is the **prevent → compensate (post-action) axis**. These are orthogonal and must stay so. *Live tension:* the governance plan **on main** still parks the cross-session/spawn-tree residual (Defensible claim #3) as Paper-2-relevant nuance, while the v2 branch's governance addendum retargets it to v1 v2. Until PR #3 merges, two documents disagree about where cross-session lives. Paper 2 should explicitly disclaim cross-session and keep claim #1 (no-compensation) as its only Omnigent hook.

**B. Empirical headline risk.** v1's strength was a *clean, surprising* signal (variance reduction, not mean). Paper 2's proposed metrics (recovery rate, cost ratio, time-to-recovery) are plausibly *softer* and partly definitional — recovery rate depends on the effectiveness function the authors define, so a critic can call the result circular ("you measured what you assumed"). The outline half-concedes this (`:108`, pushback #3 at `:135`). *Decide early:* is Paper 2 a structural-argument paper with illustrative experiments, or does it need a headline result? If the former, lead with §3 theory; if the latter, R1 must produce something non-obvious.

**C. Novelty resting on absence.** Both the "agent literature largely absent" claim and the "Sagas are 30 years old, what's new" pushback (`:133`) put the paper's contribution entirely on *application + the time-decay-as-door-composition treatment*. If a competing compensation-for-agents paper appears, the structural framing is the only defensible moat — another reason to land §3 early.
