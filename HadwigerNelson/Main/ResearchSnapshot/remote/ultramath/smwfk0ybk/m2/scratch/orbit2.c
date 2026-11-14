/* Does the MEAN bound  (1/6)sum|P_i| <= 5/2  imply the COUNT bound #ternary <= 3 ?
   Count orbits (C1&C3, k=6) with >=4 ternary but mean <= 5/2.  */
#include <stdio.h>
int m[41], sz[41], n, P[6];
long long notc5=0, notc5_but_mean=0, mean_ok_notc5_prof[4][4][4];
long long prof[7];   /* profile of #ternaries among mean<=5/2 orbits */
void rec(int i, unsigned prev){
  if(i==6){ if(m[P[5]]&m[P[0]]) return;
    int tern=0; long long sum=0;
    for(int a=0;a<6;a++){ if(sz[P[a]]==3) tern++; sum+=sz[P[a]]; }
    if(2*sum <= 6*5) { if(tern>=4){ notc5_but_mean++; prof[tern]++; } }
    return; }
  for(int j=0;j<n;j++) if(!(m[j]&prev)){ P[i]=j; rec(i+1,m[j]); }
}
int main(void){ n=0;
  for(int mask=1;mask<64;mask++){ int c=__builtin_popcount(mask); if(c<=3){m[n]=mask;sz[n]=c;n++;} }
  for(int j=0;j<n;j++){ P[0]=j; rec(1,m[j]); }
  printf("orbits (C1&C3) with >=4 ternary and mean <= 5/2 : %lld\n", notc5_but_mean);
  for(int t=4;t<=6;t++) printf("   #tern=%d : %lld\n", t, prof[t]);
  /* explicit example */
  printf("example: ternary,ternary,ternary,ternary,singleton,singleton\n");
  return 0; }
