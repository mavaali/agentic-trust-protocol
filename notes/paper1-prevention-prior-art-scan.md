# Paper 1 — Prevention-side prior-art freshness scan

**Compiled:** 2026-06-15
**Subject:** "Two-Way Doors, One-Way Trajectories" (Wagle), finalizing for arXiv (metadata prepared 2026-06-08, not yet posted).
**Trigger:** the Paper 2 compensation scan incidentally surfaced an apparent per-action-irreversibility-budget paper; this scan was run to stress-test Paper 1's *preventive* novelty (cumulative trust budget that gates before actions fire) before posting.
**Method:** deep-research harness — run `wf_a4202e54-d4a` (task `wretiat2m`), 5 angles, 15 sources, 68 claims, top 25 adversarially 3-vote verified; 18 confirmed, 7 killed. Output ledger at `.../tasks/wretiat2m.output`. Date range 2024–June 2026.
**Label key:** [DATA] = primary-sourced, harness-verified (not human-confirmed); [HYPOTHESIS] = inference w/ kill condition.

---

## 1. Verdict — **SAFE but DENTED**

[DATA] No published or preprint **paper** (2024–June 2026) independently proposes a **consumable, cumulative, path-level irreversibility/trust budget that GATES LLM-agent actions before they fire.** That specific *published* formulation — Paper 1's core preventive contribution — appears open. **Caveat (see §6):** in *deployed* code the picture is weaker — Databricks Omnigent (June 2026) ships an accumulate-then-gate policy layer with a non-fungible path-monotone risk *level*, so the bare accumulate-and-gate *mechanism* is not unprecedented in shipped systems even though no paper formalizes the irreversibility-budget version. The novelty is real but narrower than "mechanism is open" implies.

The "dent" is **thesis overlap, not mechanism overlap**, and it comes from a paper Paper 1 *already* treats as its closest prior art: **SafetyDrift**. So the situation is no worse than the lit-map already assumed — and the most alarming new suspect turned out to be a fetch artifact.

---

## 2. Correction to the previous (Paper 2) scan's incidental finding

[DATA] **arXiv:2603.03515 is NOT an irreversibility-budget paper.** It is Sahoo, *"The Controllability Trap: A Governance Framework for Military AI Agents"* (ICLR 2026 wksp, cs.CY), whose mechanism is a **Control Quality Score** (real-time human-control metric, three pillars: preventive/detective/corrective). The `ι:A→[0,1]` + `IC(t)=Σι(aⱼ)` + pause-for-reauthorization details reported in the compensation scan **do not exist in that paper** — they were bytes from arXiv:2510.14503 (RL "Learning to Undo") served by a corrupted `/pdf` mirror. Refuted 0–3 across four verification attempts via the abstract/HTML pages. **Treat the "Sahoo irreversibility budget" as non-existent prior art. Do not defensively over-cite it.**

---

## 3. The one that genuinely dents — SafetyDrift (already known)

[DATA] **SafetyDrift** — Dhodapkar & Pishori, *"Predicting When AI Agents Cross the Line Before They Actually Do,"* arXiv:2603.27148 (Mar 28 2026). Already mapped as Paper 1's most threatening prior art ([literature-map.md §G](../docs/literature-map.md), draft §6.5). The scan confirms why, in sharper terms:

- It **independently states Paper 1's core compositional thesis**, verbatim: *"individually safe actions compounding into violations"*; *"Per-step safety monitors … fundamentally cannot detect safety drift because [they lack] trajectory-level context."*
- It models an **absorbing Markov chain over state `s=(d,t,r)`** where `r ∈ {fully_reversible, partially, irreversible}` *"tracks whether the agent's cumulative actions can be undone."* The confidential-file → summary → email-externally example mirrors the two-way→one-way door spine.
- **BUT the mechanism is detection, not gating:** intervention fires when the finite-horizon absorption probability (via fundamental matrix `N=(I−Q)⁻¹`) exceeds a calibrated threshold `θ_c` — *not* when an allocated cost crosses a budget. Verbatim: *"Prior work has measured this problem; we predict it."* No consume/allocate/deplete/budget construct exists.

