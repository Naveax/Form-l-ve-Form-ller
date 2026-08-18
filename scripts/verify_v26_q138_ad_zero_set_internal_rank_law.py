#!/usr/bin/env python3
import math,sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A

SITES=[(j,i) for j in range(1,4) for i in range(31)]
SPECIAL={(1,0),(3,0)}


def coeff_rows(pos,C):
    F=T.forms(pos,(0,0,0,0,0))
    return [m for m,_rhs in D.equations(F,C,hom=True)]


def main():
    assert len(SITES)==93 and len([z for z in SITES if z not in SPECIAL])==91
    for pos in 'AD':
        top=A.internal_null(pos,D.carries([],ad=True))
        assert top is not None and top[0]==127 and len(top[2])==1
        n=top[2][0]
        top_rows=coeff_rows(pos,D.carries([],ad=True))
        assert all(((r&n).bit_count()&1)==0 for r in top_rows)

        nonspecial=0; special=0; added_rows=0
        for z in SITES:
            C=D.carries([z],ad=True)
            sol=A.internal_null(pos,C)
            assert sol is not None
            if z in SPECIAL:
                assert sol[0]==128,(pos,z,sol[0])
                special+=1
            else:
                assert sol[0]==127 and len(sol[2])==1,(pos,z,sol[0],len(sol[2]))
                rows=coeff_rows(pos,C)
                # A zero carry adds homogeneous equality rows to the top
                # coefficient system. Every newly present row must annihilate
                # the unique top null vector; hence arbitrary unions of such
                # nonspecial additions preserve that vector.
                tcount={}
                for r in top_rows:tcount[r]=tcount.get(r,0)+1
                extra=[]
                for r in rows:
                    if tcount.get(r,0):tcount[r]-=1
                    else:extra.append(r)
                assert extra
                assert all(((r&n).bit_count()&1)==0 for r in extra),(pos,z)
                added_rows+=len(extra)
                nonspecial+=1
        assert (nonspecial,special)==(91,2)
        print('position',pos,'top_rank',top[0],'top_nullity',len(top[2]),
              'nonspecial_single_zero_rank127',nonspecial,
              'special_single_zero_rank128',special,
              'checked_nonspecial_added_rows_annihilate_top_kernel',added_rows,flush=True)

    n3=math.comb(91,3)
    f4=math.comb(93,4)-math.comb(91,4)
    assert n3==121485
    assert f4==247065
    assert f4==2*math.comb(91,3)+math.comb(91,2)
    assert n3+f4==368550
    print('three_nonspecial_zero_nullity1_candidates',n3)
    print('four_zero_with_special_fullrank_candidates',f4)
    print('combined_next_family_candidates_before_external_pruning',n3+f4)
    print('PASS V26_Q138_AD_ZERO_SET_INTERNAL_RANK_LAW')
    print('scope=arbitrary A/D homogeneous carry-zero internal rank law; external reachability and higher-residue rank remain separate')

if __name__=='__main__':main()
