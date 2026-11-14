#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int nvars, *val, *trail, trail_n=0, qhead=0;
typedef struct { int *lits; int n; } Clause;
static Clause *cl; static int ncl=0, capcl=0;
static int **wlist; static int *wn, *wcap;
static int lit_idx(int l){ return 2*(abs(l)-1) + (l<0?1:0); }
static void wpush(int l,int ci){
  int k=lit_idx(l);
  if(wn[k]==wcap[k]){ wcap[k]=wcap[k]?wcap[k]*2:8; wlist[k]=realloc(wlist[k],wcap[k]*sizeof(int)); }
  wlist[k][wn[k]++]=ci;
}
static int enqueue(int l){
  int v=abs(l), want=(l>0)?1:-1;
  if(val[v]==want) return 1;
  if(val[v]==-want) return 0;
  val[v]=want; trail[trail_n++]=l; return 1;
}
static int litval(int l){ return val[abs(l)]*(l>0?1:-1); }
static int propagate(void){
  while(qhead<trail_n){
    int l=trail[qhead++], k=lit_idx(-l), i=0;
    while(i<wn[k]){
      int ci=wlist[k][i]; Clause *c=&cl[ci];
      if(c->lits[0]==-l){ int t=c->lits[0]; c->lits[0]=c->lits[1]; c->lits[1]=t; }
      int first=c->lits[0];
      if(litval(first)==1){ i++; continue; }
      int found=0;
      for(int j=2;j<c->n;j++) if(litval(c->lits[j])!=-1){
        c->lits[1]=c->lits[j]; c->lits[j]=-l; wpush(c->lits[1],ci);
        wlist[k][i]=wlist[k][--wn[k]]; found=1; break;
      }
      if(found) continue;
      if(litval(first)==-1) return 1;
      if(!enqueue(first)) return 1;
      i++;
    }
  }
  return 0;
}
static void add(int *lits,int n,int *cf){
  if(n==0){ *cf=1; return; }
  /* invariant repair: watches must be non-false literals at the current (level-0) assignment */
  for(int k=0;k<n;k++) if(litval(lits[k])==1) return;   /* satisfied now and forever at level 0 */
  int *tmp=malloc(n*sizeof(int)); int p=0;
  for(int k=0;k<n;k++) if(litval(lits[k])!=-1) tmp[p++]=lits[k];
  for(int k=0;k<n;k++) if(litval(lits[k])==-1) tmp[p++]=lits[k];
  memcpy(lits,tmp,n*sizeof(int)); free(tmp);
  int nonfalse=p;
  if(nonfalse==0){ *cf=1; return; }                       /* all literals false: level-0 conflict */
  if(n==1){ if(!enqueue(lits[0]) || propagate()) *cf=1; return; }
  if(ncl==capcl){ capcl=capcl?capcl*2:4096; cl=realloc(cl,capcl*sizeof(Clause)); }
  int ci=ncl++; cl[ci].lits=malloc(n*sizeof(int)); memcpy(cl[ci].lits,lits,n*sizeof(int)); cl[ci].n=n;
  wpush(lits[0],ci); wpush(lits[1],ci);
  if(nonfalse==1){ if(!enqueue(lits[0]) || propagate()) *cf=1; }
}
static int rup(int *lits,int n){
  int mark=trail_n, cf=0;
  for(int i=0;i<n&&!cf;i++) if(!enqueue(-lits[i])) cf=1;
  if(!cf) cf=propagate();
  for(int i=mark;i<trail_n;i++) val[abs(trail[i])]=0;
  trail_n=mark; qhead=mark;
  return cf;
}
int main(int argc,char**argv){
  char buf[1<<16]; int nc=0;
  FILE*f=fopen(argv[1],"r"); if(!f){perror("cnf");return 2;}
  if(fscanf(f,"p cnf %d %d",&nvars,&nc)!=2){fprintf(stderr,"bad header\n");return 2;}
  val=calloc(nvars+2,sizeof(int)); trail=malloc(sizeof(int)*(nvars+64));
  wlist=calloc(2*nvars+2,sizeof(int*)); wn=calloc(2*nvars+2,sizeof(int)); wcap=calloc(2*nvars+2,sizeof(int));
  int *lits=malloc(sizeof(int)*(nc+1<<10)); int n=0,x,cf=0;
  while(fscanf(f,"%d",&x)==1){ if(x==0){ add(lits,n,&cf); n=0; } else lits[n++]=x; }
  fclose(f);
  printf("initial: %d clauses added (declared %d)\n", ncl, nc);
  if(propagate()||cf){ printf("warning: level-0 conflict in input\n"); }
  FILE*g=fopen(argv[2],"r"); if(!g){perror("drup");return 2;}
  long steps=0; int empty=0; n=0;
  while(fscanf(g,"%d",&x)==1){
    if(x!=0){ lits[n++]=x; continue; }
    steps++;
    if(!rup(lits,n)){ printf("RUP FAILURE at step %ld, clause length %d\n",steps,n); return 1; }
    if(n==0) empty=1;
    else { int c2=cf; add(lits,n,&c2); if(c2&&!cf){ cf=1; propagate(); } }
    n=0;
  }
  fclose(g);
  printf("RUP VERIFIED: %ld steps, each unit-propagation refuting; empty clause %s\n",
         steps, empty?"DERIVED -> UNSAT":"MISSING");
  return empty?0:1;
}
