# Getting started

This guide takes one ordinary request through installation, useful output, a
material correction, and continuation in a fresh task.

## Before you install

You need:

- a client repository you are authorised to change;
- Python 3.10 or newer for the source-repository installer; and
- a file-aware agent host that reads repository `AGENTS.md` instructions and
  project skills, or a supported plugin host.

The repository installation is the shortest Codex route. It writes only inside
the explicit client repository. It does not change global skills, provider
settings, credentials, or another project.

## 1. Install into the client repository

The ordinary route is to send the copyable installation message in the root
README to an agent attached to the client repository. The agent retrieves the
source outside the repository, previews the exact writes, checks existing
instructions, and installs without choosing a branch or committing changes.

The manual equivalent from a clean Knowledge Work SDLC checkout is:

```bash
./install.sh --dry-run /absolute/path/to/client-repository
./install.sh /absolute/path/to/client-repository
```

The command prints a JSON inventory and `"validation_passed": true` on success.
It adds one marked block to an existing `AGENTS.md`, creates one host-discoverable
skill corpus, installs managed agents, recipes and templates, and creates only
the compact initiative index.

```text
client-repository/
  AGENTS.md                         client instructions + one managed block
  .agents/skills/                   runtime-discoverable procedures
  .knowledge-sdlc/
    agents/                         bounded specialist definitions
    recipes/                        readable composition defaults
    templates/                      shapes for earned durable artefacts
    references/                     shared optional method guidance
    install.json                    managed-file ownership for safe upgrade
  ai_docs/initiatives/index.md      identity, focus, status, run pointer
```

The installer does **not** pre-create a domain charter, source policy, method
library, protected-artifact register, or learning store. Those files acquire
meaning only when evidence or a human decision earns them.

The normal installation also includes four optional buy-side company-model
skills and their shared references. See the [buy-side first-use guide](guides/buy-side-method.md)
for an analyst-facing prompt and the distinction between availability, selected
support, the firm's own method and permission to change a workbook.

## 2. Open a genuinely new task

Open the client repository as the task's project or working directory. State a
real professional commission without naming an internal skill:

```text
Review the two source packs in inputs/. Tell me whether the renewal weakness is
better explained by onboarding friction or product risk. Give me a one-page
decision brief, distinguish management claims from customer evidence, and say
what would change your conclusion.
```

The main agent should:

1. preserve the request's exact wording;
2. inspect the named sources before asking for facts already available;
3. expose only an ambiguity that could materially change the work;
4. compose a proportional route rather than running every available method;
5. return the decision brief visibly; and
6. leave enough durable state for another capable agent to inspect and resume.

At minimum, the workspace should now contain one initiative index row, one
initiative directory, `meaning-r1.md`, and one run record under
`run-record/<run-id>.md`. Evidence maps, work orders, candidates, challenges and
decisions appear only when the commission earns them. Their exact paths are
linked from the run record; there is no second master summary.

## 3. Correct the governing meaning

Correct the work in ordinary language:

```text
One correction: logos retained on downgraded contracts still count as churn for
this decision. Update every affected conclusion; do not append a caveat while
keeping the old premise.
```

The correction should create a superseding meaning revision, identify the
claims and outputs that depended on the old definition, and re-enter the method
that owns each affected candidate. Prior revisions remain inspectable. The
visible result is a corrected work product plus any limitation that still
matters, not a ledger in place of the work.

## 4. Continue from a fresh task

End the task. Open the same client repository in a genuinely new task or host
process, without copying the old conversation, and say:

```text
Continue the renewal initiative from its next warranted action.
```

The main agent reads only the compact index first, confirms the intended
initiative, then loads its current run record, meaning revision, exact
decisions, and named live outputs. It should recover the corrected definition,
remaining uncertainty, and next legal action without asking you to reconstruct
the previous session.

## 5. Try a different commission family

The same entry route can support other work:

- **Interpret a source:** “Reconcile these two definitions of active customer
  and tell me which one this metric actually uses.”
- **Challenge a candidate:** “Try to falsify this recommendation against the
  source pack; rank only defects that could change the decision.”
- **Update protected work:** “Update the actuals in a candidate copy of this
  workbook, preserve every forecast cell, and stop if this host cannot validate
  the native file.”
- **Bring a lead-owned method:** “Import and curate this research procedure for
  project use. Do not select it merely because it is present.”
- **Consider reusable feedback:** “That correction prevented a material error.
  Assess whether it warrants a narrowly scoped lesson, but do not retain or use
  it without my decision.”

Client templates and live tools require additional bindings. See
[Protected work and runtime capabilities](guides/protected-work-and-capabilities.md).
Lead-owned methods use the lifecycle in
[Expert-owned method extensions](guides/expert-extensions.md).

## If the route cannot complete

A missing source, unavailable connector, absent native-file editor, or required
independent reviewer may narrow or halt the work. The agent should still return
the useful candidate produced so far, state exactly what it supports, and name
one executable next action. A blocked gate must not make completed semantic
work disappear behind internal files.
