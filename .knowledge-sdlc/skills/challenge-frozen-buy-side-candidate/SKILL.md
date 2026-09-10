---
name: challenge-frozen-buy-side-candidate
description: "Challenge a frozen company-model update or compare separately frozen interpretations. Look for decision-relevant source-policy violations, invented reported structure, unsupported transformations, stale retained inputs, omitted work, and misleading conclusions. Produce falsifiable challenges, not a replacement or a pass; no finding is a valid outcome."
primitive: skill
fresh_context: true
independence: producer-independent-challenge
allowed_tools: ["Read", "Grep", "Shell", "Write"]
inputs: ["work-order","candidate"]
optional_inputs: ["source-snapshot","evidence-map","expert-method-binding"]
excluded_context: ["unrelated-initiative-history", "unadmitted-firm-method-as-authority", "producer-confidence-as-proof"]
outputs: ["challenge"]
authority: candidate-support-only-no-professional-or-protected-authority
standalone: false
idempotency: "Reuse only for the same task, candidate, source and method identities and unchanged permitted use."
phase: challenge
references: [".knowledge-sdlc/references/buy-side-method/README.md",".knowledge-sdlc/references/buy-side-method/semantic-contracts.md",".knowledge-sdlc/references/buy-side-method/cross-context-recipe.md"]
---
# Challenge the model change, not the author's confidence

This optional bundled skill supplements the core SDLC and the analyst's own method. The main agent selects its bounded use in the current run; installation alone does not select it, admit a firm method, or grant workbook-write/use authority. Resolve `.knowledge-sdlc/...` reference cues from the repository's managed root, or the shared managed root declared by the plugin binding. Use the existing work-order, candidate, challenge and run records; these outputs do not require a new file family.

## Purpose and boundary

Identify a concrete way this candidate could satisfy visible expectations while failing the agreed professional task. Assume the author intended to help. Do not defend their method, but do not receive credit merely for finding an omission.

You may inspect permitted original evidence, form hypotheses, and write your review artifact. You may not edit the candidate, repair it while judging it, approve its use, change acceptance, or require another cycle. Candidate-read-only does not prohibit writing your own review note.

Use this in the separate context assigned by the orchestrator. State any known history inheritance or access limitation. A role name does not establish isolation; a second model reading the same disclosure does not supply an independent disclosure.

## Inputs and two-stage exposure

Receive the task/use, source policy, client modelling conventions, critical assertions, original evidence, candidate identity, intended-change population, and access limits.

For a semantically difficult selected region, first write brief watchpoints from the original source and task before opening the producer's mapping rationale. Then examine the unchanged candidate, actual change record, mappings, and disclosed exceptions. This is an evidence-first review inside one review context, not a claim of fully blind re-derivation.

For routine tasks the orchestrator may omit that first pass. For genuinely blind reconstruction, it invokes the derivation skill in another candidate-blind context. Do not pretend that ignoring an answer already seen restores independence.

## Adversarial prior

For the purpose of this review, assume the producer could have satisfied the visible rubric by using convenient sources, blending representations, leaving difficult updates untouched, or explaining an approximation as a match. Ask how the exact candidate could still look right. This is a search hypothesis, not a factual accusation of malicious intent.

## Follow the professional failure paths

Read both directions: do important source facts reach the model in the right form, and do actual candidate changes have an authorised basis? Check critical retained inputs as well as edits. A complete mapping ledger can omit the very item the producer failed to update.

Look especially for:

- a source-policy or reporting-vintage substitution hidden by a genuine citation;
- subtotals and overlapping components combined into invented reported detail;
- faithful reproduction, analytical normalisation, and forecasting silently exchanged;
- a correct value used for the wrong period, entity, scenario, or calculation;
- an unresolved definition left out of a ledger while an old value still drives a current conclusion;
- an unauthorised tax, formula, or assumption change made to reconcile outputs;
- a source interpretation selected to fit the template rather than supported by the disclosure;
- a workbook draft or partial inspection presented as calculated, checked, or fully updated.

Do not reject a legitimate forecast merely because its answer is not published. Do not object to a documented unit conversion or permitted row adaptation simply because the sources and target look different.

## Make a challenge earn verification

For each possible finding, identify the exact assessed proposition and candidate location, the evidence inspected, a plausible failure path, the protected decision or truthful-reporting boundary it could change, and a discriminating source check or calculation.

Search for a rule or evidence that defeats your criticism. Note that counterevidence. Separate an established textual conflict from an untested runtime hypothesis. Missing evidence supports an unresolved claim, not a fabricated assertion that the candidate is wrong.

When comparing two frozen derivations, identify meaningful differences in source basis, reporting structure, assumptions, uncertainty, or consequences. Agreement is not proof; disagreement is not automatically a defect. Do not demand reconciliation of vocabulary alone.

## Handoff

Return `CHALLENGES_READY`, `NO_DECISION_RELEVANT_CHALLENGE_FOUND`, or `REVIEW_BLOCKED`, the inspected scope, evidence limitations, and any concise non-blocking aside. The controller, not the reviewer, adjudicates materiality and routing.

“No challenge found” does not establish that the critical assertions were verified. The verifier has its own baseline checks even when your finding set is empty.

## Small example

A forecast value of 105 supported by a disclosed 5% internal-growth assumption is not fabricated merely because management guided to 8%. The question is whether an internal 5% case was authorised and labelled, rather than whether the agent copied guidance. Conversely, a reported income-tax figure changed to force reconciliation is not repaired by adding a candid footnote.

Use `.knowledge-sdlc/references/buy-side-method/semantic-contracts.md` for finding fields. `.knowledge-sdlc/references/buy-side-method/cross-context-recipe.md` controls separation, handoffs, and the revision budget.
