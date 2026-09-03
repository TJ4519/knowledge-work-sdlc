---
name: knowledge-work-correction
description: "Revisioned correction, dependency-valid invalidation, reconciliation, fresh re-derivation, and exact confirmation."
initial_inputs: ["request", "candidate", "evidence-map", "work-order"]
---
# Knowledge-work correction

Use when a correction changes meaning, evidence treatment, method, or an
accepted result and its dependants must be rederived.

## Proportional correction route

The default correction is one bounded pass, not a recursive review programme:

```text
exact correction
→ explicit dependant invalidation
→ one reconciliation pass identifying the owning producer
→ one typed successor candidate from that producer
→ optional fresh re-derivation when reproducibility is affected
→ at most one earned independent challenge
→ at most one challenge-driven repair
→ visible return with any retained limitation
```

Prune fresh re-derivation when the correction changes only presentation or
wording and no calculation, protected payload, accepted method, evidentiary
treatment, or reproducibility claim. Prune a new human gate when the exact
correction already supplies the needed authority and the revised work does not
introduce another material interpretation or protected action.

Do not repeatedly re-challenge repairs inside the same run. If the bounded
challenge exposes a further material issue after the one corrected candidate,
retain the issue visibly and halt or open a successor method-repair run. Never
optimise prose until every reviewer is silent.

## Composition

```json
[
  {"id":"interpret-correction","actor":"skill","method":"kw-meaning-consultation","provides":["meaning","decision"]},
  {"id":"confirm-correction","actor":"human","optional":true,"trigger":"material route ambiguity remains","requires":["meaning"],"provides":["decision"]},
  {"id":"invalidate-dependants","actor":"skill","method":"kw-reconciliation-control"},
  {"id":"reconcile","actor":"agent","method":"reconciler","requires":["invalidation"]},
  {"id":"reproduce-research","actor":"agent","method":"research-synthesis-producer","optional":true,"trigger":"an affected research candidate requires supersession","requires":["meaning","evidence-map"],"provides":["candidate-research"]},
  {"id":"reproduce-source-interpretation","actor":"agent","method":"research-synthesis-producer","optional":true,"trigger":"an affected source-interpretation candidate requires supersession","requires":["meaning","evidence-map"],"provides":["candidate-source-interpretation"]},
  {"id":"reproduce-method","actor":"agent","method":"research-synthesis-producer","optional":true,"trigger":"an affected candidate method requires supersession","requires":["meaning","evidence-map"],"provides":["candidate-method"]},
  {"id":"reproduce-protected-candidate","actor":"agent","method":"protected-artifact-producer","optional":true,"trigger":"an affected protected-artifact candidate requires supersession","requires":["meaning","work-order","evidence-map"],"provides":["candidate-protected-artifact-change"]},
  {"id":"rederive","actor":"agent","method":"rederivation-auditor","optional":true,"trigger":"correction affects calculation, protected payload, accepted method, evidentiary treatment, or reproducibility claim","requires":["meaning","invalidation"]},
  {"id":"challenge-corrected-candidate","actor":"agent","method":"thesis-challenger","optional":true,"trigger":"the corrected candidate will inform a consequential decision and a material inference or rival route remains","requires":["meaning","evidence-map"],"provides":["challenge"]},
  {"id":"dispose-corrected-candidate","actor":"skill","method":"kw-candidate-disposition","optional":true,"trigger":"the corrected candidate requires consequential Use, Reject, or Amend authority","provides":["decision"]}
]
```

Only explicit dependency descendants become stale. Human-approved meanings and
protected objects are proposed for disposition rather than silently rewritten.
Exactly one producer branch applies to one stale candidate type. The
orchestrator gives any challenger and disposition skill that exact successor;
the recipe does not turn the four optional branches into four outputs.
