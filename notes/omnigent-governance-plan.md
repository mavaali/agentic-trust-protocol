# Omnigent governance evaluation — rescoped plan

**Rescoped:** 2026-06-14
**Supersedes:** the original "loud-track" Omnigent governance evaluation plan (Phase 0 → Phase 2/3 external artifact).
**Gate input:** [notes/omnigent-policy-review.md](omnigent-policy-review.md) (Phase 0 falsification review, target `omnigent-ai/omnigent @ abd110c`).

## 0. 2026-06-14 update — cross-session material retargeted to Paper 1 v2

v1 is now submitted to arXiv, so the natural home for the cross-session argument is a v2
version bump of Paper 1, not a Paper 2 sidebar. Accordingly, the cross-session / spawn-tree
accumulation residual (§3 claim 3 below) is **retargeted from Paper 2 to Paper 1 v2**, where it
becomes a *structural strengthening* of the existing visibility-asymmetry claim: see the new
`docs/paper/draft.tex` §3.6 ("The cross-session boundary"), with weave-ins to §2.2 (convergence),
§7.3 (load-bearing claim), and §7.9 (scope-and-reset as the open problem). Omnigent's per-session,
root-keyed budget is cited there as the *deployed boundary / existence proof*, re-verified against
`omnigent-ai/omnigent @ 0fe2d94`.

The compensation axis is **unchanged and stays in Paper 2**: the "no compensation / saga
primitive" claim (§3 claim 1) and the prevent / accumulate / compensate matrix (§4) remain Paper 2
territory. Pulling the cross-session boundary up into Paper 1 v2 in fact keeps Paper 2's axis
*cleaner* — Paper 2 is now strictly the post-action compensation story, with no cross-session
scope-policy material competing for its thesis.

## 1. Gate outcome and decision

Phase 0 was a falsification gate on the thesis that Omnigent's policy layer *cannot express a
path-level irreversibility budget*. The gate returned **Branch C**: the thesis is refuted by the
code. Omnigent handlers receive a persisted, cross-turn, arbitrary key/value `session_state`,
mutate it with `increment`/`append` (non-fungible accumulation), gate the pre-execution
tool-call phase with `DENY`/`ASK`, and a shipped builtin (`risk_score_policy`) already
implements accumulate-a-non-fungible-path-score-then-gate.

**Decision:** the loud/external track is **killed**. There is no standalone public artifact —
the claim that would have carried it is false. The genuinely-unrefuted residual (below) folds
into **Paper 2** (the Saga / compensating-transactions paper, `docs/paper2_outline.md`) as
honest related-work positioning, where Omnigent is a *strengthening* foil, not a target.

This is the falsification gate working as designed. A false Branch-A "thesis holds" would have
shipped a refutable public claim against a named, more-capable competitor on a public repo. The
cost of the gate was one review; the cost of skipping it would have been a retraction.

## 2. Do-NOT-claim list (forbidden in any artifact)

These claims are false and must not appear in Paper 1, Paper 2, a blog post, a talk, or an
issue. Each is paired with its one-line refutation and the load-bearing code reference, so the
refutation travels with the temptation.

| Forbidden claim | Why it's false | Ref |
|---|---|---|
| "Omnigent can only accumulate fungible scalars (dollars, call-counts)." | `session_state` is arbitrary KV; `state_updates` supports `append` (lists) and `increment`. | `omnigent/spec/types.py:1097` (`StateUpdateAction`), `engine.py:845` (`_apply_one`) |
| "Omnigent evaluates only the pending action; handlers can't see accumulated state." | The engine injects persisted `session_state` + cumulative `usage` + monotonic `labels` into every handler. | `omnigent/policies/function.py:219` (`_build_event`) |
| "Session state is per-turn / can't persist across a path." | Written through to the conversation store on every ALLOW/DENY, reseeded each turn. The `types.py:96` docstring claiming otherwise is stale and contradicted by the engine. | `engine.py:498`, `builder.py:254` |
| "There is no seam where a non-fungible path-level measure could live." | A custom `FunctionPolicy` on `tool_call` is exactly that seam — and `risk_score_policy` already occupies it. | `omnigent/policies/builtins/risk_score.py:276`, `docs/POLICIES.md:345` |
| "Omnigent can't express a path-level irreversibility budget." | Relabel `risk_score_policy`'s `tool_points` as irreversibility weights and `threshold` as the budget — it *is* one, in YAML. | `risk_score.py:325` (factory) |

