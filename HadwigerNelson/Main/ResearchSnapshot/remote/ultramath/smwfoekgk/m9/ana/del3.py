import re, pathlib, json, collections, sys

ROOT = pathlib.Path("tree")
files = sorted(ROOT.glob("OAI/**/*.lean"))

HEAD = r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|unsafe\s+|scoped\s+|local\s+)*"
DECL = re.compile(HEAD + r"(theorem|lemma|def|abbrev|structure|class|inductive|instance|example)\s+([A-Za-z_][\w'.]*)")
ANON = re.compile(r"^(?:private\s+|protected\s+|noncomputable\s+|scoped\s+|local\s+)*(instance|example)\b")
STOP = re.compile(r"^(end\b|namespace\b|section\b|variable\b|open\b|#|/-|-/|\}|@\[|omit\b|include\b|"
                  r"attribute\b|set_option\b|mutual\b|where\b|noncomputable\b|private\b|protected\b|scoped\b|"
                  r"local\b|unsafe\b|partial\b|instance\b|example\b|class\b|structure\b|inductive\b|theorem\b|"
                  r"lemma\b|def\b|abbrev\b)")
MODIFIER = re.compile(r"^(omit|include|variable|set_option)\b.*\bin$")

texts = {}
blocks = []
for p in files:
    rel = str(p.relative_to(ROOT))
    mod = ".".join(p.relative_to(ROOT).with_suffix("").parts)
    t = p.read_text(errors="ignore")
    texts[rel] = t
    L = t.splitlines()
    n = len(L)
    starts = []
    for i, line in enumerate(L):
        m = DECL.match(line)
        if m:
            starts.append((i, m.group(1), m.group(2)))
        elif ANON.match(line):
            starts.append((i, "anon", "@anon"))
    for i, kind, full in starts:
        line = L[i]
        attributed = "@[" in line
        b = i - 1
        while b >= 0:
            s = L[b].strip()
            if s.startswith("@"):
                attributed = True
                b -= 1
                continue
            if s == "":
                b -= 1
                continue
            if s.endswith("-/"):
                kk = b
                while kk >= 0 and not L[kk].lstrip().startswith("/-"):
                    kk -= 1
                if kk < 0:
                    raise SystemExit("unmatched comment %s:%d" % (rel, b + 1))
                if "@[" in L[kk]:
                    attributed = True
                b = kk - 1
                continue
            if MODIFIER.match(s):
                b -= 1
                continue
            break
        start = b + 1
        e = n - 1
        for mm in range(i + 1, n):
            if DECL.match(L[mm]) or STOP.match(L[mm]):
                e = mm - 1
                break
        while e > i and L[e].strip() == "":
            e -= 1
        for j in range(start, e + 1):
            sj = L[j].strip()
            if j != i and STOP.match(L[j]) and not sj.startswith(("@[", "/-", "-/", "--")):
                print("WARN %s:%d[%s] inside block of %s" % (rel, j + 1, sj[:40], full), file=sys.stderr)
        blocks.append(dict(file=rel, mod=mod, start=start, end=e, kind=kind, full=full,
                           short=full.split(".")[-1], attr=attributed))

print("blocks %d" % len(blocks), file=sys.stderr)
TOK = re.compile(r"[A-Za-z_][\w']*")
blk = [collections.Counter(TOK.findall("\n".join(texts[b["file"]].splitlines()[b["start"]:b["end"] + 1])))
       for b in blocks]
live = collections.defaultdict(set)
for i, ts in enumerate(blk):
    for s in ts:
        live[s].add(i)
hdr = collections.Counter()
for rel, t in texts.items():
    L = t.splitlines()
    mask = [True] * len(L)
    for b in blocks:
        if b["file"] == rel:
            for j in range(b["start"], b["end"] + 1):
                mask[j] = False
    hdr.update(TOK.findall("\n".join(L[j] for j in range(len(L)) if mask[j])))

names = {"no_proper_five_coloring", "no_proper_five_coloring_algebraic", "properColoring_seven",
         "chromaticNumber_bounds", "proper_iff_weak", "algebraic_colorable_iff",
         "not_proper_five_coloring_compl_null", "six_le_planeChromaticNumber",
         "planeChromaticNumber_le_seven", "not_properColoring_five", "not_properColoring_of_le",
         "planeProperColoring_iff", "properColoring_of_plane", "plane_of_properColoring",
         "properColoring_mono", "toPlane", "ofPlane", "finite_config_proper",
         "exists_properColoring_of_finset", "properColoring_of_weak",
         "diam_le_one_of_preconnected_unitFree", "not_straddle_of_isPreconnected",
         "proper_to_borel_weak_algebraic"}
mods = {"OAI.Geometry.PlaneColoring.Chromatic", "OAI.Geometry.PlaneColoring.Seven",
        "OAI.Geometry.PlaneColoring.NullSetRobust", "OAI.Geometry.PlaneColoring.Transfer",
        "OAI.Geometry.PlaneColoring.Converse", "OAI.Geometry.PlaneColoring.ConnectedUnitFree",
        "OAI.Geometry.PlaneColoring.MeasurableProper", "OAI.Geometry.PlaneColoring.MeasurableAssembly",
        "OAI.Geometry.PlaneColoring.Metric", "OAI.Geometry.PlaneColoring.Lattice",
        "OAI.Geometry.PlaneColoring.Assembly", "OAI.Geometry.PlaneColoring.Basic",
        "OAI.Geometry.PlaneColoring.Covering"}

kinds = sys.argv[1].split(",") if len(sys.argv) > 1 else ["theorem", "lemma", "def", "abbrev"]
noattr = "noattr" in kinds
kinds = [k for k in kinds if k != "noattr"]
if "nomod" in kinds:
    mods = set(); kinds = [k for k in kinds if k != "nomod"]
D = set()
for it in range(80):
    add = [i for i, b in enumerate(blocks)
           if i not in D and b["mod"] not in mods and b["short"] not in names and b["short"] != "@anon"
           and (not b["attr"] if noattr else True) and b["kind"] in kinds
           and not hdr.get(b["short"], 0) and not (live.get(b["short"], set()) - {i} - D)]
    if not add:
        break
    D |= set(add)
print("deleting %d decls %d lines" % (len(D), sum(blocks[i]["end"] - blocks[i]["start"] + 1 for i in D)),
      file=sys.stderr)
json.dump(blocks, open("ana/blocks3.json", "w"))
json.dump(sorted(D), open("ana/dead3.json", "w"))
