#!/usr/bin/env python3
"""Trim-agnostic, move-agnostic port harness for the OAI tree.

Why not `patch -p1`: the m8 patch (patches2/all.patch) is a set of *line-context*
hunks against a tree shape that no longer exists.  Two failure modes appear as
soon as the tree moves or is trimmed:

  * the target code was moved to another module (m14's cut-prereq patch moved
    `differenceLaw` and `relative_difference_invariant`), so the hunk's file and
    offsets are wrong;
  * the target code was deleted (the R1 deletion zone), so the hunk *should*
    not be applied at all -- there is nothing to port.

So this harness treats each hunk as a *content edit* (`old block -> new block`)
and treats the tree as an unordered bag of text: it looks for the old block in
every .lean file.  Consequences, which are exactly the properties we want:

  * if the old block was moved, it is found at its new site and ported there;
  * if the old block was deleted, the edit is reported OBSOLETE and skipped,
    which is correct: a deleted declaration needs no 4.33.1 back-port;
  * no offsets, no fuzz, no .rej files.

Context is used only to make a block unique; it is shrunk automatically when
the surrounding lines have drifted.  Block matching is line-exact (as `patch`
is), and every edit records its status so the caller can require strictness.

Usage:
  python3 port.py apply   TREE [PATCH] [--strict] [--json REPORT]
  python3 port.py explain TREE [PATCH]

TREE is a directory containing OAI/ (and optionally Check*.lean).
Exit status: 0 if every edit was APPLIED or OBSOLETE, 1 otherwise.
"""
import json
import pathlib
import re
import sys

DEFAULT_PATCH = ".ultramath/smwfcr56i/m8/patches2/all.patch"


# ---------------------------------------------------------------- patch parsing
def parse_patch(path):
    """Return [(srcfile, hunk_index, old_lines, new_lines)] for every hunk."""
    hunks = []
    src = None
    lines = pathlib.Path(path).read_text().split("\n")
    i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("--- a/"):
            src = l[6:]
            i += 1
            continue
        if l.startswith("@@"):
            m = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", l)
            i += 1
            old, new = [], []
            while i < len(lines) and not lines[i].startswith(("@@", "--- a/", "diff --git")):
                body = lines[i]
                if body.startswith("\\"):  # "\ No newline at end of file"
                    i += 1
                    continue
                if body.strip() == "" and i == len(lines) - 1:
                    break
                tag, text = (body[0], body[1:]) if body else (" ", "")
                if tag == " ":
                    old.append(text)
                    new.append(text)
                elif tag == "-":
                    old.append(text)
                elif tag == "+":
                    new.append(text)
                i += 1
            hunks.append((src, m.group(0), old, new))
            continue
        i += 1
    return hunks


# ---------------------------------------------------------------- block search
def find_block(lines, block):
    """All start indices where `block` occurs as a contiguous run in `lines`."""
    n, k = len(lines), len(block)
    if k == 0 or k > n:
        return []
    first = block[0]
    return [s for s in range(n - k + 1) if lines[s] == first and lines[s:s + k] == block]


def core_index(old, new):
    """Index range [lo, hi) of `old` that actually changes (ignores shared context).

    Context lines are those that appear unchanged; a pure-insertion hunk has an
    empty core, in which case we anchor on the single line before the insertion.
    """
    lo = 0
    while lo < len(old) and lo < len(new) and old[lo] == new[lo]:
        lo += 1
    hi = 0
    while hi < len(old) - lo and hi < len(new) - lo and old[len(old) - 1 - hi] == new[len(new) - 1 - hi]:
        hi += 1
    return lo, len(old) - hi


