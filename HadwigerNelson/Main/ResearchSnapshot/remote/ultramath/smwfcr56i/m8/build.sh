#!/bin/bash
# usage: ./build.sh <Module.Name> ...   compiles work/<path>.lean -> lib/<path>.olean
set -u
export LEAN_PATH="$PWD/lib:$LEAN_PATH"
rc=0
for m in "$@"; do
  o="lib/${m//./\/}.olean"
  mkdir -p "$(dirname "$o")"
  s=$(date +%s%N)
  out=$( cd work && lean -o "../$o" "${m//./\/}.lean" 2>&1 )
  st=$?
  e=$(date +%s%N)
  printf '%s\n' "$out" | head -80
  printf '[%s rc=%d %d ms]\n' "$m" "$st" $(( (e-s)/1000000 ))
  [ $st -eq 0 ] || rc=1
done
exit $rc
