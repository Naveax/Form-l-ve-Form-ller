#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A

S=sorted(A.S1)
R=A.R1
SITES=[(j,i) for j in range(1,4) for i in range(31)]
SPECIAL={(1,0),(3,0)}
OFF={'U3':0,'V3':32,'U4':64,'V4':96}


def bit(n,name,i):
    return (n>>(OFF[name]+(i%32)))&1


def interior_sensitivity(n,i):
    return bit(n,'U3',i)^bit(n,'V3',i)^bit(n,'V4',i+8)


def main():
    assert 0 in S and 0 not in R
    assert 8 not in S
    for pos in 'AD':
        top=A.internal_null(pos,D.carries([],ad=True))
        assert top is not None and top[0]==127 and len(top[2])==1
        n=top[2][0]

        # Exact prerequisites for the arbitrary-zero-set rank law: every
        # nonspecial one-zero addition preserves the unique top kernel, while
        # either special site kills it and reaches full rank128.
        ns=sp=0
        for z in SITES:
            sol=A.internal_null(pos,D.carries([z],ad=True))
            assert sol is not None
            if z in SPECIAL:
                assert sol[0]==128
                sp+=1
            else:
                assert sol[0]==127 and len(sol[2])==1
                # Both are one-dimensional kernels containing the same top
                # kernel direction, hence the canonical basis direction must
                # satisfy the one-zero system.
                F=T.forms(pos,(0,0,0,0,0))
                for m,_rhs in D.equations(F,D.carries([z],ad=True),hom=True):
                    assert ((m&n).bit_count()&1)==0,(pos,z)
                ns+=1
        assert (ns,sp)==(91,2)

        if pos=='A':
            # Every selected right beta index is controlled by an always-
            # present j3 equation. Interior bits use u+v+w; bit31 uses u=w.
            assert all(1<=i<=31 for i in R)
            sens=[]
            for i in R:
                if i<=30:
                    s=interior_sensitivity(n,i)
                else:
                    assert i==31
                    s=bit(n,'U3',31)^bit(n,'V4',7)
                sens.append(s)
            assert sens==[0]*len(R),(pos,sens)
            print('position A selected_singleton_side right21',
                  'top_kernel_selected_beta_sensitivity_rank',sum(sens),
                  'selected_indices',R,flush=True)
        else:
            js=[(k-8)%32 for k in S]
            assert all(1<=i<=30 for i in js),js
            sens=[interior_sensitivity(n,i) for i in js]
            assert sens==[0]*len(S),(pos,js,sens)
            print('position D selected_singleton_side left11',
                  'top_kernel_selected_beta_sensitivity_rank',sum(sens),
                  'selected_indices',S,'j3_source_indices',js,flush=True)

    print('PASS V26_Q138_AD_UNIVERSAL_SINGLETON_SIDE')
    print('consequence=every reachable signed A/D carry sector at every zero-set pattern has matrix rank<=1 across S1|R1')
    print('scope=sectorwise singleton side; aggregate rank still requires global map/template collision control')

if __name__=='__main__':main()
