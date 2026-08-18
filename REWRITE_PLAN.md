# Paper Rewrite Plan — Major Surgery

*Created 2026-08-18. Companion to [PUBLICATION_PLAN.md](PUBLICATION_PLAN.md). Target: "Who Verifies the Agents?" (NeurIPS 2026 workshop, due Aug 29) as the forcing function; TMLR full version as the second output of the same surgery.*

## 1. Why a rewrite rather than a patch

Four reasons, in decreasing order of severity:

1. **The prior-art problem is load-bearing, not cosmetic.** Both competing papers are now verified (see §2) and both predate our draft date of 2026-04-27: Parallax (2026-04-14) publishes the read/write separation idea under a louder name ("AI Agents That Think Must Never Act"), and McCann (2026-04-30, essentially concurrent) publishes a machine-checked *theorem* in the same conceptual territory. A paper whose title framing pattern-matches Parallax and whose "structural argument" pattern-matches McCann's theorem, while citing neither, reads exactly like "needs significant review and revision." One citation sentence doesn't fix this — the contribution list itself has to be re-scoped around what survives their existence.
2. **The workshop version requires a 22→9 page cut anyway.** That is rewrite-scale work regardless; doing it as a rewrite around a new spine costs little more than doing it as deletion.
3. **The draft has an identity problem.** It self-describes as a "framing/thought-leadership" paper (§1.5 of research-brief; §7.1 "conceptual scaffolding"). Reviewers and moderators are hostile to framing papers. The same content re-spined as a *verification* paper — "which agent failure modes are checkable at which layer, given what each layer can observe" — is a contribution-shaped claim, and happens to be the target workshop's exact topic.
4. **Tonal drift.** Late sections read bolted-on and unedited (the §7.2 "supply-chain / data spoilage" block, parts of §7.6, §7.9). This is the kind of surface signal that makes a moderator's "not publishable in a conventional journal" call easy.

**What a rewrite cannot fix (be honest about this):** the arXiv account restriction stays regardless; the evidence base stays one model (Sonnet 4), one mock backend, N=10 unless we run new evals. Optional evidence upgrade (decision D6): an N=5–10 replication on one additional model (e.g. Haiku-class for cost) on the 4 headline scenarios (A2, A4, A3, D1) would blunt the single-model objection for the TMLR version. Not feasible before Aug 29; the workshop version owns the limitation in one sentence instead.

## 2. Prior-art repositioning (the heart of the surgery)

Verified 2026-08-18 via web search (arXiv itself is egress-blocked from this environment — **pull both PDFs and verify quotes before final text**; summaries below are from abstracts/snippets, not full texts).

### McCann (arXiv:2604.27289) — "Mechanized Foundations of Structural Governance: Machine-Checked Proofs for Governed Intelligence" (Alan L. McCann, Mashin Inc., 2026-04-30)

Five results on structural governance for cognitive workflow systems; three mechanized in Coq (Interaction Trees, parameterized coinduction), two on paper. The **Necessity Theorem** proves, by explicit reduction to **Rice's theorem**, that an architecturally opaque "reason primitive" is mathematically necessary for problems requiring semantic judgment.

**Differentiation:** our structural claim (§3.2/§3.5/§7.3) is an **input-availability argument, not a computability argument**. McCann: certain judgments are *undecidable*, so a governed system must contain an opaque reasoning component. Us: the accumulation signal (running integral of per-action irreversibility, its weights, its threshold) is *not in the input domain* of any single forward pass — the claim survives even in a world where semantic judgment is decidable and the model is computationally unbounded. These are independent axes: McCann bounds what any component can *compute*; we identify what the per-call component can *see*. They compose rather than compete — McCann's governed system still needs something that observes cross-call state, which is precisely the layer we build and measure. The rewrite states this contrast in the abstract (one sentence), §1 (one paragraph), and related work (one subsection).

**Also:** McCann owns theorem-naming in this space ("Necessity Theorem," machine-checked). We must not wave at an unstated "Separation Theorem" — see D2.

