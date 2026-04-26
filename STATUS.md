# Project Status

This is a research prototype, actively in progress. Not production-ready.

## What's working

- Both agents run end-to-end against a mock email backend.
- Five evaluation scenarios complete and producing data: A1 (accumulator), B1 (stale date), B2 (wrong John), C1 (draft vs. send), D1 (auto-responder loop).
- Five more planned (A2, A3, B3, C2, plus a defense-in-depth scenario E1) — see [docs/failure-catalog.md](docs/failure-catalog.md).
- Single-replicate runs only; multi-replicate evaluation with statistical comparison is the next milestone.

## Headline empirical finding (preliminary, single-replicate)

The four composition modes are not equally exposed by aligned 2026 frontier models. Quantity (A1) and iteration (D1) modes show ~62% reduction in unsupervised outbound actions under the airlock architecture. Premise (B2) and classification (C1) modes are mostly self-caught by Sonnet 4 itself, with the architecture's value reduced to staging-for-inspection. The pattern matches the structural argument that quantity and iteration modes are invisible to per-call alignment by construction. See [docs/paper/draft.md](docs/paper/draft.md) Section 6.4 for details.

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