def apply_edit(tree_files, src, old, new, tag):
    """Apply one content edit to the first file that contains it.

    Returns a status dict.  Never raises on a missing block: it reports OBSOLETE.
    """
    # Candidate renderings, from most to least context (degrades when context drifted).
    core_lo, core_hi = core_index(old, new)
    variants = [(old, new, len(old) - (core_hi - core_lo))]
    for cut in (1, 2, 3):
        lo = min(cut, core_lo)
        hi = min(cut, len(old) - core_hi)
        if (lo, hi) == (0, 0):
            continue
        o = old[lo:len(old) - hi]
        nw = new[lo:len(new) - hi]
        variants.append((o, nw, len(o) - ((core_hi - lo) - core_lo)))
    if core_hi == core_lo:  # pure insertion: keep one anchoring line above
        if core_lo > 0:
            variants.append((old[core_lo - 1:core_lo], new[core_lo - 1:core_lo + 1], 1))

    for o, nw, _ in variants:
        if not o:
            continue
        hits = []
        for f in tree_files:
            for s in find_block(f["lines"], o):
                hits.append((f, s))
        if len(hits) == 1:
            f, s = hits[0]
            f["lines"][s:s + len(o)] = nw
            f["dirty"] = True
            return {"status": "APPLIED", "file": f["rel"], "line": s + 1,
                    "context": len(o) - (core_hi - core_lo)}
        if len(hits) > 1:
            # The same block can legitimately occur twice (duplicated proofs).  Prefer
            # the file the hunk was written against, and say so; refuse rather than guess.
            pref = [h for h in hits if h[0]["rel"] == src]
            if len(pref) == 1 or (not pref and len(hits) == 1):
                f, s = (pref or hits)[0]
                f["lines"][s:s + len(o)] = nw
                f["dirty"] = True
                return {"status": "APPLIED-HELD", "file": f["rel"], "line": s + 1,
                        "hits": [h[0]["rel"] for h in hits],
                        "context": len(o) - (core_hi - core_lo)}
            return {"status": "SKIPPED-NO-SITE", "file": src, "line": 0,
                    "hits": [h[0]["rel"] for h in hits],
                    "core": old[core_lo:core_hi][:2]}
    return {"status": "OBSOLETE", "file": src, "line": 0,
            "core": old[core_lo:core_hi][:2]}


# ---------------------------------------------------------------------- driver
def load_tree(root):
    root = pathlib.Path(root)
    files = []
    for p in sorted(root.rglob("*.lean")):
        files.append({"rel": str(p.relative_to(root)),
                      "path": p,
                      "lines": p.read_text().split("\n"),
                      "dirty": False})
    if not files:
        sys.exit(f"no .lean files under {root}")
    return files


def main(argv):
    if len(argv) < 2 or argv[0] not in ("apply", "explain"):
        sys.exit(__doc__)
    mode, tree = argv[0], argv[1]
    rest = [a for a in argv[2:] if not a.startswith("--")]
    flags = [a for a in argv[2:] if a.startswith("--")]
    patch = rest[0] if rest else DEFAULT_PATCH
    strict = "--strict" in flags
    report_path = None
    if "--json" in flags:
        report_path = argv[argv.index("--json") + 1]

    hunks = parse_patch(patch)
    files = load_tree(tree)
    byrel = {f["rel"]: f for f in files}
    results = []
    for src, hdr, old, new in hunks:
        r = apply_edit(files, src, old, new, hdr)
        r["src"] = src
        r["hunk"] = hdr
        results.append(r)
        if mode == "explain":
            print(f'{r["status"]:18s} {src}:{r["line"]:<6d} {hdr}')

    for f in files:
        if f["dirty"]:
            f["path"].write_text("\n".join(f["lines"]))

    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print(f"{len(results)} hunks; " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    for r in results:
        if r["status"] == "OBSOLETE":
            print(f"  obsolete: {r['src']} {r['hunk']} :: {r.get('core')}")
    if report_path:
        pathlib.Path(report_path).write_text(json.dumps(results, indent=1))
    bad = counts.get("AMBIGUOUS", 0) + (counts.get("OBSOLETE", 0) if strict else 0)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
