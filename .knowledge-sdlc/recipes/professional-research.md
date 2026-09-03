---
name: professional-research
description: "Evidence-bearing research synthesis with proportionate independent challenge and exact human disposition."
initial_inputs: ["request"]
---
# Professional research

Use for a research question whose output will inform a professional decision.
Adapt the sequence visibly in the run record; optional review becomes mandatory
when source conflict or decision consequence earns it.

## Composition

```json
[
  {"id":"interpret","actor":"skill","method":"kw-meaning-consultation"},
  {"id":"confirm-meaning","actor":"human","optional":true,"trigger":"material route ambiguity","requires":["meaning"],"provides":["decision"]},
  {"id":"explore-evidence","actor":"agent","method":"evidence-explorer"},
  {"id":"prepare-work-order","actor":"skill","method":"kw-work-order"},
  {"id":"confirm-work-order","actor":"human","optional":true,"trigger":"work order adds consequential scope or method","requires":["work-order"],"provides":["decision"]},
  {"id":"produce-candidate","actor":"agent","method":"research-synthesis-producer","provides":["candidate-research"]},
  {"id":"challenge-source-meaning","actor":"agent","method":"source-meaning-challenger","optional":true,"trigger":"material source conflict","requires":["meaning","evidence-map","candidate-research"]},
  {"id":"challenge-thesis","actor":"agent","method":"thesis-challenger","optional":true,"trigger":"material claim or decision consequence","requires":["meaning","evidence-map","candidate-research"]},
  {"id":"adjudicate","actor":"agent","method":"adjudicator","optional":true,"trigger":"material producer-challenger contradiction survives main-agent triage","requires":["challenge","candidate-research"]},
  {"id":"human-disposition","actor":"skill","method":"kw-candidate-disposition","requires":["candidate-research"]}
]
```

The candidate remains provisional. A required challenge must precede Use,
Reject, or Amend; absent independence produces an explicit degraded or blocked
gate rather than a placeholder review.

The ordinary durable set is one meaning revision, one evidence map or bounded
source snapshot set, one work order when a fresh producer needs it, one live
candidate, one challenge when earned, exact decisions when supplied, and the
run record. A supporting skill's internal trajectories, claim transitions,
self-validations, traces, and taxonomies remain inline unless the run names a
distinct downstream consumer which the existing artefacts cannot serve. An
accepted challenge finding updates the candidate and run directly; agreement
does not earn an adjudication artefact.
