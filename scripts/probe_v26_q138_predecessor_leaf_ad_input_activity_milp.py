#!/usr/bin/env python3
import math,sys
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix,csr_matrix

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_predecessor_leaf_ad_input_activity as P
import probe_v26_q138_predecessor_leaf_ad_input_activity_quotient as Q


def build_problem(pos):
    objs=P.affine_supports(pos)
    conds=[Q.canonical_input_rows(can) for _,_,can in objs]
    nt=len(conds)

    # Variables: x[128] binary predecessor mask bits; z[nt] binary sector-active
    # indicators; one integer parity variable y for every affine equation.
    eqs=[]
    for t,cond in enumerate(conds):
        for row in cond:
            mask=row&((1<<128)-1); rhs=(row>>128)&1
            eqs.append((t,mask,rhs))
    ne=len(eqs)
    nx=128; z0=nx; y0=z0+nt; nv=y0+ne

    c=np.zeros(nv,dtype=float)
    c[z0:z0+nt]=-1.0  # maximize sum z
    integ=np.zeros(nv,dtype=np.uint8)
    integ[:nx]=1; integ[z0:z0+nt]=1; integ[y0:]=1
    lb=np.zeros(nv,dtype=float); ub=np.empty(nv,dtype=float)
    ub[:nx]=1; ub[z0:z0+nt]=1

    # y_e only needs 0..ceil(weight(mask)/2).
    for e,(_,mask,rhs) in enumerate(eqs):
        ub[y0+e]=math.ceil(mask.bit_count()/2)

    # Two conditional inequalities per affine equation:
    # s(x)-2y-rhs + M z <= M
    # s(x)-2y-rhs - M z >= -M
    A=lil_matrix((2*ne,nv),dtype=float)
    lo=np.full(2*ne,-np.inf,dtype=float)
    hi=np.full(2*ne,np.inf,dtype=float)
    for e,(t,mask,rhs) in enumerate(eqs):
        bits=[];m=mask
        while m:
            b=(m&-m).bit_length()-1;bits.append(b);m^=1<<b
        M=len(bits)+1
        r=2*e
        for b in bits:
            A[r,b]=1;A[r+1,b]=1
        A[r,y0+e]=-2;A[r+1,y0+e]=-2
        A[r,z0+t]=M; A[r+1,z0+t]=-M
        hi[r]=M+rhs
        lo[r+1]=-M+rhs

    return objs,Bounds(lb,ub),c,integ,LinearConstraint(csr_matrix(A),lo,hi)


def solve(pos):
    objs,bounds,c,integ,cons=build_problem(pos)
    res=milp(c,integrality=integ,bounds=bounds,constraints=cons,
             options={'time_limit':900,'mip_rel_gap':0.0,'presolve':True})
    print('position',pos,'status',res.status,'message',res.message)
    print('position',pos,'fun',res.fun,'mip_gap',getattr(res,'mip_gap',None),
          'mip_dual_bound',getattr(res,'mip_dual_bound',None),
          'mip_node_count',getattr(res,'mip_node_count',None),flush=True)
    assert res.success and res.status==0
    assert abs(getattr(res,'mip_gap',1.0))<1e-12
    opt=round(-res.fun)
    dual=round(-res.mip_dual_bound)
    assert opt==dual,(opt,dual)
    # Existing signed-quadratic worst-case terms are independent of this
    # affine activity optimization: A<=38, D<=36.
    signed=38 if pos=='A' else 36
    new_bound=opt+signed
    print('position',pos,'EXACT_max_active_affine_terms',opt,
          'uniform_second_residue_rank_bound_with_signed_worstcase',new_bound)
    return opt,new_bound


def main():
    got={p:solve(p) for p in 'AD'}
    print('PASS PROBE V26_Q138_AD_INPUT_ACTIVITY_MILP')
    print('A_opt_bound',got['A'])
    print('D_opt_bound',got['D'])
    print('scope=exact MILP optimum for affine-sector activity; theorem requires clean interpretation and independent constraint recount')

if __name__=='__main__':main()
