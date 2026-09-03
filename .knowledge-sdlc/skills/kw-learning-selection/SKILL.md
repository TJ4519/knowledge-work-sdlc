---
name: kw-learning-selection
description: "After a new commission is interpreted without lesson content, disclose one neutrally nominated lesson and record one exact Select, Narrow, or Decline decision for a bounded pending effect."
primitive: skill
fresh_context: false
independence: main-agent-post-interpretation-selection
allowed_tools: ["Read", "Shell", "Write"]
inputs: ["meaning"]
optional_inputs: ["learning-index", "retained-lesson", "exact-selection-decision"]
excluded_context: ["lesson-content-before-meaning", "unrelated-initiative-content", "retired-or-suspended-lesson"]
outputs: []
optional_outputs: ["decision"]
authority: exact-user-selection
standalone: true
idempotency: "One exact decision binds at most one retained lesson to one pending effect; a later change supersedes that decision visibly."
phase: learning-selection
---
# Deliberate learning selection

Selection occurs only after the later initiative has an evidence-bearing working
interpretation. The firewall is created by context ordering, not by a length
check or a timestamp written after the fact.

## Two-context method

1. Complete intake and record the new initiative's settled meaning while
   reusable lesson statements are excluded from context. Before opening any
   learning file, name the first potentially lesson-affectable downstream step
   in the open run record and confirm that it has not yet produced an output.
   This records the usable boundary without a separate proof artefact.
2. Only after that boundary entry exists, inspect the compact index rows in
   `ai_docs/LEARNINGS.md`: ID, short label, scope cue, status and source initiative.
   Full statements live separately under `ai_docs/learnings/`; do not read
   them while deciding which row may be analogous. If the index does not exist,
   record no nomination and continue; absence means no retained lesson.
3. If no active row is plausibly analogous, record no nomination and continue
   the professional work. Do not open any full lesson. No nomination is an
   ordinary result, not a failed learning run.
4. If one active row may be analogous, record a neutral nomination using only
   that row, name the still-pending professional step, and expose the most
   important visible scope mismatch. Then read only that one linked lesson for
   disclosure. This bounded inspection is not authority to use it.
5. Explain the lesson's actual allowed effect, prohibitions and most important
   substantive mismatch. Recheck that the named step and effect remain pending;
   if either already occurred, record why the lesson cannot be used and never
   backdate an influence claim.
6. With the actual effect visible, offer one decision: Select, Narrow, or
   Decline. Silence is decline. Neither relevance, inspection, a fixture, nor an
   agent inference supplies selection authority.
7. On exact Select or Narrow, write one ordinary decision artefact before the
   named output exists. It records the exact human wording and identity basis,
   settled meaning path/hash, retained lesson revision, one named step, bounded
   allowed effect, and prohibited evidentiary/authority effects. Link it from the
   run record and pass only that decision to the named producer. Other workers
   receive neither lesson content nor a recap.
8. On Decline, record the decision in the run and continue without lesson
   content. Leave outcome review pending only for a selected decision.

## Host enforcement differences

A host with fresh contexts may perform intake and lesson selection in separate
actors. A portable host may perform them sequentially, but must not read lesson
content until meaning is durably recorded. The claim is limited to the boundary
the host actually enforces or the files visibly establish.

## Non-authority

A selected lesson may influence only the named question, ordering, method,
presentation or escalation step. It cannot establish current facts, increase
source confidence, grant authority or change the installed procedure.
Recorded ordering alone is insufficient: the named effect must also have
remained available when selection occurred.
