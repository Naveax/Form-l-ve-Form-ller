#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S


def main():
    e0,_,_=S.H.classify_patterns()
    expected={'B':(272,252,348,668,1016),'C':(388,280,432,788,1220)}
    for pos in 'BC':
        # Direct full-fiber checks for both polar-rank-two e0 classes.
        S.validate_completion(pos,e0[0][0][0],e0[0][0][1])
        zs,cls=next((z,c) for z,c in e0[1] if c==(125,3,2))
        S.validate_completion(pos,zs,cls)

        E=S.grouped_e0_basis(pos)
        H=S.half_basis(pos)
        U=S.union_basis(E,H)
        e,h,u,support,total=expected[pos]
        assert len(E)==e and len(H)==h and len(U)==u
        assert support+u==total
        print('position',pos,'support_only_lift_rank',support,
              'grouped_e0_rank_F2',e,'half_rank_F2',h,
              'sign_union_rank_F2',u,'second_integer_lift_rank<=',total,flush=True)

    print('PASS V26_Q138_PREDECESSOR_LEAF_BC_SECOND_RESIDUE_RANK1016_1220')
    print('B: 2^121 L_B = K_B0 + 2 K_B1 + 4 R_B2; rank_Q(K_B0)<=36; rank_Q(K_B1)<=1016')
    print('C: 2^121 L_C = K_C0 + 2 K_C1 + 4 R_C2; rank_Q(K_C0)<=84; rank_Q(K_C1)<=1220')
    print('dependency=support-only integer lifts 668/788 from clean support-frequency-nesting theorem')
    print('scope=first two dyadic lifts only; no full leaf Schmidt-rank or arithmetic-work claim')

if __name__=='__main__':main()
