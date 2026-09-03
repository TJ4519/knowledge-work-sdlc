# Maintaining the harness

The maintenance rule is one semantic authority, generated delivery views, and
tests proportional to what code can actually prove.

## Read before changing structure

Read in this order:

1. [`docs/methodology.md`](../methodology.md) for the governing function and
   invariants;
2. [`DESIGN.md`](../../DESIGN.md) for file, runtime, and authority boundaries;
3. the guide for the mechanism being changed;
4. root [`AGENTS.md`](../../AGENTS.md) for always-loaded behaviour; and
5. the exact skills, agents, recipes, and templates on the affected journey.

Do not begin from generated plugin bytes or an installed workspace. Their
purpose is to expose the canonical source to a host, not to become editable
method authorities.

## Canonical sources

```text
AGENTS.md                     standing operating contract
.knowledge-sdlc/skills/       interactive and main-context procedures
.knowledge-sdlc/agents/       bounded fresh specialist definitions
.knowledge-sdlc/recipes/      human-readable composition defaults
.knowledge-sdlc/templates/    durable artefact shapes
docs/ + DESIGN.md             explanation and operator guidance
```

`tooling/projection.py` generates repository and plugin views from those
sources. The repository view puts skills under `.agents/skills/` for discovery
and managed resources under `.knowledge-sdlc/`. The plugin view puts generated
skills and agents at plugin root and method resources under `resources/`.
Neither projection may contain an independently maintained prompt body.
Provider-native enforcement fields are generated from the canonical contract;
for example, Claude agent `tools` derive from `allowed_tools`.

## What each Python module is allowed to do

| Module | Mechanical responsibility | Forbidden semantic responsibility |
|---|---|---|
| `contracts.py` | Parse declarations and verify method/recipe I/O relations | Decide which recipe or method a commission needs |
| `projection.py` | Render exact host-facing files and compare them with canonical bytes | Rewrite professional instructions for a host |
| `installer.py` | Plan, collision-check, stage, apply, upgrade, recover, and validate owned files | Infer ownership, project policy, or configured state |
| `release.py` | Create a deterministic archive and content manifest from a clean commit | Claim native activation or professional quality |
| `util.py` / `errors.py` | Shared parsing, hashing, rendering, and error types | Acquire runtime authority |

If a capable, well-instructed agent can perform a proposed function and the
function depends on meaning, evidence, professional judgement, or human
authority, it belongs in the model-mediated method rather than Python. Code is
retained where repeatable byte-level safety is the product promise.

## Change sequence

1. Name the user-visible behaviour and the invariant it must preserve.
2. Trace the journey through activation, authority, durable state,
   installation, provider projection, and continuation.
3. Change the canonical source only.
4. Update the explanatory document that owns the reason.
5. Run the focused test for the mechanical contract, then the complete local
   validation once.
6. Inspect the generated workspace or plugin when the change affects
   distribution.
7. Commit the coherent source revision before building a release archive.

Do not add a schema, receipt, registry, or test merely to make development look
more governed. Add one only when it detects a plausible failure in a retained
mechanical promise or supplies a named consumer with information no existing
artefact owns.

## Local validation

```bash
make validate
```

This checks:

- method and recipe declarations close mechanically;
- repository and plugin projections are deterministic and canonical;
- installation, upgrade, rollback, and recovery preserve client boundaries;
- package identities and versions agree; and
- public documentation links and runtime names remain coherent.

A passing suite does not show that a natural request activated the method, that
the professional answer is useful, or that a provider supplied an independent
reviewer. Observe those properties through representative real work, compare a
no-harness response when attribution matters, and retain only the evidence
needed to diagnose a consequential failure.

## Package and release

After validation, commit the source and ensure the checkout is clean:

```bash
git status --short
make package
```

`release.py` refuses a dirty tree because the archive manifest must name one
exact reproducible source commit. Inspect the generated ZIP and manifest under
`dist/`, validate it with the target host where available, and distribute it
only under the repository's licence and product authority.

Version changes belong in `.knowledge-sdlc/VERSION` and `CHANGELOG.md` together.
A Git commit, package build, provider installation, native field observation,
tag, and external publication are different events; record only the event that
actually occurred.
