# Literature Map

Annotated bibliography organized by which piece of our contribution each line of work bears on. Each entry: citation, one-line summary, relationship to our framing.

This map drives Section 2 of the paper. Coverage matters here — for thought leadership in a crowded space, citation hygiene is what insulates the work from "you missed prior art" rejection.

---

## A. Path irreversibility and option value (economics, decision theory)

The mathematical content of door composition — that locally-reversible decisions can compose into globally-irreversible trajectories — is a known result in this literature.

- **Arrow & Fisher (1974), "Environmental Preservation, Uncertainty, and Irreversibility," QJE 88(2).** Original formalization of the irreversibility effect: option value of preserving reversibility under uncertainty is strictly positive when learning is non-trivial. *Relationship: provides the formal antecedent for our path-level claim. Cite extensively.*
- **Henry (1974), "Investment Decisions Under Uncertainty: The Irreversibility Effect," AER 64(6).** Companion result. *Cite alongside Arrow-Fisher.*
- **Hanemann (1989), "Information and the Concept of Option Value," JEEM 16(1).** Quasi-option value: max{E[R*] − E[R], 0}. *Cite for the formal expression.*
- **Dixit & Pindyck (1994), Investment under Uncertainty, Princeton.** Real options theory. Bellman-equation formulation of continuation regions where waiting strictly dominates. *Cite as the canonical textbook treatment.*
- **Arthur (1989), "Competing Technologies, Increasing Returns, and Lock-In by Historical Events," Economic Journal 99(394).** Proves that under increasing returns, individually-free adoption choices converge almost surely to lock-in on one technology — the literal version of "locally reversible composes into globally irreversible." *This is the closest formal antecedent to our composition theorem. Cite as the math we are not re-proving.*
- **David (1985), "Clio and the Economics of QWERTY," AER P&P 75(2).** Path dependence in technology choice. *Cite for path-dependence framing.*

## B. Safe RL, side effects, and reversibility in sequential decision-making

Path-integral-of-irreversibility has been formalized for RL agents.

- **Krakovna, Orseau, Kumar, Martic, Legg (2018), "Penalizing Side Effects Using Stepwise Relative Reachability," arXiv:1806.01186.** Path-integrated reachability penalty: action's cost = how much it shrinks the set of reachable states relative to a baseline. *This is the closest prior art to our trust budget. Cite as the formal RL antecedent.*
- **Eysenbach, Gu, Ibarz, Levine (2017), "Leave No Trace: Learning to Reset for Safe and Autonomous Reinforcement Learning."** Trains a reset policy and refuses actions the reset policy can't undo — operational reversibility classifier in the loop. *Cite as operational antecedent for our irreversibility classifier.*
- **Grinsztajn, Ferret, Pietquin, Preux, Geist (2021), "There Is No Turning Back: A Self-Supervised Approach to Reversibility-Aware RL," NeurIPS.** Learns reversibility estimator from trajectories; uses it to gate exploration. *Cite as learned-classifier alternative to our hand-specified scores.*
- **Turner, Hadfield-Menell, Tadepalli (2020), "Conservative Agency via Attainable Utility Preservation," AAAI.** Penalizes loss of optionality. *Cite as adjacent.*
- **Armstrong & Levinstein (2017), "Low Impact Artificial Intelligences."** Earlier impact-measure work. *Brief mention.*
- **Moldovan & Abbeel (2012), "Safe Exploration in Markov Decision Processes," ICML.** Constrained MDPs with absorbing failure states. *Brief mention.*
- **Turchetta, Berkenkamp, Krause (2016), "Safe Exploration in Finite MDPs with Gaussian Processes," NeurIPS.** Adjacent; specifies "ergodic" actions. *Brief mention.*

## C. Distributed systems and compositional safety engineering

The compositional safety problem — locally-reversible operations composing into globally-irreversible trajectories — has been identified and addressed in distributed systems and CPS for decades.

