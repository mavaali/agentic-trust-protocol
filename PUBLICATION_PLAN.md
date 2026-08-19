# Publication Plan

*Created 2026-08-18, following the arXiv moderation decline. Owner: Mihir Wagle.*

## What happened

arXiv declined the submission on 2026-08-18 (moderation decision MOD-100537). Two parts:

1. **Paper declined** as "needing significant review and revision before publishable in a conventional journal." No specific technical feedback was provided.
2. **Account-level restriction:** future arXiv submissions from this account require a journal reference/DOI, or they are auto-declined.

Consequence: **arXiv-first publication is closed for this work.** The new sequencing is (a) an immediate Zenodo deposit for a priority timestamp, and (b) submission to a peer-reviewed workshop/journal venue; an arXiv posting becomes possible again only after a journal reference/DOI exists.

## Immediate action: Zenodo deposit (priority timestamp)

**Why:** the draft's claims sit close to two recent preprints — Parallax ("Why AI Agents That Think Must Never Act," Joel Fokou, arXiv:2604.12986, 2026-04-14) and McCann's Necessity Theorem ("Mechanized Foundations of Structural Governance," Alan L. McCann, arXiv:2604.27289, 2026-04-30) [identifiers/titles verified by web search 2026-08-18; neither paper is cited in this repo yet — see TODO-1 below]. With arXiv closed, the priority timestamp has to come from somewhere else. Zenodo issues a DataCite DOI at publish time, immediately and at no cost, with versioned DOIs (a concept DOI plus one DOI per version), so a v1 deposit now does not block a revised v2 later.

> **Timing revised 2026-08-18 (later same day):** both proximate papers are verified as published in April 2026, so the priority race against them specifically is already settled; the timestamp now protects this paper's *delta* against future work. Depositing the pre-revision draft — which cites neither paper — would create a permanent flawed record for negligible priority gain. **New plan: deposit the post-surgery revision (~Aug 27–28), per [REWRITE_PLAN.md](REWRITE_PLAN.md) §8–9.**

Steps (deposit itself is **not yet done** — prep only):

1. Build the PDF from `docs/paper/draft.tex` (verified building cleanly, 22 pages, 2026-08-18; see below).
2. Use the metadata drafted in [zenodo-metadata.md](zenodo-metadata.md). Two open decisions block upload — see "Open decisions" there (authorship of the unnamed second contributor per [AUTHORS.md](AUTHORS.md), and the license for the text).
3. Upload PDF (+ optionally a source tarball) as upload type "publication / preprint", link the GitHub repo as a related identifier.
4. Record the DOI back into README.md, CITATION.cff, and this file.

Note: a Zenodo DOI is a *timestamp*, not a peer-review credential. It is unlikely to satisfy arXiv's journal-reference requirement on its own [UNVERIFIED — arXiv does not publish a precise definition of what clears the restriction]; the venue submission below is what reopens arXiv.

## Target venues

Facts below were checked by web search on 2026-08-18 (direct fetches of the workshop sites were blocked from this environment, so search-snippet-sourced items are marked accordingly). Anything not confirmable is marked **[UNVERIFIED]** — no invented deadlines.

### 1. "Who Verifies the Agents?" — NeurIPS 2026 workshop (primary target)

- **Fit:** best topical match in the current cycle — a workshop specifically on verification for reliable agent development; this paper's contribution is exactly an agent-verification architecture and an empirical decomposition of what architecture (vs. per-call alignment) can verify.
- **Deadline:** submissions due **August 29, 2026 (AoE)** — 11 days from the date of this plan. Workshop in Sydney, December 11 or 12, 2026. (Source: workshop site via search snippets, 2026-08-18.)
- **Page limit:** 4–9 pages excluding references and appendices, NeurIPS 2026 template; the current 22-page draft needs cutting.
- **Review:** double-blind; posters, with select orals/lightning talks.
- **DOI policy:** **non-archival, no formal proceedings, no DOI** — accepted papers posted on OpenReview. Must therefore be paired with the Zenodo deposit; whether a non-archival workshop acceptance helps clear the arXiv restriction is **[UNVERIFIED]** and probably it does not.
- **Review timeline / notification date:** **[UNVERIFIED]** (typically late September–October for NeurIPS workshops, but not confirmed for this one).

### 2. Evaluation of Interactive Agents — NeurIPS 2026 workshop (same-cycle alternate)

