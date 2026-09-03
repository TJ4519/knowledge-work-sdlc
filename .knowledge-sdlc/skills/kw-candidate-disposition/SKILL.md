---
name: kw-candidate-disposition
description: "Present an exact candidate and review state for human Use, Reject, or Amend authority without broadening the decision in prose."
primitive: skill
fresh_context: false
independence: main-agent-human-gate
allowed_tools: ["Read", "Shell", "Write"]
inputs: []
optional_inputs: ["candidate", "candidate-protected-artifact-change", "candidate-research", "candidate-source-interpretation", "candidate-method", "challenge", "adjudication", "evidence-map", "work-order", "protected-artifact-register"]
excluded_context: ["model-confidence-as-authority", "unrelated-candidates", "superseded-candidate"]
outputs: ["decision"]
authority: human-only
standalone: false
idempotency: "A decision is tied to one exact live candidate revision, target, scope, and intended use."
phase: human-gate
---
# Candidate disposition

The decision object is the professional control seam. Present enough evidence for an expert decision without laundering model confidence into authority.

## Method

1. Verify the target is the current eligible candidate and is not stale.
2. Read the exact candidate descriptor, payload metadata where any, evidence links, validations, degraded gaps, challenges, and adjudication.
3. Show:
   - candidate revision and hash;
   - protected target and exact scope;
   - intended use;
   - what changed and what is explicitly unchanged;
   - unresolved source, method, or thesis conflict;
   - whether a native payload exists and is promotable;
   - what downstream work would require reconciliation.
4. Offer only the decisions licensed by the current gate: Use, Reject, or Amend.
5. Retain the user's exact turn and bind the decision to this candidate,
   target, scope, and intended use. Use `provider-observed` only for an identity
   the host directly exposes for this current decision turn. Preserve any
   parent/source/delegation ID separately as transport lineage; never substitute
   it for the current task/message. Otherwise use `workspace-recorded`.

## Decision semantics

- **Use:** authorises only the named candidate and scope. It does not assert universal truth or authorise a different payload.
- **Reject:** closes the candidate route as rejected or follows the recipe's named alternative.
- **Amend:** marks this candidate stale, rewinds to its producer, and requires a superseding candidate. It never edits the old candidate in place.

## Stop conditions

Do not request disposition when required adjudication is absent, a challenge targets another candidate, payload bytes fail their hash, or the candidate omits material gaps required for judgment.

## Non-authority

The presenting model may recommend a decision and explain trade-offs. Only the exact retained human turn grants authority.
