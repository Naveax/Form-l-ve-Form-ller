#!/usr/bin/env python3
import itertools,sys,math
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S


def rows():
    out=[]
    for A0,B0,C15,C16,D0 in itertools.product((0,1),repeat=5):
        r={}
        for s216,v215,s214,s10,u30,v312 in itertools.product((0,1),repeat=6):
            x=Fraction(0)
            for s215 in (0,1):x+=S.T(s216,s215,C16,D0,0)*S.T(s215,s214,C15,v215,1)
            if not x:continue
            y=S.T0(s10,A0,v312^B0,u30^D0)
            if not y:continue
            k=0
            for b in (s216,v215,s214,s10,u30,v312):k=(k<<1)|b
            r[k]=x*y
        out.append(r)
    return out

def normalize(r):
    if not r:return None,Fraction(0)
    j=min(r);a=r[j]
    return tuple(sorted((k,v/a) for k,v in r.items())),a

def main():
    R=rows();assert len(R)==32
    classes={};zero=[]
    for i,r in enumerate(R):
        k,a=normalize(r)
        if k is None:zero.append(i);continue
        classes.setdefault(k,[]).append((i,a))
    assert len(zero)==8 and len(classes)==16
    # The 24 nonzero physical rows are scalar multiples of exactly16 explicit
    # retained-column basis rows. Therefore rank_Q<=16. Existing exact rank
    # theorem gives rank16; here we also verify independence directly.
    B=[dict(k) for k in classes]
    assert len(S.basis(B))==16
    # Construct U coordinate map: each physical row has either no channel or one
    # nonzero channel coefficient; V is the list of16 normalized basis rows.
    nnz=[]
    for r in R:
        if not r:nnz.append(0);continue
        k,a=normalize(r);assert k in classes;nnz.append(1)
        assert {j:a*v for j,v in dict(k).items()}==r
    assert nnz.count(0)==8 and nnz.count(1)==24
    print('PASS V26_Q138_SIGNED_BLOCK1_EXPLICIT_FACTOR')
    print('matrix_shape=32x64 exact_rank=16')
    print('zero_physical_rows=8 nonzero_rows=24 signed/scaled_row_classes=16')
    print('U_coordinate_nnz_per_row=0_or_1; V_has16_explicit_normalized_rows')
    print('dense_U_entries=512 dense_V_entries=1024')
    print('scope=explicit exact local rank factor; global right/complement construction remains separate')
if __name__=='__main__':main()