- **Fit:** good — evaluation of interactive agents, with safety explicitly in scope; the N=10 multi-replicate harness and variance-asymmetry finding fit an evaluation framing.
- **Deadline:** **August 29, 2026 (AoE)**; workshop in Atlanta. (Source: workshop site via search snippets, 2026-08-18.)
- **Page limit, archival status, DOI policy, notification date:** **[UNVERIFIED]** — NeurIPS workshops are typically non-archival without DOIs, but this workshop's policy was not directly confirmed.
- Note: dual-submitting the same paper to two workshops at the same conference is usually disallowed — pick one **[UNVERIFIED for these two workshops' specific policies]**.

### 3. TMLR — Transactions on Machine Learning Research (journal route)

- **Fit:** strong — TMLR explicitly reviews for technical correctness rather than perceived significance, which suits an honest-negative-results paper (A3 architectural failure, refuted Structural Gaming hypothesis, corrected effect sizes).
- **Deadline:** none — rolling submissions year-round.
- **Review timeline:** reviews within ~4 weeks of submission, decisions within ~2 months (per TMLR's self-description; individual papers vary).
- **Page limit:** flexible/variable manuscript length — the 22-page draft could go in with modest trimming.
- **DOI policy: caution.** dblp indicates TMLR records carry **no DOIs**. An accepted TMLR paper is a peer-reviewed *journal reference*, which plausibly satisfies arXiv's "journal reference/DOI" requirement even without a DOI, but this is **[UNVERIFIED]** — worth emailing arXiv moderation to confirm before relying on it.

### 4. ICLR 2027 (main conference)

- **Fit:** reasonable for the safety/agents area, but the most competitive option and the empirical scale (one model, mock backend, N=10) is a likely reviewer objection.
- **Deadline:** abstract **September 18, 2026 (AoE)**; full paper **September 25, 2026 (AoE)**. Reviews released November 5, 2026; decisions **December 16, 2026**; conference April 24–28, 2027 (Brazil). (Source: iclr.cc via search snippets, 2026-08-18.)
- **Page limit:** **[UNVERIFIED]** for 2027 (historically ~9–10 pages main text, unlimited references/appendix).
- **DOI policy:** proceedings hosted on OpenReview; whether ICLR papers receive DOIs is **[UNVERIFIED]**. Conference acceptance may or may not clear arXiv's journal-reference bar **[UNVERIFIED]**.

### 5. AAAI-27 workshop program / AAAI-28 (fallback cycle)

- **AAAI-27 main track is closed** (abstracts were due July 21, 2026; full papers July 28, 2026; conference February 16–23, 2027, Montréal).
- **AAAI-27 workshops:** the workshop program typically opens calls in autumn with deadlines around **October–November 2026 [UNVERIFIED — individual workshop CFPs not yet checked]**. AAAI workshop proceedings DOI policy varies by workshop (some publish via CEUR-WS or AAAI Press, some are non-archival) **[UNVERIFIED per-workshop]**.
- **AAAI-28 main track:** deadlines expected ~July 2027 **[UNVERIFIED]** — the "if everything else misses" option; AAAI proceedings do carry DOIs (ojs.aaai.org assigns DOIs to AAAI conference papers).

### Recommended sequencing

> **Venue re-decided 2026-08-18 (D1 resolved): TMLR-primary, workshop dropped as the driver.** Mihir cannot travel to Sydney (reception commitment), so in-person presentation at *Who Verifies the Agents?* is out. The workshop was already marginal — **non-archival, no proceedings, no DOI**, and (per the venue analysis above) it **probably does not clear the arXiv restriction**. Its only remaining value was a forcing deadline plus a NeurIPS-workshop line — not worth a double-blind anonymization scramble against Aug 29 with no travel. The rewrite happens regardless: it produces the J-length paper, which **is** the Zenodo deposit (the DOI, no travel/deadline) **and** the TMLR submission (rolling; the journal reference that actually reopens arXiv). The Aug-27–28 Zenodo date and the D4 second-author clock are **no longer racing a 9-day fuse** — the authorship decision still matters, just off the critical path. **Workshop remains an optional bolt-on**: only if a same-cycle venue permits *remote* presentation, in which case the anonymized version is nearly free off the J draft (CFP remote-policy still [UNVERIFIED] — resolve only if that path is revived).

1. **Rewrite at a sane pace** (Phases 0–2 of [HANDOVER.md](HANDOVER.md)) — no Aug-29 gun. Phase 0 prior-art verification is **done** (2026-08-18; see `docs/paper/prior-art/notes.md` — TODO-1 resolved, both papers verified full-text and cited).
2. **Zenodo deposit** of the post-surgery J-length PDF → DataCite DOI (timestamp + citable home). Gate: the two open metadata decisions (second author, license). **Must bundle `eval/results/*.json` + scenario YAMLs** — they are gitignored and the Sonnet-4 baseline model is API-retired, so that archive is the only surviving record of the anchor data.
3. **TMLR** (rolling; peer-reviewed journal reference is the credential that plausibly reopens arXiv) — the real target.
4. **ICLR 2027** (Sep 25) only if the TMLR route is rejected in time or deliberately skipped — decide by mid-September.
5. **Optional workshop** (remote-only): revisit only if a same-cycle venue allows remote presentation and the CV line is wanted.

## Revision TODOs from the rejection audit

> **Superseded in part, 2026-08-18 (later same day):** the decision was made to do a full rewrite rather than patch these TODOs individually — see [REWRITE_PLAN.md](REWRITE_PLAN.md), which absorbs TODO-1 through TODO-5 into its §2 (prior-art repositioning) and §3 (new spine). The TODOs below stand as the audit record.

The most plausible substantive reading of the decline: the paper's differentiation from recent closely-related prior art is not visible where a moderator or reviewer looks first. Audit of the current draft (`docs/paper/draft.md` / `draft.tex`, 2026-08-18) against that reading:

**Finding: the differentiation is not "buried in related work" — it is entirely absent.** Specific gaps, as TODOs (theorem/technical content deliberately untouched per constraints; Mihir takes the pen per `NEXT_STEPS.md`):

- **TODO-1 (blocking any resubmission):** Neither McCann's Necessity Theorem (arXiv:2604.27289) nor Parallax (arXiv:2604.12986) is cited *anywhere* in the repo — not in the abstract, intro (§1), related work (§2), `references.bib`, or `docs/literature-map.md`. Add both to `references.bib` and `literature-map.md`, with a positioning note for each (what they claim, what this paper claims, why the claims are different). [The papers' actual titles/authors/claims are UNVERIFIED from this environment — pull the abstracts from arXiv and verify the IDs before citing.]
- **TODO-2:** State the differentiation in the **abstract**: one sentence distinguishing this paper's *structural input-availability* argument (§3.2/§3.5: accumulation signals are absent from any single forward pass's inputs — "not a capability gap; an input-availability gap") from *undecidability/impossibility-based* arguments for verification limits. The abstract currently contains no differentiation from any theorem-style prior art.
- **TODO-3:** State it again in the **intro**, most naturally as an added item in §1.5 ("What this paper does *not* claim"), which currently lists Arthur, Krakovna, Garcia-Molina & Salem, Dhodapkar & Pishori, and Del Rosario — but not McCann or Parallax. Explicitly: this paper does not prove an undecidability result and does not depend on one; the argument goes through for computationally unbounded models.
- **TODO-4 (decision, not a rewrite):** No "Separation Theorem" is *stated* in any repo document — `notes/irreversibility-bounds-autonomy.md` records this explicitly ("no document in this repo states such a theorem"; the nearest artifacts are the CQRS separation and the §3.6/§3.2 structural argument). If the venue version is to claim a theorem, the statement must first be written down and differentiated from McCann's Necessity Theorem in the statement itself; otherwise keep the current empirical/framing positioning (§1.5 already disclaims theorem novelty, which is the safer posture). Mihir decides.
- **TODO-5:** §3.2's sentence "This is a structural argument, not a capability argument: better models do not fix it" is the anchor for the differentiation — extend it (or footnote it) to also contrast with undecidability-based arguments, since "structural" currently does double duty.

