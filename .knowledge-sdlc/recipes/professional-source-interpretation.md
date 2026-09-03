---
name: professional-source-interpretation
description: "Preserve competing source definitions, produce a provisional treatment, independently challenge it, and obtain exact disposition."
initial_inputs: ["request"]
---
# Professional source interpretation

Use when source identity, definition, period, comparability, or admissible use
is itself the commissioned problem.

## Composition

```json
[
  {"id":"interpret","actor":"skill","method":"kw-meaning-consultation"},
  {"id":"confirm-meaning","actor":"human","optional":true,"trigger":"material route ambiguity","requires":["meaning"],"provides":["decision"]},
  {"id":"explore-evidence","actor":"agent","method":"evidence-explorer"},
  {"id":"produce-interpretation","actor":"agent","method":"research-synthesis-producer","provides":["candidate-source-interpretation"]},
  {"id":"challenge-source-meaning","actor":"agent","method":"source-meaning-challenger","requires":["meaning","evidence-map","candidate-source-interpretation"]},
  {"id":"adjudicate","actor":"agent","method":"adjudicator","optional":true,"trigger":"material producer-challenger contradiction survives main-agent triage","requires":["challenge","candidate-source-interpretation"]},
  {"id":"human-disposition","actor":"skill","method":"kw-candidate-disposition","requires":["candidate-source-interpretation"]}
]
```

No source ordering or interpretation becomes standing project truth unless a
separate exact human decision promotes it to the proper owner.
