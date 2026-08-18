# Zenodo Deposit Metadata (draft — nothing uploaded)

*Drafted 2026-08-18 for the priority-timestamp deposit described in [PUBLICATION_PLAN.md](PUBLICATION_PLAN.md). Prep only; the deposit has **not** been created.*

## Upload type

- **Type:** Publication → Preprint
- **File:** `docs/paper/draft.pdf` (built 2026-08-18 from `draft.tex`; 22 pages). Optionally also a source tarball (`draft.tex`, `references.bib`, `figures/`).

## Title

Two-Way Doors, One-Way Trajectories: A Compositional Account of LLM Agent Safety

## Authors

- **Wagle, Mihir** — independent / personal capacity (affiliation on the draft's title page reads "Microsoft" with a personal-capacity disclaimer footnote; decide whether the Zenodo affiliation field should say "Microsoft" or "Independent" before upload)

> **Open decision (blocks upload):** [AUTHORS.md](AUTHORS.md) commits to naming a second author — the contributor of the door-composition framing — "once the formal paper is ready for submission." A DOI deposit fixes the author list in DataCite metadata. Resolve whether they are named on v1 before uploading.

## Abstract

Contemporary aligned LLMs refuse the canonical agent-safety attacks on their own merits. The residual failure surface for agents lives at the path level — sequences of individually-reversible actions that compose into cumulatively-irreversible trajectories. We organize this surface around four composition modes — accumulation, premise, classification, iteration — and present an empirical study of a Plan-then-Execute architecture (read-path → staging area → write-path with trust budget and irreversibility classifier) across ten scenarios at N=10 replicates each. The architecture catches accumulation and audience-fan-out via budget exhaustion (deterministic 3-action cap on A2; 51% mean-write reduction on A1); catches missing-information premise failures via a read-path prompt that asks for clarification (10/10 catch on B1, B2, A4); fails to catch one specific composition mode — premise stated as fact, then propagated across action types (A3, where the airlock proposes calendar invites that the naive baseline never reaches). We argue this asymmetry is structural: the architecture observes the shape of a path (count, audience, action types, missing inputs) but not content veracity; fact-verification remains a per-call problem the architecture cannot fix. The paper's contributions are (1) the door-composition framing as analytic vocabulary, (2) the four-mode taxonomy organized by what each mode requires to detect, (3) the empirical decomposition of which architectural primitive catches which mode, and (4) the cleanest empirical signal in the suite: the architecture's contribution is variance reduction, not just mean reduction — naive's per-session write count has standard deviation up to 2.9 across replicates while the airlock's stays under 1.0 on accumulation modes, so a deployer who cares about bounding worst-case path cost gets that bound from architecture alone.

*(Verbatim from `docs/paper/draft.md` §Abstract, with LaTeX math flattened to plain text. If the abstract is revised for the venue submission — see PUBLICATION_PLAN.md TODO-2, which adds a differentiation sentence — update this before upload.)*

## Keywords

AI safety; LLM agents; agent verification; path-level safety; irreversibility; trust budget; composition modes; Plan-then-Execute; agent architecture; CQRS

## License

> **Open decision (blocks upload):** the repository code is MIT, but the paper text is a separate work. Standard choice for a preprint deposit is **CC-BY 4.0** (recommended; maximizes citability and is what most preprint servers use). Alternatives: CC-BY-SA 4.0, CC-BY-NC 4.0. Mihir to pick.

## Additional metadata

- **Version:** v1 (Zenodo will mint a version DOI plus a concept DOI; later revisions get new version DOIs under the same concept DOI)
- **Publication date:** date of upload
- **Language:** English
- **Related identifiers:**
  - `https://github.com/mavaali/agentic-trust-protocol` — *is supplemented by* (code, scenarios, eval results)
  - Parallax (arXiv:2604.12986) and McCann (arXiv:2604.27289) — *references*, once verified and cited in the draft (PUBLICATION_PLAN.md TODO-1) [UNVERIFIED identifiers — confirm on arXiv before entering them]
- **Notes field (suggested):** "Submitted to arXiv 2026-08; declined by moderation (MOD-100537). Deposited on Zenodo for timestamp priority while under submission to a peer-reviewed venue."
  - *(Optional — it is honest and preempts "why isn't this on arXiv?"; drop the parenthetical if preferred.)*

## After the deposit

1. Record the DOI in README.md, CITATION.cff (`identifiers:` block + a `preferred-citation`), STATUS.md, and PUBLICATION_PLAN.md.
2. Add the DOI badge to the README.
3. Use the DOI in the workshop/journal submission where a preprint link is requested.
