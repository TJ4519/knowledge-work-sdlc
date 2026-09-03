---
name: kw-learning-governance
description: "Record one exact authorized retain, amend, reject, suspend or retire decision over one source-linked lesson."
primitive: skill
fresh_context: false
independence: main-agent-human-gate
allowed_tools: ["Read", "Shell", "Write"]
inputs: ["lesson-candidate", "exact-governance-decision"]
optional_inputs: ["retained-lesson"]
excluded_context: ["unrelated-initiative-content", "automatic-selection-score", "method-change-proposal"]
outputs: ["lesson-disposition"]
optional_outputs: ["retained-lesson"]
authority: exact-user-decision
standalone: true
idempotency: "The same human decision yields one lesson revision and one current index pointer; it never creates duplicate active entries."
phase: feedback-governance
---
# Learning governance

Govern one proposition at a time. Evidence retention, lesson admission and
method change are separate decisions.

## Decision surface

Show the user the candidate statement, exact source, scope, rival reading,
exclusions and proposed allowed effect. Accept these decisions:

- **Retain:** admit the candidate as stated.
- **Amend:** admit only the user's revised statement, scope, exclusion or
  allowed effect.
- **Reject:** keep the candidate and exact decision in its source initiative but do
  not add it to the active catalogue.
- **Suspend:** make an admitted lesson ineligible while preserving its history.
- **Retire:** end future eligibility while preserving prior selections and
  outcomes.

## Method

1. Verify that the candidate links to source-initiative evidence.
2. Preserve the exact authorized decision, decision-maker role, capture quality
   and identity basis beside the candidate. This is the user's exact decision;
   neither a test fixture nor an agent inference can supply it.
3. For Retain or Amend, create one immutable revision at
   `ai_docs/learnings/<lesson-id>-rN.md`. Include statement, kind, scope,
   exclusions, allowed effect, source, reconsideration condition and active
   status. If `ai_docs/LEARNINGS.md` does not yet exist, instantiate it from the
   bundled template now; absence means no retained lesson, not incomplete setup.
   Add only the lesson's short label, scope cue, status, source initiative and
   link to the compact discovery index. Verify that the
   catalogue identifier, label and scope cue do not reveal the lesson's
   operative instruction, facts or allowed effect. Use a neutral stable ID and
   analogy cue; otherwise the index itself bypasses deliberate selection.
   A later amendment writes a successor revision and updates the compact pointer;
   it never mutates a revision already selected or targeted.
4. For Reject, leave the immutable candidate in the source initiative and link
   the rejection decision from the run; do not create an active catalogue entry.
5. For Suspend or Retire, write a successor lesson revision with the new status
   and update the compact index pointer/status. Link the exact decision and prior
   revision; never erase earlier wording, selections, uses, or outcomes.
6. Preserve the exact governance decision as its own decision artefact targeting
   the candidate path/hash. Link candidate, decision, and any retained lesson
   from the open run record and set the next action; never mutate the decision
   target. If the prior run is closed, use a successor governance run.

## Non-authority

This skill records exact governance authority without inflating its identity
or scope. It does not infer consent, select a lesson for later work, treat a
lesson as present evidence or alter `AGENTS.md`, skills, recipes or protected
artefacts.
