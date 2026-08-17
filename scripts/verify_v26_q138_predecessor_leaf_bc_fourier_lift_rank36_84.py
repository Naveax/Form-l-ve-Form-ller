#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_bc_input_activity_no_gain as N
import probe_v26_q138_predecessor_leaf_ad_affine_fourier_union as F
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as B
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T


def signed_cross_rank(pos):
    # Reconstruct the four rank128 weight122 sectors and XOR their quadratic
    # cross forms exactly, as in the clean first-residue verifier.
    rank128=[]
    sites=[(j,i) for j in range(1,5) for i in range(31)]
    import itertools
    for z in itertools.combinations(sites,2):
        if D.internal_class('B',D.carries(z))[0]==128:rank128.append(z)
    assert rank128==[((1,0),(2,0)),((1,0),(4,0)),((2,0),(3,0)),((3,0),(4,0))]
    supports=[A.canonical_support(pos,D.carries(z),expect_internal=128) for z in rank128]
    assert all(x==supports[0] for x in supports)
    sd=A.cut_intersection(supports[0]);assert sd==2
    rows=[0]*len(A.S1)
    for z in rank128:
        qrows=B.sign_cross_rows(pos,D.carries(z))
        rows=[a^b for a,b in zip(rows,qrows)]
    qrank=T.gf2_rank(rows,len(A.R1));assert qrank==2
    return sd,qrank


def main():
    expected={'B':(16,36),'C':(64,84)}
    for pos in 'BC':
        objs,total=N.residue_objects(pos)
        affine=objs[:-1];assert len(affine)==103
        UL=set()
        for can in affine:
            BL=F.rowspace_basis(can,F.S)
            UL |= F.enumerate_space(BL)
        union=len(UL)
        assert union==expected[pos][0],(pos,union)

        sd,qrank=signed_cross_rank(pos)
        rectangles=1<<sd
        signed_q_rank=rectangles*((1<<qrank)+1)
        assert signed_q_rank==20
        lift_rank=union+signed_q_rank
        assert lift_rank==expected[pos][1]

        # Reduction mod2 of an integer rank-r lift cannot have larger rank over F2.
        assert lift_rank < (1052 if pos=='B' else 1160)
        print('position',pos,'affine_left_frequency_union',union,
              'signed_support_rectangles',rectangles,'signed_cross_rank',qrank,
              'signed_integer_rank_bound',signed_q_rank,
              'explicit_integer_first_lift_rank_bound',lift_rank)

    print('PASS V26_Q138_PREDECESSOR_LEAF_BC_FOURIER_LIFT_RANK36_84')
    print('B: 2^121 L_B = K_B + 2 R_B with rank_Q(K_B)<=36')
    print('C: 2^121 L_C = K_C + 2 R_C with rank_Q(K_C)<=84')
    print('these_supersede_first_layer_envelopes=1052,1160')
    print('scope=explicit first dyadic integer lifts only; residuals/full leaf/work remain unresolved')

if __name__=='__main__':main()
