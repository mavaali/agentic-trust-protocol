# Handover: Paper Rewrite Execution (local Claude Code session)

*Written 2026-08-18 by the remote session that produced [PUBLICATION_PLAN.md](PUBLICATION_PLAN.md) and [REWRITE_PLAN.md](REWRITE_PLAN.md). This document is self-contained: a fresh session with no prior context can execute from it. Read those two files before starting — this doc tells you what to do; they tell you why.*

---

> **STATUS UPDATE 2026-08-18 — read before executing.** Two things changed after this doc was first written:
> 1. **Venue re-decided: TMLR-primary, workshop dropped as the driver (D1 resolved).** Mihir cannot travel to Sydney (reception commitment); *Who Verifies the Agents?* is non-archival / no-DOI / probably-doesn't-clear-arXiv, so it is not worth an anonymization scramble against Aug 29. **There is no Aug-29 deadline anymore.** Run Phases 0–2 at a sane pace; the output is the J-length paper = the Zenodo deposit + the TMLR submission. **Phase 3 (workshop version) is now OPTIONAL** — do it only if a same-cycle venue allows *remote* presentation and Mihir wants the CV line. The deadline table in §8 is superseded (kept for history). See PUBLICATION_PLAN.md → "Recommended sequencing" for the current plan.
> 2. **Phase 0 is DONE (2026-08-18).** Both prior-art papers verified full-text; neither escalation trigger fired (McCann is orthogonal Rice's-theorem work; Parallax is explicitly per-action — it *inherits* our accumulation blindness, strengthening the paper). Notes: `docs/paper/prior-art/notes.md`; bib entries added; `literature-map.md` §J written; paper still builds (22pp, 0 errors). Remaining Phase-0 nit: re-anchor the prior-art quotes to PDF page numbers before finalizing §2.6. **Start execution at Phase 1.**

## 0. Session setup

### Model for this session

Run the session on **Claude Fable 5** (`claude-fable-5`): `claude --model claude-fable-5`, or `/model` inside the session. Rationale: the work is judgment-heavy scholarly surgery — restating a formal claim so it survives adversarial review next to a Coq-mechanized theorem, compressing 22 pages to 9 without losing the honest-negative results, and writing differentiation language that concedes exactly enough. That is the profile where the most capable model earns its cost. If Fable 5 is not available on this account, use **Claude Opus 5** (`claude-opus-5`) — do not go below Opus-tier for the drafting phases. Keep effort at the Claude Code default (`xhigh`); use `max` via `/model` settings for Phase 2 (the Proposition and abstract) if output quality seems off. Mechanical subtasks (BibTeX formatting, figure regeneration, LaTeX debugging) can be delegated to subagents on `claude-sonnet-5` or `claude-haiku-4-5` — never the prose.

**Verify model availability before Phase 1.** The IDs above (`claude-fable-5`, `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5`) are the intended tiers, not hard requirements — provisioning varies by account. If a named model isn't available, substitute the nearest equivalent from the same tier (any Opus-tier is acceptable for the drafting phases; do not drop below Opus-tier for prose). Don't stall the kickoff on an exact ID.

Separate question, often confused: the **models used *inside* the paper's experiments** are fixed by Phase 6 below (`claude-sonnet-4-20250514` baseline, unchanged; additions only per decision D6). Do not "upgrade" the eval model as part of the rewrite — comparability with the published N=10 data would be destroyed.

### Git

```bash
git fetch origin claude/arxiv-rejection-publication-plan-ivbo6w
git checkout -b paper-rewrite origin/claude/arxiv-rejection-publication-plan-ivbo6w
```

Work on `paper-rewrite`. The parent branch has an open PR (#5, the planning docs); if it merges to main first, rebase `paper-rewrite` onto main. Commit per phase with plain descriptive messages. Never push to `main`.

### Build toolchain

The paper needs pdflatex + bibtex (TeX Live; `texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended` suffice — verified 2026-08-18, builds 22 pp with 0 errors, 0 undefined citations). Verify before touching anything:

```bash
cd docs/paper && pdflatex -interaction=nonstopmode draft.tex && bibtex draft \
  && pdflatex -interaction=nonstopmode draft.tex && pdflatex -interaction=nonstopmode draft.tex
```

### Hard rules (from Mihir, standing)

1. **Mihir takes the pen.** This session produces *draft* text; Mihir revises and owns final voice and all claims. Do not treat any drafted section as final. Present each major unit (abstract, §1, Proposition, etc.) for his review as it's produced — this is a local interactive session; use that.
2. **No changes to eval data, result JSONs, scenario YAMLs, or library code** (`src/`, `eval/`) in Phases 0–5. Phase 6 (post-deadline) may touch harness *configuration* only, per its scope note.
3. **No theorem overclaim.** The formal statement is a Proposition with a near-definitional argument (see Phase 2). Never call it a theorem; never name it "Separation Theorem."
4. Numbers in the paper come from `eval/results/*.json` — never retype from memory; if a number is edited, trace it to the JSON.

### Decisions gate — confirm with Mihir at session start

Ask Mihir to confirm (recommendations from the remote session in parentheses; full reasoning in REWRITE_PLAN.md §10 and the conversation of 2026-08-18):

- **D1** venue — **RESOLVED 2026-08-18: TMLR-primary, workshop optional/remote-only** (Mihir can't travel; deadline dropped). No confirmation needed; see the status banner above.
- **D2** formal posture (recommended: named Proposition + corollaries)
- **D3** title (recommended: "What the Forward Pass Cannot See: Verifying Path-Level Safety in LLM Agents"; can slide to Aug 26)
- **D4** second author — remind him to contact the colleague **this week**; blocks Zenodo (Aug 27)
- **D5** license (recommended: CC-BY 4.0)
- **D7** affiliation (recommended: "Independent" unless Microsoft publication approval already exists)

If Mihir is unavailable at session start, proceed under the recommended defaults for D1–D3 and mark every affected artifact `[PENDING Dn]` — but do not deposit or submit anything without explicit go-ahead.

---

## 1. Phase 0 — Prior-art verification (do this FIRST; the remote session could not)

The remote session verified these papers only via search snippets — arxiv.org was egress-blocked there. **This machine can fetch them. Nothing in Phase 2 may be finalized until this is done.**

1. Download and read both papers in full:
   - arXiv:2604.27289 — McCann, "Mechanized Foundations of Structural Governance: Machine-Checked Proofs for Governed Intelligence" (Alan L. McCann, Mashin Inc., 2026-04-30)
   - arXiv:2604.12986 — Fokou, "Parallax: Why AI Agents That Think Must Never Act" (Joel Fokou, 2026-04-14)
   - Save PDFs to `docs/paper/prior-art/` (gitignore them if large; keep notes in git).
2. Verify the characterizations in REWRITE_PLAN.md §2 against the full texts, specifically:
   - McCann: confirm the Necessity Theorem is a Rice's-theorem reduction; confirm what exactly it quantifies over; note anything McCann says about *cross-call state* or accumulation (if he covers it, the differentiation must be rewritten — escalate to Mihir).
   - Parallax: confirm whether its validator is strictly per-action or has any path/cumulative component (its "Graduated Determinism" tiers and Reversible Execution sections are the places to check); confirm whether OpenParallax has any budget-like primitive. If it does anything cumulative, our delta #1 shrinks — escalate to Mihir before drafting.
3. Write `docs/paper/prior-art/notes.md`: for each paper — claim, proof/evidence type, exact quotable sentences (with page numbers) for the related-work section, and a one-paragraph "what they do NOT do" that our differentiation stands on.
4. Add both to `docs/paper/references.bib` (keys: `mccann2026governance`, `fokou2026parallax`) and to `docs/literature-map.md` with positioning annotations.
5. While online, also resolve the plan's remaining [UNVERIFIED] items: the chosen workshop's CFP page (notification date, dual-submission/preprint policy, anonymization mechanism, remote presentation policy, required template) — update PUBLICATION_PLAN.md in place, removing the [UNVERIFIED] tags you resolve. Download the NeurIPS 2026 LaTeX style files.

**Definition of done:** notes.md exists with page-referenced quotes; bib entries compile; PUBLICATION_PLAN.md venue section has no unresolved [UNVERIFIED] tags for the chosen venue.

## 2. Phase 1 — New spine drafting (REWRITE_PLAN.md §2–§3 govern content)

Target files: work in `docs/paper/draft.tex` (canonical). `docs/paper/draft.md` is frozen — add a header line pointing to the tex and stop maintaining it.

Draft, in order, presenting each to Mihir before the next:

1. **The Proposition** (assuming D2 = yes). A formally stated **Input-Availability Proposition** (or "Observability Proposition" — Mihir picks the name): for the standard per-call agent loop, no evaluator whose inputs are (prompt, local context, single proposed action) can be nontrivially sensitive to the running irreversibility integral, its per-action weights, or the threshold — because those are not in its input domain. Two corollaries: (a) this holds for *any* per-action evaluator, external validators included (→ Parallax's tiers inherit the blindness); (b) it is independent of model capability and of computability assumptions (→ orthogonal to McCann's Rice's-theorem result; survives a decidable world and an unbounded model). **Two traps to draft around, explicitly:** the triviality objection (the payload is the corollaries + the taxonomy partition, say so in the prose) and the context-window objection (scope the hypothesis precisely: history-in-context still lacks the scoring function and threshold anchor; the "Prompted-Budget" cell of draft §7.9 must remain visibly *outside* the Proposition's hypothesis, flagged as untested future work, not contradicted).
2. **Abstract** — ≤150 words, zero scenario IDs, one differentiation sentence covering both prior works, built around the repositioned one-liner in REWRITE_PLAN.md §2.
3. **§1** — merge current §1.1–1.3; keep the three concrete vignettes; contributions list cut to 4 (claim / taxonomy / mechanism+measurement / boundary).
4. **§1.5 additions** — McCann entry ("we do not prove an undecidability or necessity result; our claim is input-availability and is complementary to…"), Parallax entry ("we do not claim the reasoner/executor separation; our contribution sits inside it and adds the path dimension").
5. **§2.6 "Concurrent 2026 work"** — the McCann/Parallax positioning subsection, using Phase 0's quotes.
6. **§3 restructure** — §3.1–3.3 compressed to intuition + the Proposition; §3.5 expanded as the centerpiece; fold current §7.3 into it.

**Definition of done:** draft.tex builds; Mihir has seen and reacted to items 1–2 at minimum.

## 3. Phase 2 — Cuts (REWRITE_PLAN.md §4 table governs; apply to draft.tex)

Non-negotiable deletions: the §7.2 supply-chain/"data spoilage" block (from "The Airlock primitives directly address 'Data Spoilage'…" through "…propagate unchecked across irreversible doors."); §7.9 compressed to ≤3 sentences of future work; §7.6 rewritten without the marketing cadence ("Both are essential components of a complete defense stack" and kin). §6 evidence sections are protected — tighten prose, never drop the A3 failure, the B1 narrative, the Structural Gaming refutation, or the variance-asymmetry section. Result should land ~16–18 pp: this *is* the TMLR/J version and the Zenodo deposit text.

## 4. Phase 3 — Workshop version

1. Create `docs/paper/workshop/workshop.tex` on the NeurIPS 2026 template (fetched in Phase 0), sharing `../references.bib` and `../figures/`. Fit to the venue's limit (WVA: 4–9 pp excluding references/appendices) using the W column of REWRITE_PLAN.md §4.
2. **Anonymization checklist** (double-blind; any miss is a desk-reject):
   - [ ] No author name, no `\thanks` footnote, no email, no "Microsoft"
   - [ ] No `github.com/mavaali/...` links — replace with anonymized mirror (Anonymous GitHub / 4open.science, per whatever the CFP permits — resolved in Phase 0)
   - [ ] No `waglesworld.com`, no link to the Zenodo record, no "our earlier draft" phrasing
   - [ ] `grep -ri "wagle\|mihir\|mavaali\|microsoft\|waglesworld" workshop/` returns nothing
   - [ ] Check figure PDFs for embedded author metadata (`pdfinfo`, `exiftool`); regenerate via `figures/generate_figures.py` if dirty
   - [ ] AUTHORS.md/acknowledgments content absent from the submission
3. Figure work: regenerate figs from eval JSONs unchanged; fig 5 gets one added element showing the budget spanning calls (the path dimension) — edit `generate_figures.py` (this is figure code, not library code; allowed).

## 5. Phase 4 — QA, deposit prep, submission prep

1. Both texes build clean: 0 errors, 0 undefined citations/references, 0 overfull hboxes worth caring about; page counts within limits.
2. Adversarial read of the workshop PDF: check every number against `eval/results/*.json`; check the Proposition against the two traps; check no de-anonymizing string survived.
3. Update `zenodo-metadata.md`: new title (D3), new abstract, resolve the two open-decision blocks (D4, D5), affiliation (D7). The deposit file is the post-surgery J-length PDF, **not** the old draft (timing rationale: PUBLICATION_PLAN.md, revised section).
4. **Gates that require Mihir's explicit go, in his own words, at the moment of action:** the Zenodo upload (~Aug 27–28) and the OpenReview submission (Aug 29 AoE). Prepare both fully; press neither button autonomously.

## 6. Phase 5 (post-Aug 29, only if D6 = yes) — Cross-model replication for the TMLR version

Scope: scenarios `A2_fanout`, `A4` (see naming note below), `A3_compounding`, `D1_auto_responder_loop`; both agents; N=10; **three** models:

**Baseline data location (read before you look for per-scenario files).** There are *no* `eval_n10_A2.json` / `_A3` / `_D1` standalone files. The published N=10 baseline for these lives inside `eval/results/eval_n10_full_v2.json` under the `scenarios` array, keyed by full scenario ID (`A2_fanout`, `A3_compounding`, `D1_auto_responder_loop`, etc.). `A4` is the exception — it *does* have a standalone `eval/results/eval_n10_A4.json`. Extract each scenario's baseline object from `full_v2.json` (or the standalone file for A4) as your comparison anchor; do not re-run the Sonnet-4 baseline.

| Role | Model ID | Note |
|---|---|---|
| Baseline (unchanged) | `claude-sonnet-4-20250514` | The published N=10 data — **API-RETIRED (404 as of 2026-08-18)**, so it is frozen by necessity: use the archived JSONs as the anchor, do not attempt to re-run or spot-verify it live |
| Cheaper/weaker | `claude-haiku-4-5` | 200K context — fine for these scenarios |
| Stronger | `claude-opus-5` | The "does the blindness survive capability" data point |

Predictions to test (write them down *before* running, they go in the paper): accumulation blindness and the A3 failure persist on the stronger model; variance asymmetry persists everywhere; premise-MISSING catches may improve model-side on `claude-opus-5`.

**Baseline model is API-retired.** `claude-sonnet-4-20250514` returns 404 `not_found_error` on the account (verified 2026-08-18; the key is live — Haiku 4.5 and Sonnet 4.5 both 200). Consequences: (1) the Sonnet-4 baseline is the archived `eval/results/*.json` and nothing else — any code path that tries to hit it live will 404, so do not "verify" a baseline cell against the API; (2) the Zenodo deposit **must** bundle `eval/results/*.json` + the scenario YAMLs, since that archive is now the only surviving record of the anchor data; (3) Phase 5 replication is strictly additive on still-live models (Haiku 4.5 confirmed; use a current Opus/Sonnet-4.5-tier model for the "survives capability" arm and record the exact resolved ID in the results JSON).

**Harness migration warning — check before running.** The harness was written for Sonnet 4, and the API surface changed for newer models. Audit `src/` + `eval/` for these and fix *minimally* (config-level; this is the one sanctioned touch of harness code, post-deadline):

- `temperature`/`top_p`/`top_k`: **removed on `claude-opus-5`** (400 error). Fine on Sonnet 4 and Haiku 4.5.
- Assistant-message prefill: **400 on `claude-opus-5`** (fine on Sonnet 4 / Haiku 4.5). Grep for messages ending in an assistant turn.
- `thinking: {type:"enabled", budget_tokens:N}`: **400 on `claude-opus-5`** (it's adaptive-or-omit there); Haiku 4.5 still uses `budget_tokens` if thinking is wanted. Simplest uniform choice: run all models with thinking omitted **except** note that `claude-opus-5` then runs adaptive by default — if the baseline ran without thinking, either accept the asymmetry and disclose it in the paper's methods, or ask Mihir. Do not silently change what "one LLM call" means across models; `llm_step_count` comparability is a published metric.
- Model ID is *already* a parameter — `src/shared/llm.py:15` defines `model: str = "claude-sonnet-4-20250514"` as the client default (not a hardcoded constant). The remaining work is only to expose it: add a `--model` flag to the harness CLI and thread it into `LLMClient`, keeping `claude-sonnet-4-20250514` the default. Don't go hunting for a hardcoded constant to replace — there isn't one.

Cost is small (order of 1–2K API calls; likely single-digit dollars on Haiku, tens on Opus 5 at $5/$25 per MTok). Results go to new JSONs named with the **full scenario ID** to match the baseline keys: `eval_n10_<full_scenario_id>_<model>.json` (e.g. `eval_n10_A2_fanout_claude-opus-5.json`) — never overwrite the originals or the shared `eval_n10_full_v2.json`.

---

## 7. Escalation triggers — stop and ask Mihir

- Phase 0 finds either prior paper already covers cumulative/path-level gating (kills or reshapes delta #1).
- The Proposition can't be stated without either overclaiming or collapsing into triviality after honest effort.
- The workshop CFP has a requirement the plan didn't anticipate (page format, mandatory artifact submission, in-person-only).
- Anything requiring changes to `src/`, `eval/`, or result data before the deadline.
- Word from the colleague (D4) changes the author list mid-phase.

## 8. Deadline summary

| Date (2026) | Event |
|---|---|
| Aug 20 | D1–D2 confirmed; Phase 0 done |
| Aug 24 | Phases 1–2 drafted, Mihir's pen pass underway |
| Aug 26 | D3–D5, D7 resolved; workshop.tex assembled + anonymized |
| Aug 27–28 | Zenodo deposit (Mihir presses the button) |
| Aug 29 AoE | Workshop submission (Mihir presses the button) |
| Sept+ | TMLR submission from the J version; Phase 5 if D6 = yes |

---

## Kickoff prompt (paste into the local session)

> Read HANDOVER.md at the repo root and execute it. Start with the session-setup section — confirm the drafting model is available (substitute a same-tier model if not) — and the decisions gate: ask me to confirm D1–D3 before drafting. Then do Phase 0 (download and verify the two arXiv papers) before any prose work. I take the pen on all paper text: show me each major unit as you draft it.
