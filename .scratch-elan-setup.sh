#!/usr/bin/env bash
# Reproducible, task-local Lean/Mathlib v4.35.0 setup for THIS checkout.
#
# Guarantees:
#   * resolves an already-validated installation, or bootstraps one from the
#     official elan installer (https://github.com/leanprover/elan) into a
#     task-local directory; never writes to /opt;
#   * does NOT modify lean-toolchain or lakefile.toml (repository pins stay);
#   * cd's to its own checkout before doing anything;
#   * clears any inherited LEAN_PATH so the pinned toolchain is actually used
#     (an inherited LEAN_PATH makes `lean` silently use a foreign Mathlib);
#   * verifies the pinned lean/lake versions before declaring success;
#   * reuses the existing Mathlib artifact cache (no needless reinstall).
#
# Usage:  ./.scratch-elan-setup.sh          # set up + verify + build
#         ./.scratch-elan-setup.sh --env    # set up + verify, print exports
set -euo pipefail

PINNED="v4.35.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# --- locate a usable ELAN_HOME ------------------------------------------------
# Candidates, in order: an explicitly supplied ELAN_HOME, a task-local one inside
# this checkout, and the project-root one used during the first successful
# installation (.scratch/elan of the SAIR project root, i.e. the parent of the
# checkout). The first that actually contains the pinned toolchain wins.
CANDIDATES=()
[ -n "${ELAN_HOME:-}" ] && CANDIDATES+=("$ELAN_HOME")
CANDIDATES+=("$SCRIPT_DIR/.scratch/elan")
CANDIDATES+=("$(dirname "$SCRIPT_DIR")/.scratch/elan")
[ -d "$HOME/.elan" ] && CANDIDATES+=("$HOME/.elan")

ELAN_HOME=""
for c in "${CANDIDATES[@]}"; do
  if [ -x "$c/bin/elan" ] && [ -d "$c/toolchains/leanprover--lean4---$PINNED" ]; then
    ELAN_HOME="$c"; break
  fi
done

if [ -z "$ELAN_HOME" ]; then
  echo "== no validated elan installation found; bootstrapping task-local one" >&2
  ELAN_HOME="$SCRIPT_DIR/.scratch/elan"
  mkdir -p "$(dirname "$ELAN_HOME")"
  if [ -x "$ELAN_HOME/bin/elan" ]; then
    :
  else
    TMP_INST="$(mktemp -d)"
    echo "   downloading official elan installer" >&2
    curl --fail --silent --show-error --location \
      https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh \
      -o "$TMP_INST/elan-init.sh"
    # official installer; --no-modify-path keeps it out of shell rc files
    sh "$TMP_INST/elan-init.sh" -y --no-modify-path --default-toolchain none \
      --install-dir "$ELAN_HOME" >/dev/null
    rm -rf "$TMP_INST"
  fi
fi

export ELAN_HOME
export PATH="$ELAN_HOME/bin:$PATH"
unset LEAN_PATH LEAN_SRC_PATH LEAN_PATH_EXTRA

echo "== ELAN_HOME=$ELAN_HOME"

# --- install the pinned toolchain only if absent ------------------------------
if [ ! -d "$ELAN_HOME/toolchains/leanprover--lean4---$PINNED" ]; then
  echo "== installing leanprover/lean4:$PINNED (official release)" >&2
  elan toolchain install "leanprover/lean4:$PINNED"
else
  echo "== toolchain leanprover/lean4:$PINNED already present"
fi

# --- verify the pinned versions BEFORE touching Mathlib -----------------------
echo "== resolved toolchain: $(elan show 2>/dev/null | head -1)"
LEAN_V="$(lean --version | head -1)"
LAKE_V="$(lake --version | head -1)"
echo "== $LEAN_V"
echo "== $LAKE_V"
case "$LEAN_V" in
  *"version 4.35.0"*) : ;;
  *) echo "FATAL: lean is not the pinned 4.35.0: $LEAN_V" >&2; exit 1 ;;
esac
if ! grep -q "leanprover/lean4:$PINNED" lean-toolchain; then
  echo "FATAL: lean-toolchain does not pin $PINNED (pins were changed?)" >&2
  cat lean-toolchain >&2; exit 1
fi
command -v lean | grep -q "$ELAN_HOME" \
  || { echo "FATAL: lean resolves outside ELAN_HOME" >&2; exit 1; }

# --- reuse or fetch the Mathlib artifact cache --------------------------------
if [ -d .lake/packages/mathlib/.lake/build/lib/lean ] \
   && [ -n "$(ls -A .lake/packages/mathlib/.lake/build/lib/lean 2>/dev/null)" ]; then
  echo "== Mathlib artifact cache already present; not re-downloading"
else
  echo "== fetching official Mathlib v4.35.0 artifact cache"
  lake exe cache get
fi

if [ "${1:-}" = "--env" ]; then
  echo
  echo "export ELAN_HOME=\"$ELAN_HOME\""
  echo "export PATH=\"\$ELAN_HOME/bin:\$PATH\""
  echo "unset LEAN_PATH"
  exit 0
fi

echo "== lake build ZetaFive"
lake build ZetaFive
