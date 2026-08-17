#!/usr/bin/env python3
import itertools,sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as B


def residue_objects(pos):
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
    rank127=[];rank128=[]
    for z in itertools.combinations(sites,2):
        cls=D.internal_class('B',D.carries(z))
        if cls[0]==127:rank127.append(z)
        if cls[0]==128:rank128.append(z)
    assert len(keep123)==22 and len(rank127)==74 and len(rank128)==4

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
    weighted=sum(1<<A.cut_intersection(can) for can in odd)
    assert weighted==(1036 if pos=='B' else 1144)

    signed=[A.canonical_support(pos,D.carries(z),expect_internal=128) for z in rank128]
    assert all(x==signed[0] for x in signed)
    assert A.cut_intersection(signed[0])==2
    return odd+[signed[0]],weighted+16


def input_equations(can):
    rows=list(can);r=0
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
    assert T.rref(eq,n=128) is not None
    return eq


def main():
    for pos in 'BC':
        objs,total=residue_objects(pos);assert len(objs)==104
        all_eq=[]
        for can in objs:all_eq.extend(input_equations(can))
        sol=T.rref(all_eq,n=128)
        assert sol is not None
        rank,x0,basis=sol
        assert rank<=128 and len(basis)==128-rank
        expected=1052 if pos=='B' else 1160
        assert total==expected
        print('position',pos,'objects',len(objs),'combined_input_condition_rank',rank,
              'common_input_coset_dimension',len(basis),'all_objects_simultaneously_active_possible',
              'weighted_activity_exact',total)

    print('PASS V26_Q138_PREDECESSOR_LEAF_BC_INPUT_ACTIVITY_NO_GAIN')
    print('B_weighted_activity_exact=1052')
    print('C_weighted_activity_exact=1160')
    print('consequence=input-mask mutual exclusion cannot sharpen current B/C first-residue sum bounds')
    print('scope=method-scope no-gain; true matrix-rank dependencies may still exist')

if __name__=='__main__':main()
