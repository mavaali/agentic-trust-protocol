# Omnigent policy subsystem teardown

**Investigated:** 2026-06-14
**Target:** github.com/omnigent-ai/omnigent @ `abd110c2688cecfa5d318eea886d05aa4f4b207a` (`docs: clarify local development setup (#51)`, 2026-06-14)
**Investigator:** automated teardown per Phase 0 of the omnigent governance evaluation plan

> **Verdict up front: Branch C.** The thesis-as-stated is refuted by the code. Omnigent's
> policy layer does *not* evaluate only "the pending action + a fungible scalar." Handlers
> receive a persisted, cross-turn, arbitrary key/value `session_state`, can mutate it with
> `increment`/`append` (not just numeric scalars), and gate the pre-execution tool-call phase
> with `DENY`/`ASK`. An accumulate-a-non-fungible-path-score-then-gate primitive is not merely
> *expressible* — it ships as a documented builtin (`risk_score_policy`). Details and the
> single load-bearing reference are below; the residual differentiator for the envelope is
> narrow (airlock/two-phase-commit + irreversibility-as-a-typed-unit), not "they can't
> accumulate."

A note on structure vs. the plan's framing: the plan assumed `omnigent/policies/` with
`builtins/safety.py` + `builtins/cost.py`, `docs/POLICIES.md`, `docs/AGENT_YAML_SPEC.md`. All
of these exist exactly as described. The only adaptation: the *runtime* half of the subsystem
(the evaluation loop, state persistence, composition) lives in a sibling package
`omnigent/runtime/policies/` (`engine.py`, `builder.py`, `enforcement.py`), while
`omnigent/policies/` holds the pure-evaluator contract and builtins. The architecture is
cleanly policy-handler-shaped — the plan's structure holds.

---

## Handler interface (verbatim)

Every policy is a subclass of `Policy` with a single `evaluate` method. `omnigent/policies/base.py:49`:

```python
@abstractmethod
async def evaluate(
    self,
    ctx: EvaluationContext,
    context: dict[str, Any],
) -> PolicyResult:
```

The same module also declares a per-turn lifecycle hook — important for the "sequence hook"
question below. `omnigent/policies/base.py:73`:

```python
def reset_turn(self) -> None:  # noqa: B027 — intentional no-op default (see docstring)
    """
    Reset per-turn state, if any.
    ...
    The runtime calls this once per "turn" — defined as one
    user prompt → terminal assistant response cycle ...
    Sub-iteration steps (tool calls within a turn) do NOT trigger a reset.
    """
```

The concrete, author-facing handler is `FunctionPolicy`, which adapts a Python callable. The
callable receives an `event` dict and returns a result dict. The **event shape it actually
gets** is built in `omnigent/policies/function.py:219` (`_build_event`):

```python
event: dict[str, Any] = {
    "type": _phase_to_event_type(ctx.phase),
    "target": ctx.tool_name,
    "data": ctx.content,
    "context": {
        "actor": dict(ctx.actor) if ctx.actor else {},
        "usage": dict(ctx.usage) if ctx.usage else {},
        "user_daily_cost": dict(ctx.user_daily_cost) if ctx.user_daily_cost else {},
        "model": ctx.model,
        "harness": ctx.harness,
        "labels": dict(ctx.labels) if ctx.labels is not None else {},
    },
    "session_state": dict(ctx.session_state) if ctx.session_state is not None else {},
    "llm_client": ctx.llm_client,
}
if ctx.request_data is not None:
    event["request_data"] = ctx.request_data
return event
```

The documented public interface (`docs/POLICIES.md:392`) and the event/response examples
(`docs/POLICIES.md:426`) match this: a tool-call event carries `data: {name, arguments}`,
`context.usage`, and `session_state: {...}`, and the response may carry `state_updates` with
`"set" | "increment" | "delete" | "append"` (`docs/POLICIES.md:466`).

**What `check`/`evaluate` receives — precise answer:**
- The pending action (`data`/`target`), **plus** persisted accumulated state: `session_state`
  (arbitrary KV), `context.usage` (cumulative token/cost counters), `context.labels`
  (persisted conversation labels), `context.user_daily_cost`, `context.model`, `context.actor`.
