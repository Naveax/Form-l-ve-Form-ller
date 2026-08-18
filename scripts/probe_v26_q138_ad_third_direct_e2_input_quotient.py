#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I

MASK=(1<<128)-1


def canonical_condition(cond):
    rank,eq=cond
    rows=[m|((rhs&1)<<128) for m,rhs in eq]
    r=0
    for col in range(128):
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        r+=1
    return tuple(rows[:r])


def weighted_groups(pos):
    raw,_=P.direct_supports(pos)
    C=Counter(can for _,_,can in raw)
    odd=[can for can,n in C.items() if n&1]
    G=Counter()
    for can in odd:
        cut=P.A.cut_intersection(can)
        cond=canonical_condition(I.input_condition(can))
        G[cond]+=1<<cut
    return G,len(odd)


def build_mask_basis(masks):
    basis={}
    next_id=0
    for m in masks:
        y=m;coord=0
        while y:
            p=y.bit_length()-1
            if p in basis:
                v,c=basis[p];y^=v;coord^=c
            else:
                basis[p]=(y,1<<next_id)
                next_id+=1
                break
    return basis


def coordinates(m,basis):
    y=m;coord=0
    while y:
        p=y.bit_length()-1
        v,c=basis[p]
        y^=v;coord^=c
    return coord


def main():
    for pos in 'AD':
        G,nodd=weighted_groups(pos)
        masks=[]
        for cond in G:
            for row in cond:
                m=row&MASK
                if m:masks.append(m)
        basis=build_mask_basis(masks)
        q=len(basis)
        qconds=[]
        ranks=Counter();weights=Counter()
        for cond,w in G.items():
            eq=[]
            for row in cond:
                m=row&MASK;rhs=(row>>128)&1
                if m: eq.append((coordinates(m,basis),rhs))
                else: assert rhs==0
            eq=tuple(eq)
            qconds.append((eq,w))
            ranks[len(eq)]+=1;weights[len(eq)]+=w
        assert len({eq for eq,_ in qconds})==len(G)
        total_weight=sum(G.values())
        print('position',pos,'odd_supports',nodd,'distinct_weighted_conditions',len(G),
              'total_weight',total_weight,'global_input_functional_rank',q,
              'condition_rank_distribution',dict(sorted(ranks.items())),
              'weight_by_condition_rank',dict(sorted(weights.items())),flush=True)
        if q<=24:
            best=-1;arg=0
            for y in range(1<<q):
                s=0
                for eq,w in qconds:
                    if all(((a&y).bit_count()&1)==rhs for a,rhs in eq):s+=w
                if s>best:best=s;arg=y
            print('position',pos,'EXACT_ENUM_OPT',best,'arg',arg,flush=True)
        else:
            print('position',pos,'enumeration_skipped_rank_gt_24',q,flush=True)
    print('PASS PROBE V26_Q138_AD_THIRD_DIRECT_E2_INPUT_QUOTIENT')
    print('scope=exact quotient geometry for direct e=2 support-indicator component only')

if __name__=='__main__':main()
