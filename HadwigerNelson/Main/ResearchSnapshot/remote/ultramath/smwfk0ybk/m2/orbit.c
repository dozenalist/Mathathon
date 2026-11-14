/* k=6 orbit-level exhaustive enumeration.  C1: 1<=|P|<=3 (41 masks).
   C3: consecutive disjoint cyclically.  Records C4 (complementary pair anywhere),
   C4adj (distance 1), C4far (distance 2 or 3), C5 (#ternary<=3), mean.  */
#include <stdio.h>
#include <stdlib.h>
int m[41], sz[41], n;
int P[6];
long long cnt=0, tot_c3=0, c4_ok=0, notc4=0, notc5=0, c4_and_notc5=0, c5_and_notc4=0;
long long far_only=0, adj_viol=0, mean_hist[7], tern_hist[7], maxmean2=0;
void rec(int i, unsigned disjprev){
  if(i==6){ if(m[P[5]]&m[P[0]]) return; tot_c3++;
    int tern=0, comp=0, adj=0;
    for(int a=0;a<6;a++){ if(sz[P[a]]==3) tern++;
      for(int b=a+1;b<6;b++) if((m[P[a]]|m[P[b]])==63){ comp=1; if((b-a==1)||(b-a==5)) adj=1; } }
    long long sum=0; for(int a=0;a<6;a++) sum+=sz[P[a]];
    int mean2 = (int)(sum*2/6);
    if(mean2>maxmean2) maxmean2=mean2;
    mean_hist[mean2]++; tern_hist[tern]++;
    if(!comp) c4_ok++; else { notc4++; if(!adj) far_only++; else adj_viol++; }
    if(tern>3) notc5++;
    if(!comp && tern>3) c4_and_notc5++;
    if(comp && tern<=3) c5_and_notc4++;
    return; }
  for(int j=0;j<n;j++){ if(j & 0) continue; }
  for(int j=0;j<n;j++){ if(!(m[j]&disjprev)){ P[i]=j; rec(i+1, m[j]); } }
}
int main(void){
  n=0;
  for(int mask=1; mask<64; mask++){ int c=__builtin_popcount(mask); if(c<=3){ m[n]=mask; sz[n]=c; n++; } }
  printf("admissible masks: %d\n", n);
  /* position 0: all; positions 1..5 must be disjoint from previous; close cyclically */
  for(int j=0;j<n;j++){ P[0]=j; rec(1, m[j]); }
  printf("total C1&C3 (6-cycle): %lld   (m6 table says 10581680)\n", tot_c3);
  printf("C4 holds: %lld   C4 fails: %lld\n", c4_ok, notc4);
  printf("  of the failures: adjacent complementary pair %lld, far-only %lld\n", adj_viol, far_only);
  printf("C5 fails (#ternary>=4): %lld\n", notc5);
  printf("C4 & not C5: %lld   (0 = C4 implies C5 at k=6)\n", c4_and_notc5);
  printf("C5 & not C4: %lld   (far complementary pair with <=3 ternary: C4 is not C4adj)\n", c5_and_notc4);
  printf("ternary histogram:\n"); for(int t=0;t<=6;t++) printf("  #tern=%d : %lld\n", t, tern_hist[t]);
  printf("mean-size histogram (2*sum/6):\n"); for(int t=0;t<=6;t++) printf("  2*mean=%d : %lld\n", t, mean_hist[t]);
  return 0;
}
