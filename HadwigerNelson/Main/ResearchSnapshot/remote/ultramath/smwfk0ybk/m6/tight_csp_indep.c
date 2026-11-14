/* Independent decision procedure B for the tightened interface CSP at k = 6.
 *
 * Differences from tight_csp.py (procedure A) by construction:
 *   - C instead of Python; no shared code.
 *   - O_i, I_i are computed from the ACTUAL ray angles via floating point
 *     cos(theta_j - i*pi/3) with an explicit |cos| > 0.4 guard, instead of from
 *     the algebraic table sign(cos(m pi/3)) on m in Z/6.
 *   - The decision is a forward reachability DP over the state set
 *        (last palette, bitmask of the ternary triples used so far)
 *     iterated from each candidate first palette, not a depth-first search.
 *   - (C4) and (C5) are enforced inside the transition relation.
 *
 * Instance space: ell in {3,4,5,6}, cell vectors c in {0..5}^ell with c_0 = 0.
 * Output: one line per ell: "ell total sat", then the sorted list of sat vectors.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define K 6
#define FULL ((1 << K) - 1)
#define MAXADM 64

static int ntrip;
static int tripidx[1 << K];       /* index of a 3-set among the 20 triples, else -1 */

static int popcount(int x) { int c = 0; while (x) { c += x & 1; x >>= 1; } return c; }

/* state: (last palette, tmask over 20 triples) */
typedef struct { int last; unsigned tmask; } St;
static St cur[1 << 16], nxt[1 << 16];
static int ncur, nnxt;
static unsigned char seen[1 << 20];

static void add_state(St *arr, int *n, int last, unsigned tmask) {
    unsigned h = (unsigned)(last * 2654435761u) ^ (tmask * 40503u);
    unsigned hh = h & ((1u << 20) - 1);
    /* linear probing on the seen table; cleared per layer by memset */
    while (seen[hh]) {
        /* store index+1 in seen: we need the actual entries; use a parallel array */
        hh = (hh + 1) & ((1u << 20) - 1);
    }
    seen[hh] = 1;
    arr[*n].last = last; arr[*n].tmask = tmask; (*n)++;
}

/* We need dedup with equality, so keep a simple type-1 hash table per layer. */
typedef struct { int last; unsigned tmask; int used; } Slot;
static Slot tab[1 << 17];

static unsigned keyof(int last, unsigned tmask) {
    return ((unsigned)last * 2654435761u) ^ (tmask * 2246822519u);
}

static int tab_insert(int last, unsigned tmask) {          /* 1 if new */
    unsigned h = keyof(last, tmask) & ((1u << 17) - 1);
    while (tab[h].used) {
        if (tab[h].last == last && tab[h].tmask == tmask) return 0;
        h = (h + 1) & ((1u << 17) - 1);
    }
    tab[h].used = 1; tab[h].last = last; tab[h].tmask = tmask;
    return 1;
}
static void tab_clear(void) { memset(tab, 0, sizeof tab); }

int main(void) {
    ntrip = 0;
    for (int p = 0; p < (1 << K); p++) tripidx[p] = -1;
    for (int p = 0; p < (1 << K); p++) if (popcount(p) == 3) tripidx[p] = ntrip++;
    if (ntrip != 20) { fprintf(stderr, "ntrip=%d\n", ntrip); return 1; }

    const double PI = M_PI;
    int total_all = 0, sat_all = 0;

    for (int ell = 3; ell <= K; ell++) {
        int total = 0, sat = 0;
        long long ng = 1;
        for (int i = 1; i < ell; i++) ng *= 6;
        printf("ell %d geometries %lld\n", ell, ng);
        for (long long g = 0; g < ng; g++) {
            int cells[6];
            cells[0] = 0;
            long long t = g;
            for (int j = 1; j < ell; j++) { cells[j] = (int)(t % 6); t /= 6; }
            total++;

            /* sign matrix from the actual angles: theta_j = (c_j+1)*pi/3 */
            int sig[6][6];
            int bad = 0;
            for (int j = 0; j < ell; j++) {
                double th = (cells[j] + 1.0) * PI / 3.0;
                for (int i = 0; i < 6; i++) {
                    double cs = cos(th - i * PI / 3.0);
                    if (fabs(cs) < 0.4) { bad = 1; }
                    sig[i][j] = (cs > 0) ? 1 : -1;
                }
            }
            if (bad) { fprintf(stderr, "degenerate angle!\n"); return 1; }

            /* O_i, I_i  (paper 8.1) */
            int O[6], I[6], adm[6][MAXADM], nadm[6];
            int T = (1 << ell) - 1, U = FULL ^ T;
            for (int i = 0; i < 6; i++) {
                O[i] = I[i] = U;
                for (int j = 0; j < ell; j++) {
                    int a = sig[i][(j - 1 + ell) % ell], b = sig[i][j];
                    if (a == -1 && b == -1) O[i] |= 1 << j;
                    if (a ==  1 && b ==  1) I[i] |= 1 << j;
                }
            }
            for (int i = 0; i < 6; i++) {
                nadm[i] = 0;
                for (int p = 1; p < (1 << K); p++) {
                    int sz = popcount(p);
                    if (sz < 1 || sz > K - 3) continue;
                    if (!(p & O[i]) || !(p & I[i])) continue;
                    if (nadm[i] < MAXADM) adm[i][nadm[i]++] = p;
                }
            }
            int feasible = 1;
            for (int i = 0; i < 6; i++) if (nadm[i] == 0) feasible = 0;

            int found = 0;
            if (feasible) {
                for (int a = 0; a < nadm[0] && !found; a++) {
                    int p0 = adm[0][a];
                    unsigned t0 = (tripidx[p0] >= 0) ? (1u << tripidx[p0]) : 0u;
                    ncur = 0; tab_clear();
                    if (tab_insert(p0, t0)) { cur[ncur].last = p0; cur[ncur].tmask = t0; ncur++; }
                    for (int i = 1; i <= 5 && ncur > 0; i++) {
                        tab_clear(); nnxt = 0;
                        for (int s = 0; s < ncur; s++) {
                            int last = cur[s].last; unsigned tm = cur[s].tmask;
                            for (int q = 0; q < nadm[i]; q++) {
                                int p = adm[i][q];
                                if (p & last) continue;
                                unsigned ntm = tm;
                                int ti = tripidx[p];
                                if (ti >= 0) {
                                    if (popcount((int)tm) >= 3) continue;          /* C5 */
                                    if (tm & (1u << ti)) continue;                 /* repeat */
                                    if (tm & (1u << tripidx[p ^ FULL])) continue;  /* C4 */
                                    ntm = tm | (1u << ti);
                                }
                                if (i == 5) {
                                    if (p & p0) continue;
                                    found = 1; break;
                                }
                                if (tab_insert(p, ntm)) {
                                    nxt[nnxt].last = p; nxt[nnxt].tmask = ntm; nnxt++;
                                }
                            }
                            if (found) break;
                        }
                        memcpy(cur, nxt, sizeof(St) * (size_t)nnxt);
                        ncur = nnxt;
                    }
                }
            }
            if (found) { sat++; printf("SAT %d", ell); for (int j = 0; j < ell; j++) printf(" %d", cells[j]); printf("\n"); }
        }
        printf("ell %d total %d sat %d\n", ell, total, sat);
        total_all += total; sat_all += sat;
    }
    printf("TOTAL %d %d\n", total_all, sat_all);
    return 0;
}
