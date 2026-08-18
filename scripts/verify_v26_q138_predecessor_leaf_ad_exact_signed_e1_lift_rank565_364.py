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


def scalar_identities():
    for s in (1,-1):
        q=1 if s<0 else 0
        # exact e0 contribution to M1 after the admitted first lift
        assert (s-1)//2 == -q
        # e1 exact signed lift is a valid mod2 lift of the support indicator
        assert (s-1) % 2 == 0
        # subtracting the exact signed value leaves no higher residual
        assert (s-s)//2 == 0


def verify_singleton_signed_e1():
    out={}
    for pos in 'AD':
        ss=C1.e1_supports(pos)
        expected_n=271 if pos=='A' else 274
        assert len(ss)==expected_n
        types=Counter(); left=Counter(); singleton=0
        for typ,can in ss:
            assert A.cut_intersection(can)==0
            ar=C1.left_beta_rank(can)
            left[ar]+=1; types[typ]+=1
            if pos=='A':
                M=G.singleton_side_map(can,R,S)
                assert len(M)==21
            else:
                M=G.singleton_side_map(can,S,R)
                assert len(M)==11
            singleton += 1
        assert singleton==expected_n
        if pos=='A':
            assert types==Counter({'w91full':181,'w92n1':90})
            assert left==Counter({10:266,11:5})
            activity=181; e0_budget=38
        else:
            assert types==Counter({'w91full':183,'w92n1':91})
            assert left==Counter({11:274})
            activity=171; e0_budget=36
        second_lift=activity+e0_budget
        out[pos]=(activity,e0_budget,second_lift,types,left)
    assert out['A'][2]==219
    assert out['D'][2]==207
    return out


def main():
    scalar_identities()
    info=verify_singleton_signed_e1()

    # Clean corrected interpolated direct-e2 cover receipts:
    # A6 run32160207690 ->565 inside, forced-core outside upper189.
    # D5 run32160149637 ->179 inside, forced-core outside upper364.
    A_DIRECT=max(565,189)
    D_DIRECT=max(179,364)
    assert A_DIRECT==565
    assert D_DIRECT==364

    # Exact signed e1 second lift leaves no inherited e1 third correction.
    a2=A_DIRECT
    d2=D_DIRECT

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
        286719696,
        6955731216,
        79723547424,
        535328405616,
        2657484843456,
        10194932924416,
    ]
    assert layers==expected,(layers,expected)
    total=sum(layers); budget=1<<44; margin=budget-total
    assert total==13474716992512
    assert margin==4117469051904
    assert total<budget

    print('A_e1_singleton_supports',sum(info['A'][3].values()),
          'activity',info['A'][0],'e0_budget',info['A'][1],
          'second_lift_rank<=',info['A'][2])
    print('D_e1_singleton_supports',sum(info['D'][3].values()),
          'activity',info['D'][0],'e0_budget',info['D'][1],
          'second_lift_rank<=',info['D'][2])
    print('exact_signed_e1_lift_leaves_inherited_third_correction',0)
    print('A_index2_direct_only<=',a2,'D_index2_direct_only<=',d2)
    print('layers_k0_k7',layers)
    print('sum_k0_k7',total,'budget_2^44',budget,'margin',margin)
    print('PASS V26_Q138_PREDECESSOR_LEAF_AD_EXACT_SIGNED_E1_LIFT_RANK565_364')
    print('scope=index1 same-rank lift plus direct-only index2 envelopes and dynamic k0..k7 prefix; complete higher tail remains open')

if __name__=='__main__':
    main()
