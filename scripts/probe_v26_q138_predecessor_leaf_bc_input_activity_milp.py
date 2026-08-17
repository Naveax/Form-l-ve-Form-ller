#!/usr/bin/env python3
import itertools,math,sys
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import lil_matrix,csr_matrix

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as B
import probe_v26_q138_predecessor_leaf_ad_input_activity_quotient as Q


def build_bc_objects(pos):
    sites=[(j,i) for j in range(1,5) for i in range(31)]
    F0=T.forms('B',(0,0,0,0,0));base=A.internal_null('B',D.carries([]))
    assert base[0]==124 and len(base[2])==4
    sig={z:B.quotient_signature(F0,base[2],*z) for z in sites}
    full121=[]
    for z in itertools.combinations(sites,3):
        rows=[]
        for x in z:rows.extend(sig[x])
        if B.rank4(rows)==4:full121.append(z)
    assert len(full121)==484

    keep123=[]
    for z in sites:
        cls=D.internal_class('B',D.carries([z]))
        if cls in ((125,3,2),(126,2,0)):keep123.append((z,cls))
    assert len(keep123)==22

    rank127=[];rank128=[]
    for z in itertools.combinations(sites,2):
        cls=D.internal_class('B',D.carries(z))
        if cls[0]==127:rank127.append(z)
        if cls[0]==128:rank128.append(z)
    assert len(rank127)==74 and len(rank128)==4

    affine=[]
    for z in full121:
        can=A.canonical_support(pos,D.carries(z),expect_internal=128)
        if can is not None:affine.append(can)
    for z in rank127:
        can,cls,rd=B.gauss_nonzero_support(pos,D.carries(z))
        assert cls==(127,1,0) and rd==1 and can is not None
        affine.append(can)
    for z,cls0 in keep123:
        can,cls,rd=B.gauss_nonzero_support(pos,D.carries([z]))
        assert cls==cls0 and can is not None
        affine.append(can)
    can,cls,rd=B.gauss_nonzero_support(pos,D.carries([]))
    assert cls==(124,4,2) and rd==2 and can is not None
    affine.append(can)

    C=Counter(affine);odd=[can for can,n in C.items() if n&1]
    assert len(odd)==103
    objs=[(can,1<<A.cut_intersection(can),'affine') for can in odd]

    supports=[A.canonical_support(pos,D.carries(z),expect_internal=128) for z in rank128]
    assert all(x==supports[0] for x in supports)
    assert A.cut_intersection(supports[0])==2
    # Existing theorem bounds the combined signed term by16 whenever its
    # common support is active. Include that support as one weighted object.
    objs.append((supports[0],16,'signed4'))
    return objs


def build_milp(pos):
    objs=build_bc_objects(pos)
    conds=[Q.canonical_input_rows(can) for can,w,k in objs]
    weights=[w for can,w,k in objs]
    nt=len(objs);eqs=[]
    for t,cond in enumerate(conds):
        for row in cond:
            eqs.append((t,row&((1<<128)-1),(row>>128)&1))
    nx=128;z0=nx;y0=z0+nt;nv=y0+len(eqs)
    c=np.zeros(nv); c[z0:z0+nt]=-np.asarray(weights,dtype=float)
    integ=np.ones(nv,dtype=np.uint8)
    lb=np.zeros(nv);ub=np.ones(nv)
    for e,(_,mask,rhs) in enumerate(eqs):ub[y0+e]=math.ceil(mask.bit_count()/2)
    A0=lil_matrix((2*len(eqs),nv),dtype=float)
    lo=np.full(2*len(eqs),-np.inf);hi=np.full(2*len(eqs),np.inf)
    for e,(t,mask,rhs) in enumerate(eqs):
        bits=[];m=mask
        while m:
            b=(m&-m).bit_length()-1;bits.append(b);m^=1<<b
        M=len(bits)+1;r=2*e
        for b in bits:A0[r,b]=1;A0[r+1,b]=1
        A0[r,y0+e]=-2;A0[r+1,y0+e]=-2
        A0[r,z0+t]=M;A0[r+1,z0+t]=-M
        hi[r]=M+rhs;lo[r+1]=-M+rhs
    return objs,Bounds(lb,ub),c,integ,LinearConstraint(csr_matrix(A0),lo,hi)


def solve(pos):
    objs,bounds,c,integ,cons=build_milp(pos)
    res=milp(c,integrality=integ,bounds=bounds,constraints=cons,
             options={'time_limit':900,'mip_rel_gap':0.0,'presolve':True})
    print('position',pos,'status',res.status,'message',res.message)
    print('position',pos,'fun',res.fun,'mip_gap',getattr(res,'mip_gap',None),
          'mip_dual_bound',getattr(res,'mip_dual_bound',None),
          'mip_node_count',getattr(res,'mip_node_count',None),flush=True)
    assert res.success and res.status==0 and abs(res.mip_gap)<1e-12
    opt=round(-res.fun);dual=round(-res.mip_dual_bound);assert opt==dual
    x=res.x[128:128+len(objs)]
    active=[i for i,v in enumerate(x) if v>0.5]
    dist=Counter((objs[i][1],objs[i][2]) for i in active)
    print('position',pos,'EXACT_weighted_activity_max',opt,
          'active_object_distribution',dict(dist),'object_count',len(objs))
    return opt


def main():
    vals={p:solve(p) for p in 'BC'}
    print('PASS PROBE V26_Q138_BC_INPUT_ACTIVITY_MILP')
    print('weighted_uniform_candidate_bounds',vals)
    print('scope=exact weighted input-activity MILP; theorem requires independent constraint recount')

if __name__=='__main__':main()
