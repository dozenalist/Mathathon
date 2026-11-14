/* d12: independent (C) re-decision of the k=6 single-centre classification.
 * Different language, different data representation (bitmasks + integer loops)
 * from the Python implementations in classify2.py / verify_witnesses.py.
 *
 * For each of the 2^15 graphs G on {0..5}:
 *   admissible value  S  <=>  S != 0, |S| <= 3, and for every edge {i,j} of G, S is not a
 *                             subset of {i,j}
 *   compatible        <=>  exist admissible S,T with S&T == 0 and (S|T) != 63
 * Print the number of incompatible graphs and their edge counts.
 *
 * Also count, for G = K_6, how many ordered pairs of admissible values there are and how
 * many of them are "good" -- by a direct count, not by search.
 */
#include <stdio.h>
#include <stdint.h>

static int popcount6(int m){ int c=0; while(m){ c += m&1; m >>= 1; } return c; }

int main(void){
    const int n = 6;
    int pairs[15][2]; int np = 0;
    for (int i = 0; i < n; i++) for (int j = i+1; j < n; j++){ pairs[np][0]=i; pairs[np][1]=j; np++; }
    const int FULL = 63;

    int incompatible = 0;
    long compatible = 0;
    int hist[16]; for (int i=0;i<16;i++) hist[i]=0;

    for (int g = 0; g < (1<<np); g++){
        int imm[15]; int adj = 0;
        for (int e = 0; e < np; e++) if (g >> e & 1){ imm[adj++] = (1<<pairs[e][0]) | (1<<pairs[e][1]); }
        /* admissible values */
        int vals[64]; int nv = 0;
        for (int m = 1; m <= FULL; m++){
            if (popcount6(m) > 3) continue;
            int bad = 0;
            for (int e = 0; e < adj; e++) if ((m & ~imm[e]) == 0){ bad = 1; break; }
            if (!bad) vals[nv++] = m;
        }
        int ok = 0;
        for (int a = 0; a < nv && !ok; a++)
            for (int b = a; b < nv; b++){
                if (vals[a] & vals[b]) continue;
                if ((vals[a] | vals[b]) == FULL) continue;
                ok = 1; break;
            }
        if (!ok){ incompatible++; hist[adj]++; }
        else compatible++;
    }
    printf("C check, k=6: graphs = %d, compatible = %ld, incompatible = %d\n",
           1<<np, compatible, incompatible);
    printf("  edge-counts of the incompatible graphs:");
    for (int i = 0; i <= np; i++) if (hist[i]) printf(" %d edges x%d", i, hist[i]);
    printf("\n");

    /* independent count for K_6: admissible values are the size-3 masks only */
    int triples[20]; int nt = 0;
    for (int m = 1; m <= FULL; m++) if (popcount6(m) == 3) triples[nt++] = m;
    int good = 0, total = 0;
    for (int a = 0; a < nt; a++) for (int b = a; b < nt; b++){
        total++;
        if ((triples[a] & triples[b]) == 0 && (triples[a] | triples[b]) != FULL) good++;
    }
    printf("K_6: admissible values = %d (the triples); value pairs = %d; good pairs = %d\n",
           nt, total, good);
    printf("     two disjoint triples in a 6-set always have union of size 6 = FULL, so good = 0\n");
    return (incompatible == 1 && good == 0) ? 0 : 1;
}
