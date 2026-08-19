# Prior-Art Verification Notes (Phase 0)

*Verified 2026-08-18 (local session; arXiv reachable here — the remote planning session was egress-blocked and worked from search snippets only). Source PDFs downloaded to this directory (gitignored); abstracts verified against the arXiv abstract pages, the load-bearing differentiation claims verified against the full-text HTML (arxiv.org/html). **Caveat:** quotes below carry section references, not PDF page numbers — before the related-work section is finalized, re-anchor each quote to a page number from the committed PDF.*

**Bottom line: neither escalation trigger fired. Our path-level / cumulative-gating contribution (delta #1) is intact — and Parallax's own design strengthens it.**

---

## 1. McCann 2026 — "Mechanized Foundations of Structural Governance"

- **Cite key:** `mccann2026governance`
- **arXiv:** 2604.27289 (v1 2026-04-30; v3 2026-05-26)
- **Author:** Alan L. McCann

**What it does.** Five results in the theory of structural governance for cognitive-workflow systems; three mechanized in Coq 8.19 (Interaction Trees + parameterized coinduction), two paper proofs. ~12,000 lines, 36 modules, 454 theorems, zero admitted lemmas. The headline for our purposes is the **Necessity Theorem**.

**Proof/evidence type.** Machine-checked (Coq) for three results; **paper proof by explicit reduction to Rice's theorem** for the Necessity Theorem.

**The load-bearing claim (verbatim, abstract):**
> "The Necessity Theorem proves via explicit reduction to Rice's theorem that an architecturally opaque component (the reason primitive) is mathematically necessary for problems requiring semantic judgment (paper proof)."

**What they do NOT do.** McCann's result is a **computability/undecidability necessity** claim: it argues *why* an opaque semantic-judgment component must exist. It says nothing about **cross-call state, cumulative irreversibility, per-action-weight accumulation, or a path-level threshold**. It quantifies over the *existence and opacity* of the reason primitive, not over what an evaluator can *observe* about a running action sequence. Our Input-Availability Proposition is **orthogonal**: it holds in a decidable world and against an unbounded model (independent of computability assumptions), and it is about the evaluator's *input domain*, not the decidability of its judgment. → §1.5 entry: "we do not prove an undecidability or necessity result; our claim is input-availability and is complementary."

**Escalation check (handover §1.2):** McCann does **not** cover cross-call state or accumulation. No escalation. Differentiation stands as written in REWRITE_PLAN.md §2.

---

## 2. Fokou 2026 — "Parallax: Why AI Agents That Think Must Never Act"

- **Cite key:** `fokou2026parallax`
- **arXiv:** 2604.12986 (2026-04-14)
- **Author:** Joel Fokou
- **Artifact:** OpenParallax (open-source Go reference implementation)

**What it does.** Argues prompt-level guardrails are architecturally insufficient once agents can execute, and proposes Parallax: four principles — (1) **Cognitive-Executive Separation** (reasoner structurally cannot execute), (2) **Adversarial Validation with Graduated Determinism** (an independent multi-tier validator between reasoning and execution), (3) **Information Flow Control** (sensitivity labels propagate through the workflow), (4) **Reversible Execution** (pre-destructive state capture for rollback). Evaluated via "Assume-Compromise Evaluation" (bypass the reasoner, test the boundary under full compromise): 280 adversarial cases / 9 categories, blocks 98.9% (zero FP) default, 100% at max config.

**Proof/evidence type.** Empirical (adversarial test suite) + an architectural argument. No formal theorem.

**The load-bearing claims (verbatim, full text):**
> "Shield evaluates each action independently, with no carry-over of approval from previous actions." — §4.2 (Principle 2: Adversarial Validation with Graduated Determinism)

> "Conversational momentum in the agent's reasoning does not influence the validation layer, because the validation layer has no access to the agent's conversational state." — §6.3 (Adversarial Results)

> "Tier 2 is budget-limited (a configurable maximum number of calls per day, default 100) to prevent budget exhaustion attacks." — §4.2 (this is a **rate limit on validator LLM calls**, not a security/risk accumulation)

> "When the agent reads a file classified as containing credentials, the content receives a sensitivity label. This label propagates through every subsequent operation that touches the tagged content." — §4.3 (IFC labels **flow** but are **not summed** into a cumulative risk score)

**What they do NOT do.** Parallax validates **each action atomically and in isolation**. Graduated Determinism is *tiered severity of response*, not cumulative scoring. The only "budget" is a per-day LLM-call rate limit. IFC propagates labels but does not accumulate an irreversibility integral or a path-level threshold. Crucially, this per-action design is **intentional** (stated rationale: avoid an adversary "preparing" the system through benign-action sequences that lower cumulative guards).

**Why this strengthens our paper (not just survives it).** Parallax is exactly the *per-action external validator* our Proposition's **corollary (a)** ranges over. By its own explicit design, Parallax's validator has no access to accumulated/cross-action state — so it *inherits the accumulation blindness* our result identifies. Parallax owns the reasoner/executor **separation** dimension; our contribution sits **inside** that separation and adds the **path/cumulative** dimension it deliberately omits. → §1.5 entry: "we do not claim the reasoner/executor separation; our contribution sits inside it and adds the path dimension." → §2.6 positioning subsection writes itself from the two quotes above.

**Escalation check (handover §1.2):** OpenParallax has **no** budget-like cumulative primitive (the day-rate-limit is not one). No escalation. Delta #1 does not shrink; if anything the positioning sharpens.

---

## Actions still open from handover §1 (Phase 0)

- [x] Both PDFs downloaded to `docs/paper/prior-art/` (gitignored).
- [x] Characterizations in REWRITE_PLAN.md §2 verified against the papers (abstracts + the two flagged full-text sections).
- [x] This notes file with section-referenced quotes.
- [ ] Bib entries `mccann2026governance` + `fokou2026parallax` added to `references.bib` — **done in the same commit; verify they compile in the next `pdflatex+bibtex` run.**
- [ ] `docs/literature-map.md` positioning annotations — done in the same commit.
- [ ] **Re-anchor every quote above to a PDF page number** before finalizing §2.6 / related work.
- [ ] Workshop-CFP [UNVERIFIED] items — **deprioritized:** venue re-decided to TMLR-primary (Mihir can't travel; see PUBLICATION_PLAN.md). Only needed if the optional remote-workshop path is revived.
