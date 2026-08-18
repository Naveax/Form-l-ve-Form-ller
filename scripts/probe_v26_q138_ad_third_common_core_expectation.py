#!/usr/bin/env python3
import math
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T

MASK=(1<<128)-1


def solve_rows(rows):
    return T.rref([(r&MASK,(r>>128)&1) for r in rows],n=128)


def group_data(pos):
    raw,_=P.direct_supports(pos)
    C=Counter(can for _t,_z,can in raw)
    odd=[can for can,n in C.items() if n&1]
    groups=defaultdict(list)
    for can in odd:
        cond=P.canonical_condition(I.input_condition(can))
        groups[cond].append(can)
    expected={'A':4531,'D':8629}[pos]
    assert len(groups)==expected
    return list(groups)


def node_stats(groups,node):
    ns=solve_rows(node)
    assert ns is not None
    nr=ns[0]
    rd=Counter(); compatible=0; mu=Fraction(0,1)
    for cond in groups:
        s=solve_rows(tuple(node)+tuple(cond))
        if s is None:continue
        compatible+=1
        rr=s[0]-nr
        assert rr>=0
        rd[rr]+=1
        mu += Fraction(1,1<<rr)
    return nr,compatible,rd,mu


def main():
    for pos in 'AD':
        groups=group_data(pos)
        freq=Counter(r for cond in groups for r in cond)
        top=[r for r,_n in freq.most_common(12)]
        print('position',pos,'groups',len(groups),
              'top_frequencies',[freq[r] for r in top],flush=True)
        best_forced=0
        for k in range(0,9):
            node=tuple(top[:k])
            s=solve_rows(node)
            if s is None:
                print('position',pos,'k',k,'common_node_INCONSISTENT',flush=True)
                break
            nr,U,rd,mu=node_stats(groups,node)
            lower=(mu.numerator+mu.denominator-1)//mu.denominator
            comp_bounds=[len(groups)-freq[r] for r in top[:k]]
            max_comp=max(comp_bounds,default=0)
            all_forced=(k>0 and lower>max_comp)
            if all_forced:best_forced=k
            print('position',pos,'k',k,'node_rank',nr,
                  'compatible_groups',U,
                  'residual_rank_distribution',dict(sorted(rd.items())),
                  'mean_active_exact',f'{mu.numerator}/{mu.denominator}',
                  'mean_active_float',float(mu),
                  'certified_global_lower_from_mean',lower,
                  'largest_literal_complement_upper',max_comp,
                  'all_first_k_literals_forced_for_any_global_maximizer',all_forced,
                  flush=True)
        print('position',pos,'largest_prefix_certified_forced_by_mean_vs_literal_complements',best_forced,flush=True)
    print('PASS PROBE V26_Q138_AD_THIRD_COMMON_CORE_EXPECTATION')
    print('scope=exact common-core forcing/lower-bound geometry for active condition groups; no complete assembled-rank upper theorem')

if __name__=='__main__':main()
