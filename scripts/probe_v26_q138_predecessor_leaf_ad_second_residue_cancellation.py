#!/usr/bin/env python3
import itertools
from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A


def main():
    sites=[(j,i) for j in range(1,4) for i in range(31)]
    special={(1,0),(3,0)}
    for pos in 'AD':
        affine=[];labels=[]

        # Reachable weight91 full-rank supports.
        for z in itertools.combinations(sites,2):
            C=D.carries(z,ad=True)
            if A.internal_null(pos,C)[0]!=128:continue
            can=A.canonical_support(pos,C,expect_internal=128)
            if can is None:continue
            assert A.cut_intersection(can)==0
            affine.append(can);labels.append(('w91',z))

        # Reachable weight92 nullity-one equal-sign supports.
        FF=D.full_forms(pos)
        for z in sites:
            C=D.carries([z],ad=True)
            sol=A.internal_null(pos,C)
            if sol[0]!=127:continue
            assert len(sol[2])==1
            der=A.derivative_form(FF,A.map_internal_to_full(sol[2][0]))
            can=A.canonical_support(pos,C,der,127)
            if can is None:continue
            assert A.cut_intersection(can)==0
            affine.append(can);labels.append(('w92',z))

        raw=len(affine)
        C=Counter(affine)
        mult=Counter(C.values())
        odd=[x for x,n in C.items() if n&1]
        even_cancelled=raw-sum(1 for x in odd)

        # Recover label groups for repeated supports.
        groups={}
        for lab,can in zip(labels,affine):groups.setdefault(can,[]).append(lab)
        repeated=sorted((v for v in groups.values() if len(v)>1),key=lambda v:(-len(v),repr(v)))

        print('position',pos,'raw_affine',raw,'unique_supports',len(C),
              'multiplicity_distribution',dict(mult),'odd_supports',len(odd),
              'raw_minus_odd',even_cancelled)
        print('position',pos,'repeated_group_count',len(repeated))
        for g in repeated[:40]:print('repeat',pos,repr(g))

        # The three signed quadratic terms: compare support identities.
        signed=[]
        for z in ((1,0),(3,0)):
            C0=D.carries([z],ad=True)
            can=A.canonical_support(pos,C0,expect_internal=128)
            assert can is not None
            q,r=A.sign_cross_rank(pos,C0)
            signed.append((('w92',z),can,q))
        Ctop=D.carries([],ad=True)
        sol=A.internal_null(pos,Ctop);assert sol[0]==127 and len(sol[2])==1
        der=A.derivative_form(FF,A.map_internal_to_full(sol[2][0]))
        can=A.canonical_support(pos,Ctop,der,127);assert can is not None
        q,r=A.sign_cross_rank(pos,Ctop,der)
        signed.append((('w93','top'),can,q))
        print('position',pos,'signed_support_equalities',
              [[signed[i][1]==signed[j][1] for j in range(3)] for i in range(3)],
              'cross_ranks',[x[2] for x in signed])

    print('PASS PROBE V26_Q138_AD_SECOND_RESIDUE_CANCELLATION')
    print('scope=exploratory canonical-support cancellation probe; theorem only after interpreting exact result')

if __name__=='__main__':main()