- It does **not** receive the raw conversation history. `EvaluationContext` *has* a
  `trajectory` field (`omnigent/policies/types.py:159`, the last 10 items —
  `_TRAJECTORY_WINDOW = 10`, `omnigent/runtime/policies/engine.py:40`), but `_build_event`
  above omits it. Per `types.py:80`, "`FunctionPolicy` ignores the field; `PromptPolicy`
  formats it into the classifier prompt." So a *function* policy sees the path only through
  state it has itself accumulated; an LLM-classifier (`PromptPolicy`) sees a bounded 10-item
  window but returns a verdict, not an accumulator.

The return type carries the accumulation channel. `omnigent/policies/types.py:227`:

```python
state_updates: list[StateUpdate] | None = None
```

where `StateUpdateAction` (`omnigent/spec/types.py:1097`) is:

```python
class StateUpdateAction(str, Enum):
    SET = "set"
    INCREMENT = "increment"
    DELETE = "delete"
    APPEND = "append"
```

`APPEND` is the load-bearing one for non-fungibility: it accumulates a **list** of arbitrary
author-defined items, not a scalar.

## State model

Per-session state is **not** a closure on the handler and **not** ephemeral. It lives in the
`PolicyEngine`'s hot cache and is **persisted to the conversation store**, surviving across
turns. The `EvaluationContext` docstring (`omnigent/policies/types.py:96`) claims session_state
"Does NOT persist across turns" — **this docstring is stale and contradicted by the engine code**,
which is what actually runs:

`omnigent/runtime/policies/engine.py:498` (`apply_state_updates`), with docstring "the
resulting snapshot is persisted to the conversation store so session state survives across
turns":

```python
if session_ops:
    for op in session_ops:
        _apply_one(self._session_state, op)
    self._store.set_session_state(self._conversation_id, self._session_state)
```

The matching seed on the read side — `build_policy_engine` rehydrates state from the store at
the top of every turn. `omnigent/runtime/policies/builder.py:254`:

```python
initial_session_state = _load_session_state(conversation_id, conversation_store)
```

`_load_session_state` (`builder.py:545`) reads `conv.session_state` straight from the persisted
conversation row. **Write-back on every ALLOW/DENY, seed on every build → cross-turn
persistence is real.** The `APPEND`/`INCREMENT` semantics are in `_apply_one`
(`omnigent/runtime/policies/engine.py:845`):

```python
elif op.action == StateUpdateAction.INCREMENT:
    current = state.get(op.key, 0)
    state[op.key] = current + op.value
...
elif op.action == StateUpdateAction.APPEND:
    existing = state.get(op.key)
    if existing is None:
        state[op.key] = [op.value]
    else:
        if not isinstance(existing, list):
            raise TypeError(...)
        existing.append(op.value)
```

**How the two named builtins implement accumulation:**

- `max_tool_calls_per_session` (`omnigent/policies/builtins/safety.py`) is the canonical
  counter. It reads `state.get("_policy_tool_call_count", 0)`, DENYs at the limit, and returns
  `state_updates: [{"key": "_policy_tool_call_count", "action": "increment", "value": 1}]`.
  Its docstring: "Uses `event["session_state"]` to persist the counter across turns." This is
  the plan's "already known wrong" naive-form refutation, confirmed verbatim.

- `cost_budget` (`omnigent/policies/builtins/cost.py:288`) does **not** keep its own counter —
  it reads the engine-maintained cumulative spend `event["context"]["usage"]["total_cost_usd"]`
  (`cost.py:89`), and uses `session_state` only to remember the highest soft-threshold the user
  approved (`cost.py:336`, a `set` op). The cumulative usage is summed engine-side, even
  tree-wide across sub-agents (`builder.py:728`, `_policy_usage_seed`). So cost gating is a
  *session-wide* (whole spawn tree) fungible accumulator.

There are also persisted **labels** with an optional ordered value-set and a monotonic
direction (`LabelDef`, `omnigent/spec/types.py:1186`): `values: list[str]` + `monotonic:
"increasing" | "decreasing"`. This is, structurally, a ratchet primitive — an ordinal level
that the engine will only let move one way (`engine.py:1090`, `_monotonic_ok`). It is an
ordinal *level*, not an accumulating *budget*, but it is non-fungible and path-monotone.

