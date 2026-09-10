# Buy-side skills are included in the normal installation

The package includes four optional skills for public-equity company-model work: clarify the requested treatment, produce a candidate update, challenge its reasoning, and verify consequential claims. They help keep sources, calculations, assumptions and review evidence connected. They are not a complete stock-selection or valuation system, and they do not supply a firm's model, paid research or an Excel engine.

## Install a current main checkout into your own client repository

The ordinary route is to give an agent attached to the intended client repository
the installation message in the root README. It retrieves current main outside
the client repository, previews all writes, checks the existing instructions for
conflicts, and installs only when those checks pass. The tester does not need to
operate Git. See [installation and provider boundaries](installation-and-providers.md).

The manual equivalent, from the Knowledge Work SDLC source checkout, is:

```bash
./install.sh --dry-run /absolute/path/to/client-repository
./install.sh /absolute/path/to/client-repository
```

The target must already be a Git repository. If this is a new test workspace, create the directory and initialise Git there first. Open that client repository in a new agent task after installation. Use a fresh directory if a proposed destination already exists; do not replace someone else's files.

The standard installer includes all four skills under .agents/skills/ and one shared reference directory at .knowledge-sdlc/references/buy-side-method/. It creates no company policy, model, admitted house method or investment approval. Existing instructions are preserved with one managed block. A same-name existing skill or edited managed file causes an explicit collision, not an overwrite.

For an unedited existing SDLC installation, use the documented [guarded upgrade](installation-and-providers.md#upgrade-and-recovery). A separately copied older buy-side skill must be reconciled explicitly before upgrade; do not delete it merely to suppress the collision.

Plugin packages built from this source include the same skills and shared references. Check their VERSION; an older release archive may predate this addition. The source repository installation is the simplest route for this tester handoff.

## Start with the analyst's actual problem

For example:

```text
Use the bundled buy-side skills for this company-model update. Read my supplied
model, modelling instructions and sources first. Preserve the original.
Distinguish reported actuals, guidance and our forecast assumptions. Explain
what should change, what should stay, and what checks matter for my research
question. Ask only about choices that materially change the work or permissions.
```

Replace the example with the actual intended job. “Refresh actuals; preserve my forecast,” “reconsider this assumption,” and “test a separate scenario” authorise different changes. A missing workbook can still permit a useful read-only plan; it cannot justify inventing the model's contents. Existing useful analyst skills and conventions should be retained.

| Skill | What it returns |
|---|---|
| derive-buy-side-decision-to-data | A bounded brief: intended use, allowed changes, source basis and important checks |
| produce-evidence-bound-model-candidate | An actual candidate and account of changed, retained or unresolved work |
| challenge-frozen-buy-side-candidate | Evidence-linked objections, or an explicit no-finding result |
| verify-discriminating-buy-side-claims | Support, contradiction or uncertainty for checked propositions, even with no reviewer findings |

The main agent remains responsible for selecting the relevant helpers, resolving sources/capabilities, assigning genuinely separate checks where needed and delivering the explanation. This is not four always-running agents or a mandatory four-step chain.

## What should be visible in the return

The reader should receive the material result and its conditions first, then what was actually changed, why each important input was suitable for that use, which assumptions remained, and what was checked. Exact source and model locations should be reachable behind that explanation. Missing evidence, an uncalculated draft, self-review and a scoped independent check must remain distinct.

An analyst-supplied house method remains separately governed through [expert extensions](expert-extensions.md). Using the product's bundled support does not import or approve a house method, adopt a forecast or authorise replacing an original. A check of formulas does not prove that future assumptions will hold.

## Limits of this release

Distribution tests establish that the four skills and shared references are present, resolve in both layouts, and participate in normal install/upgrade protection. They do not establish native Excel operation, analyst acceptance or superiority over an ordinary capable agent. Real spreadsheet access, calculation, licensed-source permissions and fresh-context behaviour must be observed in the tester's environment. Use remains subject to the repository licence.
