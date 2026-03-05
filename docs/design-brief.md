# Design Brief

## For Collaborators

This document describes the *experience* of working with the airlock agent, not the API. It's meant to help you understand what we're building and why.

## What Problem Are We Solving?

AI agents that can send emails are dangerous. Not because the model is bad, but because the architecture lets a bad thought become a bad action with no circuit breaker in between.

## The Experience We Want

### For the user (Alice):

1. Alice tells the agent: "Handle my inbox"
2. The agent reads emails, reasons about them, and *proposes* actions
3. Low-risk actions (reading, drafting) happen automatically
4. High-risk actions (sending to 200 people, replying to suspicious emails) pause and ask Alice
5. Alice sees what the agent wants to do, why it wants to do it, and how risky it is
6. Alice approves or rejects

### For the evaluator (us):

1. We run 10 scenarios against both agents
2. We measure: how many harmful actions did each agent take?
3. The naive agent has no guardrails → more harmful actions
4. The airlock agent has architectural guardrails → fewer harmful actions, at the cost of some latency

## What "Good" Looks Like

- **Benign scenarios:** Both agents handle correctly. The airlock agent is slightly slower but equally correct.
- **Adversarial scenarios:** The naive agent falls for prompt injections, urgency manipulation, and social engineering. The airlock agent stages these actions, and the checkpoint rejects them.
- **Edge cases:** The airlock agent correctly identifies ambiguous situations (draft vs. send, meeting invite notifications) and either auto-handles them within budget or flags them.

## Key Constraint

This is a research prototype, not a product. We optimize for clarity of demonstration, not production readiness. The mock email backend exists so we never risk sending real emails during adversarial testing.
