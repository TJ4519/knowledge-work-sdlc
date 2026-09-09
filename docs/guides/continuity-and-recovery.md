# Continuity and recovery

## Why summaries are insufficient

A conversational summary contains whatever the summariser happened to retain.
The harness instead makes each required fact durable in the file that owns it.
Fresh-session cost therefore scales with the current run and its live inputs,
not the length of the previous conversation.

## The recovery chain

```text
initiative index
→ user names or confirms one initiative
→ prime reads its active/latest run record
→ prime reads current meaning, exact decisions and named live outputs
→ prime checks freshness that can change the next action
→ orchestration continues the existing run or a linked successor
```

The compact index contains no initiative's substantive work. The main agent
reads it directly at the start of continuation; no lifecycle hook is required.

Before a consequential resumed return, `kw-prime` directs the main agent to
the evidence-backed delivery procedure in `kw-orchestration`. The agent must
reconcile the current candidate and relevant source or method state before
repeating an earlier assurance claim. An unchanged number does not guarantee
unchanged meaning, and a check of one revision does not automatically cover
another. Unknown dependency effects remain explicit review needs.

A saved presentation is a dated snapshot, not a monitor. Continuation should
produce a useful current explanation without requiring the user to reconstruct
the old conversation. No additional evidence ledger or automatic invalidation
engine is introduced.

Prime runs in the main context because its purpose is reconstruction. A
separate worker returning a recap would recreate the failure this mechanism
avoids.

## Conflicts and missing state

- If index and run disagree, neither wins by position. Resolve from run records
  and linked artefacts, record the repair, then correct the index.
- If a required output is missing, name the downstream claim it blocks. Do not
  substitute an old summary.
- If a closed run omitted an earned gate, keep it immutable and open one linked
  recovery/correction run.
- If the commission boundary cannot be recovered from exact retained wording,
  ask for the smallest missing fact rather than inventing history.

Reusable lessons are not part of ordinary recovery. A lesson already selected
for this run is linked through its exact decision. Any new nomination waits until
present meaning is reconstructed without lesson content.
