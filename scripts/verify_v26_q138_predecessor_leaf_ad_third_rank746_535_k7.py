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


def conv4_layer(seqs,k):
    a,b,c,d=seqs
    s=0
    for i in range(k+1):
        for j in range(k-i+1):
            for q in range(k-i-j+1):
                r=k-i-j-q
                s += a[i]*b[j]*c[q]*d[r]
    return s


def verify_a_correction181():
    ss=C1.e1_supports('A')
    assert len(ss)==271
    types=Counter(); left=Counter()
    for typ,can in ss:
        assert A.cut_intersection(can)==0
        ar=C1.left_beta_rank(can)
        assert ar in (10,11)
        M=G.singleton_side_map(can,R,S)
        assert len(M)==21
        types[typ]+=1; left[ar]+=1
    assert types==Counter({'w91full':181,'w92n1':90})
    assert left==Counter({10:266,11:5})
    activity=181
    per_sector_rank=1
    bound=activity*per_sector_rank
    assert bound==181
    return bound,types,left


def main():
    a_corr,types,left=verify_a_correction181()

    # Constructive cover constants are exact outputs of the clean corrected
    # PR-checkout receipts named in the theorem. This verifier checks the
    # corollary arithmetic and independently rechecks the new A singleton
    # correction lemma on all271 supports.
    A_DIRECT_INSIDE=565   # clean 32160207690, A6 interpolated cover
    A_DIRECT_OUTSIDE=189  # admitted forced-core theorem
    D_DIRECT_INSIDE=179   # clean 32160149637, D5 interpolated cover
    D_DIRECT_OUTSIDE=364  # admitted forced-core theorem
    D_CORR_INSIDE=265     # clean 32159421297, D5-compatible e1 sectors
    D_CORR_OUTSIDE=171    # admitted global D e1 correction bound

    a_inside=A_DIRECT_INSIDE+a_corr
    a_outside=A_DIRECT_OUTSIDE+a_corr
    a2=max(a_inside,a_outside)
    assert (a_inside,a_outside,a2)==(746,370,746)

    d_inside=D_DIRECT_INSIDE+D_CORR_INSIDE
    d_outside=D_DIRECT_OUTSIDE+D_CORR_OUTSIDE
    d2=max(d_inside,d_outside)
    assert (d_inside,d_outside,d2)==(444,535,535)

    seqs=(
        [3,219,a2]+[2048]*8,
        [36,812,2048]+[2048]*8,
        [84,972,2048]+[2048]*8,
        [3,207,d2]+[2048]*8,
    )
    layers=[conv4_layer(seqs,k) for k in range(8)]
    expected=[
        27216,
        4793472,
        289913040,
        7291256400,
        89132856768,
        639130051056,
        3234960487008,
        12391314882560,
    ]
    assert layers==expected,(layers,expected)
    total=sum(layers)
    budget=1<<44
    margin=budget-total
    assert total==16362124267520
    assert margin==1230061776896
    assert total<budget

    print('A_e1_types',dict(types),'A_left_beta_rank_distribution',dict(sorted(left.items())))
    print('A_e1_right21_singleton_all271',True,'A_correction_rank<=',a_corr)
    print('A_direct_inside_A6<=',A_DIRECT_INSIDE,'A_direct_outside_A6<=',A_DIRECT_OUTSIDE)
    print('A_complete_third_inside_outside_uniform',(a_inside,a_outside,a2))
    print('D_direct_inside_D5<=',D_DIRECT_INSIDE,'D_direct_outside_D5<=',D_DIRECT_OUTSIDE)
    print('D_correction_inside_D5<=',D_CORR_INSIDE,'D_correction_outside_D5<=',D_CORR_OUTSIDE)
    print('D_complete_third_inside_outside_uniform',(d_inside,d_outside,d2))
    print('current_index2_envelopes',{'A':a2,'B':2048,'C':2048,'D':d2})
    print('layers_k0_k7',layers)
    print('sum_k0_k7',total,'budget_2^44',budget,'margin',margin)
    print('PASS V26_Q138_PREDECESSOR_LEAF_AD_THIRD_RANK746_535_K7')
    print('scope=complete A/D index2 dyadic envelopes plus dynamic k0..k7 prefix only; k>=8 tail remains open')

if __name__=='__main__':
    main()
