#!/usr/bin/env python3
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_leaf_ht95 as H

N=32

def nleaf(t):return 1 if isinstance(t,int) else nleaf(t[0])+nleaf(t[1])
def rexp(k):return min(k,N-k)

def storage(t,root=True):
    if isinstance(t,int):
        # physical basis matrix: 2 x rank2
        return 4,[]
    ka=nleaf(t[0]);kb=nleaf(t[1]);k=ka+kb
    sa,na=storage(t[0],False);sb,nb=storage(t[1],False)
    ra=1<<rexp(ka);rb=1<<rexp(kb)
    if root:core=ra*rb
    else:core=ra*rb*(1<<rexp(k))
    return sa+sb+core,na+nb+[(k,ka,kb,core)]

def main():
    one,nodes=storage(H.TREE,True)
    assert one==4308611904,one
    largest=max(nodes,key=lambda x:x[3]);assert largest==(21,10,11,2**32),largest
    dense=2**32;four=4*one
    assert one>dense
    print('PASS V26_Q138_DOUBLE_ROUND_STORAGE_ACCOUNTING')
    print('one_generic_leaf_dense_coefficients='+str(dense))
    print('one_generic_leaf_HT_scalar_upper_bound='+str(one)+' log2='+repr(math.log2(one)))
    print('four_leaf_HT_scalar_upper_bound='+str(four)+' log2='+repr(math.log2(four)))
    print('largest_single_HT_core=2^32 on cluster21 children10+11')
    print('information_dimension_lower_bound_per_arbitrary_leaf=2^32 scalars for any uniform linear parametrization')
    print('consequence=generic HT improves separator geometry but not generic factor storage')
if __name__=='__main__':main()
