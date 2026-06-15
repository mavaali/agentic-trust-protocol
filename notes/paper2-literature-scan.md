# Paper 2 — Literature Scan: the compensation-gap claim

**Compiled:** 2026-06-14
**Target claim under test** (`docs/paper2_outline.md:50`): *"Compensating transactions in agent literature: largely absent. (We position this as the gap we're filling.)"*
**Method:** deep-research harness — 5 search angles, 16 sources fetched, 70 falsifiable claims extracted, top 25 adversarially verified (3-vote, 2/3-to-kill); 24 confirmed, 1 killed. Date range 2024–June 2026.
**Provenance / audit trail:** deep-research workflow run `wf_4f7993b9-2f9` (task `wz3szvdgl`), this session. Full per-agent transcripts, the verified-claim ledger, and source URLs/quotes are in the workflow output at `.../tasks/wz3szvdgl.output` and the subagent transcript dir `.../subagents/workflows/wf_4f7993b9-2f9`. Every [DATA] item below traces to a primary URL in §5/the ledger; **none of these citations has been independently confirmed by a human yet** — see follow-up #1. This memo is a research finding, not a verified bibliography.
**Label key:** [DATA] = primary-sourced and verified by the harness's 3-vote check in this scan (not human-confirmed); [HYPOTHESIS] = inference with kill condition; [TRAINING] = general background knowledge.

---

## 1. Headline verdict — **REFUTED**

The claim does not hold as of June 2026. **Do not soften this.** At least three named, primary-sourced frameworks now apply *saga-pattern semantic compensation directly to LLM agents*, and a fourth provides transactional checkpoint+undo for agent tool-use:

- **SagaLLM** (Chang & Geng, Stanford; VLDB 2025) [DATA]
- **RAC — Robust Agent Compensation** (Perera, Hapuarachchi, **Leymann**, Khalaf; CAIS 2026) [DATA]
- **Atomix** (Mohammadi et al.; ICLR 2026 workshop) [DATA]
- **STRATUS** (Chen et al., IBM+UIUC; NeurIPS 2025) [DATA] — adjacent (exact-state undo, not semantic compensation)

SagaLLM and RAC explicitly cite Garcia-Molina & Salem (1987) and implement automated compensation, LIFO / reverse-dependency-order rollback, and compensable execution for LLM agents. RAC is co-authored by **Frank Leymann** — himself a seminal workflow-compensation figure — so the DB/workflow anchor Paper 2 planned to extend *has already been extended to LLM agents by the people who wrote the anchor.* The sentence at `:50` cannot survive in its current form, and the framing in the Conceptual Frame (`:15`, *"It has not been seriously developed for LLM agents"*) and pushback #1 (`:133`) are now false as written.

**The contribution must be re-scoped before drafting.** What remains genuinely open is narrower and still defensible (§4 below), but the blanket absence claim is dead.

The single biggest surprise: **SagaLLM is dated March 2025 (VLDB vol. 18)** — it predates the model knowledge cutoff and predates the outline's most recent edits. This was findable months ago; the gap claim was already false when written.

---

## 2. Method

