#!/usr/bin/env python3
import itertools,sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as B
import probe_v26_q138_predecessor_leaf_ad_affine_fourier_union as F
import probe_v26_q138_predecessor_leaf_bc_second_residue_correction_classes as C


def classify_patterns():
    sites,sig,P=C.setup()
    e0={0:[],1:[],2:[],3:[]};e1={0:[],1:[],2:[],3:[]};half=[]
    for k in range(4):
        for zs in itertools.combinations(sites,k):
            ir,n,pr=C.cls(zs,sig,P)
            e=k-3+n-pr//2
            if e==0:e0[k].append((zs,(ir,n,pr)))
            elif e==1:e1[k].append((zs,(ir,n,pr)))
            elif e==-1:half.append((zs,(ir,n,pr)))
    assert [len(e0[k]) for k in range(4)]==[1,22,74,484]
    assert [len(e1[k]) for k in range(4)]==[0,102,2397,8196]
    assert len(half)==4
    return e0,e1,half


def support_for(pos,zs,cls):
    ir,n,pr=cls
    Cmask=D.carries(zs)
    if n==0:
        return A.canonical_support(pos,Cmask,expect_internal=128)
    can,c2,rd=B.gauss_nonzero_support(pos,Cmask)
    assert c2==(ir,n,pr),(pos,zs,c2,(ir,n,pr))
    return can


def union_size(supports):
    U=set()
    for can in supports:
        BL=F.rowspace_basis(can,F.S);U |= F.enumerate_space(BL)
    return len(U)


def main():
    e0,e1,half=classify_patterns()
    print('classified_e0_counts',[len(e0[k]) for k in range(4)],
          'e1_counts',[len(e1[k]) for k in range(4)],'half',len(half),flush=True)
    for pos in 'BC':
        raw0=[];imp0=0
        for k in range(4):
            for zs,cls in e0[k]:
                can=support_for(pos,zs,cls)
                if can is None:imp0+=1
                else:raw0.append(can)
        expected_raw=581 if pos=='B' else 577
        assert len(raw0)==expected_raw,(pos,len(raw0))
        raw0_union=union_size(raw0)

        raw1=[];imp1=0
        byk={}
        for k in range(4):
            arr=[]
            for zs,cls in e1[k]:
                can=support_for(pos,zs,cls)
                if can is None:imp1+=1
                else:arr.append(can);raw1.append(can)
            byk[k]=len(arr)
        CC=Counter(raw1);odd1=[can for can,n in CC.items() if n&1]
        mult=Counter(CC.values())
        raw1_union=union_size(raw1)
        odd1_union=union_size(odd1)
        print('position',pos,
              'first_parity_raw_supports',len(raw0),'raw_first_parity_left_union',raw0_union,'impossible_e0',imp0,
              'e1_consistent_by_zero_count',byk,'e1_raw_supports',len(raw1),'impossible_e1',imp1,
              'e1_unique_supports',len(CC),'e1_multiplicity_distribution',dict(mult),
              'e1_odd_supports',len(odd1),'e1_raw_left_union',raw1_union,
              'e1_odd_left_union',odd1_union,flush=True)

    print('PASS PROBE V26_Q138_BC_SECOND_RESIDUE_HIGH_CORRECTION_FOURIER')
    print('scope=e1 support correction + raw e0 support Fourier geometry; sign-negative and four-half correction functions not yet bounded')

if __name__=='__main__':main()