## Ambiguities flagged (not guessed at)

1. **Repo/package naming mismatch:** the decision context refers to "this repo: boundary" and "PyPI: boundary-envelope." This repo is `agentic-trust-protocol` and `pyproject.toml` declares `name = "agentic-trust-protocol"` with no PyPI publishing config; the strings "boundary" (as a name) and "boundary-envelope" appear nowhere in the repo. If a rename/rebrand is underway, the Zenodo metadata and CITATION.cff need reconciling before deposit — the drafted metadata uses the repo's actual current names.
2. **What exactly was submitted to arXiv** (which PDF revision, which title) is not recorded in the repo — `.gitignore` references `docs/paper/arxiv_submission.tar.gz` but the tarball is untracked. The audit above was run against the current `draft.md`/`draft.tex` head.
3. **Authorship before deposit:** [AUTHORS.md](AUTHORS.md) promises a second author (the door-composition framing contributor) will be named "once the formal paper is ready for submission." A DOI-issuing deposit is that moment for attribution purposes — this needs resolving *before* the Zenodo upload, since DOI metadata authorship is awkward to amend.

## Build status (2026-08-18)

`docs/paper/draft.tex` compiles cleanly with pdflatex + bibtex (TeX Live): 22 pages, 0 errors, 0 undefined citations/references. Figures present in `docs/paper/figures/` (PDF + PNG, regenerable from `generate_figures.py`). `docs/paper/draft.pdf` in the repo is the current build.
