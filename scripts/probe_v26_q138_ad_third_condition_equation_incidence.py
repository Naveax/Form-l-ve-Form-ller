#!/usr/bin/env python3
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I


def main():
    expected={'A':(12098,4531,Counter({1:617,2:261,3:3653})),
              'D':(12363,8629,Counter({1:4895,2:3734}))}
    for pos in 'AD':
        raw,_=P.direct_supports(pos)
        C=Counter(can for _t,_z,can in raw)
        odd=[can for can,n in C.items() if n&1]
        groups=defaultdict(list)
        for can in odd:
            cond=P.canonical_condition(I.input_condition(can))
            groups[cond].append(can)
        nodd,ng,mult=expected[pos]
        assert len(odd)==nodd and len(groups)==ng
        assert Counter(map(len,groups.values()))==mult

        eqfreq=Counter()
        rankdist=Counter()
        for cond in groups:
            rankdist[len(cond)] +=1
            for row in cond:eqfreq[row]+=1
        fd=Counter(eqfreq.values())
        top=eqfreq.most_common(40)
        covered={k:sum(1 for cond in groups if any(r in dict(top[:k]) for r in cond))
                 for k in (1,2,4,8,16,32,40)}
        print('position',pos,
              'condition_groups',len(groups),
              'condition_rank_distribution',dict(sorted(rankdist.items())),
              'distinct_canonical_affine_equations',len(eqfreq),
              'equation_group_frequency_distribution',dict(sorted(fd.items())),
              'top_equation_frequencies',[n for _r,n in top],
              'groups_touched_by_top_equations',covered,flush=True)
    print('PASS PROBE V26_Q138_AD_THIRD_CONDITION_EQUATION_INCIDENCE')
    print('scope=exact canonical condition-row incidence geometry; no assembled-rank theorem')

if __name__=='__main__':main()