### Parallax (arXiv:2604.12986) — "Parallax: Why AI Agents That Think Must Never Act" (Joel Fokou, 2026-04-14)

Argues prompt-level guardrails are architecturally insufficient; proposes four principles — **Cognitive-Executive Separation** (the reasoner cannot act; the executor cannot think), Adversarial Validation with Graduated Determinism, Information Flow Control, Reversible Execution — plus OpenParallax, a process-isolated reference implementation.

**Differentiation:** concede the shared ground explicitly — read-path/write-path separation is Parallax's Cognitive-Executive Separation, and Del Rosario's Plan-then-Execute before that; the *separation itself is not our contribution and never was* (§1.5 already disclaims architecture novelty; now it must name Parallax). Our delta, stated positively:

1. **The path-level primitive.** Parallax validates and can roll back *individual* actions; our trust budget gates the *cumulative path* — the running irreversibility integral. Accumulation harm (A1/A2/D1: every action individually valid, the sequence is the harm) passes any per-action validator, including Parallax's tiers, by construction.
2. **The taxonomy as a verification instrument.** Composition modes organized by *what information detection requires* — which is what tells you which layer (model, prompt, validator, budget) can possibly catch what.
3. **The empirical decomposition.** N=10 × 10 scenarios of which primitive catches which mode — including two honest negatives (A3 architectural failure; Structural Gaming refuted). Parallax, per its abstract, argues from principles + reference implementation; we bring the measurement.
4. **Variance asymmetry** as the quantitative signature of what architecture adds over alignment.

### The repositioned one-liner (candidate, for Mihir's pen)

> Prior work establishes that agent reasoning must be architecturally separated from execution (Parallax; Plan-then-Execute) and that governed systems provably require opaque semantic judgment (McCann). We ask the question between those results: *of the failures that survive a well-aligned reasoner behind a per-action validator, which are verifiable at all — and from where?* We show a class (accumulation) whose detection signal exists in no single forward pass's inputs, give the minimal trace-free primitive that observes it, and measure which primitive catches which failure class.

## 3. The new spine

Old spine: "here is a framing (door composition) and a taxonomy; we operationalize and evaluate it." New spine, contribution-shaped and workshop-aligned:

