---
name: kw-protected-promotion
description: "Apply an exact human-authorised native candidate payload to a registered protected artefact through a pre-bound mechanical operation with validation and rollback."
primitive: skill
fresh_context: false
independence: deterministic-host
allowed_tools: ["Read", "Shell", "Write"]
inputs: ["candidate-protected-artifact-change", "decision"]
optional_inputs: ["native-payload", "protected-artifact-register", "adjudication"]
excluded_context: ["model-judgment-as-authority", "descriptor-as-payload"]
outputs: ["promotion"]
authority: exact-human-use-required
standalone: false
idempotency: "Reuse a completed promotion only when target, candidate payload hash, decision, and pre-promotion target hash are identical."
phase: promotion
---
# Protected promotion

Promotion is a mechanical custody operation invoked by the main agent. The agent
may execute only the exact pre-bound operation after every authority and identity
precondition passes. It cannot use model judgment to choose different bytes,
scope, target, or success criteria, and it cannot simulate a protected write.

## Preconditions

- the current recipe stage is promotion;
- the protected target is registered;
- the candidate descriptor is live and references one native payload revision;
- payload media type matches the target policy;
- payload bytes match their retained hash;
- an exact human `Use` decision targets the candidate and names the same target, scope, and intended use;
- any required adjudication targets the same candidate;
- the target's current hash matches the registered or stage-prepared expectation;
- the bound promotion facility can preserve or create a recoverable prior state
  and expose enough evidence to verify the resulting target.

## Host procedure

1. Recheck the candidate, payload, decision, target identity, current target hash,
   and exact operation-specific capability binding.
2. Preserve a recoverable prior state and record its identity/hash.
3. Stage the exact candidate payload through the bound facility and run the
   target-specific validation before protected replacement when that surface
   permits it.
4. Apply the bound replacement only if its atomicity or transactional guarantee
   is observed; otherwise halt with promotion blocked.
5. Re-read or rehash the protected target and verify it equals the authorised
   payload for full-file promotion, or the registered postconditions for an
   approved delta mechanism.
6. Record candidate, payload, decision, facility, target, before/after identity,
   validation result, timestamp, and rollback handle.
7. Advance only after the promotion artefact is durable.

## Failure

On any mismatch, leave the protected target unchanged and record the precise
failed attempt, observed target state, and next legal action in the open run
record. Do not weaken validation, copy the descriptor, or fall back to direct
editing.

## Boundary

A report-only or degraded candidate without native payload is not promotable. Delta candidates require a registered deterministic applier; they are not treated as full files.