## 3. Defensible narrow claims (the residual that survives Branch C)

What is *true* and citable against Omnigent. These are narrower than the original move, but the
evidence supports them and they are the only Omnigent claims permitted downstream.

1. **No compensation / saga primitive.** Omnigent's policy layer is a synchronous per-action
   `ALLOW`/`ASK`/`DENY` gate (`PolicyAction`, `omnigent/spec/types.py:1081`). There is no
   construct to stage reversible steps, commit atomically at a boundary, or compensate/roll back
   after an action has fired. *This is the gap Paper 2 fills* — and it is unrefuted.
2. **Irreversibility is not a typed first-class unit.** It can only be encoded as an opaque
   author-maintained integer (`risk_score`'s points). The runtime understands "labels" (monotonic
   ordinals) and "usage" (priced tokens) as first-class; it has no irreversibility quantity with
   its own semantics, decay, or compensability.
3. **The accumulator is per-session / per-spawn-tree, and resets at the independent-session
   boundary.** The built-in session budget is routed to the root conversation, so it ratchets
   across a parent+sub-agent spawn tree but resets when a new top-level session resolves to its
   own root (`engine.py` root resolution `root_conversation_id or conversation_id`; spawn-tree
   routing of the session budget to root; per-conversation persistence via `set_session_state` to
   a JSON column in `conversation_store/sqlalchemy_store.py` — re-verified @ `0fe2d94`). Custom
   (arbitrary-key) accumulators are per-conversation only; tree-wide aggregation is hardcoded for
   usage/cost. The cross-session integral, its weights, and a reset-and-scope policy are not
   expressed. **Retargeted (2026-06-14, §0) to Paper 1 v2 as the deployed-boundary existence proof
   in `draft.tex` §3.6** — no longer a Paper 2 sidebar.

Claim discipline: (1) is the strong, paper-bearing claim for **Paper 2** (compensation). (3) is
now a structural strengthening for **Paper 1 v2** (the cross-session boundary, §3.6). (2) remains
supporting nuance, not a headline.

## 4. Paper 2 fold — related-work hooks

Pointers only. Mihir holds the pen on paper prose; this section says *where* and *what*, not the
final wording.

- **`docs/paper2_outline.md` §2 (Background and Related Work)** — add Omnigent as the concrete
  contemporary foil. Framing: *a production agent framework (Databricks Omnigent, Apache-2.0,
  June 2026) whose policy layer already accumulates non-fungible path state — a configurable
  "risk score" that ratchets across a session and gates sensitive tools — yet still has no
  compensation primitive once an action has fired.* This **sharpens** Paper 2's central gap: the
  missing half is not accumulation (the field has that now) but recovery.
- **`docs/paper2_outline.md` §"Positioning" (the CaMeL parallel, currently §7.6 of Paper 1)** —
  extend the non-overlapping-primitives table to three contemporaries:

  | System | Prevent (perimeter) | Accumulate (trajectory) | Compensate (post-action) |
  |---|---|---|---|
  | CaMeL | ✓ information-flow | — | — |
  | Omnigent policy layer | ✓ per-action gate | ✓ `risk_score` / budgets | — |
  | Airlock (this work) | ✓ staging gate | ✓ trust budget | Paper 2: saga / compensation |

  The point the table makes: Omnigent closing the accumulate column is *evidence for* Paper 2's
  thesis, not against it — accumulation is becoming table stakes; compensation is the frontier.
- **Paper 1 (`docs/paper/draft.md`)** — at most a single honest related-work sentence if it
  survives review: prior/contemporary frameworks accumulate non-fungible path state, so Paper 1's
  contribution is *not* "accumulation is possible" but the empirical variance-asymmetry /
  predictable-upper-bound result, which is Omnigent-independent. Do not overclaim differentiation.

## 5. Rescoped phases

| Phase | Old (struck) | New |
|---|---|---|
| 0 | Falsification gate | **Done** — Branch C. [review memo](omnigent-policy-review.md). |
| 1 | Build the loud external artifact | Land the §4 hooks in `docs/paper2_outline.md` (Mihir, the pen). |
| 2 | Publish blog / LW post / paper section making the differentiation claim | One honest related-work sentence in Paper 1 *iff* it survives review (§4). |
| 3 | Amplify | **Struck.** No amplification of a refuted claim. |

**Done condition:** Omnigent appears in Paper 2 §2 as the accumulate-but-can't-compensate foil,
and nowhere does any artifact assert a claim from §2's forbidden list. No external/loud artifact
ships.
