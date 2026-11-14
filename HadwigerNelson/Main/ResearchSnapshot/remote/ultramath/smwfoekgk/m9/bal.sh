#!/bin/bash
# build helper: $1 = tree root (dir containing OAI), $2 = build dir, rest = module names
set -e
T=$1; B=$2; shift 2
export LEAN_PATH="$(cd $B && pwd):$LEAN_PATH"
for n in "$@"; do
  out="$B/$(echo $n | tr . /).olean"
  mkdir -p "$(dirname $out)"
  ( cd "$T" && time lean -o "$(cd $(dirname $out) && pwd)/$(basename $out)" "$(echo $n | tr . /).lean" )
done
