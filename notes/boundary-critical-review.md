# Boundary — critical repo review

**Repo:** github.com/mavaali/boundary
**Commit reviewed:** `05665d58bb98c1921df26cbd11c284a47528e58d` (0.5.0, "feat(scheduler): cross-platform headless scheduling")
**Date:** 2026-06-20
**Method:** code as primary source; README/GUIDE as claims to verify. Citations are `file:line` from the pinned checkout. Labels: `[DATA]` = read from code, `[HYPOTHESIS]` = inference + kill condition, `[TRAINING]` = general best practice.

---

## Headline

No exploitable vulnerability. The workspace jail is sound, YAML is safe-loaded, subprocess is list-form, and the sandbox/commit gates do what the README says — unusually solid for a six-day-old repo. The real problem is **honesty drift in three load-bearing claims**: the Third Umpire *does* grade prose (it checks for the literal string `[DATA]` in the final message), the taint gate fires only on `fetch_url` and silently resets at every pipeline-stage boundary, and the headline "staging pivot — resume from stage" is a sticky flag plus a prompt, not a state-restore primitive.

**CRITICAL (exploitable):** none found. No injection primitive, no jail escape, no unsafe deserialization.

---

## Top issues (ranked)

### 1. Taint detection is narrower than "any subsequent write" — and resets per pipeline stage  `[DATA]`
Taint is set in exactly one place: `envelope.py:453-462`, inside `if base.kind == "external"`. The only `external`-kind tool is `fetch_url` (`web.py:23`). `read_file` is workspace-jailed (`workspace.py:20`), so it **cannot** read outside the workspace — which makes the "outside-workspace" half of the taint comment dead:

> `envelope.py:124-126`: "When the run has read untrusted external content (fetch_url / outside-workspace), a subsequent write is a potential exfil channel."

Worse, the pipeline runs each stage as a fresh `run_headless` → fresh `Envelope` → fresh counters (`pipeline.py:200-204`, `headless.py:257-272`), and `tainted_reads` lives in those per-run counters (`envelope.py:606`). So taint resets every stage, and **all stages share one workspace** (`pipeline.py:200`, `config.workspace`).

