#!/usr/bin/env python3
import itertools,random,sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import probe_v26_q138_predecessor_leaf_ad_input_activity as I


def conds(pos):
    sites=[(j,i) for j in range(1,4) for i in range(31)]
    special={(1,0),(3,0)}
    out=[]
    for zs in itertools.combinations(sites,3):
        if not (set(zs)&special):continue
        C=D.carries(zs,ad=True)
        assert A.internal_null(pos,C)[0]==128
        can=A.canonical_support(pos,C,expect_internal=128)
        if can is None:continue
        out.append((zs,I.input_condition(can)))
    return out


def active(c,x):
    if c is None:return False
    rank,eq=c
    return all(((m&x).bit_count()&1)==rhs for m,rhs in eq)


def main():
    rng=random.Random(13890)
    samples=[0,(1<<128)-1]
    for b in (0,31,32,63,64,95,96,127):samples.append(1<<b)
    samples += [rng.getrandbits(128) for _ in range(2000)]
    for pos in 'AD':
        C=conds(pos)
        print('position',pos,'affine_consistent_weight90_sectors',len(C),flush=True)
        rd=Counter(c[1][0] for c in C)
        vals=[]
        for x in samples:vals.append(sum(active(c,x) for _,c in C))
        print('position',pos,'input_condition_rank_distribution',dict(sorted(rd.items())),
              'sample_max_active',max(vals),'nonzero_samples',sum(v>0 for v in vals),
              'activity_hist',dict(sorted(Counter(vals).items())),flush=True)
    print('PASS PROBE V26_Q138_AD_THIRD_WEIGHT90_INPUT_ACTIVITY')
    print('scope=sampled input activity only; maximum is not a theorem')

if __name__=='__main__':main()
