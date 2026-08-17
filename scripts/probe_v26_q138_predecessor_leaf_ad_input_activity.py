#!/usr/bin/env python3
import itertools,random,sys
from collections import Counter
from pathlib import Path

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
        if can is not None:out.append(('w91',z,can))
    FF=D.full_forms(pos)
    for z in sites:
        C=D.carries([z],ad=True);sol=A.internal_null(pos,C)
        if sol[0]!=127:continue
        der=A.derivative_form(FF,A.map_internal_to_full(sol[2][0]))
        can=A.canonical_support(pos,C,der,127)
        if can is not None:out.append(('w92',z,can))
    return out


def input_condition(can):
    # Eliminate the32 beta variables from the affine external support. The
    # residual equations characterize exactly which128-bit predecessor masks
    # admit at least one beta assignment in this sector.
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
    sol=T.rref(eq,n=128)
    if sol is None:return None
    rank=sol[0]
    # canonical RREF equation representation for equality/grouping
    rr=[]
    for p,row in sorted(sol[3].items()) if len(sol)>3 else []:
        rr.append((p,row))
    # T.rref API does not expose canonical rows in all versions; retain eq for
    # activity tests and rank statistics.
    return rank,tuple(eq)


def active(cond,x):
    if cond is None:return False
    _,eq=cond
    return all(((m&x).bit_count()&1)==rhs for m,rhs in eq)


def main():
    rng=random.Random(138)
    for pos in 'AD':
        objs=affine_supports(pos)
        conds=[input_condition(can) for _,_,can in objs]
        assert all(c is not None for c in conds)
        ranks=Counter(c[0] for c in conds)
        dims=Counter(128-c[0] for c in conds)
        print('position',pos,'term_count',len(objs),'input_condition_rank_distribution',dict(sorted(ranks.items())),
              'dimension_distribution',dict(sorted(dims.items())))

        # Deterministic exploratory activity sampling only.
        samples=[0,(1<<128)-1]
        for bit in (0,1,31,32,63,64,95,96,127):samples.append(1<<bit)
        samples += [rng.getrandbits(128) for _ in range(2000)]
        counts=[sum(active(c,x) for c in conds) for x in samples]
        print('position',pos,'sample_activity_max',max(counts),'nonzero_samples',sum(c>0 for c in counts),
              'sample_activity_hist',dict(sorted(Counter(counts).items())))

    print('PASS PROBE V26_Q138_AD_INPUT_ACTIVITY')
    print('scope=input-condition geometry probe; sampled activity maximum is not a theorem')

if __name__=='__main__':main()
