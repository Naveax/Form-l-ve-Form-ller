#!/usr/bin/env python3
import itertools,sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import probe_v26_q138_predecessor_leaf_ad_affine_fourier_union as F


def main():
    sites=[(j,i) for j in range(1,4) for i in range(31)]
    special={(1,0),(3,0)}
    triples=[z for z in itertools.combinations(sites,3) if set(z)&special]
    assert len(triples)==8281

    for pos in 'AD':
        UL=set();consistent=0;growth=[];rank128=0
        for idx,z in enumerate(triples,1):
            C=D.carries(z,ad=True)
            r=A.internal_null(pos,C)[0]
            assert r==128,(pos,z,r)
            rank128+=1
            can=A.canonical_support(pos,C,expect_internal=128)
            if can is None:continue
            consistent+=1
            BL=F.rowspace_basis(can,F.S)
            before=len(UL);UL |= F.enumerate_space(BL)
            if len(UL)>before and len(growth)<40:growth.append((idx,z,len(BL),len(UL)))
            if len(UL)==2048:break
        print('position',pos,'rank128_triples_seen',rank128,'consistent_seen',consistent,
              'left_frequency_union',len(UL),'saturated',len(UL)==2048,
              'growth_events',repr(growth),flush=True)
    print('PASS PROBE V26_Q138_AD_WEIGHT90_FOURIER_UNION')
    print('scope=weight90 rank128 unique-solution sector probe only; no third-residue theorem')

if __name__=='__main__':main()
