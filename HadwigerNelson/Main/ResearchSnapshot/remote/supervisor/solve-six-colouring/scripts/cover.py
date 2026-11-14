"""Certified cover of the rectangular cell-tiling family: where does a 7-clique among
guaranteed-forced differences kill every proper 6-colouring?  Exact integer arithmetic."""
import json, time, sys
sys.path.insert(0, "scripts")
from cells import H, M, guaranteed_box, clique_with_origin, forced_set_point, forced_at_int

def max_clique_size(G, cap=8, budget=200000):
    """best clique size found with 0 in it (lower bound on omega), bounded search."""
    for t in range(cap, 2, -1):
        c = clique_with_origin(G, t, budget=budget)
        if c: return t, c
    return 1, [(0, 0)]

def main():
    t0 = time.time()
    certified, undecided = [], []
    for i in range(1, H):
        for j in range(i, H):
            if i * i + j * j >= M: continue          # lower corner outside s^2+t^2 < 1
            B = guaranteed_box(i, j)
            c = clique_with_origin(B, 7, budget=60000)
            if c:
                certified.append({"box": [i, j], "D2": (i * i + j * j) / M,
                                  "clique": sorted(c), "size_guaranteed": len(B)})
            else:
                omega, cl = max_clique_size(B, cap=6, budget=40000)
                undecided.append({"box": [i, j], "D2": (i * i + j * j) / M,
                                  "size_guaranteed": len(B), "max_clique_found": omega})
        if i % 10 == 0:
            print(f"  i={i} done, certified={len(certified)} undecided={len(undecided)}, "
                  f"{time.time()-t0:.1f}s", flush=True)
    out = {"H": H, "certified": certified, "undecided": undecided,
           "seconds": round(time.time() - t0, 1)}
    json.dump(out, open("out/cover.json", "w"))
    print(f"TOTAL boxes={len(certified)+len(undecided)} certified={len(certified)} "
          f"undecided={len(undecided)} ({time.time()-t0:.1f}s)", flush=True)
    if undecided:
        ds = sorted(undecided, key=lambda r: r["D2"])
        print("undecided, smallest D2:", [(round(r['D2'],4), r['box'], r['max_clique_found']) for r in ds[:10]], flush=True)
        print("undecided, largest D2:", [(round(r['D2'],4), r['box'], r['max_clique_found']) for r in ds[-6:]], flush=True)
        print("max clique found over undecided:", max(r['max_clique_found'] for r in undecided), flush=True)
    if certified:
        ds = sorted(certified, key=lambda r: r["D2"])
        print("certified D2 range:", round(ds[0]['D2'],4), "to", round(ds[-1]['D2'],4), flush=True)
        print("example certificate:", ds[len(ds)//2]['box'], ds[len(ds)//2]['clique'], flush=True)

if __name__ == "__main__":
    main()
