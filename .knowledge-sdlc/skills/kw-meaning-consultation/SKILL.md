---
name: kw-meaning-consultation
description: "Make the consequential interpretation of an imperfect commission visible and revisable without turning the user into a specification writer."
primitive: skill
fresh_context: false
independence: main-agent-consultation
allowed_tools: ["Read", "Grep", "Shell", "Write"]
inputs: ["request"]
optional_inputs: ["intent", "domain-charter", "source-policy", "protected-artifact-register"]
excluded_context: ["unconfirmed-treatment", "future-producer-rationale", "unrelated-initiative-content", "reusable-lesson-content"]
outputs: ["meaning"]
optional_outputs: ["rival-route", "decision"]
authority: model-interpreted-unless-material-rival-requires-human-decision
standalone: partial
idempotency: "Revise the initiative's meaning artefact; do not create a parallel specification for the same commission."
phase: specification
---
# Meaning consultation

The exact commission records what the user said. The working interpretation
records what the agent thinks that wording means for the professional work.
Keep both visibly separate in the immutable `meaning-rN.md` revision.

## Trigger

Load during intake when an inferred field can materially alter the route, or
when later correction reopens the meaning of the commission.

## Method

1. Read the exact commission and inspect the referenced workspace evidence.
2. State the latent undertaking in natural language: intended outcome,
   consequential object, scope, audience or use, and success condition.
3. Attribute each material part as direct user wording, agent inference,
   project default, source-derived fact or unresolved.
4. Include only fields the commission earns. A structured-model commission may need
   subject, period or version, definition, protected artefact, scenario, boundary and use;
   a short research brief may not.
5. Separate absence from ambiguity. Resolve low-consequence absence through
   professional judgment; expose ambiguity only when rival readings alter the
   method, evidence, output or authority.
6. Where two readings are genuinely material, write both, their consequences
   and what would distinguish them. Do not manufacture a rival for ceremony.
7. Present a focused correction surface the user can react to. Prefer “I have
   treated X as Y; if you meant Z the route changes because…” over a blank form.
8. When the user corrects or explicitly accepts the interpretation, record that
   act in a decision artefact targeting the exact meaning path and hash. Absence
   of a material rival may settle the attributed working interpretation without
   manufacturing a human approval. A material interpretation is immutable once
   another file or decision targets it: write `meaning-r1.md`, `meaning-r2.md`,
   and so on; never overwrite targeted bytes. Link the current revision and
   decision from the open run record and preserve every superseded revision.

Apply the `knowledge-work` run-and-artefact save contract in that same action.
Meaning is not corrected until affected outputs are superseded or rederived and
the open run record's plan, outcomes, unresolved consequences, and next action
agree with the revision.

The exact target file and SHA-256 named by a correction must remain present and
recomputable. A summary of the prior reading is not a substitute for its bytes.

## Reopen condition

New evidence or user feedback reopens meaning only when it contradicts a live
assumption or changes the professional outcome. A different session or model
does not reopen meaning by itself.

## Non-authority

This method cannot turn a route-changing inference into human confirmation,
turn a project convention into a human instruction, or use personalisation as
present-initiative evidence.