1. **Claim (stated formally, see D2):** accumulation-mode failures are undetectable by any per-call evaluator — aligned model *or* external per-action validator — because the required signal (running irreversibility integral + threshold) is absent from per-call inputs. Input-availability, not undecidability.
2. **Instrument:** the composition-mode taxonomy, organized by information-required-to-detect. (Door composition survives as the intuition/vocabulary, one paragraph, not the headline.)
3. **Mechanism:** trust budget + staging + classifier as the minimal trace-free layer that has the missing signal. Architecture explicitly positioned *inside* Parallax/Plan-then-Execute-style separation, adding the path dimension.
4. **Evidence:** the N=10 decomposition — five wins, one tie, one marginal, one instructive failure (A3), variance asymmetry as the headline quantitative signal, cost-of-safety inversion as the surprise.
5. **Boundary (kept prominent — it's the credibility anchor):** A3 defines the claim's edge: architecture sees path *shape*, never content *veracity*. B1's failure→fix→win narrative shows the taxonomy has engineering payoff.

## 4. Section-by-section surgery

Page budgets for **W** = workshop version (9 pp max excl. refs, NeurIPS template) and **J** = TMLR version (~16–18 pp). Current draft: 22 pp.

| Current section | Action | W | J |
|---|---|---|---|
| Abstract (250+ words, scenario IDs A1/B2/… throughout) | **Rewrite from scratch.** ≤150 words, zero internal scenario IDs, differentiation sentence vs McCann+Parallax included | ¼ pp | ¼ pp |
| §1.1–1.3 (motivating shift / reframe / framing) | **Merge into one §1** around the new spine; keep the three concrete failure vignettes (they're good), cut the "that fight is settled" swagger | ¾ pp | 1½ pp |
| §1.4 Contributions (6 items) | **Rewrite to 4 items** = the spine (claim, taxonomy, mechanism+measurement, boundary). Variance asymmetry moves inside item 3; Structural Gaming refutation demotes to §6 | ⅓ pp | ½ pp |
| §1.5 "does not claim" | **Keep — it's the paper's best defensive asset.** Add McCann + Parallax entries; add "not an undecidability result" | ⅓ pp | ½ pp |
| §2 Related work (5 subsections) | **Compress to ~½ pp for W** (McCann/Parallax subsection + SafetyDrift/CaMeL/Plan-then-Execute + one-sentence sweeps of econ/RL/systems). J keeps full structure + new §2.6 "Concurrent 2026 work" | ½ pp | 1½ pp |
| §3 Framing (3.1–3.5) | §3.1–3.3 compress to intuition paragraph + formal statement (D2). **§3.5 (input-availability asymmetry) is now the paper's centerpiece — expand, contrast with Rice's-theorem-style arguments explicitly** | 1 pp | 2 pp |
| §4 Architecture (4.1–4.7) | Keep fig 5 + budget + classifier table. §4.6 fold into taxonomy table. §4.7 (Sagas scope note) → one sentence in W, keep in J | 1 pp | 2 pp |
| §5 Implementation | Two sentences + repo pointer in W; keep as short section in J | ⅛ pp | ½ pp |
| §6 Evaluation (6.1–6.10) | The evidence — protect it. W: §6.3 headline table + fig 2 (variance) + A3 (§6.6, incl. dot-plot) + B1 narrative compressed + cost inversion (2 sentences) + Structural Gaming (2 sentences). J: keep all, tighten prose ~30% | 3½ pp | 6 pp |
| §7 Discussion (7.1–7.10) | **Heaviest cuts.** Delete §7.2's supply-chain/"data spoilage" block entirely (tonal misfit; reads generated — this alone may have cost us at moderation). §7.6 rewrite minus marketing cadence. §7.9 phase diagram → 3-sentence future work. §7.3 merges into §3.5. W keeps: limitations + 3-bullet future work | ¾ pp | 2 pp |
| §8 Conclusion | Rewrite to new spine, ½ length | ¼ pp | ½ pp |
| Appendices | J/repo only; W points at repo (anonymized — see §6 below) | 0 | as needed |

Also: `draft.md`'s References section is still a placeholder ("[To be assembled in BibTeX]") while `draft.tex` has `references.bib` — the two sources have drifted. See §7 (mechanics).

## 5. Title (decision D3)

"Two-Way Doors, One-Way Trajectories" is blog-flavored and, post-Parallax, metaphor-titles in this niche read as derivative. Candidates (Mihir picks; keep the doors line as the §1 hook regardless):

- *What the Forward Pass Cannot See: Verifying Path-Level Safety in LLM Agents*
- *Verification Beyond the Call: Composition-Mode Failures and the Trust Budget*
- Keep current title, add differentiating subtitle (weakest option)

## 6. Anonymization (workshop is double-blind — currently we'd be desk-rejected)

The draft carries the author name, personal email, "Microsoft" affiliation, and de-anonymizing links throughout (github.com/mavaali/…, waglesworld.com). For W: strip title-page block; replace repo links with an anonymized mirror (Anonymous GitHub / 4open.science **[UNVERIFIED — confirm the workshop's accepted anonymization mechanisms]**); scrub `\thanks` footnote; check figure PDFs' metadata for author strings. The public repo and any Zenodo DOI must **not** be linked from the W submission (Zenodo deposit is fine to exist — dual-anonymity norms treat public preprints as tolerated — but do not cite it in the submission **[UNVERIFIED for this workshop — check its CFP dual-submission/preprint clause]**).

## 7. Mechanics: one source of truth

- `docs/paper/draft.tex` becomes canonical for **J**. `docs/paper/draft.md` is frozen as an archive header pointing at the tex (it has already drifted; stop maintaining both).
- **W** lives at `docs/paper/workshop/workshop.tex` on the NeurIPS 2026 template **[template to be fetched — neurips.cc styles; verify the workshop mandates it]**, sharing `references.bib` and `figures/`.
- Figures: regenerate fig 1/2/4 from eval JSONs unchanged; fig 5 (architecture) needs one added visual element locating the budget *across* calls (the path dimension) to support the Parallax differentiation. No data changes.

## 8. Zenodo timing — revised recommendation

PUBLICATION_PLAN.md said "deposit v1 now." **Revising:** both proximate papers are verified as *already published in April 2026* — the priority race against them is settled (they're earlier); the timestamp now protects our *delta* (taxonomy, budget-as-path-integral, empirical decomposition) against *future* work. A permanent DOI record of a version that fails to cite the two closest papers is a liability, and a few days changes nothing. **Deposit the post-surgery J-length draft (v1 on Zenodo) alongside workshop submission, ~Aug 27–28.** The two metadata blockers (second author, license) still need resolving by then.

## 9. Work plan to Aug 29 (11 days)

Ownership per the standing split: Claude produces draft text; **Mihir takes the pen** — final voice, all claims, and every decision below. Theorem/formal content: Claude may draft the formal statement *only after* D2 is decided; Mihir owns its final form.

| Days | Work | Owner |
|---|---|---|
| 1–2 (by Aug 20) | Decisions D1–D5 below. Pull McCann + Parallax PDFs, verify §2 summaries against full texts, extract quotable claim statements | Mihir (papers + decisions) |
| 2–4 | New spine draft: abstract, §1, §1.5 additions, related-work §2.6, §3 restructure with formal statement per D2 | Claude drafts → Mihir pens |
| 4–6 | §6 compression for W; §7 cuts (incl. deleting the supply-chain block); conclusion | Claude drafts → Mihir pens |
| 6–7 | Assemble workshop.tex on NeurIPS template; fit to 9 pp; anonymization pass | Claude |
| 7–9 (by Aug 27) | Mihir full-pen pass on W; Claude applies edits; build + proof | Both |
| 9–10 (Aug 27–28) | Zenodo deposit of J-length revision (needs D4/D5 resolved); OpenReview submission dry run | Mihir uploads |
| 11 (Aug 29 AoE) | Submit W. J/TMLR work continues on its own clock after notification | Mihir |

Slack: if the schedule slips past ~Aug 26 with W unfinished, fall back to the Evaluation of Interactive Agents workshop only if its requirements are lighter (unknown — [UNVERIFIED]), else skip the cycle and go straight to TMLR; the surgery is required for TMLR anyway, so no work is wasted.

## 10. Decisions needed from Mihir

- **D1 — Venue:** Who Verifies the Agents? (recommended; exact topical fit) vs Evaluation of Interactive Agents. One only.
- **D2 — Formal posture:** state the input-availability claim as a formally-stated **Proposition** with its (short) argument, explicitly contrasted with Rice's-theorem/undecidability results (recommended — it's the spine, and vagueness here is what the McCann proximity punishes), vs keep it prose-only. Under no circumstances an unstated "Separation Theorem" — per `notes/irreversibility-bounds-autonomy.md`, no such statement exists in writing, and McCann occupies the named-theorem ground with machine-checked proofs.
- **D3 — Title** (candidates in §5).
- **D4 — Second author** named on the deposited/submitted version (AUTHORS.md commitment) — affects Zenodo metadata and W's author block post-review.
- **D5 — License** for the Zenodo text deposit (CC-BY 4.0 recommended).
- **D6 — Second-model replication** for J (post-Aug 29; ~N=5–10 on A2/A3/A4/D1): yes/no/defer.
- **D7 — Affiliation** on the deposited version ("Microsoft" + personal-capacity footnote, as drafted, vs "Independent").