**Cost:** the canonical lethal-trifecta path is invisible to the gate. Stage 1 `fetch_url`s untrusted bytes and writes them into the shared workspace; stage 2 `read_file`s them (untainted — workspace read) and commits/exfils. Zero `taint_flow` events, clean Third Umpire report. Single-stage bypass also exists: `bash: python3 -c "import urllib.request; ..."` fetches untrusted content with no taint (bash never taints; `curl` is denylisted but `python` isn't).

**Suggestion:** carry a taint marker across stages (e.g. a `.boundary/taint` file in the workspace) and taint reads of provenance-tracked files. Until then, correct the README/GUIDE/comment to read "fetch_url only, single-stage" — this is the headline safety story and the gap is currently unstated.

### 2. README overstates the Third Umpire as "not prose grading"  `[DATA]`
> README: "Third Umpire: property checks against the envelope spec, not against the agent's prose quality."

Three of fourteen checks grade the final **message text**, not the envelope:
- Check 5 (`third_umpire.py:211-219`) passes iff `"[DATA]" in final_text` — pure prose-format grading.
- Check 4 "grounding" (`third_umpire.py:189-209`) regex-extracts numbers from the final and substring-tests them against the concatenated tool blob; a `2` or `4.5` anywhere in any tool result satisfies any `2`/`4.5` in the final (`ungrounded <= 1` tolerance).
- Check 3 (`third_umpire.py:161-187`) matches `INTERPOLATION_PHRASES` against final text.

The `fail`-severity checks (1, 2, 6, 6.5, 12 — allowlist, reason, produced-output, staging order, commit-policy) **are** genuine envelope-property checks on logged events. The prose checks are `warn`/`info`. **Cost:** the differentiation vs Cupcake ("the Third Umpire grades whether the envelope held") is weakened — it also grades message hygiene. **Suggestion:** relabel as "structural envelope checks (fail) + heuristic output-hygiene checks (warn)," or drop Check 5 to `info`.

### 3. "Staging pivot — resume from stage" is a sticky flag + prompt, not state machinery  `[HYPOTHESIS]`
`stage_proposal` sets `counters["staged"] = 1` and logs an event carrying a thesis summary (`envelope.py:508-517`). It stores **no reloadable artifact.** On write refusal the tool returns an `ENVELOPE REFUSED` string (e.g. `envelope.py:316-320`); "resume from the staged thesis instead of restarting research" happens only because (a) the conversation messages persist and (b) the refusal *text* says "revise from the same staged proposal" (`envelope.py:240-243`). No code re-injects the staged thesis/evidence on refusal.

The **gate** (must stage before write/commit/bash) is real, enforced (`envelope.py:233-243`), and tested. The **resume** is emergent from the persistent message thread + a one-bit flag.

**Kill condition:** if there were code that, on `write_refused`, re-injected the `stage_proposal` payload into `messages`, the claim would be literal. There isn't — the payload is only logged, never re-read (grep confirms `stage_proposal` output is consumed by the model as a tool result and never persisted/reloaded). **Suggestion:** either build the resume (persist staged proposal, re-inject on refusal) or soften to "the staging gate persists, so a refused write resumes against the existing thesis and reads."

### 4. `--egress-allow` is a silent no-op under the default driver  `[DATA]`
`_srt_settings` (`sandbox.py:115-124`) is the only consumer of `egress_allowlist`; `seatbelt` and `none` ignore it (`sandbox.py:59-65`). `cli.py` passes it through regardless of driver. A user running default `seatbelt` with `--egress-allow api.internal` gets **no egress enforcement and no warning** — false sense of containment exactly where it matters. **Suggestion:** warn (or refuse) when `egress_allowlist` is non-empty and `driver != "srt"`.

### 5. `ThirdUmpire.grade(envelope=...)` parameter is dead  `[DATA]`
`third_umpire.py:104` accepts `envelope: Envelope | None`, and the module docstring (`third_umpire.py:8`) shows it used — but the 315-line body never reads it; everything is re-derived from the transcript's `envelope_start`/`envelope_end` events. **Cost:** a contributor wires logic to the param expecting it to matter; also a missed chance to cross-check logged-vs-declared spec (transcript-tamper detection). **Suggestion:** delete the param, or use it to validate the logged spec against the live `Envelope`.

---

## What's done well

- **Workspace jail is correct.** `workspace.py:13-25`: `.resolve()` collapses `../` and follows symlinks, then `relative_to(self.root)` raises `PermissionError` on escape. The fnmatch allowlist (`envelope.py:160-168`) doesn't normalize, but the real jail backs it — so the lack of normalization is **not** exploitable for escape.
- **Security hygiene is clean.** All YAML is `safe_load` (`schedule.py:51`, `overlay.py:24`, `pipeline.py:102`); no `eval`/`exec`/`pickle`/`shell=True`/`os.system`; subprocess is list-form argv (`sandbox.py:97-99,139-141`).
- **Honesty is high where it counts.** The seatbelt-egress gap and the write-as-exfil gap are stated repeatedly and routed to `srt` (README:38-39, 74-76; GUIDE:597, 705-706, 713-724, 626-653). The denylist is explicitly "a nudge, not containment."
- **Clean acyclic layering.** The `Envelope` spec is a single serializable dataclass (`envelope.py:86-168`); the runner core (`agent.py`/`loop.py`) imports neither `envelope` nor `third_umpire`.
- **Tests assert real behavior on the enforcement-critical paths.** Write boundary, commit kill-list, single-stage taint, staging gate, and downgrade tags all carry genuine assertions through a shared `selftest.py` core that also backs CI (`test_envelope_writes.py` 44 asserts, `test_commit_killlist.py` 56 incl. a 20-row denylist table).

---

## Smaller findings

- fnmatch `*` matches `/`: `--envelope-writable 'docs/*'` also allows `docs/a/b/c` (`envelope.py:166`). Surprising vs glob; document it or switch to `PurePath.match`. `[DATA]`
- `fielding-coach` (shell-on-by-default mode) exposes none of `run`'s `--sandbox-driver` / `--egress-allow` / `--on-taint` / `--envelope-*` flags (`cli.py:54-66`) — the riskiest mode has the thinnest CLI controls. `[DATA]`
- Bash denylist bypassable via `env curl`, `\curl`, `command curl`, pipes (`echo x && curl …`), `python -c` (`envelope.py:57-83`). Documented as bypassable; reinforces "don't trust default seatbelt for egress." `[DATA]`
- "Plan-Then-Execute" gates write/commit/bash but **not** `fetch_url` (`envelope.py:233-237` lists write/commit/bash only) — untrusted network reads happen before any plan. `[DATA]`
- CI tests only Python 3.12 despite `requires-python >= 3.10` + 3.10/3.11 classifiers (`selftest.yml`; `pyproject.toml:5,11-20`). No lint/type-check job. No lockfile; deps floating `>=` with no upper cap (`pyproject.toml:21-25`). `[DATA]`
- `pydantic>=2.0` is a hard dependency, but core models are stdlib dataclasses — verify it's actually used or drop it. `[HYPOTHESIS]`; kill: `rg pydantic boundary/` finds a real import.
- No `py.typed` despite typed source; no SPDX headers (LICENSE present, MIT). `[DATA]` / `[TRAINING]`
- CHANGELOG is real (Keep-a-Changelog) but 0.2.0–0.5.0 all share date 2026-06-16 (squashed); 0.1.0 undated. `[DATA]`
- Missing-`srt` returns a clear ERROR string (`sandbox.py:129-133`) but no test asserts it — srt tests `skipif(not SRT_AVAILABLE)`, so the fallback path is untested in CI on machines without srt. `[DATA]`
- Low-sev TOCTOU `[TRAINING]`: path is resolved (`workspace.py`) then re-opened in `write_text`; a local FS attacker swapping a parent dir to a symlink in that window could escape. Outside the stated threat model (adversary is the agent/content, not a local user) — note, don't fix.

---

## Risk audit — README claim → verdict

| README claim | Verdict |
|---|---|
| staging pivot: stage mid-run, resume refused write from stage | **weakened** — gate real/enforced/tested; "resume" is sticky-flag + prompt, no state restore |
| Third Umpire: property checks vs envelope, not prose quality | **weakened** — 3/14 checks grade final-message text (`[DATA]` literal at `:212`) |
| taint gate: any subsequent write = potential exfil channel | **weakened** — fires only on `fetch_url`; resets per pipeline stage; bash/indirect content untainted |
| srt: OS-enforced egress allowlist over whole process tree | **verified** — delegated to srt correctly; empty allowlist = no network (fail-closed), `sandbox.py:127-141` |
| commit-tool gating + write allowlist, no traversal bypass | **verified** — typed commit gate `envelope.py:378-450`; jail catches `../`/symlink `workspace.py:20` |
| Plan-Then-Execute forces plan before irreversible action | **weakened** — gates write/commit/bash, not `fetch_url`; defeatable via `--no-staging-gate` |
| seatbelt does not bound egress (the named gap) | **verified** — `sandbox.py:8-9`; docs repeat |
| IFC for tainted allowlisted write = roadmap, not shipped | **verified** — genuinely absent (but taint *detection* gap above is additional + unnamed) |
| no exploitable security vulnerability | **verified** — no injection primitive, `safe_load`, list-form subprocess |

---

## Recommended next moves (ranked by leverage)

1. **Fix taint truthfulness.** Carry taint across pipeline stages + taint reads of provenance-tracked files; until then, change README/GUIDE/comment to "fetch_url only, single-stage." Highest leverage — it's the headline safety story and the gap is silent today.
2. **Split or soften the Third Umpire claim** and drop Check 5 (`[DATA]`-string) to `info`. The "not prose grading" line is contradicted by `"[DATA]" in final_text`.
3. **Add the `--egress-allow`-without-`srt` warning** (one guard in `cli.py` / `Agent.__init__`). Cheap; closes a silent foot-gun.
4. **Make staging "resume" real or reword it** — persist the staged proposal and re-inject on `write_refused`, or align the headline differentiator with the sticky-flag reality.
5. **CI hardening:** 3.10/3.11 matrix + a `ruff`/`mypy` job + a lockfile; delete the dead `envelope` param on `grade`.
