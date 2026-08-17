#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_predecessor_leaf_ad_third_weight90_input_activity as P

MASK=(1<<128)-1

def canonical(cond):
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
    for row in rows[r:]:
        assert (row&MASK) or not ((row>>128)&1)
    out=tuple(rows[:r])
    assert len(out)==rank
    return out


def main():
    for pos in 'AD':
        raw=P.conds(pos)
        C=Counter(canonical(c) for _,c in raw)
        weighted_ranks=Counter()
        group_ranks=Counter()
        mult=Counter(C.values())
        for cond,n in C.items():
            rr=len(cond);group_ranks[rr]+=1;weighted_ranks[rr]+=n
        print('position',pos,'raw_sectors',len(raw),'distinct_input_cosets',len(C),
              'multiplicity_distribution',dict(sorted(mult.items())),
              'max_multiplicity',max(C.values()),
              'group_rank_distribution',dict(sorted(group_ranks.items())),
              'weighted_rank_distribution',dict(sorted(weighted_ranks.items())),flush=True)
    print('PASS PROBE V26_Q138_AD_THIRD_WEIGHT90_CONDITION_GROUPS')
    print('scope=exact canonical grouping of predecessor-input affine support conditions; no maximum-activity theorem yet')

if __name__=='__main__':main()
