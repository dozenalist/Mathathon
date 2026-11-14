import re, pathlib, sys
ROOT=pathlib.Path("lean/OAI")
files=sorted(ROOT.rglob("*.lean"))
texts={p:p.read_text(errors="ignore") for p in files}
DECL=re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*(?:theorem|lemma|def|abbrev|structure|instance)\s+([A-Za-z0-9_'.]+)")
decls=[]
for p,t in texts.items():
    for i,ln in enumerate(t.splitlines(),1):
        m=DECL.match(ln)
        if m: decls.append((m.group(1).split('.')[-1], str(p.relative_to(ROOT)), i))
items = {
 "1.2 Weak measurable coloring": ["WeakColoring"],
 "1.3 Transfer": ["proper_iff_weak","proper_to_borel_weak"],
 "1.4 no weak 5-colouring": ["no_measurable_weak_five_coloring"],
 "1.5 positive badness": ["bad"],
 "2.3 rigidity": ["wild_fourier","residual_fourier"],
 "2.4 cosets null": ["wild_coset_null","wild_independent_difference"],
 "2.5 line average": ["wild_line_null","wild_continuous_coefficient_zero"],
 "2.6 (approximation)": ["approx"],
 "2.7 relative singularity": ["relative_singularity"],
 "3.1 compact tower": ["exists_terminal_factor","strict_compact_successor"],
 "3.2 conditional multi averages": ["multiple","multi"],
 "3.3 radial identities": ["massReal_vanish","radial"],
 "3.4 general position number field": ["general_position","spanning_selection","General"],
 "3.5 addition under cap": ["addition","cap"],
 "4.1 continuous vectors": ["space","residual_fourier"],
 "4.2 proper to weak": ["proper_to_borel_weak_algebraic"],
 "4.3 density points": ["density"],
 "5.1 palettes": ["Palette","palette"],
 "5.2 palette transfer": ["PaletteTransport","transfer"],
 "5.4 sixty degree": ["sixty","rotation"],
 "5.5 binary separation": ["binary","delta"],
 "5.6 palette cardinality": ["palette_card","card"],
 "6.1 transition graph": ["transitionGraph","Transitions"],
 "6.2 avoiding trace": ["avoid"],
 "6.3 strict state separation": ["state_separation","strict"],
 "6.4 singleton-pair": ["singleton","pair"],
 "6.5 local finiteness": ["cyclicCore_compact_finite","locallyFinite"],
 "6.6 four-cycle continuity": ["FourContinuity","four"],
 "6.7 angular step ban": ["angular","FiveSupport"],
 "7.1 common exclusion continua": ["CommonInterface","commonInterface"],
 "7.2 disk inequalities": ["diskAverage_unit_pair"],
 "7.3 missing edge overlap": ["missing_edge","overlap"],
 "7.4 small holes tree fillings": ["HoleApprox","holeApprox"],
 "7.5 cover obstruction": ["compact_open_cover_impossible"],
 "7.6 non-null core loops": ["core","loop"],
 "7.7 midpoint detection": ["midpoint","reduced"],
 "7.8 connected midpoint preimage": ["annulus","straddle_connected_unit"],
 "8.1 one-sided strips": ["outer_strip","inner_strip"],
 "8.2 length five": ["FiveSupport","five"],
 "8.3 six-position words": ["six","word"],
 "8.4 four split rays": ["four"],
 "8.5 length four": ["FourTransport","four"],
 "8.6 local binary rigidity": ["binary"],
 "8.7 boundary one orbit": ["angleBoundary_one_orbit","one_orbit"],
 "8.8 polynomial 3-label region": ["polynomial_region_angles"],
 "8.9 seven-point certificate": ["seven_point"],
 "8.10 length three": ["no_triangle_interfaces","Moser"],
}
for item, keys in items.items():
    hits=[]
    for k in keys:
        for name,f,l in decls:
            if k.lower() in name.lower(): hits.append((name,f,l))
    seen=set(); out=[]
    for h in hits:
        if h[0] in seen: continue
        seen.add(h[0]); out.append(h)
    print(f"## {item}")
    for name,f,l in out[:4]:
        print(f"     {name:44s} {f}:{l}")
    if not out: print("     *** NO CANDIDATE ***")
