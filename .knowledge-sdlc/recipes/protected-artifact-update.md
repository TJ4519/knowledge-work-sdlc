---
name: protected-artifact-update
description: "Bounded native-artifact update with exact template and capability binding, candidate custody, challenge, promotion, and re-derivation."
initial_inputs: ["request"]
---
# Protected artefact update

Use for a workbook, presentation, document, model, or other native object whose
original must remain protected during production.

## Composition

```json
[
  {"id":"interpret","actor":"skill","method":"kw-meaning-consultation"},
  {"id":"confirm-meaning","actor":"human","optional":true,"trigger":"material route ambiguity","requires":["meaning"],"provides":["decision"]},
  {"id":"explore-source-and-object","actor":"agent","method":"evidence-explorer"},
  {"id":"prepare-work-order","actor":"agent","method":"work-object-preparer"},
  {"id":"confirm-work-order","actor":"human","optional":true,"trigger":"work order adds consequential scope or method","requires":["work-order"],"provides":["decision"]},
  {"id":"produce-candidate","actor":"agent","method":"protected-artifact-producer"},
  {"id":"challenge-source","actor":"agent","method":"source-meaning-challenger","optional":true,"trigger":"material source conflict","requires":["meaning","evidence-map","candidate-protected-artifact-change"]},
  {"id":"challenge-thesis","actor":"agent","method":"thesis-challenger","optional":true,"trigger":"material claim or decision consequence","requires":["meaning","evidence-map","candidate-protected-artifact-change"]},
  {"id":"adjudicate","actor":"agent","method":"adjudicator","optional":true,"trigger":"material producer-challenger contradiction survives main-agent triage","requires":["challenge","candidate-protected-artifact-change"]},
  {"id":"human-disposition","actor":"skill","method":"kw-candidate-disposition","requires":["candidate-protected-artifact-change"]},
  {"id":"promote","actor":"skill","method":"kw-protected-promotion","optional":true,"trigger":"exact Use decision and protected action authorised"},
  {"id":"reconcile","actor":"agent","method":"reconciler","optional":true,"trigger":"promotion or accepted change occurred"},
  {"id":"rederive","actor":"agent","method":"rederivation-auditor","optional":true,"trigger":"promotion or material accepted change occurred"}
]
```

Capability reconnaissance and an operation-specific proof occur before the
producer writes a candidate. A missing native capability degrades or blocks; it
never permits a fake replacement or a claim that a save proves fidelity.
