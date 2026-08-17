#!/usr/bin/env python3
import math,sys
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import lil_matrix,csr_matrix

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import probe_v26_q138_predecessor_leaf_ad_input_activity as P
import probe_v26_q138_predecessor_leaf_ad_input_activity_quotient as Q


def objects(pos):
    out=[(can,1,'affine') for _,_,can in P.affine_supports(pos)]
    signed=[]
    for z in ((1,0),(3,0)):
        C=D.carries([z],ad=True)
        can=A.canonical_support(pos,C,expect_internal=128)
        assert can is not None and A.cut_intersection(can)==0
        q,r=A.sign_cross_rank(pos,C);assert r==128
        signed.append((can,q+2,'signed92'))
    FF=D.full_forms(pos);C=D.carries([],ad=True)
    sol=A.internal_null(pos,C);assert sol[0]==127 and len(sol[2])==1
    der=A.derivative_form(FF,A.map_internal_to_full(sol[2][0]))
    can=A.canonical_support(pos,C,der,127)
    assert can is not None and A.cut_intersection(can)==0
    q,r=A.sign_cross_rank(pos,C,der);assert r==127
    signed.append((can,q+2,'signed93'))
    out.extend(signed)
    return out


def solve(pos):
    objs=objects(pos);conds=[Q.canonical_input_rows(can) for can,w,k in objs]
    weights=[w for can,w,k in objs];nt=len(objs);eqs=[]
    for t,cond in enumerate(conds):
        for row in cond:eqs.append((t,row&((1<<128)-1),(row>>128)&1))
    nx=128;z0=nx;y0=z0+nt;nv=y0+len(eqs)
    c=np.zeros(nv);c[z0:z0+nt]=-np.asarray(weights,float)
    integ=np.ones(nv,dtype=np.uint8);lb=np.zeros(nv);ub=np.ones(nv)
    for e,(_,mask,rhs) in enumerate(eqs):ub[y0+e]=math.ceil(mask.bit_count()/2)
    Mx=lil_matrix((2*len(eqs),nv),dtype=float);lo=np.full(2*len(eqs),-np.inf);hi=np.full(2*len(eqs),np.inf)
    for e,(t,mask,rhs) in enumerate(eqs):
        bits=[];m=mask
        while m:
            b=(m&-m).bit_length()-1;bits.append(b);m^=1<<b
        big=len(bits)+1;r=2*e
        for b in bits:Mx[r,b]=1;Mx[r+1,b]=1
        Mx[r,y0+e]=-2;Mx[r+1,y0+e]=-2
        Mx[r,z0+t]=big;Mx[r+1,z0+t]=-big
        hi[r]=big+rhs;lo[r+1]=-big+rhs
    res=milp(c,integrality=integ,bounds=Bounds(lb,ub),constraints=LinearConstraint(csr_matrix(Mx),lo,hi),
             options={'time_limit':900,'mip_rel_gap':0.0,'presolve':True})
    print('position',pos,'status',res.status,'message',res.message,'mip_gap',getattr(res,'mip_gap',None),
          'dual',getattr(res,'mip_dual_bound',None),'nodes',getattr(res,'mip_node_count',None),flush=True)
    assert res.success and res.status==0 and abs(res.mip_gap)<1e-12
    opt=round(-res.fun);dual=round(-res.mip_dual_bound);assert opt==dual
    active=[i for i,v in enumerate(res.x[z0:z0+nt]) if v>0.5]
    dist=Counter((objs[i][1],objs[i][2]) for i in active)
    print('position',pos,'EXACT_weighted_activity_max',opt,'active_distribution',dict(dist))
    return opt


def main():
    vals={p:solve(p) for p in 'AD'}
    print('PASS PROBE V26_Q138_AD_WEIGHTED_ACTIVITY_MILP')
    print('weighted_uniform_candidate_bounds',vals)
    print('scope=exact weighted support-activity MILP; theorem requires independent recount')

if __name__=='__main__':main()
