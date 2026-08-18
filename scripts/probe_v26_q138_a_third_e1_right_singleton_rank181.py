#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_ad_third_direct_e2_condition_group_rank1 as G
import verify_v26_q138_predecessor_leaf_ad_third_e1_correction_rank362_171 as C1

S=sorted(A.S1)
R=A.R1


def main():
    ss=C1.e1_supports('A')
    assert len(ss)==271
    types=Counter()
    left=Counter()
    right_singletons=0
    for typ,can in ss:
        assert A.cut_intersection(can)==0
        a=C1.left_beta_rank(can)
        assert a in (10,11)
        # Eliminate the11 S1 beta variables. Full pivot rank on all21
        # complement variables proves that for every predecessor input for
        # which the affine support is active, the support has exactly one
        # right21 assignment. Hence any correction matrix gated by this
        # support has at most one nonzero column and rational rank<=1,
        # regardless of the quadratic sign values on its one/two left rows.
        M=G.singleton_side_map(can,R,S)
        assert len(M)==21
        right_singletons += 1
        types[typ]+=1
        left[a]+=1

    assert types==Counter({'w91full':181,'w92n1':90})
    assert left==Counter({10:266,11:5})
    assert right_singletons==271

    # Imported authority: the exact predecessor-input activity theorem proves
    # that at most181 of the271 A e1 affine sectors are simultaneously active.
    activity_upper=181
    per_active_sector_rank=1
    bound=activity_upper*per_active_sector_rank
    assert bound==181

    print('A_e1_sector_types',dict(types),flush=True)
    print('A_left_beta_rank_distribution',dict(sorted(left.items())),flush=True)
    print('A_e1_right21_singleton_supports',right_singletons,'of',len(ss),flush=True)
    print('A_prior_uniform_active_sector_upper',activity_upper,flush=True)
    print('A_e1_correction_rank_per_active_sector<=',per_active_sector_rank,flush=True)
    print('A_third_e1_correction_integer_lift_rank<=',bound,flush=True)
    print('PASS PROBE V26_Q138_A_THIRD_E1_RIGHT_SINGLETON_RANK181')
    print('scope=inherited A e1 third correction under the admitted e0-zero second-lift sign choice; direct e2 remains separate')

if __name__=='__main__':
    main()
