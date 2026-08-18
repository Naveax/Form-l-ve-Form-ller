#!/usr/bin/env python3
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T

MASK=(1<<128)-1
RHSBIT=1<<128


def solve_rows(rows):
    return T.rref([(r&MASK,(r>>128)&1) for r in rows],n=128)


def groups_for(pos):
    raw,_=P.direct_supports(pos)
    C=Counter(can for _t,_z,can in raw)
    odd=[can for can,n in C.items() if n&1]
    G=defaultdict(list)
    for can in odd:
        cond=P.canonical_condition(I.input_condition(can))
        G[cond].append(can)
    return list(G)


def stats(groups,node):
    ns=solve_rows(node)
    if ns is None:return None
    nr=ns[0];U=0;rd=Counter();mu=Fraction(0,1)
    for cond in groups:
        s=solve_rows(tuple(node)+tuple(cond))
        if s is None:continue
        rr=s[0]-nr;U+=1;rd[rr]+=1;mu+=Fraction(1,1<<rr)
    return nr,U,rd,mu


def main():
    for pos in 'AD':
        groups=groups_for(pos);N=len(groups)
        freq=Counter(r for cond in groups for r in cond)
        top=[r for r,_ in freq.most_common(12)]
        base=tuple(top[:5]);six=top[5]
        sb=stats(groups,base);sp=stats(groups,base+(six,));sn=stats(groups,base+(six^RHSBIT,))
        assert sb and sp and sn
        lower=(sp[3].numerator+sp[3].denominator-1)//sp[3].denominator
        print('position',pos,'global_groups',N,
              'first5_frequencies',[freq[r] for r in top[:5]],
              'sixth_frequency',freq[six],flush=True)
        for name,s in [('V5',sb),('V5_plus_sixth_true',sp),('V5_plus_sixth_false',sn)]:
            nr,U,rd,mu=s
            print('position',pos,name,'node_rank',nr,'compatible_groups',U,
                  'residual_rank_distribution',dict(sorted(rd.items())),
                  'mean_active_exact',f'{mu.numerator}/{mu.denominator}',
                  'mean_active_float',float(mu),flush=True)
        print('position',pos,'certified_global_lower_from_true_sixth_mean',lower,
              'false_sixth_compatible_upper',sn[1],
              'sixth_forced_for_every_global_maximizer',sn[1]<lower,flush=True)
        if len(top)>=7:
            s7=stats(groups,base+(six,top[6]))
            print('position',pos,'seventh_true_after_first6_consistent',s7 is not None,flush=True)
    print('PASS PROBE V26_Q138_AD_THIRD_SIXTH_COMMON_BRANCH')
    print('scope=exact active-condition common-core branch geometry; no assembled-rank upper theorem')

if __name__=='__main__':main()
