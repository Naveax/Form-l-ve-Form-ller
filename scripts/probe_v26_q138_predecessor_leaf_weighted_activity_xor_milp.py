#!/usr/bin/env python3
import math,sys
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import lil_matrix,csr_matrix

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_predecessor_leaf_ad_input_activity_quotient as Q
import probe_v26_q138_predecessor_leaf_ad_weighted_activity_milp as AW
import probe_v26_q138_predecessor_leaf_bc_input_activity_milp as BW


def position_objects(pos):
    return AW.objects(pos) if pos in 'AD' else BW.build_bc_objects(pos)


def build(pos):
    objs=position_objects(pos)
    conds=[Q.canonical_input_rows(can) for can,w,k in objs]
    weights=[w for can,w,k in objs]
    eqs=[]
    for t,cond in enumerate(conds):
        for row in cond:eqs.append((t,row&((1<<128)-1),(row>>128)&1))

    nx=128;nt=len(objs);ne=len(eqs)
    z0=nx;v0=z0+nt;y0=v0+ne;nv=y0+ne
    c=np.zeros(nv);c[z0:z0+nt]=-np.asarray(weights,float)
    integrality=np.ones(nv,dtype=np.uint8)
    lb=np.zeros(nv);ub=np.ones(nv)
    for e,(_,mask,rhs) in enumerate(eqs):ub[y0+e]=math.ceil(mask.bit_count()/2)

    # ne exact parity equalities + ne implication inequalities z_t+v_e<=1.
    A=lil_matrix((2*ne,nv),dtype=float)
    lo=np.full(2*ne,-np.inf);hi=np.full(2*ne,np.inf)
    for e,(t,mask,rhs) in enumerate(eqs):
        m=mask
        while m:
            bit=(m&-m).bit_length()-1;A[e,bit]=1;m^=1<<bit
        A[e,y0+e]=-2
        # sum a_i x_i - 2y - (1-2b)v = b
        A[e,v0+e]=-(1-2*rhs)
        lo[e]=hi[e]=rhs
        r=ne+e
        A[r,z0+t]=1;A[r,v0+e]=1;hi[r]=1
    return objs,Bounds(lb,ub),c,integrality,LinearConstraint(csr_matrix(A),lo,hi)


def solve(pos):
    objs,bounds,c,integrality,constraint=build(pos)
    res=milp(c,integrality=integrality,bounds=bounds,constraints=constraint,
             options={'time_limit':900,'mip_rel_gap':0.0,'presolve':True})
    print('position',pos,'status',res.status,'message',res.message,
          'fun',res.fun,'gap',getattr(res,'mip_gap',None),
          'dual',getattr(res,'mip_dual_bound',None),'nodes',getattr(res,'mip_node_count',None),flush=True)
    assert res.success and res.status==0 and abs(res.mip_gap)<1e-12
    opt=round(-res.fun);dual=round(-res.mip_dual_bound);assert opt==dual,(opt,dual)
    z=res.x[128:128+len(objs)]
    active=[i for i,a in enumerate(z) if a>0.5]
    dist=Counter((objs[i][1],objs[i][2]) for i in active)
    print('position',pos,'EXACT_weighted_support_activity_max',opt,
          'active_distribution',dict(dist),'object_count',len(objs),flush=True)
    return opt


def main():
    vals={p:solve(p) for p in 'ABCD'}
    print('PASS PROBE V26_Q138_PREDECESSOR_LEAF_WEIGHTED_ACTIVITY_XOR_MILP')
    print('weighted_uniform_candidate_bounds',vals)
    print('scope=exact XOR-MILP weighted support activity; theorem requires independent mathematical statement/recount')

if __name__=='__main__':main()
