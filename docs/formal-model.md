# Formal Model

## Read/Write Boundary

### Definitions

- **Read action (R):** An operation that observes state without modifying it. Examples: `read_email`, `list_inbox`, `search_inbox`.
- **Write action (W):** An operation that modifies external state. Examples: `send_email`, `reply_all`, `schedule_meeting`, `delete_email`.
- **Per-action irreversibility (I):** A function `I: W → [0, 1]` mapping each write action to its stand-alone irreversibility. `I(w) = 0` is fully reversible; `I(w) = 1` is fully irreversible at the moment of execution.

### Architecture

The naive agent operates as:

```
input → [reason + act] → output
         (single chain)
```

The airlock agent separates this:

```
input → [Read Path] → [Staging Area] → [Write Path] → output
         observe         propose          gate + execute
         reason          draft
```

### Invariants

1. **Read path cannot execute write actions.** The read path has no access to write tools. It can only propose actions via the staging area.
2. **All write actions pass through the irreversibility gate.** No write action bypasses the trust-budget check.
3. **Budget is monotonically decreasing within a session.** Actions can only deduct from the budget, never add to it.

---

## Path Irreversibility

The per-action irreversibility score `I(w)` is necessary but not sufficient for agent safety. The fundamental claim of this work is that irreversibility composes along a path in ways the per-action score cannot capture.

### Definitions

- **Path:** A sequence of actions `π = (a₁, a₂, …, aₙ)` taken by the agent within a session.
- **World state:** `W` is the externally-observable state at a given moment. Each action transitions it: `W_{t+1} = step(W_t, aₜ)`.
- **Path irreversibility (I*):** The cost — in time, attention, social capital, or external state changes — to return the world to `W₀` after walking `π`. Formally, `I*: Π × W → [0, 1]`, where `Π` is the space of paths.

### The Composition Claim

> For a path `π = (a₁, …, aₙ)` in which every individual action is two-way (`I(aᵢ) < 1`), the path irreversibility `I*(π, W₀)` can equal 1.

A series of two-way doors can compose into a one-way door.

**Mechanism.** Each action `aᵢ` changes the world state from `W_{i-1}` to `Wᵢ`. The reversibility of `aᵢ` was evaluated against `W_{i-1}`. Reversal at time `n` requires reverting from `Wₙ` to `W_{i-1}`, which is a different operation than reversing `aᵢ` at the moment it was taken. In particular, if `a_{i+1}, …, aₙ` condition on `Wᵢ` (which they often do — that's what makes them coherent actions), then reversing `aᵢ` requires reversing all of them as well, often in an order that is not feasible.

**Concrete example.** `a₁` = "send email to Alice describing plan X." Reversible at time 1: send a follow-up retraction. `a₂` = "send email to Bob asking him to coordinate with Alice on plan X." Reversible at time 2: same. By time 2, however, reversing `a₁` requires also retracting `a₂` to Bob, then explaining to Alice why a coordinator was assigned and then unassigned, then absorbing the cost to professional credibility. `I(a₁) = 0.9, I(a₂) = 0.9`, but `I*((a₁, a₂)) = 1`.

### The Visibility Asymmetry

The model evaluates `aₜ` given `W_{t-1}` and the prompt. It cannot, by construction, compute `I*(π, W₀)` because:

1. `π` includes future actions not yet decided.
2. `W₀` is not in the model's input — only the current `W_{t-1}` and recent action context.
3. `I*` depends on counterfactual reversal trajectories, which are not in any forward pass.

Therefore: **per-call alignment is structurally incapable of evaluating path irreversibility**, regardless of model capability. This is not a model-quality argument; it is a model-input argument.

### Composition Modes

`I*(π, W₀) = 1` can arise from any of four mechanisms (see [failure-catalog.md](failure-catalog.md) for cases):

1. **Quantity:** `n` is large enough that retracing all `n` actions is infeasible regardless of individual `I(aᵢ)`.
2. **Premise:** Some `aᵢ` is correct given a premise that turns out to be wrong; subsequent actions condition on the wrong premise; reversal requires identifying which premise broke.
3. **Classification:** The model assigns `aᵢ` an incorrect `I(aᵢ)` (treats a one-way door as two-way), so `aᵢ` is taken under false reversibility assumptions.
4. **Iteration:** A locally-reversible loop exits the recoverable region of state space because each iteration moves the world.

---

## Trust Budget Framework

The trust budget is a deliberately conservative approximation of the path integral of irreversibility.

### Parameters

- `B₀`: Initial trust budget per session.
- `Bₜ`: Remaining budget at step t.
- `I(aₜ)`: Per-action irreversibility score.

### Rules

1. **Auto-approve:** If `I(aₜ) ≤ Bₜ`, the action executes and `B_{t+1} = Bₜ - I(aₜ)`.
2. **Checkpoint:** If `I(aₜ) > Bₜ`, a human checkpoint is triggered.
3. **Reset:** `B₀` resets at session boundary.

### Why this approximates path irreversibility

The sum `Σ I(aᵢ)` is not equal to `I*(π)`, but it is a *lower bound on a useful proxy*: if individual actions are independently irreversible, the sum captures their cumulative cost. When actions are not independent (which is the interesting case), `Σ I(aᵢ) < I*(π)`, meaning the budget *under*-estimates path irreversibility — making it a conservative gate. The budget will trigger checkpoints before path irreversibility is fully reached, which is the correct error direction.

### Properties

- Read-only actions have `I = 0` and are free.
- A fresh session can auto-approve `⌊B₀ / I_min_write⌋` write actions before checkpointing.
- For default parameters (`B₀ = 3.0`, `I_min_write = 0.1` for draft), the cap is 30 drafts or roughly 3 sends.

### Calibration note

The original parameters (`B₀ = 3.0`, `send_email I = 0.9`, `reply_all I = 1.0`) were tuned for a per-action threat model: gate single dangerous actions. Under the path-irreversibility framing, the calibration target is different: the budget should trigger at the action-count where path-level harm typically composes, which the eval will determine empirically. Expected adjustments include lowering `send_email` toward 0.6–0.7 (so 4–5 sends auto-approve, 5th–6th gates) and adding blast-radius weighting to actions whose `I` should scale with recipient count.

---

## Theorem (informal, door composition)

> For any path `π = (a₁, …, aₙ)` with `n ≥ 2` and `I(aᵢ) < 1` for all `i`, there exist world states `W₀` and action sequences `π` such that `I*(π, W₀) = 1`.

**Sketch.** Construct `π` so that `aⱼ` for `j > 1` conditions on the state change caused by `a₁`. Specifically, let `a₂` reference content delivered by `a₁`, `a₃` reference content delivered by `a₂`, and so on. After step 2, reversing `a₁` requires also reversing `a₂` (else `a₂` is incoherent); after step 3, reversing `a₂` requires reversing `a₃`; etc. The reversal cost grows with `n`, and at sufficient `n` the cost exceeds any practical threshold — in the limit, `I*(π) → 1` even when each `I(aᵢ)` remains bounded below 1. This corresponds to composition mode 1 (quantity). Analogous constructions exist for modes 2 (premise), 3 (classification), and 4 (iteration).

A formal proof is out of scope; the empirical demonstration is the paper's contribution.
