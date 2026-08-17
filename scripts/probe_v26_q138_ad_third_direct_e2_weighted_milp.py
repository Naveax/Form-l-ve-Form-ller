#!/usr/bin/env python3
import math,sys
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import lil_matrix,csr_matrix

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I

MASK=(1<<128)-1

def canonical_condition(cond):
    rank,eq=cond;rows=[m|((rhs&1)<<128) for m,rhs in eq];r=0
    for col in range(128):
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        r+=1
    return tuple(rows[:r])


def weighted_groups(pos):
    raw,_=P.direct_supports(pos)
    C=Counter(can for _,_,can in raw)
    odd=[can for can,n in C.items() if n&1]
    G=defaultdict(int);cuts=Counter()
    for can in odd:
        cut=P.A.cut_intersection(can);cuts[cut]+=1
        cond=canonical_condition(I.input_condition(can))
        G[cond]+=1<<cut
    return G,len(odd),cuts


def exact_opt(pos):
    G,nodd,cuts=weighted_groups(pos)
    conds=list(G);weights=np.array([G[c] for c in conds],dtype=float)
    eqs=[]
    for t,cond in enumerate(conds):
        for row in cond:eqs.append((t,row&MASK,(row>>128)&1))
    nx=128;nt=len(conds);ne=len(eqs);z0=nx;v0=z0+nt;y0=v0+ne;nv=y0+ne
    c=np.zeros(nv);c[z0:z0+nt]=-weights
    integrality=np.ones(nv,dtype=np.uint8)
    lb=np.zeros(nv);ub=np.ones(nv)
    for e,(_,mask,rhs) in enumerate(eqs):ub[y0+e]=math.ceil(mask.bit_count()/2)
    M=lil_matrix((2*ne,nv),dtype=float);lo=np.full(2*ne,-np.inf);hi=np.full(2*ne,np.inf)
    for e,(t,mask,rhs) in enumerate(eqs):
        m=mask
        while m:
            bit=(m&-m).bit_length()-1;M[e,bit]=1;m^=1<<bit
        M[e,y0+e]=-2;M[e,v0+e]=-(1-2*rhs);lo[e]=hi[e]=rhs
        r=ne+e;M[r,z0+t]=1;M[r,v0+e]=1;hi[r]=1
    res=milp(c,integrality=integrality,bounds=Bounds(lb,ub),
             constraints=LinearConstraint(csr_matrix(M),lo,hi),
             options={'time_limit':1500,'mip_rel_gap':0.0,'presolve':True})
    primal=round(-res.fun) if res.fun is not None else None
    dual=round(-res.mip_dual_bound) if getattr(res,'mip_dual_bound',None) is not None else None
    print('position',pos,'odd_supports',nodd,'cut_distribution',dict(sorted(cuts.items())),
          'distinct_weighted_input_conditions',nt,'equations',ne,
          'solver_status',res.status,'success',res.success,'primal',primal,'dual',dual,
          'mip_gap',getattr(res,'mip_gap',None),'nodes',getattr(res,'mip_node_count',None),flush=True)
    if res.success and res.status==0 and primal==dual:
        print(f'EXACT_OPT {pos} {primal}',flush=True)
        return primal
    return None


def main():
    vals={p:exact_opt(p) for p in 'AD'}
    print('PASS PROBE V26_Q138_AD_THIRD_DIRECT_E2_WEIGHTED_MILP')
    print('results',vals)
    if all(v is not None for v in vals.values()):
        print(f"STATUS_DESC=A direct-e2<={vals['A']}; D direct-e2<={vals['D']} exact weighted MILP")
    else:
        print('STATUS_DESC=direct-e2 weighted MILP incomplete; inspect primal/dual')
    print('scope=direct e=2 support-indicator component only; higher-bit corrections from earlier dyadic sectors are excluded')

if __name__=='__main__':main()
