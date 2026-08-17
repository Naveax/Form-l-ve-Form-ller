#!/usr/bin/env python3
import itertools,sys,math
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S


def product_channels():
    vec=[];meta=[]
    for ds in itertools.product((0,1),repeat=4):
        D=dict(zip((13,14,15,16),ds))
        B1,d1=S.j1_segment_basis(D);H,d2=S.j2_high_vector(D);B0,d3=S.j2_bit0_basis(D[16])
        assert (len(B1),len(B0),d1,d2,d3)==(112,2,256,128,8)
        for ia,a in enumerate(B1):
            for ic,c in enumerate(B0):
                vec.append(S.kron3(a,H,c,d2,d3));meta.append((ds,ia,ic))
    assert len(vec)==16*112*2==3584
    return vec,meta

def echelon(rows):
    B={}
    for r0 in rows:
        r={j:Fraction(v) for j,v in r0.items() if v}
        while r:
            c=min(r);a=r[c]
            if c not in B:
                q=1/a;B[c]={j:x*q for j,x in r.items()};break
            b=B[c]
            for j,x in b.items():
                z=r.get(j,Fraction(0))-a*x
                if z:r[j]=z
                elif j in r:r.pop(j)
    return B

def coords(B,r0):
    r={j:Fraction(v) for j,v in r0.items() if v};co={}
    while r:
        c=min(r);a=r[c];assert c in B
        co[c]=a;b=B[c]
        for j,x in b.items():
            z=r.get(j,Fraction(0))-a*x
            if z:r[j]=z
            elif j in r:r.pop(j)
    return co

def reconstruct(B,co):
    r={}
    for c,a in co.items():
        for j,x in B[c].items():
            z=r.get(j,Fraction(0))+a*x
            if z:r[j]=z
            elif j in r:r.pop(j)
    return r

def main():
    V,meta=product_channels();B=echelon(V);assert len(B)==2784
    nnz=[];nums=[];dens=[]
    for v in V:
        c=coords(B,v);assert reconstruct(B,c)=={j:Fraction(x) for j,x in v.items() if x}
        nnz.append(len(c))
        for x in c.values():nums.append(abs(x.numerator));dens.append(x.denominator)
    assert max(nnz)==41
    assert abs(sum(nnz)/len(nnz)-2.5398995535714284)<1e-15
    expected_den={1,2,3,4,6,8,9,12,16,24,32,48,64,96,128,256,512}
    assert set(dens)==expected_den,set(dens)
    assert max(nums)==37 and max(dens)==512
    coord_dense=3584*2784
    basis_dense=2784*(2**18)
    assert coord_dense<2**24 and basis_dense<2**30
    print('PASS V26_Q138_SIGNED_BLOCK2_EXPLICIT_FACTOR')
    print('natural_product_channels=3584 exact_basis_rank=2784 column_dimension=2^18')
    print('all_3584_channels_reconstruct_exactly')
    print('coordinate_nnz_max=41 mean=%.15f' % (sum(nnz)/len(nnz)))
    print('coordinate_denominators='+','.join(map(str,sorted(expected_den))))
    print('coordinate_max_abs_numerator=37 max_denominator=512')
    print('dense_coordinate_table_log2=%.15f dense_V_basis_log2=%.15f' % (math.log2(coord_dense),math.log2(basis_dense)))
    print('scope=explicit exact local rational rank factor; full constructive right/complement contraction remains separate')
if __name__=='__main__':main()