Five angles: exact-construct primary, venue-scoped academic, adjacent near-neighbor mechanisms, deployed practitioner harnesses, contrarian/anchor-verification. 16 sources fetched (12 primary papers, 1 secondary AWS guidance, 3 blogs). 70 claims extracted; the 25 highest-signal verified by 3 independent adversarial voters each. Evidence that counts: primary papers (arXiv/venue PDFs, abstracts, algorithm listings, limitations sections), cross-citation between the works themselves, and one corroborating IBM Research blog. Marketing/blog claims were down-weighted and not used as load-bearing evidence. One fetch artifact noted (arXiv:2603.03515's `/pdf` endpoint returned bytes from a different paper; the HTML render confirmed correct content, so conclusions unaffected).

---

## 3. What's NEW since the outline was written

### OVERLAP — existential threats to the contribution as currently framed

**SagaLLM** — Chang & Geng (Stanford). arXiv:2503.11951 (Mar 2025); *Proc. VLDB Endowment* 18(12):4874–4886; DOI 10.14778/3750601.3750611. [DATA]
*"Integrating the Saga transactional pattern with persistent memory, automated compensation, and independent validation agents"* for multi-agent LLM planning; *"workflow-wide consistency and recovery through modular checkpointing and compensable execution"*; explicitly *"relaxes strict ACID guarantees."* Algorithm 1 auto-generates compensation agents; compensations are stacked and rolled back in LIFO / reverse-dependency order (cancel reservation → release seat → refund). **Classification: OVERLAP.** This is the closest prior art and it is peer-reviewed at a top DB venue. *Implication:* the saga-for-LLM-agents move is taken. Paper 2 cannot claim to introduce it.

**RAC — Robust Agent Compensation** — Perera, Hapuarachchi (WSO2), Leymann (Univ. Stuttgart), Khalaf (WSO2). arXiv:2605.03409v2 (May 2026); accepted CAIS 2026 (ACM Conf. on AI and Agentic Systems); DOI 10.1145/3786335.3813141. [DATA]
A log-based saga framework deployable as an architectural extension over existing agent frameworks (*works on LangGraph agents without code change*). A Tool Interceptor records each call in a persistent **Transaction Log**; on failure a Recovery & Compensation Manager rebuilds the execution graph, topologically reverses it, and invokes compensation tools (sourced from framework APIs, MCP annotations, or LLM inference). Cites Garcia-Molina & Salem (1987), Leymann (1995), Khalaf et al. (2009). Evaluated on τ-bench/τ²-bench and REALM-Bench; **benchmarks head-to-head against SagaLLM** and claims 1.5–8× latency/token economy over LLM-based recovery. **Classification: OVERLAP** — and it occupies precisely the "registry + compensation-log + reverse-LIFO compensate" architecture that Paper 2 §5 specifies. *Implication:* Paper 2's proposed architecture (`outline:81–85`) is substantially pre-empted, including the LangGraph deployment story.

**Atomix** — Mohammadi, Potamitis, Klein, Arora, Bindschaedler. arXiv:2602.14849 (Feb 2026); ICLR 2026 AIWILD workshop. [DATA]
A transactional (atomicity-style) runtime for LLM-agent tool calls. **Classifies tool effects by reversibility — bufferable / reversible-external / irreversible — and handles each differently at commit**; on abort it *"replays Saga-style compensations in reverse dependency order"* for externalized reversible effects, gates irreversible ones. Explicitly *"adapts Sagas, Try-Confirm-Cancel, and streaming watermarks to the LLM tool interface."* **Classification: OVERLAP** on both the compensation mechanism *and* the compensability taxonomy Paper 2 §4 proposes (three-way reversibility classes). *Implication:* the taxonomy contribution (`outline:63–79`) is also partly pre-empted. *Caveat:* workshop (not main-conference); compensation is best-effort ("where possible").

### ADJACENT — cite as related work; do not threaten the (narrowed) gap

**STRATUS** — Chen et al. (IBM + UIUC). arXiv:2506.02009; NeurIPS 2025 (poster). [DATA]
Formalizes **Transactional No-Regression (TNR)**: checkpoint → execute → commit-if-improving-else-abort, with a stack-based **faithful undo** operator `U(s_post)=s_pre` for cloud-ops/SRE agents; converts irreversible actions (file-delete → move-to-backup) or rejects them. **Crucially, its Limitations section states operations needing *"more sophisticated compensation logic not covered by a simple U(s_post)=s_pre"* are delegated to external state-reconciliation operators** — i.e. STRATUS itself does *not* implement semantic compensation and explicitly flags that as out of its scope. **Classification: ADJACENT** (exact-state undo ≠ semantic compensation), but OVERLAP for the narrower "transactional undo for LLM agents." *Implication:* STRATUS is both a citation and a gift — it draws the exact-state-undo / semantic-compensation line for you in print.

**AgentSpec** (Wang, Poskitt, Sun; ICSE 2026), **"Towards Verifiably Safe Tool Use"** (Doshi et al.; ICSE-NIER 2026, arXiv:2601.08012), **Irreversibility Budget / "The Controllability Trap"** (Sahoo; arXiv:2603.03515, ICLR 2026 workshop). [DATA]
All three enforce safety *before* execution — pre-action interception, HITL confirmation, self-reflection, abort/substitution, or cumulative-irreversibility budget-throttling (`IC(t)=Σ ι(a_j)`, pause for re-authorization when `IC(t)≥IB`). **None compensates, rolls back, or repairs a committed action.** **Classification: ADJACENT (prevention).** The Irreversibility-Budget paper is notable: it independently uses a per-action irreversibility score `ι:A→[0,1]` and a cumulative budget — close to the v1 trust-budget idea — but anchored in RL safe-exploration (García & Fernández 2015), *not* compensation. *Implication:* the per-call irreversibility-classification idea is also now in the air, though not composed into path-level safety (see §4).

### ORTHOGONAL — footnote at most

**"Learning to Undo: Rollback-Augmented RL with Reversibility Signals"** (Sorstkins, Tariq & Bilal; arXiv:2510.14503, Oct 2025). [DATA] Value-based RL with simulator state-reset during TD training, tabular benchmarks only (CliffWalking, Taxi). Shares the "rollback/reversibility" vocabulary but is not an LLM agent and not semantic compensation. **ORTHOGONAL.**

---

## 4. What's STILL absent (the survivable wedge)

The blanket claim is refuted, but three specific shapes remain open [DATA from the works' own limitations sections; [HYPOTHESIS] on what that leaves Paper 2]:

1. **Failure-stress-tested empirical validation of compensation.** SagaLLM's compensators are *designed and LLM-generated but never failure-injected* — it reports no compensation success-rate or recovery-time metrics. None of the OVERLAP works deliberately triggers aborts to measure whether compensation actually recovers harm. *This is the strongest remaining novelty wedge:* Paper 2's R1/R2/R3 (`outline:92–96`) with N≥10 and recovery-rate/time-to-recovery metrics would be the first failure-stress evaluation — **if** they produce a clean signal (note the circularity risk already flagged in state-of-play Risk B). [HYPOTHESIS — kill condition: a 2026 paper exists with injected-abort compensation-success metrics; not found in this scan.]

2. **Time-decay of compensation effectiveness as a door-composition phenomenon.** No surveyed work models `C(σ, Wₙ)` as a *decaying-with-time* effectiveness function, nor treats compensating actions as themselves doors that narrow over time (`outline:55–61`). SagaLLM/RAC/Atomix treat compensation as roughly binary (a compensator exists and fires, or doesn't). **The time-decay-as-door-composition treatment is the cleanest surviving conceptual contribution.** [HYPOTHESIS — kill condition: any of the four model effectiveness as time-dependent; checked, none do.]

3. **Per-call irreversibility *classification* composed into architecture-level *path* safety.** The Irreversibility-Budget paper and Atomix taxonomy classify per-action reversibility; none composes it into the "series of two-way doors → one-way door" path thesis. The composition is still unclaimed. [HYPOTHESIS — kill condition: a path-level composition over per-call reversibility appears; not found.]

**Seminal-but-orthogonal anchors remain correct** [DATA]: Garcia-Molina & Salem 1987 (Sagas), Leymann 1995 (workflow compensation), Weikum & Vossen 2001 (TIS), Richardson 2018 (microservices), Lynch & Merritt. No third party extends Weikum/Richardson/Lynch *directly* to LLM agents except through SagaLLM and RAC. CaMeL (arXiv:2503.18813) confirmed prevention-via-capability-control-flow, not compensation. SafetyDrift confirmed detect-not-compensate.

---

## 5. Recommended citation set for Paper 2 §2

Drop-in bibliography with one-line annotations. The §2 narrative must change from *"largely absent"* to *"an emerging cluster (2025–26) that Paper 2 sharpens past."*

**The new must-cite cluster (the works that refute the old framing — engage head-on):**
- `chang2025sagallm` — SagaLLM (VLDB 2025). *First saga+compensation for multi-agent LLM planning; the closest prior art. Paper 2 must distinguish on time-decay + failure-stress eval.*
- `perera2026rac` — RAC (CAIS 2026, Leymann co-author). *Log-based saga compensation deployable over LangGraph; pre-empts Paper 2's §5 architecture. Cite and differentiate.*
- `mohammadi2026atomix` — Atomix (ICLR 2026 wksp). *Reversibility-classed transactional tool-call runtime; overlaps Paper 2's taxonomy. Cite as concurrent.*
- `chen2025stratus` — STRATUS (NeurIPS 2025). *Transactional exact-state undo for cloud-ops agents; explicitly flags semantic compensation as out-of-scope — use to draw the undo-vs-compensation line.*

**Prevention-side neighbors (the "before the gate" contrast):**
- `sahoo2026irreversibility` — Irreversibility Budget / Controllability Trap. *Per-action irreversibility score + cumulative budget, RL-anchored; closest independent echo of the v1 trust budget. Important to cite to pre-empt "you missed it."*
- `wang2026agentspec` — AgentSpec (ICSE 2026). *Pre-execution runtime enforcement; prevention foil.*
- `doshi2026verifiablysafe` — Towards Verifiably Safe Tool Use (ICSE-NIER 2026). *Capability-enhanced MCP gating; prevention foil.*
- (retain) CaMeL `debenedetti2025camel`, SafetyDrift `dhodapkar2026safetydrift` — already in the map; still correct as prevention / detection foils.

**Seminal anchors (retain exactly as mapped — still the origin, now reached *through* SagaLLM/RAC):**
- `garcia1987sagas`, `leymann1995`, `weikum2001tis` (add to bib), `richardson2018` (add to bib), `lynch1988`.

---

## 6. Open follow-ups (for Mihir to chase)

1. **Verify the post-cutoff papers personally.** RAC (May 2026) and Atomix (Feb 2026) postdate the model knowledge cutoff and were confirmed only via web fetch + 3-vote adversarial check. SagaLLM (VLDB) and STRATUS (NeurIPS) are pre-cutoff and lower-risk. **Pull the RAC and Atomix PDFs and confirm the saga/compensation claims firsthand before they go in the bib** — the entire re-scope hinges on them, and the verdict is REFUTED on SagaLLM alone regardless.
2. **DOIs / venue confirmation.** Confirm RAC's `10.1145/3786335.3813141` and CAIS 2026 acceptance; confirm Atomix's ICLR 2026 AIWILD workshop listing (workshop, not main track — weight accordingly).
3. **Deployed-harness check (unresolved).** No confirmation that Omnigent, AutoGen, LangGraph, or Semantic Kernel has shipped a *first-class* compensation primitive (vs. RAC's research-prototype extension). If one has post-June-2026, follow-up #1's wedge narrows further. Worth a targeted re-check before submission.
4. **Workflow-engine bridge.** No direct Temporal/Camunda/BPMN→LLM-agent compensation integration paper surfaced (RAC carries the BPEL/workflow lineage via Leymann). If Paper 2 leans on the workflow-engine analogy, confirm nobody has published the direct bridge.
5. **RAC's 1.5–8× claim is unreproduced** — authors' own benchmark. Do not cite the number as established.

---

## Bottom line

The novelty claim as written is dead. The paper is **not** dead — but it must pivot from *"compensation for agents doesn't exist"* to *"compensation for agents has just emerged (SagaLLM, RAC, Atomix), and none of it (a) models compensation effectiveness as time-decaying, (b) composes per-call reversibility into path-level safety, or (c) failure-stress-tests recovery empirically."* That is a thinner, sharper, and still-defensible wedge — but it requires rewriting §1, §2, §4, §5, and pushback #1 before any drafting. Land §3 (the time-decay theory) first; it is the one contribution no surveyed work touches.
