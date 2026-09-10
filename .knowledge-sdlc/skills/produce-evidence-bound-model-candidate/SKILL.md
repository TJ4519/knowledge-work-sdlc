---
name: produce-evidence-bound-model-candidate
description: "Carry out a bounded company-model update using the client's approved modelling method. Preserve reported detail, separate transformations and forecasts, account for intended changes and unresolved dependencies, and read back the actual candidate. Do not invent hybrid reported lines, silently switch sources, or force reconciliation by altering protected facts."
primitive: skill
fresh_context: false
independence: producer-no-self-approval
allowed_tools: ["Read", "Grep", "Shell", "Write"]
inputs: ["work-order"]
optional_inputs: ["source-snapshot","evidence-map","protected-artifact-snapshot","expert-method-binding"]
excluded_context: ["unrelated-initiative-history", "unadmitted-firm-method-as-authority", "producer-confidence-as-proof"]
outputs: ["candidate-protected-artifact-change"]
authority: candidate-support-only-no-professional-or-protected-authority
standalone: false
idempotency: "Reuse only for the same task, candidate, source and method identities and unchanged permitted use."
phase: production
references: [".knowledge-sdlc/references/buy-side-method/README.md",".knowledge-sdlc/references/buy-side-method/semantic-contracts.md",".knowledge-sdlc/references/buy-side-method/cross-context-recipe.md"]
---
# Produce a defensible model change

This optional bundled skill supplements the core SDLC and the analyst's own method. The main agent selects its bounded use in the current run; installation alone does not select it, admit a firm method, or grant workbook-write/use authority. Resolve `.knowledge-sdlc/...` reference cues from the repository's managed root, or the shared managed root declared by the plugin binding. Use the existing work-order, candidate, challenge and run records; these outputs do not require a new file family.

## Purpose and authority

Do the analyst's requested work, not merely populate a mapping table. Use their approved modelling skill, template, source policy, and scoped assumptions. This supporting skill adds evidence and change discipline; it is not a replacement forecasting method.

A useful incomplete result is preferable to counterfeit completion. But declaring `UNKNOWN` is not a substitute for reasonable in-scope investigation. Complete what is justified, explain what remains, and show which conclusions are affected.

You may read permitted evidence and change only the authorised candidate surface. A plan-only assignment permits no workbook editing. Do not overwrite the authoritative workbook, approve an exception, change core skills, obtain new entitlements, or send client data to another service on your own authority.

## Entry

Read the confirmed task brief, client method, original workbook or template, intended-change population, critical assertions, and route limitations. Check the exact inputs and operations you need at entry; reuse still-valid access evidence rather than repeating a whole setup ceremony.

If an essential input is absent, preserve completed work and return the precise missing fact or capability to the concierge. A missing connector does not authorise another source. An accessible summary is not proof that the original evidence was read.

## Understand before assigning

Reconstruct the meaning of the affected row, period, scenario, assumption, or formula from the actual workbook and task. Treat that interpretation as revisable, not a truth supplied by the row label.

Read each source on its own terms before fitting it to the target. Preserve the company, period, source role, reporting basis, units, useful row detail, and exact locator. Keep reported actual, restated comparative, management guidance, consensus, internal estimate, and analyst assumption distinguishable.

For repeated routine rows, one precise source-table reference and a recoverable row/range mapping can serve the group. Expand the explanation only for a meaningful difference, transformation, overlap, uncertainty, or protected judgment. Do not generate a paragraph per straightforward cell merely to demonstrate diligence.

## Preserve reporting structure and explain transformations

A subtotal and the components that constitute it are alternative representations of the same contribution. Establish whether rows overlap, are disjoint, or have an unresolved relationship before aggregating them. Neither matching labels nor a balancing total establishes that relationship.

Do not blend detailed statements and an abbreviated release into a new line described as company-reported. Keep the selected as-reported representation intact. If the template lacks necessary rows, make only the structural adaptation the user authorised, or propose it; preserve layout and scenario conventions where possible.

A source restriction remains a restriction when another website is easier. Conflicting permitted disclosures require a basis/vintage explanation, not averaging, silent preference, or an unsupported correction. Record a requested source change separately for the concierge.

Before a consequential assignment, state briefly: what this target needs; what the source establishes; the conversion, composition, or estimate being made; and any difference that the use would tolerate. More than one operation may apply. A conversion can still be a proxy, and a derived measure can be exactly reproducible without being a reported fact.

For an ambiguous case, test a plausible alternative: would using the neighbouring subtotal, another period, or another definition change the meaning? Which source detail settles it? Record only the decision-relevant explanation, not private chain of thought.

## Treat facts, estimates, and unresolved inputs differently

A reported fact must retain its source meaning. A legitimate analytical measure needs its inputs and declared method. A forecast needs its evidence, assumptions, scenario, and uncertainty; it need not have a published answer. Do not promote management guidance or consensus to the analyst's base case without the existing method or user instruction permitting that step.

An unresolved input is not zero and not permission for a silent carry-forward. Name whether the prior value is deliberately retained under an existing assumption, an alternative scenario is proposed, or the dependent output cannot support the requested current conclusion. Trace only relevant dependants; do not paralyse unrelated work.

Do not alter a reported tax figure, source value, or unrelated assumption solely to force agreement. Disclosure of an unauthorised plug does not make it acceptable. A legitimate balancing account or forecast rule must be defined by the approved model method and visibly kept separate from reported actuals.

## Apply and reconcile the actual result

Apply justified changes to the authorised candidate, retaining source references and client-owned layout. Record any permitted formula or structural changes. Do not claim a calculation occurred merely because formulas were written or cached values are present.

Read back the candidate using the available tools. Compare actual changes with the intended-change population and mappings, including protected formulas and relevant assumptions. Identify requested items that were omitted, not just changed cells. If the host cannot expose a required workbook surface, narrow the checked claim explicitly.

Account for each intended section or item as updated, checked and retained, unresolved with its consequence, or outside scope for a stated reason. Trace source meaning into its use and trace actual workbook changes back to their evidence. Neither direction alone is enough.

Recalculate or refresh only as authorised. Distinguish a produced workbook draft from a recalculated and checked workbook. A draft may be useful when clearly labelled; it cannot inherit a stronger assurance claim.

## Handoff and client output

Freeze the exact candidate and its basis before handing it to another role. Reuse existing initiative/result records for the brief, compact mappings, change/coverage record, calculation evidence, and exceptions; these need not become separate files.

Return: what was actually changed; what was deliberately not changed; source/basis decisions; effects on dependent conclusions; the candidate's identity; and what needs analyst judgment. The concierge, not this role, combines reports for the user.

Finish as `CANDIDATE_PRODUCED`, `PARTIAL_CANDIDATE_PRODUCED`, or `BLOCKED_FOR_THIS_TASK`, with separate factual statements about calculation and review status. None means approved for use.

## Small example

A source note supplies receivables −8, inventory −4, and payables +3, whose subtotal is −9. Including both the −9 subtotal and those components in the same sum double-counts the effect. A separate release's adjusted −6 cannot repair that mistake by substitution. Preserve the chosen reported representation or show a separately authorised adjustment bridge.

See `.knowledge-sdlc/references/buy-side-method/semantic-contracts.md` for the compact handoff fields. Do not spawn reviewers or grant use authority; `.knowledge-sdlc/references/buy-side-method/cross-context-recipe.md` owns those transitions.
