# Project Status

This is a research prototype, actively in progress. Not production-ready.

## What's working

- Both agents run end-to-end against a mock email backend.
- All ten evaluation scenarios complete at N=10 replicates per (scenario, agent): A1–A4 (accumulation), B1–B3 (premise), C1–C2 (classification), D1 (iteration). E1 (defense-in-depth) is catalogued but not in the N=10 sweep — see [docs/failure-catalog.md](docs/failure-catalog.md).
- Result files in [eval/results/](eval/results/): `eval_n10_full_v2.json` (9-scenario sweep), `eval_n10_A4.json`, `eval_n10_C2_sharpened.json` — the source data for the draft.md §6.3 tables.
- Multi-replicate harness implemented: `python -m eval.harness --replicates N --scenario <id>` runs N independent runs per (scenario, agent), reports bootstrap 95% CIs, and runs a paired-bootstrap difference test. N≥3 enables CIs and p-values.

## Headline empirical findings (full N=10 multi-replicate data)

The four composition modes are not equally exposed by aligned 2026 frontier models. Accumulation (A1, A2, A4) and iteration (D1) modes show architectural reduction in unsupervised outbound actions under the airlock; premise-MISSING (B1, B2) is caught by the read-path premise-check after the §6.5 fix; premise-WRONG-AS-FACT (A3) is the one mode the architecture does *not* catch; classification (C1) is mostly self-caught by Sonnet 4. The pattern matches the structural argument that accumulation and iteration modes are invisible to per-call alignment by construction. See [docs/paper/draft.md](docs/paper/draft.md) §6.3–6.7 for the full tables.

**A1 (full N=10):** mean writes naive 3.8 vs. airlock 2.4 (36.8% reduction). The variance asymmetry is the cleaner finding — naive std=2.9 (inconsistent self-limiting), airlock std=0.7 (the cap is hard, behavior is predictable). No Structural Gaming visible (§6.9). Per-scenario LLM-step cost is in draft §6.8 (the airlock is cheaper on 8/10 scenarios; A1 is one of two where it costs slightly more, 9.3 vs. 10.0 steps).

**Important note on effect size:** the earlier single-run reports of 62-75% reduction were cherry-picks of naive's high-variance tail. The honest mean reduction at A1 is ~37%. The empirical headline shifts from "the architecture cuts unsupervised actions by N%" to "the architecture provides a predictable upper bound on path-level cost where the model alone does not."

**Eval status:** complete. All ten scenarios run at N=10 with paired-bootstrap CIs. (An earlier 2026-04-26 run was truncated mid-A1 by API-credit exhaustion; it was subsequently re-run to completion — result files dated 2026-04-27.)

## What's not here yet

- Head-to-head comparison against SafetyDrift's benchmark or CaMeL's defenses.
- Real email integration (the mock backend is intentional — adversarial scenarios cannot be run against real systems).
- Learned irreversibility classifier (current implementation uses hand-specified scores).
- Multi-agent coordination.
- Published paper. arXiv submission was declined by moderation on 2026-08-18 (MOD-100537: "needing significant review and revision before publishable in a conventional journal"; account now requires a journal reference/DOI for future arXiv submissions). New sequencing: peer-reviewed workshop/journal venue + Zenodo DOI deposit for a priority timestamp. See [PUBLICATION_PLAN.md](PUBLICATION_PLAN.md).

## Known limitations

- All scenarios target Sonnet 4 specifically. Robustness to stronger models (Opus 4.7, GPT-5, etc.) is the predicted-but-untested validation.
- The naive agent and the airlock agent currently have slightly asymmetric tool surfaces (`schedule_meeting` is in the airlock's `propose_action` enum but not in the naive agent's tool list). The airlock executor handles both, but naive will reach for `send_email` for calendar-style requests. Consider this when interpreting per-mode results.
- Premise-WRONG-AS-FACT (A3) is the one composition mode the architecture does not catch: a wrong premise stated as fact in the input propagates, and the budget gates path *shape*, not content *veracity* (draft §6.6). The earlier premise-MISSING gap — B1, where the airlock initially fell into a trap naive caught — was fixed by adding premise-validity + information-sufficiency items to the read-path prompt (§6.5); B1 and B2 are now clean wins (airlock 0/10).

## How to engage

If you find a sharp counter to the framing, an issue with the empirical methodology, or a piece of prior art the literature map missed, open an issue or reach out. Pre-publication feedback is more valuable than post-publication.
