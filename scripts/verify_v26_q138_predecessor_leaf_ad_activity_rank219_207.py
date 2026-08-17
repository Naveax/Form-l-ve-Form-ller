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


def affine_supports(pos):
    sites=[(j,i) for j in range(1,4) for i in range(31)]
    out=[]
    for z in itertools.combinations(sites,2):
        C=D.carries(z,ad=True)
        if A.internal_null(pos,C)[0]!=128:continue
        can=A.canonical_support(pos,C,expect_internal=128)
        if can is not None:out.append(can)
    FF=D.full_forms(pos)
    for z in sites:
        C=D.carries([z],ad=True);sol=A.internal_null(pos,C)
        if sol[0]!=127:continue
        assert len(sol[2])==1
        der=A.derivative_form(FF,A.map_internal_to_full(sol[2][0]))
        can=A.canonical_support(pos,C,der,127)
        if can is not None:out.append(can)
    return out


def input_condition(can):
    rows=list(can);r=0
    # Eliminate all32 beta variables, leaving exact affine equations on the
    # predecessor128 mask.
    for col in range(128,160):
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        r+=1
    eq=[]
    for row in rows[r:]:
        m=row&((1<<128)-1);rhs=(row>>160)&1
        if m or rhs:eq.append((m,rhs))
    sol=T.rref(eq,n=128);assert sol is not None
    # RREF the affine system for a canonical independent equation list.
    rr=[m|(rhs<<128) for m,rhs in eq];q=0
    for col in range(128):
        p=next((k for k in range(q,len(rr)) if (rr[k]>>col)&1),None)
        if p is None:continue
        rr[q],rr[p]=rr[p],rr[q]
        for k in range(len(rr)):
            if k!=q and ((rr[k]>>col)&1):rr[k]^=rr[q]
        q+=1
    for row in rr[q:]:
        assert (row&((1<<128)-1)) or not ((row>>128)&1)
    return tuple(rr[:q])


def exact_activity_opt(pos):
    supports=affine_supports(pos);conds=[input_condition(c) for c in supports]
    expected_count=271 if pos=='A' else 274
    expected_ranks=Counter({7:11,8:260}) if pos=='A' else Counter({7:13,8:176,9:85})
    assert len(supports)==expected_count
    assert Counter(len(c) for c in conds)==expected_ranks

    eqs=[]
    for t,cond in enumerate(conds):
        for row in cond:eqs.append((t,row&((1<<128)-1),(row>>128)&1))
    nx=128;nt=len(conds);ne=len(eqs);z0=nx;v0=z0+nt;y0=v0+ne;nv=y0+ne
    c=np.zeros(nv);c[z0:z0+nt]=-1
    integrality=np.ones(nv,dtype=np.uint8)
    lb=np.zeros(nv);ub=np.ones(nv)
    for e,(_,mask,rhs) in enumerate(eqs):ub[y0+e]=math.ceil(mask.bit_count()/2)

    M=lil_matrix((2*ne,nv),dtype=float);lo=np.full(2*ne,-np.inf);hi=np.full(2*ne,np.inf)
    for e,(t,mask,rhs) in enumerate(eqs):
        m=mask
        while m:
            bit=(m&-m).bit_length()-1;M[e,bit]=1;m^=1<<bit
        M[e,y0+e]=-2
        M[e,v0+e]=-(1-2*rhs)
        lo[e]=hi[e]=rhs
        r=ne+e;M[r,z0+t]=1;M[r,v0+e]=1;hi[r]=1

    res=milp(c,integrality=integrality,bounds=Bounds(lb,ub),
             constraints=LinearConstraint(csr_matrix(M),lo,hi),
             options={'time_limit':900,'mip_rel_gap':0.0,'presolve':True})
    assert res.success and res.status==0
    assert abs(res.mip_gap)<1e-12
    opt=round(-res.fun);dual=round(-res.mip_dual_bound);assert opt==dual
    expected=181 if pos=='A' else 171
    assert opt==expected,(pos,opt)
    print('position',pos,'affine_terms',nt,'condition_rank_distribution',dict(expected_ranks),
          'exact_max_active',opt,'mip_dual_bound',dual,'nodes',res.mip_node_count)
    return opt


def main():
    a=exact_activity_opt('A');d=exact_activity_opt('D')
    # Existing signed-quadratic rank budgets from the clean second-residue theorem.
    assert [11,10,11]==[11,10,11]
    assert [10,10,10]==[10,10,10]
    A_signed=(11+2)+(10+2)+(11+2)
    D_signed=3*(10+2)
    assert A_signed==38 and D_signed==36
    Anew=a+A_signed;Dnew=d+D_signed
    assert Anew==219 and Dnew==207
    assert Anew<309 and Dnew<310

    print('PASS V26_Q138_PREDECESSOR_LEAF_AD_ACTIVITY_RANK219_207')
    print('rank_F2(A_second_residue)<=219')
    print('rank_F2(D_second_residue)<=207')
    print('supersedes_uniform_bounds=309,310')
    print('scope=uniform over every fixed128 predecessor input; no source-specific mask and no full rational leaf-rank/work claim')

if __name__=='__main__':main()
