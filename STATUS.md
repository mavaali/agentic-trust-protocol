# Project Status

This is a research prototype, actively in progress. Not production-ready.

## What's working

- Both agents run end-to-end against a mock email backend.
- Five evaluation scenarios complete and producing data: A1 (accumulator), B1 (stale date), B2 (wrong John), C1 (draft vs. send), D1 (auto-responder loop).
- Five more planned (A2, A3, B3, C2, plus a defense-in-depth scenario E1) — see [docs/failure-catalog.md](docs/failure-catalog.md).
- Multi-replicate harness implemented: `python -m eval.harness --replicates N --scenario <id>` runs N independent runs per (scenario, agent), reports bootstrap 95% CIs, and runs a paired-bootstrap difference test. N≥3 enables CIs and p-values.

## Headline empirical findings (preliminary, partial multi-replicate data)

The four composition modes are not equally exposed by aligned 2026 frontier models. Accumulation (A1) and iteration (D1) modes show architectural reduction in unsupervised outbound actions under the airlock; premise (B2) and classification (C1) modes are mostly self-caught by Sonnet 4 itself, with the architecture's value reduced to staging-for-inspection. The pattern matches the structural argument that accumulation and iteration modes are invisible to per-call alignment by construction. See [docs/paper/draft.md](docs/paper/draft.md) Sections 6.5–6.7 for details.

**A1 partial multi-replicate data (N=7 naive, N=6 airlock):** mean writes 3.71 vs. 2.50 (~33% reduction in mean unsupervised writes). The variance asymmetry is the cleaner finding — naive std=2.93 (highly inconsistent self-limiting), airlock std=0.84 (cap is hard, behavior is predictable). LLM steps are *fewer* under airlock (5.83 vs. 11.71 mean), suggesting the gate truncates read-path exploration rather than imposing a long-way-around cost. No Structural Gaming visible at this N — all executed writes were `send_email` in both conditions; the draft-vs-send shift hypothesis remains testable but unsupported by current data.

**Important note on effect size:** the earlier single-run reports of 62-75% reduction were cherry-picks of naive's high-variance tail. The honest mean reduction at A1 is closer to 33%. The empirical headline shifts from "the architecture cuts unsupervised actions by N%" to "the architecture provides a predictable upper bound on path-level cost where the model alone does not."

**Eval status:** the N=10 run on 2026-04-26 was truncated by API credit exhaustion partway through A1. We have 7 naive + 6 airlock replicates of A1; zero replicates for B1, B2, C1, D1. Remaining work before preprint: top up Anthropic API credit, re-run `python -m eval.harness --replicates 10` to fill in B1/B2/C1/D1. Estimated cost: ~$10-15 in Sonnet calls.

## What's not here yet

- Multi-replicate runs with bootstrap CIs.
- Head-to-head comparison against SafetyDrift's benchmark or CaMeL's defenses.
- Real email integration (the mock backend is intentional — adversarial scenarios cannot be run against real systems).
- Learned irreversibility classifier (current implementation uses hand-specified scores).
- Multi-agent coordination.
- arXiv preprint (target: 5-6 weeks from project start).

## Known limitations

- All scenarios target Sonnet 4 specifically. Robustness to stronger models (Opus 4.7, GPT-5, etc.) is the predicted-but-untested validation.
- The naive agent and the airlock agent currently have slightly asymmetric tool surfaces (`schedule_meeting` is in the airlock's `propose_action` enum but not in the naive agent's tool list). The airlock executor handles both, but naive will reach for `send_email` for calendar-style requests. Consider this when interpreting per-mode results.
- The airlock's read-path system prompt emphasizes blast-radius and trustworthiness but not premise freshness. B1's result (airlock fell into the trap that naive caught) reflects this and is documented honestly.

## How to engage

If you find a sharp counter to the framing, an issue with the empirical methodology, or a piece of prior art the literature map missed, open an issue or reach out. Pre-publication feedback is more valuable than post-publication.
