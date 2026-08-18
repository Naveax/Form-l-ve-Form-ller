#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_bc_second_residue_support_frequency_nesting as N
import verify_v26_q138_bc_third_weight119_frequency_envelope1796_2048 as E


def xor_sumset(U):
    U=list(U)
    return {a^b for a in U for b in U}


def bitmask(S):
    z=0
    for x in S:z|=1<<x
    return z


def bc_top_quotient():
    sites=[(j,i) for j in range(1,5) for i in range(31)]
    F0=E.T.forms('B',(0,0,0,0,0))
    base=E.A.internal_null('B',E.D.carries([]))
    assert base[0]==124 and len(base[2])==4
    sig={z:E.V.quotient_signature(F0,base[2],*z) for z in sites}
    inert=[z for z in sites if sig[z]==(0,0)]
    active=[z for z in sites if sig[z]!=(0,0)]
    assert len(inert)==95 and len(active)==29
    return active,inert,sig


def main():
    expected={'B':668,'C':788}
    sumsets={}
    for pos in 'BC':
        U=N.weight120_union(pos)
        assert len(U)==expected[pos],(pos,len(U))
        S=xor_sumset(U);sumsets[pos]=S
        print('position',pos,'second_support_frequency_space',len(U),
              'pairwise_xor_sumset',len(S),'missing_from_full2048',2048-len(S),flush=True)

    SB=sumsets['B']
    if len(SB)<2048:
        active,inert,sig=bc_top_quotient()
        tested,UB,maxrank,sat,spaces=E.weight119_union('B',active,inert,sig)
        assert tested==1_152_040 and UB.bit_count()==1796 and sat is None
        SM=bitmask(SB)
        print('position B','direct_e2_envelope',UB.bit_count(),
              'support_carry_sumset',len(SB),
              'carry_subset_direct',SM&~UB==0,
              'direct_subset_carry',UB&~SM==0,
              'symmetric_difference',(SM^UB).bit_count(),flush=True)

    print('PASS PROBE V26_Q138_BC_SECOND_LIFT_SUPPORT_CARRY_SUMSET')
    print('interpretation=natural integer support-lift XOR-vs-sum third-bit carry has left frequencies inside U120 xor U120; exact B comparison to the direct-e2 envelope is printed when subgeneric')
    print('scope=support-lift carry correction only; sign-dependent lift correction and complete b2/c2 remain open')

if __name__=='__main__':main()
# clean PR trigger v3
