# Expert-owned method extensions

## Purpose

The core supplies commissioning, evidence, challenge, authority, continuity,
and learning discipline. It cannot contain every domain method a professional
lead already knows. Extensions let that lead bring a better method without
turning it into ambient instruction or modifying the core.

Use an extension for a repeatable professional procedure: an investment
research method, diligence checklist, modelling convention, interview method,
or house review standard. Do not use one for facts about the current project,
the layout of one client workbook, access to a live tool, or a preference
learned from one correction; those have different owners.

## Lifecycle

```text
import bytes
→ curate purpose, authority, contract and conflicts
→ human/expert admits immutable revision A
→ one run binds A explicitly
→ update creates immutable revision B
→ old run still resolves A; new run may bind B
→ unbind, suspend, retire, or remove eligibility
```

Ask in ordinary language to import, inspect, update, bind, unbind, retire, or
remove an expert method. The entry skill routes the request to
`kw-expert-extension`; no registry automatically selects it.

For example:

```text
Import and curate methods/customer-retention/ as a project method. Preserve its
source bytes, show me its authority and conflicts, and do not select it for a
run merely because it is installed.
```

Project custody lives under:

```text
ai_docs/methods/extensions/<extension-id>/
  revisions/<revision-id>/
    method files
    extension.md
```

Each immutable revision records owner and use basis, licence, purpose, inputs,
outputs, tools/capabilities, allowed and prohibited effects, precedence,
conflicts, content inventory/hashes, and the exact digest a later decision must
target. Separate decision artefacts record admission, rejection, suspension,
or retirement. The neutral methods index alone carries current eligibility; a
run record binds one exact eligible revision and its permitted effect.

## Curation is not copying

Import proves custody only. Admission refuses unknown ownership, illicit tools,
hidden executable instructions, prompt-injection content, claims to human or
protected authority, silent core overrides, or an incoherent input/output
contract. A lead may amend the method, narrow its scope, or reject it.

An optional provider-native copy is a separate explicit installation action. It
does not select the extension for a run, and provider configuration never
becomes the portable authority.

A lead-owned bundle may adapt professional vocabulary and method cues, but it
cannot change the generic initiative/run grammar, manufacture evidence, or
acquire protected-write and human authority. The core ships no profession-
specific method bundle; the lead supplies the method to be curated.
