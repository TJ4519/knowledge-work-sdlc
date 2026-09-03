---
name: kw-prime
description: "Resume one initiative from its run record and named output artefacts after a new session, compaction, or replacement agent."
primitive: skill
fresh_context: false
independence: main-agent-recovery
allowed_tools: ["Read", "Grep", "Shell", "Write"]
inputs: ["initiative-catalogue", "run-record"]
optional_inputs: ["linked-output-artefacts", "domain-charter", "git-history", "provider-attestation"]
excluded_context: ["old-transcript", "superseded-artefacts", "unrelated-initiative-content", "generated-recap", "unselected-reusable-lesson"]
outputs: ["recovery-view", "initiative-route"]
authority: reconstruction-only
standalone: true
idempotency: "Repeated recovery from the same run record and linked artefact revisions yields the same current obligation unless newer durable evidence exists."
phase: recovery
---
# Prime and recovery

Recovery means the main agent can continue one confirmed initiative from durable
state. It does not mean replaying hidden reasoning or rebuilding a transcript.

## Trigger

Load on a fresh session, after compaction or actor replacement, or whenever the
current obligation is uncertain. Run inline so the durable artefacts enter the
main agent's own context.

## Method

1. Read `ai_docs/initiatives/index.md` only. If it is absent and initiative
   directories exist, reconstruct the compact index from their run records as a
   recovery action before selecting; never create a blank index over retained
   work. If neither index nor initiative content exists, there is nothing to
   resume: load `knowledge-work` for a new commission. A named initiative or an
   unambiguous “continue” against the proposed focus confirms selection;
   otherwise show compact candidates without substantive contents.
2. Read the active/latest run record identified by the selected index row. Read
   a predecessor record only when the active record names it as a required
   dependency.
3. Read the current meaning revision, exact decisions, and every live output
   artefact the run record names as required for its next action. Do not replace
   those reads with summaries.
4. Verify paths and hashes where recorded. Check that plan, stage outcomes,
   gates, unresolved matters, and next legal action agree with the named
   artefacts.
5. Treat `complete` as a claim. If an earned review, authority, promotion,
   reconciliation, or recovery obligation remains open, do not rewrite the
   closed record. Open a successor recovery/correction run linked to it, make the
   missing obligation the plan, and update the index.
6. Resume an `open` or `halted` run in its existing record. Do not mint a new
   run because the conversation or model changed.
7. Check external state whose freshness can change the next action. Use Git or
   provider attestation when present, but label their absence honestly.
8. State a compact recovery view: accepted intent, latest completed stage, live
   outputs, material uncertainty, and next action. Then load
   `kw-orchestration` and continue without asking the user to reconstruct
   durable facts.

Any recovery repair follows the entry skill's run-and-artefact save contract:
write recovered or superseding semantic artefacts first, update the open run
record, then update the index. Do not create a parallel reconstruction summary.

## Failure paths

- **Missing run record:** inspect retained initiative outputs and Git only far
  enough to identify what can be proved. Open a recovery run that labels missing
  history, or stop on the exact unrecoverable dependency; never invent events.
- **Missing current meaning:** the commission boundary is absent. Recover exact
  wording from provider observation or user evidence when possible and label the
  source; otherwise ask for the smallest missing fact.
- **Run lacks a next action:** infer the strongest next step from its plan and
  outputs only when consequence is low; otherwise expose the decision.
- **Linked required artefact missing:** name the exact dependency and downstream
  claim it blocks. Do not substitute an old recap.
- **Index/run mismatch:** trust neither by position. Resolve from the run records
  and artefacts, record the repair in an open run, then correct the index.

## Lessons firewall

Do not preload `ai_docs/LEARNINGS.md` or full lessons during recovery. A lesson
already selected for the current run must be linked through its exact decision
artefact. Any new nomination occurs only after current meaning is reconstructed
and while the named effect is still pending.

## Non-authority

Prime reconstructs and continues. It does not reinterpret settled meaning,
accept a candidate, admit a lesson, or grant consequential authority.
