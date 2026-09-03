---
name: kw-learning-outcome-review
description: "Evaluate the observable marginal effect of one bounded lesson-selection decision and record an honest outcome."
primitive: skill
fresh_context: false
independence: main-agent-or-preferably-fresh-evaluator
allowed_tools: ["Read", "Grep", "Write", "Task"]
inputs: ["decision", "initiative-evidence"]
optional_inputs: ["treatment-output", "control-output", "user-correction"]
excluded_context: ["builder-private-rationale", "unrelated-initiative-content", "method-change-proposal"]
outputs: ["lesson-outcome"]
authority: evaluative-proposal-only
standalone: true
idempotency: "One lesson-selection decision has one cumulative outcome record whose later evidence amends rather than replaces earlier uncertainty."
phase: learning-outcome
---
# Learning outcome review

Judge what the selected lesson changed, not whether the later work merely
completed. A successful initiative is not automatically evidence that the lesson
helped.

## Method

1. Read the selection decision's expected effect, named step and prohibited effects.
2. Identify observable later-initiative evidence: changed questions, route choice,
   work product, user correction, contradiction or an independently produced
   treatment/control comparison.
3. Ask the counterfactual question: what material difference is attributable
   to the lesson rather than the new initiative's own evidence or ordinary method?
   Separate an observed difference from an attributable effect. In a
   non-deterministic producer, **one-shot generative variation** outside the
   named effect cannot by itself support `helped` or `harmed`.
4. Check contamination: did lesson content or the selection decision's instruction
   trace into present facts, confidence, authority or a step outside its
   allowed effect? Unmatched phrasing is a rival account, not proof of leakage.
5. Record one disposition in `lesson-outcome.md`:
   `helped`, `harmed`, `ignored`, `contradicted`, `corrected`, or
   `inconclusive`. Explain the evidence and remaining rival account.
6. Link the outcome from the later initiative's open run record. The decision
   and outcome already link the exact retained lesson revision; do not rewrite
   that revision or the source initiative to append history.
7. If the evidence suggests the lesson itself should change, create a new
   governance candidate. If it suggests the professional method should change,
   create a separate method-change commission.

## Attribution threshold

`helped` and `harmed` require lesson-specific causal evidence, such as a direct
content trace into the named effect, a repeatable treatment difference, an
explicit user correction targeting that effect, a deterministic transform, or
an outcome measure tied to the intended use. Merely following the activation
proves application, not benefit. A single treatment/control pair can show that
the permitted effect appeared, but unrelated textual variation must remain a
rival account unless it is itself traced to the lesson.

Use `ignored` when the selected decision was available but its named effect did not
appear. Use `contradicted` when later initiative evidence conflicts with the retained
proposition. Use `corrected` when later evidence or exact user feedback revises
the applied statement or scope. Use `inconclusive` when application is visible
but causal attribution, benefit or harm remains underdetermined. Do not choose a
more dramatic disposition merely because the comparison contains more visible
differences.

## Independent review

Prefer a fresh evaluator when the host supports one and the selection was
material. Give it the decision, treatment output, optional control output and
initiative evidence, but not the builder's private reasoning. The portable path is
this same review method used inline with the limitation stated.

## Non-authority

Outcome review cannot suspend, amend or retire a lesson by itself and cannot
promote a procedural change. It may only propose the next governed decision.
