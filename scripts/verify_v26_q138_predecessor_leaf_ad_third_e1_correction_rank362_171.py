#!/usr/bin/env python3
import itertools,sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A

LEFT=sorted(A.S1)


def left_beta_rank(can):
    r=len(can);cols=[]
    for i in LEFT:
        v=0
        for k,row in enumerate(can):
            if (row>>(128+i))&1:v|=1<<k
        cols.append(v)
    return T.gf2_rank(cols,r)


def e1_supports(pos):
    sites=[(j,i) for j in range(1,4) for i in range(31)]
    FF=D.full_forms(pos);out=[]
    for zs in itertools.combinations(sites,2):
        C=D.carries(zs,ad=True)
        if A.internal_null(pos,C)[0]!=128:continue
        can=A.canonical_support(pos,C,expect_internal=128)
        if can is not None:out.append(('w91full',can))
    for z in sites:
        C=D.carries([z],ad=True);sol=A.internal_null(pos,C)
        if sol[0]!=127:continue
        assert len(sol[2])==1
        der=A.derivative_form(FF,A.map_internal_to_full(sol[2][0]))
        can=A.canonical_support(pos,C,der,127)
        if can is not None:out.append(('w92n1',can))
    return out


def scalar_lift_identities():
    for s in (1,-1):
        q=1 if s<0 else 0
        # e=0 after the first parity lift.
        m1=(s-1)//2
        assert m1==-q
        k1=-q
        assert (m1-k1)//2==0
        # e=1 after the first lift: choose the support indicator +1 in K1.
        assert (s-1)//2==-q


def main():
    scalar_lift_identities()
    expected={
        'A':{
            'types':Counter({'w91full':181,'w92n1':90}),
            'left':Counter({10:266,11:5}),
            'typed':Counter({('w91full',10):178,('w91full',11):3,('w92n1',10):88,('w92n1',11):2}),
            'activity':181,'bound':362,
        },
        'D':{
            'types':Counter({'w91full':183,'w92n1':91}),
            'left':Counter({11:274}),
            'typed':Counter({('w91full',11):183,('w92n1',11):91}),
            'activity':171,'bound':171,
        },
    }
    for pos in 'AD':
        ss=e1_supports(pos);types=Counter();left=Counter();typed=Counter()
        for typ,can in ss:
            # Dependency already admitted in the second-residue theorem; recheck
            # the beta-side separation on the exact supports used here.
            assert A.cut_intersection(can)==0
            a=left_beta_rank(can)
            types[typ]+=1;left[a]+=1;typed[(typ,a)]+=1
            assert a in (10,11)
        E=expected[pos]
        assert types==E['types'],(pos,types)
        assert left==E['left'],(pos,left)
        assert typed==E['typed'],(pos,typed)
        max_rows=max(1<<(11-a) for a in left)
        bound=E['activity']*max_rows
        assert bound==E['bound'],(pos,bound)
        print('position',pos,'e1_sector_types',dict(types),
              'left_beta_rank_distribution',dict(sorted(left.items())),
              'typed_distribution',dict(sorted(typed.items())),
              'prior_uniform_activity_max',E['activity'],
              'max_left_rows_per_active_sector',max_rows,
              'third_e1_correction_integer_lift_rank<=',bound,flush=True)
    print('PASS V26_Q138_PREDECESSOR_LEAF_AD_THIRD_E1_CORRECTION_RANK362_171')
    print('A_third_e1_correction_rank_Q<=362')
    print('D_third_e1_correction_rank_Q<=171')
    print('e0_second_lift_sign_choice=-q leaves zero e0 third correction')
    print('scope=inherited e1 correction only; direct e=2 third-residue component remains unresolved')

if __name__=='__main__':main()
