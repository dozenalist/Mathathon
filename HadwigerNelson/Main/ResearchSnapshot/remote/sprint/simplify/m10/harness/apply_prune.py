#!/usr/bin/env python3
"""Apply PRUNE.json to a tree: delete unreferenced declarations and modules.

  python3 apply_prune.py --tree DIR --prune PRUNE.json [--dry]

TREE must contain lean/OAI/**.  Declarations are located by fully-qualified name
(or, when namespace tracking has drifted after another patch, by an unambiguous
short name), so the same prune file applies to the pristine 4.34.1 sources and to
the 4.33.1 port, whose line numbers differ.

Deletion rules, in order:
  1. a declaration's raw span is [attribute/doc block .. line before the next declaration];
  2. a comment block is deleted only as a whole -- a partially covered block is kept
     entirely, so no block comment is ever truncated;
  3. structural commands (`namespace`/`section`/`open`/`variable`/`end`/`instance`/...
     with their indented continuation lines) are never deleted.
Every rule is conservative: it can only keep lines, never delete a line that the
elaborator needs for structure.  The authoritative check is a full build.
"""
import argparse, json, pathlib, re

DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+|unsafe\s+|scoped\s+)*"
                  r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+([^\s:{(\[]+)")
NS = re.compile(r"^namespace\s+([\w.]+)\s*$")
SEC = re.compile(r"^(?:noncomputable\s+|private\s+|protected\s+|public\s+)?section(?:\s+[\w.]+)?\s*$")
MUT = re.compile(r"^mutual\s*$")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")
IMP = re.compile(r"^import\s+(OAI\.[\w.]+)\s*$")
ATTR = re.compile(r"^@\[")
STRUCT0 = {"open", "end", "namespace", "variable", "noncomputable", "omit", "import",
           "include", "instance", "section", "local", "universe", "attribute", "scoped",
           "mutual", "set_option", "example", "notation", "infix", "infixl", "infixr",
           "prefix", "postfix", "macro", "syntax", "elab", "deriving"}

def is_struct(ln):
    if not ln.strip(): return True
    if ln.startswith("#"): return True
    return ln.split(None, 1)[0] in STRUCT0

def comment_blocks(lines):
    """(start,end) 0-based inclusive for each /- ... -/ block."""
    blocks = []
    i = 0
    while i < len(lines):
        if "/-" in lines[i]:
            j = i
            while j < len(lines) and not (j > i and "-/" in lines[j]) and not (j == i and lines[i].count("-/") > 0 and lines[i].index("-/") > lines[i].index("/-")):
                j += 1
            blocks.append((i, min(j, len(lines) - 1)))
            i = j + 1; continue
        i += 1
    return blocks

def decl_spans(lines):
    stack, found = [], []
    for i, ln in enumerate(lines, 1):
        if NS.match(ln): stack.append(NS.match(ln).group(1)); continue
        if SEC.match(ln) or MUT.match(ln): stack.append(""); continue
        eo = END.match(ln)
        if eo:
            nm = eo.group(1)
            if nm and nm in stack:
                while stack and stack.pop() != nm: pass
            elif stack: stack.pop()
            continue
        d = DECL.match(ln)
        if d and d.group(2) not in ("where", "at", "at'"):
            pre = ".".join(x for x in stack if x)
            found.append((f"{pre}.{d.group(2)}" if pre else d.group(2), i))
    starts = []
    for full, i in found:
        s = i
        k = i - 2
        while k >= 0 and ATTR.match(lines[k]): s = k + 1; k -= 1
        if s >= 2 and lines[s-2].rstrip().endswith("-/"):
            k = s - 2
            while k >= 0:
                if "/-" in lines[k]: s = k + 1; break
                if "-/" in lines[k] and k != s - 2: break
                k -= 1
        starts.append((full, s))
    out = []
    for j, (full, s) in enumerate(starts):
        e = (starts[j+1][1] - 1) if j + 1 < len(starts) else len(lines)
        out.append((full, s, e))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True)
    ap.add_argument("--prune", default=str(pathlib.Path(__file__).resolve().parent / "PRUNE.json"))
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    tree = pathlib.Path(a.tree).resolve()
    pr = json.loads(pathlib.Path(a.prune).read_text())
    drop_by_mod = {}
    for name, v in pr["drop_decls"].items():
        drop_by_mod.setdefault(v["mod"], set()).add(name)
    drop_mods = set(pr["drop_modules"])
    no_block = set(pr.get("no_block", []))
    keep_attr = set(pr.get("keep_attr", []))
    imp_drop = {m: set(v) for m, v in pr["drop_imports"].items()}
    total = 0
    report = []
    for mod in sorted(set(drop_by_mod) | drop_mods | set(imp_drop)):
        p = tree / "lean" / (mod.replace(".", "/") + ".lean")
        if not p.exists():
            report.append(f"  MISSING {mod}"); continue
        lines = p.read_text().splitlines(keepends=True)
        if mod in drop_mods:
            total += len(lines)
            report.append(f"  -{len(lines):5d}  {mod}  (whole module)")
            if not a.dry: p.unlink()
            continue
        plain = [l.rstrip("\n") for l in lines]
        spans = decl_spans(plain)
        names = drop_by_mod.get(mod, set())
        if mod in keep_attr:
            keepn = set()
            for full, s0, e0 in decl_spans([l.rstrip("\n") for l in lines]):
                ln0 = plain[s0-1]
                if ln0.startswith("@[") or (s0 >= 2 and plain[s0-2].strip().startswith("@[")):
                    keepn.add(full)
            names = names - keepn
        short_count = {}
        for full, s, e in spans: short_count[full.split(".")[-1]] = short_count.get(full.split(".")[-1], 0) + 1
        prune_shorts = {n.split(".")[-1] for n in names}
        kill, hit = set(), 0
        for full, s, e in spans:
            ok = full in names
            if not ok:
                sn = full.split(".")[-1]
                ok = short_count.get(sn, 0) == 1 and sn in prune_shorts
            if ok:
                hit += 1
                kill.update(range(s - 1, e))
        if len(names) - hit:
            report.append(f"  !! {mod}: {len(names)-hit}/{len(names)} names unmatched")
        # rule 2: comment blocks whole or not at all
        for (a0, b0) in comment_blocks(plain):
            rng = list(range(a0, b0 + 1))
            if not all(x in kill for x in rng):
                for x in rng: kill.discard(x)
        # rule 2b: a section/namespace block whose whole content is deleted goes entirely
        # (switchable per module: the pairing of `end X` with `namespace ...` can be
        #  broken by another patch that merges namespaces, so failures are rolled back)
        blocks = []
        st = []
        for i, ln in enumerate(plain):
            if SEC.match(ln) or NS.match(ln) or MUT.match(ln):
                st.append(i)
            elif END.match(ln) and st:
                blocks.append((st.pop(), i))
        blockkill = set()
        for (b0, b1) in blocks:
            real = [x for x in range(b0, b1 + 1)
                    if plain[x].strip() and not plain[x].lstrip().startswith(("/-", "-/", "--"))
                    and not is_struct(plain[x])]
            if real and all(x in kill for x in real):
                blockkill.update(range(b0, b1 + 1))
        if mod not in no_block: kill |= blockkill
        # rule 3: never delete a structural command (nor its continuation lines)
        i = 0
        while i < len(plain):
            if is_struct(plain[i]) and i not in blockkill:
                kill.discard(i)
                j = i + 1
                while j < len(plain) and plain[j].startswith((" ", "\t")) and plain[j].strip():
                    kill.discard(j); j += 1
            i += 1
        for i, l in enumerate(plain):
            mm = IMP.match(l)
            if mm and mm.group(1) in imp_drop.get(mod, set()): kill.add(i)
        if kill:
            out = [l for i, l in enumerate(lines) if i not in kill]
            n = len(lines) - len(out); total += n
            report.append(f"  -{n:5d}  {mod}")
            if not a.dry: p.write_text("".join(out))
    print("\n".join(report))
    print(f"TOTAL lines removed: {total}")

main()
