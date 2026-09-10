# Installation and provider boundaries

Knowledge Work SDLC has one authored method and two generated delivery shapes.

```text
source repository
  canonical methods + docs + mechanical author tooling

repository installation
  managed AGENTS block + discoverable skills + method resources
  + compact initiative index inside one client repository

plugin archive
  Codex and Claude manifests + generated skills/agents + method resources
```

The installed workspace and plugin are deterministic projections. They are not
second authored copies of the method.

## Repository installation

Prerequisites: Python 3.10 or newer and an existing client repository.

The ordinary route is agent-led. Give an agent attached to the client
repository the installation message in the root README. It acquires this source
in a temporary directory outside the client repository, previews the plan,
checks the existing instructions, and applies the install only when both checks
pass. The agent must not change branches, commit, push, or clone this source
inside the client repository unless the user separately requests that action.

The equivalent manual commands are:

```bash
git clone https://github.com/TJ4519/knowledge-work-sdlc.git
cd knowledge-work-sdlc
./install.sh --dry-run /absolute/path/to/client-repository
./install.sh /absolute/path/to/client-repository
```

Fresh-install dry-run validates the target and complete payload, reports every
planned file and the proposed `AGENTS.md` action, and performs no writes. It
also states that semantic review remains required; deterministic code cannot
decide whether two natural-language instruction sets agree.

Apply refuses unsafe paths and collisions, stages and validates the payload,
then writes only inside the named repository. An existing `AGENTS.md` and
existing client-owned `.agents/skills/` content are preserved. Managed files
are listed in `.knowledge-sdlc/install.json`; project state under `ai_docs/`
becomes client-owned immediately.

For Codex, open the client repository as a new task or start a new CLI session
from its root. Codex reads root-to-leaf `AGENTS.md` guidance before work and can
activate project skills by description. See the official
[AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and
[skills](https://learn.chatgpt.com/docs/build-skills) documentation.

Another host may use the same repository projection only if it actually reads
the managed `AGENTS.md` block and discovers the projected skills. Verify those
behaviours on that host rather than inferring compatibility from file shape.

## Upgrade and recovery

Upgrade only a workspace previously installed by version 0.6 or later. Preview
first:

```bash
./install.sh --upgrade --dry-run /absolute/path/to/client-repository
./install.sh --upgrade --apply /absolute/path/to/client-repository
```

Upgrade refuses edited managed files, an edited managed `AGENTS.md` block, and
new managed paths occupied by client content. It never replaces `ai_docs/`.

If an interrupted upgrade leaves
`.knowledge-sdlc/UPGRADE_RECOVERY.json`, normal upgrade refuses to guess. Restore
the recorded prior managed bytes with:

```bash
./install.sh --recover /absolute/path/to/client-repository
```

The recovery command validates the marker and backup before changing anything.
A legacy 0.5 workspace has no compatible ownership record; install 0.6 into a
clean client repository or perform a separately reviewed migration.

## Build the plugin archive

Packaging is a maintainer operation and requires a clean committed checkout:

```bash
make validate
make package
```

The output is `dist/knowledge-work-sdlc-harness-v0.6.1.zip` plus a manifest that
binds every packaged path to its SHA-256 and the exact source commit. The
archive contains no Python or lifecycle hooks. It supplies methods and
specialists; credentials, connectors, and client files remain host- or
workspace-owned.

## Claude Code

Extract the archive to a dedicated directory, then load that directory for a
new process:

```bash
mkdir -p /absolute/path/to/knowledge-work-sdlc-plugin
unzip dist/knowledge-work-sdlc-harness-v0.6.1.zip \
  -d /absolute/path/to/knowledge-work-sdlc-plugin
claude --plugin-dir /absolute/path/to/knowledge-work-sdlc-plugin
```

Claude Code documents `--plugin-dir` as its local development/test route and
discovers `skills/` and `agents/` at plugin root. See
[Create plugins](https://code.claude.com/docs/en/plugins).

## Claude Cowork

In the Claude desktop app:

1. open **Cowork**;
2. open **Customize → Plugins**;
3. add a custom plugin and select the generated ZIP; and
4. attach or grant access to the client workspace before stating a commission.

Anthropic documents custom plugin upload and notes that plugin skills and
subagents run in Cowork. See
[Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude).

The package deliberately has no append-log hook. User-defined lifecycle hooks
are not required for continuity: the main agent writes material semantic events
to the initiative, and a fresh session reconstructs from those files. If a
particular Cowork environment exposes transcripts, telemetry, or organisation
infrastructure, those remain optional observation sources rather than canonical
memory.

## Codex plugin distribution

The archive also contains `.codex-plugin/plugin.json`. ChatGPT and Codex install
shared plugins through their plugin directory; local development uses a local
marketplace, while the repository-install route above remains the shortest way
to test this harness against a local project. See the official
[Codex plugin](https://learn.chatgpt.com/docs/plugins) and
[build-plugins](https://learn.chatgpt.com/docs/build-plugins) documentation.

## Capability boundaries

A plugin can carry instructions for using a facility; it does not make that
facility available. At run time the orchestrator derives semantic needs from
the concrete plan, then checks the actual host:

```text
required operation
→ visible facility
→ reachable asset
→ authentication and scope
→ harmless same-actor proof
→ bind, degrade, or stop
```

The user may already have Excel, a connector, an MCP server, a CLI, or no
relevant facility. The method adapts to observed capability instead of shipping
a hard-coded connector registry. One provider's successful operation never
proves another provider can perform it.

Provider instructions and linked product documentation were checked on
2026-09-02. Product interfaces can change; keep the method invariant and update
only the host-specific route when they do.