## Scope binding

Policies attach at three scopes, merged into one ordered list per workflow in
`build_policy_engine` (`omnigent/runtime/policies/builder.py:222-246`):

1. **Session** policies (per-conversation, via the CRUD/REST API and `sys_add_policy`).
2. **Agent** policies (`spec.guardrails.policies` in the agent YAML — `docs/AGENT_YAML_SPEC.md:172`).
3. **Server/admin** default policies (server config + `POST /v1/policies`, `docs/POLICIES.md:505`).

**Run order:** session → agent → admin (`builder.py:240`). Sub-agents inherit the *root*
conversation's session policies, deduped by name with child-wins (`builder.py:232-238`).

**Conflict semantics on overlap** (`engine.py:289-342`, the `evaluate` loop): policies run in
that order; `DENY` short-circuits immediately (`engine.py:301`); `ASK` accumulates and the
first-in-order ASK becomes the deciding policy; `ALLOW` continues. Label writes from multiple
policies in one pass merge most-restrictively in the monotonic direction (`engine.py:1017`,
`_merge_monotonic_writes`). On `ASK`, label writes and state updates are **withheld** until the
user approves (`engine.py:318-331`) — a denied ASK leaves no trace.

**State scope caveat (the real limit):** generic `session_state` is **per-conversation**.
Tree-wide aggregation is hardcoded for *usage/cost only* (`_policy_usage_seed`, and the two
reserved keys `SESSION_COST_ASK_APPROVED_STATE_KEY` / `USER_DAILY_ASK_APPROVED_STATE_KEY`
that `apply_state_updates` routes to the root conversation / user-day store,
`engine.py:487-497`). A *custom* accumulator gets no such tree-wide plumbing: across a
multi-agent spawn tree it would accumulate per-conversation unless the author replicates the
reserved-key root-routing pattern. For a single-conversation path it is fully path-level.

## Hook surface

There is **no post-hoc / batch / end-of-turn evaluation hook that sees a sequence of actions
at once.** Enforcement is strictly per-phase. `Phase` (`omnigent/spec/types.py:1073`) is
`REQUEST`, `TOOL_CALL`, `TOOL_RESULT`, `RESPONSE`, `LLM_REQUEST`, `LLM_RESPONSE`. Each fires a
single `engine.evaluate(ctx)` for one phase (`omnigent/runtime/policies/enforcement.py:35`;
call sites in `omnigent/server/routes/sessions.py:8867, 8994, 9139, 11146, 11214, 11406`).
`TOOL_CALL` fires **before** the tool runs — `cost.py`'s docstring: "the one point a native
`PreToolUse` hook can actually block before the action runs." That is the pre-execution
commit-gate point.

The closest things to "sees a sequence":
- `reset_turn()` (`base.py:73`, dispatched by `engine.reset_turn`, `engine.py:776`) — a
  per-turn *lifecycle* callback that *clears* per-turn counters. It makes no decision and sees
  no actions; it exists so a "per-turn" limit doesn't silently become "per-session."
- `trajectory` — a bounded last-10-item window (`engine.py:40`, `_populate_trajectory`
  `engine.py:815`), injected **only** to `PromptPolicy` classifiers, not to function handlers.

So: no transactional/batch hook, no commit/rollback/compensation construct. A handler can
block the action it is currently looking at; it cannot atomically stage a sequence and
commit-or-abort it, and it cannot undo earlier reversible steps.

## The seam

A custom path-level budget plugs in as a `FunctionPolicy` registered by dotted path
(`docs/POLICIES.md:468`, `policy_modules:` / `POLICY_REGISTRY`), declared `on: [tool_call]`
(or self-selecting on `event["type"] == "tool_call"`). Exact contract it plugs into:

```python
def my_budget(event: PolicyEvent) -> PolicyResponse | None:   # docs/POLICIES.md:397
    # event["type"] == "tool_call"  (pre-execution)
    # event["data"] == {"name": <tool>, "arguments": {...}}   # the pending action
    # event["session_state"]        -> persisted, cross-turn accumulator (read)
    # event["context"]["usage"]     -> cumulative fungible counters
    # event["context"]["labels"]    -> persisted monotonic labels
    # event["context"]["model" / "actor" / "harness"]
    # return {"result": "DENY"|"ASK"|"ALLOW",
    #         "state_updates": [{"key": k, "action": "increment"|"append", "value": v}]}
```

