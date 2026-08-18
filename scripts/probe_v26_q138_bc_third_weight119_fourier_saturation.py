#!/usr/bin/env python3
import itertools,sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_predecessor_leaf_fast_nullspace_fourier as Q
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as V

MAX_FULL=2_000_000


def qrank(sig,zs):
    rows=[]
    for z in zs:rows.extend(sig[z])
    return T.gf2_rank(rows,4)


def candidate_fullrank5(active,inert,sig):
    # Inert sites have zero quotient signature, so the active subset alone
    # decides whether the old 4D nullspace is killed. Generate only exact
    # rank4 active cores and fill the remaining slots with inert sites.
    for r in range(2,6):
        for core in itertools.combinations(active,r):
            if qrank(sig,core)!=4:continue
            for fill in itertools.combinations(inert,5-r):
                yield tuple(sorted(core+fill))


def main():
    sites=[(j,i) for j in range(1,5) for i in range(31)]
    F0=T.forms('B',(0,0,0,0,0));base=A.internal_null('B',D.carries([]))
    assert base[0]==124 and len(base[2])==4
    sig={z:V.quotient_signature(F0,base[2],*z) for z in sites}
    inert=[z for z in sites if sig[z]==(0,0)];active=[z for z in sites if sig[z]!=(0,0)]
    assert len(inert)==95 and len(active)==29
    print('quotient_signature_zero_sites',len(inert),'active_sites',len(active),
          'active_signature_multiplicity',dict(Counter(sig[z] for z in active)),flush=True)

    for pos in 'BC':
        F,res,free,extra=Q.setup(pos,False)
        U=set();full=0;growth=[];sat_at=None
        seen=set()
        for zs in candidate_fullrank5(active,inert,sig):
            if zs in seen:continue
            seen.add(zs);full+=1
            B=Q.left_space(res,free,extra,zs)
            assert B is not None,(pos,zs)
            before=len(U);U |= Q.enumerate_space(B)
            if len(U)>before and len(growth)<40:growth.append((full,zs,len(B),len(U)))
            if len(U)==2048:
                sat_at=full;break
            if full>=MAX_FULL:break
        print('position',pos,'weight119_fullrank_tested',full,
              'left_frequency_union',len(U),'saturated',sat_at is not None,
              'saturation_at_fullrank_candidate',sat_at,'growth',repr(growth),flush=True)
    print('PASS PROBE V26_Q138_BC_THIRD_WEIGHT119_FOURIER_SATURATION')
    print('scope=deterministic exact full-rank candidate saturation witness search; if saturated, exact union=2048; otherwise no upper-bound claim')

if __name__=='__main__':main()
