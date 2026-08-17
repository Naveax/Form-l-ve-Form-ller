#!/usr/bin/env python3
import itertools,sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as B


def setup():
    sites=[(j,i) for j in range(1,5) for i in range(31)]
    F0=T.forms('B',(0,0,0,0,0))
    top=A.internal_null('B',D.carries([]))
    assert top[0]==124 and len(top[2])==4
    basis=top[2]
    sig={z:B.quotient_signature(F0,basis,*z) for z in sites}
    P=B.polar_rows('B',basis)
    assert T.gf2_rank(P,4)==2
    return sites,sig,P


def kernel_basis(rows,n=4):
    sol=T.rref([(r,0) for r in rows],n=n)
    assert sol is not None
    return sol[0],sol[2]


def polar_rank_on_kernel(K,P):
    m=len(K);rows=[]
    for a in K:
        row=0
        for j,b in enumerate(K):
            z=0
            for i in range(4):
                if (a>>i)&1:z ^= (P[i]&b).bit_count()&1
            row |= z<<j
        rows.append(row)
    return T.gf2_rank(rows,m)


def cls(zs,sig,P):
    rows=[]
    for z in zs:rows.extend(sig[z])
    qrank,K=kernel_basis(rows)
    n=4-qrank
    pr=polar_rank_on_kernel(K,P)
    assert pr%2==0 and pr<=n
    irank=128-n
    return irank,n,pr


def main():
    sites,sig,P=setup()
    # k zeros => carry weight124-k; scaled M amplitude exponent when Gauss is nonzero:
    # e=(121-(124-k)) + n - pr/2 = k-3+n-pr/2.
    for k in range(4):
        C=Counter();E=Counter();total=0
        for zs in itertools.combinations(sites,k):
            total+=1
            c=cls(zs,sig,P);C[c]+=1
            _,n,pr=c;e=k-3+n-pr//2;E[e]+=1
        assert total==[1,124,7626,310124][k]
        print('zero_count',k,'carry_weight',124-k,'class_distribution',dict(sorted(C.items())),
              'nonzero_gauss_amplitude_exponent_distribution',dict(sorted(E.items())),flush=True)
    print('PASS PROBE V26_Q138_BC_SECOND_RESIDUE_CORRECTION_CLASSES')
    print('interpretation=e0 sectors are first-parity signed corrections; e1 sectors contribute support indicators to second residue; e>=2 vanish mod2 after dividing by2; weight122 e=-1 four-sector group handled jointly')

if __name__=='__main__':main()