- **Garcia-Molina & Salem (1987), "Sagas," SIGMOD.** Long-lived transactions composed of sub-transactions, each with a compensating action for partial reversal. Acknowledges that compensation is *semantic*, not state-restoring (you cannot un-send an email, only mail an apology). *Closest formal antecedent for compositional reversibility. Cite as the systems origin of the framework we apply.*
- **Lynch & Merritt (1986), "Introduction to the Theory of Nested Transactions."** Theoretical foundations for compensation-consistency. *Cite for the formal treatment.*
- **Weikum & Vossen (2001), Transactional Information Systems.** Comprehensive treatment of compensation-consistency. *Cite as canonical reference.*
- **Leveson (2011), Engineering a Safer World: Systems Thinking Applied to Safety.** STAMP framework — safety as emergent control property, not reducible to component reliability. *Cite as the systems-engineering antecedent for our visibility-asymmetry argument.*
- **Leveson (2004), "A New Accident Model for Engineering Safer Systems," Safety Science.** STAMP origin paper. *Cite alongside the book.*
- **Leveson & Thomas (2018), "STPA Handbook."** Methodology for systematic hazard analysis over action sequences. *Cite for methodological antecedent.*
- **Laprie (1985), "Dependable Computing and Fault Tolerance: Concepts and Terminology."** Foundational dependability vocabulary. *Brief mention.*
- **Avizienis, Laprie, Randell, Landwehr (2004), "Basic Concepts and Taxonomy of Dependable and Secure Computing."** Updated dependability taxonomy. *Brief mention.*
- **Richardson (2018), Microservices Patterns.** Saga pattern in modern engineering practice. *Cite for contemporary engineering relevance.*

## D. Agent foundations and corrigibility

Adjacent literature on cumulative-consequence bounds and the limits of optimization-time safety.

- **Soares, Fallenstein, Yudkowsky, Armstrong (2015), "Corrigibility."** Desiderata for shutdownability; proves no straightforward utility function satisfies them. *Cite for the broader limit-of-optimizer-safety argument.*
- **Hadfield-Menell, Dragan, Abbeel, Russell (2017), "The Off-Switch Game."** Uncertainty about reward makes the agent prefer deferring; per-decision result. *Cite as adjacent.*
- **Taylor (2016), "Quantilizers: A Safer Alternative to Maximizers for Limited Optimization."** Bounds expected catastrophic loss by sampling top-q of a base distribution. Cumulative-consequence argument operating *inside* the optimizer. *Cite as the closest objective-level analog to our trust budget; contrast: our mechanism is architectural, not in the objective.*
- **Bostrom (2014), Superintelligence.** Instrumental convergence. *Cite for the framing of why agents take irreversible actions.*

## E. LLM agent architectures and the Plan-then-Execute pattern

Architectural separation has been proposed for LLM agents under "Plan-then-Execute." We adopt this skeleton.

- **Yao, Zhao, Yu, Du, Shafran, Narasimhan, Cao (2023), "ReAct: Synergizing Reasoning and Acting in Language Models," ICLR.** The dominant single-chain agent paradigm. Our naive baseline. *Cite as the pattern we contrast against.*
- **Del Rosario, Krawiecka, Schroeder de Witt (2025), "Architecting Resilient LLM Agents: A Guide to Secure Plan-then-Execute Implementations," arXiv:2509.08646.** Plan-then-Execute pattern explicitly framed as agentic design with security focus on indirect prompt injection via control-flow integrity. *Cite as the architectural skeleton we adopt. Our contribution sits inside this pattern.*
- **Young (2010), "CQRS Documents."** Original CQRS framing in distributed systems. *Cite for terminology origin.*
- **Camarques (2024), "Ask vs Act: RAG, Tool Use and AI agents," DEV Community blog.** Informal application of CQRS to LLM agents with HITL moderation queue. *Cite as informal precedent; no formal claims.*
- **Hua et al. (2024), "TrustAgent: Towards Safe and Trustworthy LLM-based Agents through Agent Constitution," EMNLP Findings, arXiv:2402.01586.** Constitution-style policy framework for agents. *Cite as adjacent governance approach.*
- **Reversec Labs (2025), "Design Patterns to Secure LLM Agents In Action."** Pattern catalog including Plan-Then-Execute, Dual LLM, Action Selector. *Cite as practitioner-facing pattern catalog.*

## F. Per-call defenses and their limits

Model-side defenses are necessary but, by the visibility-asymmetry argument, structurally incomplete for path-level safety.

