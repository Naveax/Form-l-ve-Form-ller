#!/usr/bin/env python3
import sys
from collections import Counter,defaultdict
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_ad_third_direct_e2_condition_group_rank1 as G

MASK=(1<<128)-1
S=sorted(A.S1);R=A.R1


def insert(B,x):
    y=x
    while y:
        p=y.bit_length()-1
        if p not in B:
            B[p]=y;return True
        y^=B[p]
    return False


def parity(x):return x.bit_count()&1


def dual_constraints(cond):
    B=G.affine_basis(cond)
    piv=set(B)
    out=[]
    for t in range(128):
        if t in piv:continue
        h=1<<t
        for p,row in B.items():
            if (row>>t)&1:h|=1<<p
        out.append(h)
    h=1<<128
    for p,row in B.items():
        if (row>>128)&1:h|=1<<p
    out.append(h)
    assert len(out)==129-len(B)
    for h in out:
        assert all(parity(h&row)==0 for row in cond)
    return out


def map_vectors(M):
    return [m|((b&1)<<128) for m,b in M]


def main():
    raw,_=P.direct_supports('D')
    C=Counter(can for _,_,can in raw)
    odd=[can for can,n in C.items() if n&1]
    assert len(odd)==12363

    groups=defaultdict(list)
    for can in odd:
        cond=P.canonical_condition(I.input_condition(can))
        groups[cond].append(can)
    assert len(groups)==8629

    H={};FULL={};rank_dist=Counter();eq_count=0
    for cond,cans in groups.items():
        rank_dist[len(cond)]+=1
        M0=G.singleton_side_map(cans[0],S,R)
        B=G.affine_basis(cond)
        for can in cans[1:]:
            M=G.singleton_side_map(can,S,R)
            for (m,b),(m0,b0) in zip(M,M0):
                assert G.implied_zero(B,m^m0,b^b0)
        mv=map_vectors(M0)
        for h in dual_constraints(cond):
            ell=0
            for j,v in enumerate(mv):
                if parity(h&v):ell|=1<<j
            insert(H,h)
            insert(FULL,h|(ell<<129))
            eq_count+=1

    rank_h=len(H);rank_full=len(FULL)
    imposed=rank_full-rank_h
    feasible_ell_dim=11-imposed
    assert 0<=imposed<=11
    assert feasible_ell_dim>=0
    label_affine_dim=11-feasible_ell_dim
    distinct_bound=1<<label_affine_dim

    print('D_condition_groups',len(groups),'condition_rank_distribution',dict(sorted(rank_dist.items())),
          'stacked_membership_equations',eq_count,flush=True)
    print('global_q_rank',rank_h,'joint_q_ell_rank',rank_full,
          'independent_constraints_on_ell',imposed,
          'feasible_global_label_relation_dimension',feasible_ell_dim,flush=True)
    print('uniform_active_label_affine_dimension<=',label_affine_dim,
          'uniform_distinct_left_singleton_labels<=',distinct_bound,flush=True)
    print('PASS PROBE V26_Q138_AD_THIRD_D_GLOBAL_LABEL_RELATIONS')
    print('interpretation=each feasible ell has some global affine q_ell(x) with ell.y_g(x)=q_ell(x) on every group condition; for fixed x all active labels satisfy all such relations')
    print('scope=D direct-e2 assembled left-singleton rank only; inherited e1 correction remains separate')

if __name__=='__main__':main()
# clean PR trigger
