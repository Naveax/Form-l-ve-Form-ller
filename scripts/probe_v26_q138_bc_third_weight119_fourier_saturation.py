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
MAX_CORE4=2000


def qrank(sig,zs):
    rows=[]
    for z in zs:rows.extend(sig[z])
    return T.gf2_rank(rows,4)


def candidate_fullrank_k(k,active,inert,sig):
    for r in range(2,k+1):
        for core in itertools.combinations(active,r):
            if qrank(sig,core)!=4:continue
            for fill in itertools.combinations(inert,k-r):
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

        # Cheapest exact closure: if one full-rank five-zero sector has left
        # rowspace rank11, its Walsh frequency space alone is all2048.
        witness=None;core_seen=0;extensions=0
        seen5=set()
        for z4 in candidate_fullrank_k(4,active,inert,sig):
            core_seen+=1
            for z in sites:
                if z in z4:continue
                z5=tuple(sorted(z4+(z,)))
                if z5 in seen5:continue
                seen5.add(z5);extensions+=1
                B=Q.left_space(res,free,extra,z5)
                assert B is not None,(pos,z5)
                if len(B)==11:
                    witness=z5;break
            if witness is not None or core_seen>=MAX_CORE4:break
        if witness is not None:
            print('position',pos,'SINGLE_SUPPORT_SATURATION_WITNESS',repr(witness),
                  'fullrank_weight120_cores_tested',core_seen,'extensions_tested',extensions,
                  'left_rank',11,'left_frequency_union',2048,flush=True)
            continue

        # Fallback: exact union over directly generated full-rank five-zero
        # candidates, stopping as soon as all2048 frequencies are witnessed.
        U=set();full=0;growth=[];sat_at=None;seen=set()
        for zs in candidate_fullrank_k(5,active,inert,sig):
            if zs in seen:continue
            seen.add(zs);full+=1
            B=Q.left_space(res,free,extra,zs)
            assert B is not None,(pos,zs)
            before=len(U);U |= Q.enumerate_space(B)
            if len(U)>before and len(growth)<40:growth.append((full,zs,len(B),len(U)))
            if len(U)==2048:
                sat_at=full;break
            if full>=MAX_FULL:break
        print('position',pos,'single_support_rank11_witness',None,
              'weight119_fullrank_tested',full,
              'left_frequency_union',len(U),'saturated',sat_at is not None,
              'saturation_at_fullrank_candidate',sat_at,'growth',repr(growth),flush=True)
    print('PASS PROBE V26_Q138_BC_THIRD_WEIGHT119_FOURIER_SATURATION')
    print('scope=deterministic exact full-rank saturation witness search; any rank11 single support or2048 union proves exact saturation; otherwise no upper-bound claim')

if __name__=='__main__':main()