- **Bai et al. (2022), "Constitutional AI: Harmlessness from AI Feedback."** Training-time alignment via principles. *Cite as canonical per-call defense.*
- **Ouyang et al. (2022), "Training language models to follow instructions with human feedback" (InstructGPT).** RLHF. *Cite as canonical.*
- **Wallace, Xiao, Leike, Weng, Heidecke, Beutel (2024), "The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions."** Architectural-ish per-call defense via prompt hierarchy. *Cite as the strongest model-side defense to date.*
- **Greshake, Abdelnabi, Mishra, Endres, Holz, Fritz (2023), "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection."** Foundational indirect injection paper. *Cite as the canonical attack reference.*
- **Perez & Ribeiro (2022), "Ignore Previous Prompt: Attack Techniques For Language Models."** Direct prompt injection. *Cite as foundational.*
- **Hines et al. (2024), "Defending Against Indirect Prompt Injection Attacks With Spotlighting."** Defense via input separation. *Cite as defense.*
- **Debenedetti, Shumailov, Fan, Hayes, Carlini, Fabian, Kern, Shi, Terzis, Tramèr (2025), "Defeating Prompt Injections by Design" (CaMeL), arXiv:2503.18813.** Capability-based provable defense; 77% task completion under attack with provable security. *Cite as the strongest provable per-call-injection defense; contrast: our architecture addresses different failure modes (path-level composition rather than data-flow exfiltration), with weaker guarantees but lower annotation overhead.*
- **Willison (2023), "Dual LLM pattern for prompt injection," blog.** Practitioner pattern. *Brief mention.*

## G. Path-level safety for LLM agents (the immediate predecessor)

This is the most threatening prior art: path-level safety claim for LLM agents specifically, with formal machinery and empirical validation.

- **Dhodapkar & Pishori (2026), "SafetyDrift: Predicting When AI Agents Cross the Line Before They Actually Do," arXiv:2603.27148.** Models agent safety trajectories as absorbing Markov chains over a 3-dim cumulative state (data exposure, tool escalation, reversibility). 285 training traces; 94.7% violation detection with 3.7 steps advance warning. *This is our most important comparison point. Position carefully: SafetyDrift = empirical learned monitor; ours = analytic trace-free preventive gate. Different epistemic objects. Section 6.5 of the paper handles this comparison explicitly.*

## H. LLM agent benchmarks

Existing benchmarks measure pieces of what we'd measure, but none use composition mode as the organizing axis.

- **Ruan et al. (2023), "Identifying the Risks of LM Agents with an LM-Emulated Sandbox" (ToolEmu).** Path-level harm scoring via LM judge across full trajectories; ~144 test cases. Closest path-level harm benchmark. *Cite as primary benchmark predecessor; our contribution is a reversibility-indexed re-cut of trajectory failures organized by composition mode rather than harm category.*
- **Yao et al. (2024), "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains."** ~165 retail / ~115 airline tasks; pass^k metric for k=1..8. Closest to iteration-mode reliability. *Cite as iteration-mode benchmark.*
- **Debenedetti et al. (2024), "AgentDojo: A Dynamic Environment to Evaluate Attacks and Defenses for LLM Agents."** Per-injection, attack-typed. *Cite as injection-defense benchmark.*
- **Andriushchenko et al. (2024), "AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents."** ~110 harmful + benign-paired tasks; multi-step refusal scoring. *Cite as harm benchmark.*
- **Liu et al. (2023), "AgentBench: Evaluating LLMs as Agents."** Multi-task agent evaluation. *Brief mention.*
- **Mazeika et al. (2024), "HarmBench."** General harmfulness. *Brief mention.*
- **Zhou et al. (2023), "WebArena."** Web agent benchmark. *Brief mention.*
- **Jimenez et al. (2023), "SWE-bench."** Multi-step software engineering. *Brief mention.*
- **Shridhar et al. (2020), "ALFWorld."** Embodied agent benchmark. *Brief mention.*

## I. Two-way / one-way doors

The framing antecedent. Used widely in business decision-making; we apply it to agent safety.

- **Bezos, J. (1997 onward), Annual Letter to Shareholders.** Two-way doors / one-way doors as a per-decision rubric for reversibility. *Cite for framing origin. Note: the original framing is per-decision; our extension (composition into one-way trajectories) is the contribution to apply to agent safety.*

---

## Synthesis: where this paper sits

The path-irreversibility claim is held by Arthur 1989 (economics), Krakovna 2018 (RL), Sagas 1987 (distributed systems), and SafetyDrift 2026 (LLM agents). The architectural separation is held by Del Rosario 2025 (Plan-then-Execute). The capability-defense angle is held by CaMeL 2025.

The contribution that survives this lit map:
- The **door-composition framing** applied specifically to LLM agents in the post-aligned-model era.
- The **four composition modes** (accumulation, premise, classification, iteration) as an analytic taxonomy not present in any prior work.
- A **trace-free, preventive operationalization** (trust budget + staging + classifier) inside the Plan-then-Execute skeleton, as an alternative to SafetyDrift's empirical learned monitor.
- An **empirical demonstration** that aligned 2026 frontier models produce path-level failures across all four modes, organized by composition mode rather than harm category.

This is conceptual scaffolding plus methodological re-cut, not novel theory. The thought-leadership value is in the framing and taxonomy becoming the vocabulary the field uses.
