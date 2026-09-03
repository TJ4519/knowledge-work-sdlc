---
name: professional-challenge
description: "Fresh independent challenge of an existing candidate using retained evidence and no producer transcript."
initial_inputs: ["request", "candidate"]
---
# Professional challenge

Use when the candidate already exists and the commission is to test it rather
than regenerate it.

## Composition

```json
[
  {"id":"interpret-challenge","actor":"skill","method":"kw-meaning-consultation"},
  {"id":"confirm-meaning","actor":"human","optional":true,"trigger":"material route ambiguity","requires":["meaning"],"provides":["decision"]},
  {"id":"explore-challenge-evidence","actor":"agent","method":"evidence-explorer","requires":["request","meaning","candidate"]},
  {"id":"challenge","actor":"agent","method":"thesis-challenger","requires":["meaning","evidence-map","candidate"]},
  {"id":"adjudicate","actor":"agent","method":"adjudicator","optional":true,"trigger":"material candidate-challenger contradiction survives main-agent triage"},
  {"id":"confirm-adjudication","actor":"human","optional":true,"trigger":"adjudication requires human disposition","requires":["adjudication"],"provides":["decision"]}
]
```

The challenger receives the frozen candidate and evidence packet, not producer
private rationale. The human decision targets the exact reviewed revision.
