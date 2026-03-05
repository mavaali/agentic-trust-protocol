# Literature Map

Annotated bibliography across four domains relevant to the Agentic Trust Protocol.

## Domain 1: Agent Architectures

*How are AI agents currently structured?*

- **ReAct (Yao et al., 2023)** — Interleaving reasoning and acting. The dominant paradigm. Key limitation: single chain means reasoning errors flow directly to actions.
- **Toolformer (Schick et al., 2023)** — LLMs learning to use tools. Focuses on capability, not safety.
- **AutoGPT / BabyAGI** — Autonomous agent frameworks. Demonstrate the risks of unsupervised agent loops.

*Gap:* Existing architectures focus on capability (can the agent do it?) not safety (should the agent do it?).

## Domain 2: CQRS & Event Sourcing

*How do distributed systems separate reads from writes?*

- **CQRS (Young, 2010)** — Command Query Responsibility Segregation. Separate models for read and write operations. Enables different scaling, security, and optimization strategies for each path.
- **Event Sourcing (Fowler)** — Store state changes as events. Provides audit trail and ability to reconstruct state.

*Insight:* The read/write separation in CQRS maps directly to observe/act separation in agents.

## Domain 3: AI Safety & Alignment

*How do we make AI systems trustworthy?*

- **Constitutional AI (Bai et al., 2022)** — Training-time alignment via principles. Addresses model behavior but not architectural safety.
- **RLHF (Ouyang et al., 2022)** — Reinforcement learning from human feedback. Improves model outputs but doesn't prevent architectural failures.
- **Prompt injection surveys** — Growing body of work on injection attacks. Mostly defensive prompting, not architectural solutions.

*Gap:* Most safety work focuses on the model layer, not the architecture layer.

## Domain 4: Human-in-the-Loop Systems

*How do systems involve humans in decision-making?*

- **Confirmation dialogs** — Simple but effective for high-risk actions. The airlock checkpoint is a generalization.
- **Approval workflows** — Enterprise systems (PR reviews, deployment gates). Trust budgets are a form of delegated approval.
- **Supervisory control** — Human factors research on automation trust. Relevant to calibrating trust budget parameters.

*Insight:* The trust budget is a quantitative version of "how much rope to give the agent."

---

## Key Synthesis

The novel contribution is applying CQRS architecture to agent safety. This bridges:
- Agent architectures (capability) + AI safety (alignment) + distributed systems (architecture patterns)

No existing work combines these three domains for agent trust.
