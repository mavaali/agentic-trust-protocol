# Formal Model

## Read/Write Boundary

### Definitions

- **Read action (R):** An operation that observes state without modifying it. Examples: `read_email`, `list_inbox`, `search_inbox`.
- **Write action (W):** An operation that modifies external state. Examples: `send_email`, `reply_all`, `schedule_meeting`.
- **Irreversibility score (I):** A function `I: W → [0, 1]` mapping write actions to their irreversibility. `I(w) = 0` means fully reversible; `I(w) = 1` means fully irreversible.

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
2. **All write actions pass through the irreversibility gate.** No write action bypasses the trust budget check.
3. **Budget is monotonically decreasing within a session.** Actions can only deduct from the budget, never add to it.

## Trust Budget Framework

### Parameters

- `B₀`: Initial trust budget (default: 3.0)
- `Bₜ`: Remaining budget at time t
- `I(wₜ)`: Irreversibility score of action wₜ

### Rules

1. **Auto-approve:** If `I(wₜ) ≤ Bₜ`, the action executes and `Bₜ₊₁ = Bₜ - I(wₜ)`
2. **Checkpoint:** If `I(wₜ) > Bₜ`, a human checkpoint is triggered
3. **Reset:** `B₀` resets at session boundary

### Properties

- Low-risk actions (drafts, reads) have `I ≈ 0` and are effectively free
- A fresh session can auto-approve ~3 medium-risk actions before checkpointing
- A single `reply_all` (`I = 1.0`) consumes 1/3 of the budget
- Two `send_email` actions (`I = 0.9` each) consume `1.8` of `3.0`, leaving room for one more medium-risk action

### Theorem (informal)

> An airlock agent with trust budget B₀ cannot execute more than ⌊B₀ / I_min_write⌋ write actions without human approval, where I_min_write is the minimum irreversibility score of any write action.

For default parameters (B₀ = 3.0, I_min_write = 0.1 for draft), this means at most 30 drafts or 3 sends before checkpoint.