**What it can see at that point:** the pending tool name + arguments; the full *accumulated*
state it (or other policies) has persisted in `session_state` (any shape, via `append`/
`increment`); cumulative usage scalars; persisted labels; the active model and actor; and an
`llm_client` to classify the action if heuristics aren't enough.

**What it cannot see / cannot do:** the raw conversation path beyond what it accumulated (no
`trajectory` in the function-handler event); state from sibling sub-agents (per-conversation
scope, no tree-wide plumbing for custom keys); and there is no commit/rollback/compensation —
it can only `ALLOW`/`ASK`/`DENY` the one pending action.

The seam **carries non-fungible path state today.** The cleanest existing proof is not a
hypothetical custom handler but a shipped, documented builtin —

## Verdict

**Branch C.** An irreversibility-style budget is already expressible *and* a near-identical
primitive is already present. The single most load-bearing reference is the builtin
`risk_score_policy` (`omnigent/policies/builtins/risk_score.py`, documented at
`docs/POLICIES.md:345`), which accrues an author-defined, non-fungible "risk score" across the
path and gates on it. The accrual is a persisted `session_state` increment
(`risk_score.py:240`, `_increment` → `{"action": "increment"}`), driven by per-tool points and
per-result sensitivity labels (`risk_score.py:292`, `risk_score.py:319`), and the gate
escalates configured tools from ALLOW to ASK/DENY once the accumulated score crosses a
threshold (`risk_score.py:276`):

```python
if _is_guarded(raw_tool, cfg.guarded_tools):
    score = _current_score(event, cfg)
    if score >= cfg.threshold:
        return cast(PolicyResponse, {
            "result": cfg.escalate_action,            # "ASK" or "DENY"
            "reason": f"{cfg.reason} Session risk score {score} ≥ threshold "
                      f"{cfg.threshold}; {raw_tool} requires review.",
        })
points = _points_for_tool(raw_tool, cfg.tool_points)
if points > 0:
    return _increment(cfg.state_key, points)          # persisted, cross-turn
```

Relabel `tool_points` as irreversibility weights, `guarded_tools` as the irreversible actions,
and `threshold` as the path budget, and this *is* a path-level irreversibility budget —
configurable in YAML, no Python required. Combined with `cost_budget`'s "DENY the pending
action while over the limit" pattern, every primitive a true irreversibility budget needs is
shipped. This rules out **Branch A** decisively (handlers see far more than a fungible scalar:
persisted arbitrary state, `append`/`increment`, the pending action's args) and rules out
**Branch B** as the framing (the mechanism isn't merely *expressible by a custom handler* — it
is *present as a builtin* and documented).

Per the plan, Branch C means the loud "they can only do per-step fungible scalars / cannot
express a path-level irreversibility budget" track **stops**. Any surviving contribution must
pivot to the genuinely-absent residual, all three of which the code confirms are missing:

1. **Airlock / two-phase-commit with compensation.** The policy layer is a synchronous
   `ALLOW`/`ASK`/`DENY` gate per action (`PolicyAction`, `spec/types.py:1081`). There is no
   construct to stage reversible steps, commit them atomically at a boundary, or roll
   back/compensate on abort. A budget can block the step that would tip it; it cannot make a
   sequence transactional.
2. **Irreversibility as a typed, first-class unit.** Today it is an opaque integer the author
   defines and maintains. The runtime understands "labels" (monotonic ordinals) and "usage"
   (priced tokens) as first-class, but not an irreversibility quantity with its own semantics.
3. **Path scope across a spawn tree for custom accumulators.** Tree-wide aggregation is
   hardcoded for usage/cost; a custom irreversibility accumulator would be per-conversation
   unless it reimplements the reserved-key root-routing.

**Recommendation for the plan:** the thesis line ("evaluates per-step over fungible scalars and
cannot express a path-level irreversibility budget") is false and should be removed. If the
loud track is to continue at all, it must be re-scoped to (1) airlock/transactional-commit
semantics and (2) irreversibility-as-a-typed-unit — narrower claims that the evidence does
*not* refute, but that are materially smaller than the original move.
