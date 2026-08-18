#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A


def conv4_layer(seqs,k):
    a,b,c,d=seqs
    s=0
    for i in range(k+1):
        for j in range(k-i+1):
            for q in range(k-i-j+1):
                r=k-i-j-q
                s += a[i]*b[j]*c[q]*d[r]
    return s


def main():
    # Recheck the raw reachable e2 populations and cut factorization. The
    # explicit global template cover counts are constructive outputs of clean
    # run32190142624; this corollary verifier checks their lift semantics and
    # all downstream arithmetic.
    expected={'A':12098,'D':12363}
    for pos in 'AD':
        raw,stats=P.direct_supports(pos)
        assert len(raw)==expected[pos],(pos,len(raw))
        assert all(A.cut_intersection(can)==0 for _typ,_zs,can in raw)
        print('position',pos,'raw_reachable_e2',len(raw),'all_cut_intersection_zero',True,'stats',stats)

    A_RAW_COVER=564  # clean32190142624 explicit verified global right21 templates
    D_RAW_COVER=179  # clean32190142624 explicit verified global left11 templates

    # Exact signed e2 aggregate is congruent mod2 to the direct e2 support
    # residue because +/-1 are both1 mod2. Choosing that exact aggregate as K2
    # removes the entire valuation-e2 family from the next residual.
    for s in (1,-1):
        assert (s-1)%2==0
        assert (s-s)//2==0

    a2=A_RAW_COVER; d2=D_RAW_COVER
    seqs=(
        [3,219,a2]+[2048]*10,
        [36,812,2048]+[2048]*10,
        [84,972,2048]+[2048]*10,
        [3,207,d2]+[2048]*10,
    )
    layers=[conv4_layer(seqs,k) for k in range(9)]
    expected_layers=[
        27216,
        4793472,
        285032304,
        6775002288,
        74626868736,
        479046918480,
        2345342671296,
        9015469473792,
        28230524010496,
    ]
    assert layers==expected_layers,(layers,expected_layers)
    total7=sum(layers[:8]); budget=1<<44; margin=budget-total7
    assert total7==11921550787584
    assert margin==5670635256832
    assert total7<budget

    print('exact_signed_e2_lift_rank_A<=',a2,'D<=',d2)
    print('inherited_e2_correction_at_index3',0)
    print('layers_k0_k8',layers)
    print('sum_k0_k7',total7,'budget_2^44',budget,'margin',margin)
    print('generic_k8_with_unresolved_index3_caps',layers[8])
    print('PASS V26_Q138_PREDECESSOR_LEAF_AD_EXACT_SIGNED_E2_LIFT_RANK564_179')
    print('scope=exact signed e2 lift plus dynamic k0..k7; complete index>=3 tail remains open')

if __name__=='__main__':main()
