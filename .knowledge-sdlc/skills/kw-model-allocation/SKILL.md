---
name: kw-model-allocation
description: "Record exact user model overrides and observed concierge/worker identity without autonomously choosing a model or turning provider defaults into proof."
primitive: skill
fresh_context: false
independence: main-agent-configuration
allowed_tools: ["Read", "Shell", "Write"]
inputs: ["provider-surface"]
optional_inputs: ["model-policy", "available-models", "exact-user-override"]
excluded_context: ["provider-preference-as-quality-proof", "silent-fallback", "autonomous-model-ranking"]
outputs: ["model-policy"]
authority: exact-user-configuration-only
standalone: true
idempotency: "An exact override affects only its declared future scope; historical model observations remain immutable."
phase: configuration
---
# Model observation and override

The desired default is the concierge model. The harness does not maintain
capability tiers or choose a cheaper, stronger, or different-family model on
the user's behalf.

1. If the host exposes the exact concierge identity and permits forwarding it,
   pass that exact identity to the worker.
2. If it does not, omit the selector and record only `unobservable`. The host
   then applies its own default; omission proves nothing about the resulting
   model identity or inheritance.
3. When actual child identity is exposed, record `inherited | different` with
   both identities and provider evidence. A material unexpected difference
   degrades or blocks the affected independence claim.
4. Apply a different model only from an exact user-authored override naming
   provider, model, reasoning setting, scope, fallback, and effective revision.
   Never infer an override from an old profile or provider preference.
5. Model identity never grants human authority or proves professional
   correctness or epistemic independence.

The project model-policy file stores only confirmed overrides and observed
limitations. Provisional model names are ignored.
