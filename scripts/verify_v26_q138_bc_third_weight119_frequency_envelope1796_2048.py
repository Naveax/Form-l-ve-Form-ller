#!/usr/bin/env python3
import itertools,math,sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_predecessor_leaf_fast_nullspace_fourier as Q
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as V


def qrank(sig,zs):
    rows=[]
    for z in zs:rows.extend(sig[z])
    return T.gf2_rank(rows,4)


def candidates(active,inert,sig):
    for r in range(2,6):
        for core in itertools.combinations(active,r):
            if qrank(sig,core)!=4:continue
            for fill in itertools.combinations(inert,5-r):
                yield tuple(sorted(core+fill))


def space_mask(B):
    vals=[0]
    for b in B:vals += [x^b for x in vals]
    out=0
    for x in vals:out |= 1<<x
    return out


def main():
    sites=[(j,i) for j in range(1,5) for i in range(31)]
    F0=T.forms('B',(0,0,0,0,0));base=A.internal_null('B',D.carries([]))
    assert base[0]==124 and len(base[2])==4
    sig={z:V.quotient_signature(F0,base[2],*z) for z in sites}
    inert=[z for z in sites if sig[z]==(0,0)]
    active=[z for z in sites if sig[z]!=(0,0)]
    assert len(inert)==95 and len(active)==29

    core={r:sum(qrank(sig,z)==4 for z in itertools.combinations(active,r)) for r in range(2,6)}
    assert core=={2:4,3:104,4:1301,5:10425},core
    assert core[2]*95+core[3]==484
    assert core[2]*math.comb(95,2)+core[3]*95+core[4]==29041
    total5=(core[2]*math.comb(95,3)+core[3]*math.comb(95,2)+core[4]*95+core[5])
    assert total5==1_152_040

    expected={'B':(1_152_040,1796,8,None),'C':(934_476,2048,8,934_476)}
    for pos in 'BC':
        _,res,free,extra=Q.setup(pos,False)
        U=0;tested=0;maxrank=0;saturation=None;cache={}
        for zs in candidates(active,inert,sig):
            tested+=1
            B=Q.left_space(res,free,extra,zs)
            assert B is not None,(pos,zs)
            maxrank=max(maxrank,len(B))
            key=tuple(sorted(B))
            if key not in cache:cache[key]=space_mask(B)
            U |= cache[key]
            if U.bit_count()==2048:
                saturation=tested
                break
        etested,eunion,emax,esat=expected[pos]
        assert tested==etested,(pos,tested,etested)
        assert U.bit_count()==eunion,(pos,U.bit_count(),eunion)
        assert maxrank==emax,(pos,maxrank,emax)
        assert saturation==esat,(pos,saturation,esat)
        print('position',pos,'fullrank_candidates_tested',tested,
              'distinct_left_spaces',len(cache),
              'max_individual_left_rank',maxrank,
              'candidate_left_frequency_union',U.bit_count(),
              'saturation_at',saturation,flush=True)

    print('PASS V26_Q138_BC_THIRD_WEIGHT119_FREQUENCY_ENVELOPE1796_2048')
    print('active_core_rank4_counts=2:4,3:104,4:1301,5:10425')
    print('fullrank_weight119_candidate_count=1152040')
    print('B_weight119_fullrank_support_left_factor_envelope<=1796')
    print('C_weight119_fullrank_candidate_homogeneous_envelope=2048_NO_GAIN')
    print('scope=weight119 internally-full-rank homogeneous support-frequency envelope only; no complete b2/c2 claim')

if __name__=='__main__':main()