**How Paper 1 must distinguish (the thesis-overlap is real — acknowledge it, don't bury it):** position Paper 1 as **preventive gating via a consumable trust budget, operationalized trace-free inside a Plan-then-Execute (Airlock) agent**, vs. SafetyDrift's **reactive probabilistic early-warning detector**. The novel delta is (a) gate-vs-detect, (b) consumable-budget-vs-probability-threshold, (c) the four-mode composition taxonomy, (d) trace-free operationalization. A reviewer who knows SafetyDrift will expect this differentiation explicitly. [HYPOTHESIS — kill condition: a SafetyDrift v2 that adds a gating/enforcement layer on accumulated state would narrow the delta from (a)/(b) to just (c)/(d); v1 lists "blocking the action" only as a downstream deployment choice. Re-check before posting.]

---

## 4. Adjacent — cite to bound scope, no threat

[DATA, all four]
- **Atomix** (arXiv:2602.14849, Feb 2026). Three-way reversibility-classed tool-effect taxonomy (bufferable / reversible-external / irreversible) serving **transactional commit/rollback reliability**, not safety gating. Its "gate" is a commit-ordering device, not a harm classifier; *"no accumulation mechanism, budget, or trajectory-level thresholds appear anywhere."* Distinguish on the cumulative/path-level axis — it settles effects *after* execution; Paper 1 gates *before* and accumulates.
- **CaMeL** (arXiv:2503.18813, v2 Jun 2025) + **Operationalizing CaMeL** (arXiv:2505.22852). Per-tool-call capability/control-flow separation; the only irreversibility notion (Green/Yellow/Red tiers → Red requires approval) is *"action-centric and stateless rather than trajectory-aware,"* with no accumulation. The canonical prevention-by-design baseline; distinguish on the accumulation axis.
- **SafeGate** (arXiv:2604.05427, Apr 2026). A genuine **pre-execution** safety gate — but per-command deterministic authorize/defer/reject for **robot** control, with Z3-checked per-state invariants, no cumulative budget, no door framing. Closest "pre-execution gate" label; distinguish on domain (LLM tool-use vs robot control) *and* accumulation.

## 5. Gap-confirming — independent authors saying the gap is open (cite as positioning gifts)

[DATA]
- **GAP / Edictum** (Cartagena & Teixeira, arXiv:2602.16943, *"Mind the GAP: Text Safety Does Not Transfer to Tool-Call Safety"*). Its enforce mode blocks forbidden calls **per-call** and explicitly disclaims accumulation: *"Sequential composition attacks … fall outside the scope of our per-call scoring"*; *"Governance contracts evaluate each tool call in isolation."* **Concedes the exact composition gap Paper 1 fills.**
- **Turan** (arXiv:2606.08919, *"Oversight Has a Capacity,"* Jun 8 2026). §7.3 Future Work: *"A single action can be safe while the sequence is lethal (read secret → write public file → push); trajectory-level guarding [1,2] is the detection layer this oversight calibration would consume."* An independent author, **one week before Paper 1's target**, flags the composition thesis as an open downstream problem.
- **TRACES** (arXiv:2605.27690, May 2026). Trajectory-state risk monitor that produces *"dense prefix-level risk estimates"* but *"remains external to the system's scope"* — detect-but-don't-gate.

These three are the best cites for "the field has recognized this gap but not filled it." Use them; they de-risk the novelty claim rather than threaten it.

---

## 6. Deployed-harness prior art — Omnigent IS the counterexample [DATA — corrects the scan]

**The scan's "none found" is wrong; this repo's own Phase 0 review refutes it.** The deep-research corpus was paper-centric (it fetched the Omnigent blog but didn't connect it). Per [notes/omnigent-policy-review.md](omnigent-policy-review.md): **Databricks Omnigent (June 2026) ships an accumulate-then-gate policy layer** — *"an accumulate-a-non-fungible-path-score-then-gate primitive … ships as a documented builtin (`risk_score_policy`)"* — a non-fungible, path-monotone risk *level* that gates the pending action with `ALLOW`/`ASK`/`DENY` **before it fires**, plus fungible accumulating budgets (`cost_budget`, `tool_call_count`) and a `session_state` accumulator seam for custom path-level budgets. So a deployed harness **does** do preventive accumulate-and-gate. (The other vendor harnesses — AutoGen, LangGraph, Semantic Kernel — remain not-found, medium confidence.)

**What Omnigent does NOT ship as a builtin:** specifically an *accumulating non-fungible irreversibility-cost budget* (Σ per-action irreversibility cost). `risk_score` is an ordinal level, not a summed cost; the cost/count budgets are fungible. The seam to build the non-fungible version as a custom `FunctionPolicy` exists — and per the Phase 0 **do-not-claim list**, Paper 1 must NOT assert Omnigent *"can't express a path-level irreversibility budget"*; that is code-refuted.

**Implication for Paper 1 (timing).** Omnigent shipped ~the same week Paper 1 finalized (both June 2026) → **concurrent deployed work, not strictly prior art**; recency legitimately explains the missing cite. But two things follow: (1) **drop any "no deployed system does this" framing** — false, and the team knows it from Phase 0; (2) a one-line **concurrent-work acknowledgment is the honest, cheap move** (Databricks is a major vendor; reviewers will know Omnigent; the team has a deep review on file). The defensible delta vs Omnigent is the **conceptual frame (door composition), the four-mode taxonomy, trace-free operationalization, the empirical mode-decomposition, and the specific accumulating-irreversibility-budget formulation** — NOT the bare accumulate-and-gate mechanism, which Omnigent makes table stakes. This mirrors the governance plan's Paper 2 line ("accumulation is becoming table stakes; compensation is the frontier") — the same logic dents Paper 1's *mechanism* claim and pushes its novelty onto frame + taxonomy + empirics.

---

## 7. Classical anchors — still un-ported [DATA]

No third party was found porting Krakovna 2018 (stepwise reachability), Grinsztajn 2021, Turner 2020 (AUP), Eysenbach 2017, or the Arrow-Fisher/Henry/Arthur economics anchors *directly to LLM agents.* Paper 1's port remains the novel bridge. [HYPOTHESIS — absence finding, not exhaustive; kill condition: a 2025–26 paper explicitly porting AUP/stepwise-reachability to LLM tool-use.]

---

## 8. Recommended must-cite-and-distinguish set for Paper 1

- **Tier 1 (concede thesis, claim mechanism delta):** SafetyDrift (2603.27148) — already in the bib; sharpen the gate-vs-detect / budget-vs-threshold distinction in §6.5.
- **Tier 2 (adjacent, bound scope):** Atomix (2602.14849), CaMeL (2503.18813) + Operationalizing CaMeL (2505.22852), SafeGate (2604.05427).
- **Tier 3 (gap-confirming, positioning):** GAP/Edictum (2602.16943), Turan (2606.08919), TRACES (2605.27690).
- **Retain:** Krakovna 2018, Grinsztajn 2021, Turner 2020, Eysenbach 2017, Arrow-Fisher 1974, Henry 1974, Arthur 1989.

Tiers 2–3 are six papers (Feb–Jun 2026) **not yet in [literature-map.md](../docs/literature-map.md)** — add them before posting.

---

## 9. Open follow-ups (chase before arXiv)

1. **Re-run this exact scan immediately before submission.** Every Tier-1/3 suspect is a Feb–Jun 2026 preprint; this field moves weekly. The "irreversibility budget" / "trajectory-level safety budget" query is the one to repeat.
2. **Check for SafetyDrift v2** with a gating/enforcement layer — that is the single thing that would narrow Paper 1's delta most.
3. **Targeted harness-docs sweep** (Omnigent / LangGraph / AutoGen / Semantic Kernel) to upgrade §6 from "not found" to "confirmed absent."
4. **Stress-test the four-mode taxonomy's novelty separately** — this scan verified the budget/gating mechanism and the thesis, not the accumulation/premise/classification/iteration taxonomy against prior work.
5. **Verify the post-cutoff IDs firsthand** (2602.14849, 2604.05427, 2605.27690, 2606.08919, 2602.16943) before they enter the bib — same web-only caveat as the compensation scan, and this scan already caught one phantom (2603.03515).

---

## Bottom line

Paper 1 is in **better** shape than the previous turn's incidental finding implied: the scary budget-twin was a fetch artifact, and the genuine overlap (SafetyDrift) is the already-known one Paper 1 was built to differentiate from. The gating-budget mechanism is unclaimed; two independent June-2026 papers explicitly call the composition gap open. **Action before posting:** add the six new Feb–Jun 2026 cites, sharpen the SafetyDrift gate-vs-detect paragraph, and re-run the freshness query on submission day.
