#!/usr/bin/env bash
# Source-repository wrapper for repository-local install and guarded upgrade.
# Nothing launched here participates in the client's agent lifecycle.
set -euo pipefail
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 [--upgrade --dry-run|--apply|--recover] /absolute/path/to/target-workspace" >&2
  exit 2
fi
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m tooling.installer --source-root "$ROOT" "$@"
