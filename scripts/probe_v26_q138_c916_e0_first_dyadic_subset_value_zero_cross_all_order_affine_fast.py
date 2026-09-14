#!/usr/bin/env python3
import random
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_subset_value_zero_cross_all_order_affine_exact as A

OLD_CANONICAL=A.canonical_affine
MASK=(1<<A.PHYS_N)-1

def insert_rref(state,x):
    x=int(x)
    if not x: return state
    piv=[]
    for r in state:
        phys=r&MASK
        if phys: piv.append((phys.bit_length()-1,r))
    piv.sort(reverse=True)
    for p,r in piv:
        if (x>>p)&1: x^=r
    phys=x&MASK
    if not phys:
        return None if ((x>>A.PHYS_N)&1) else state
    p=phys.bit_length()-1
    out=[(r^x if ((r>>p)&1) else r) for r in state]
    out.append(x)
    return tuple(sorted((r for r in out if r&MASK),reverse=True))

def canonical_fast(rows):
    s=()
    for x in rows:
        s=insert_rref(s,x)
        if s is None: return None
    return s

def inter_fast(a,b,stats=None):
    if not a: return b
    if not b: return a
    key=(a,b) if a<=b else (b,a)
    if key in A._INTERSECTIONS:
        if stats is not None: stats["intersection_cache_hits"]+=1
        return A._INTERSECTIONS[key]
    s=a
    for x in b:
        s=insert_rref(s,x)
        if s is None: break
    A._INTERSECTIONS[key]=s
    if stats is not None: stats["intersection_cache_misses"]+=1
    return s

def regression():
    rng=random.Random(20260914)
    for n in range(1,25):
        for _ in range(24):
            rows=[rng.getrandbits(A.PHYS_N)|(rng.randrange(2)<<A.PHYS_N) for __ in range(n)]
            assert canonical_fast(rows)==OLD_CANONICAL(rows)
    print("fast-rref regression",24*24,"cases",flush=True)

regression()
A.canonical_affine=canonical_fast
A.inter=inter_fast
A._INTERSECTIONS.clear()

if __name__=="__main__":
    A.analyze()
