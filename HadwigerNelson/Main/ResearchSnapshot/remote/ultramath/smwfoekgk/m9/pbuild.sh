#!/bin/bash
# $1 tree dir, $2 out dir, $3 keep-lines-or-empty, then module list on stdin
set -u
T=$(cd $1 && pwd); O=$(cd $2 && pwd)
cd $T
LEAN_PATH="$O:$LEAN_PATH"
export LEAN_PATH
fail=0
one(){
  m=$1; out="$O/$(echo $m | tr . /).olean"; mkdir -p "$(dirname "$out")"
  if lean -o "$out" "$(echo $m | tr . /).lean" > /tmp/err_$$_$(basename $m).log 2>&1; then echo "OK   $m"; else echo "FAIL $m"; fi
}
export -f one
export O
cat | xargs -P 8 -I{} bash -c 'one {}' 2>&1
