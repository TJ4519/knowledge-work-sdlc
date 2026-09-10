---
name: verify-discriminating-buy-side-claims
description: "Check a frozen company-model candidate against acceptance-critical assertions and decision-relevant challenges using original evidence and actual workbook observations. Verification must still examine its baseline assertions when the reviewer finds nothing. Report proposition-level support and limits without editing the candidate or approving its use."
primitive: skill
fresh_context: true
independence: producer-and-challenger-independent-verification
allowed_tools: ["Read", "Grep", "Shell", "Write"]
inputs: ["work-order","candidate"]
optional_inputs: ["challenge","source-snapshot","evidence-map","expert-method-binding"]
excluded_context: ["unrelated-initiative-history", "unadmitted-firm-method-as-authority", "producer-confidence-as-proof"]
outputs: ["verification"]
authority: candidate-support-only-no-professional-or-protected-authority
standalone: false
idempotency: "Reuse only for the same task, candidate, source and method identities and unchanged permitted use."
phase: verification
references: [".knowledge-sdlc/references/buy-side-method/README.md",".knowledge-sdlc/references/buy-side-method/semantic-contracts.md",".knowledge-sdlc/references/buy-side-method/cross-context-recipe.md"]
---
# Verify evidence, including what nobody challenged

This optional bundled skill supplements the core SDLC and the analyst's own method. The main agent selects its bounded use in the current run; installation alone does not select it, admit a firm method, or grant workbook-write/use authority. Resolve `.knowledge-sdlc/...` reference cues from the repository's managed root, or the shared managed root declared by the plugin binding. Use the existing work-order, candidate, challenge and run records; these outputs do not require a new file family.

## Purpose and authority

Determine what the evidence supports, rather than endorse either an articulate producer or an articulate reviewer. Independently reacquire or inspect the permitted original material and the actual candidate. An immutable source snapshot may serve both roles; independence of inspection is not independence of source origin.

You may read the candidate, inspect evidence, perform authorised scratch calculations, and write your own receipt. Do not modify or repair the reviewed candidate, change source policy, or issue use authority. Record any practical limit on context separation or candidate protection.

## Verification has two inputs

Always inspect the acceptance-critical assertions named in the brief. Add relevant reviewer hypotheses and differences between independent derivations. An empty challenge set does not make verification empty or successful.

Check that the baseline assertions still cover the important claims made by this candidate. The producer must not be the sole selector of what counts as critical. Within the agreed review budget, select a bounded unflagged item or source-to-output path where omission or common-mode error is plausible. Do not describe a sample as exhaustive coverage.

If the baseline itself is absent or plainly misses the claimed use, report an acceptance gap to the concierge. Do not invent an unlimited verification programme or return a vacuous pass.

## Work from neutral propositions

Write what is being assessed affirmatively and narrowly. For example: “This historical tax cell reproduces the selected statement's reported tax amount” is clearer than “reviewer F3 is right.” Record the reviewer's hypothesis separately if useful.

Identify what would support or contradict that proposition and acquire the necessary evidence through permitted routes. No discovery tool limits the source universe; inability to read the required source limits verification of its content. They are not the same deficiency.

Check identity, source role, period/vintage, entity, units, relevant definition, and permitted use. Inspect surrounding table structure where totals/components may overlap. A source citation, nonempty field, or matching total is insufficient by itself.

Follow the selected value or derivation into its actual candidate location. Check both the declared transformation and the written value/formula. Inspect protected or consequential retained assumptions where an unresolved update could leave a misleading current result.

For a forecast, assess evidence use, calculation, scenario, assumptions, and truthful status. Do not claim to have verified the future realised outcome. For a plan, assess dependencies and permitted operations, not unexecuted model behaviour.

Check reconciliation without accepting an unauthorised balancing plug. A permitted forecast balancing mechanism is distinct from rewriting a company-reported fact. Check relevant valid alternatives too, so caution does not falsely reject correct work.

## Results

For each assessed proposition, return one of:

- `SUPPORTED`: the cited observations support this proposition within its stated scope.
- `CONTRADICTED`: the evidence conflicts with the proposition.
- `UNRESOLVED`: the available evidence does not decide it.
- `NOT_EXAMINED`: it was outside the recorded inspection scope or could not be attempted.

These refer to the proposition, not the reviewer's status. Completing this procedure does not imply all propositions were supported.

Record the exact candidate, evidence and locator, observation or calculation performed, result, consequence for use, and unsupported stronger claim. Distinguish source/inspection failure from financial uncertainty. Preserve refuted challenges rather than silently deleting them.

## Capability failure and stopping

Use the approved capability route. A permission denial, unsupported operation, or user-declined access returns a precise limitation; do not retry unchanged calls or bypass the restriction. A transient failure permits only the bounded retry authorised in the recipe. Continue unrelated checks that remain meaningful.

Stop after the declared checks and warranted discriminating probes. Additional questions must identify a changed decision and useful observation. Do not hold the whole model hostage to a peripheral uncertainty.

Return `VERIFICATION_RECORDED`, `PARTIAL_VERIFICATION_RECORDED`, or `VERIFICATION_BLOCKED`, plus proposition results and scope. The concierge reconciles those results with unresolved dependencies; only the authorised analyst disposes of the exact candidate.

## Small example

The reviewer finds no problem with a workbook whose reported tax cell was altered to make net income agree with an adjusted release. If preservation of the reported tax figure is a baseline assertion, open the permitted original and inspect the actual cell anyway. A zero-length challenge list cannot satisfy that check.

`.knowledge-sdlc/references/buy-side-method/semantic-contracts.md` defines the receipt. `.knowledge-sdlc/references/buy-side-method/cross-context-recipe.md` owns sequencing and acceptance amendments.
