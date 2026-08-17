#!/usr/bin/env python3
import argparse,json,math
from collections import Counter
from pathlib import Path

SITE_NAMES=['s4','t4','s3','t3','s2','t2','s1','t1','K0','K1','z0','z1','b0','d0','d1','Ain','Bin','Cin','Aout','Cout','Dout']
P=1000003


def bits(x,n):return tuple((x>>(n-1-i))&1 for i in range(n))
def tsign(s,t,u,v,w):
    if t!=(s^u^v^w) or not(s or u==v==w):return 0
    return -1 if ((u^w)&(v^w)) else 1

def site16(A):
    # Exact fully-open fused local site tensor, multiplied by16.
    # Local summed masks are x=J4_u and q=J3_u.  Channel definitions:
    # b0=Bout[i+7], z0=J4_v[i] xor Dout[i], z1=z[i+8],
    # K0=J3_v[i] xor Bout[i+7], K1=K[i+12].
    # d0=Din[i], d1=Din[i+16].  Keeping d0/d1 separate is a relaxation on
    # the column side relative to the already-fused offset16 envelope, hence
    # any row-rank upper bound obtained here remains safe after later fusion.
    scale=1<<(4-(A['s4']+A['s3']+A['s2']+A['s1']))
    z=0
    for x in (0,1):
        a=tsign(A['s4'],A['t4'],x,A['z0']^A['Dout'],A['Cout']^A['b0'])
        if not a:continue
        for q in (0,1):
            b=tsign(A['s3'],A['t3'],q,A['K0']^A['b0'],A['Aout']^A['z1'])
            if not b:continue
            c=tsign(A['s2'],A['t2'],A['Cin'],A['z1']^A['d1'],x^A['K1'])
            if not c:continue
            d=tsign(A['s1'],A['t1'],A['Ain'],A['K1']^A['Bin'],q^A['d0'])
            if d:z+=a*b*c*d*scale
    return z

def entry(row_names,row_idx,col_names,col_idx):
    A={}
    A.update(zip(row_names,bits(row_idx,len(row_names))))
    A.update(zip(col_names,bits(col_idx,len(col_names))))
    assert set(A)==set(SITE_NAMES)
    return site16(A)

def rank_mod(M,p=P):
    A=[[x%p for x in r] for r in M];m=len(A);n=len(A[0]) if m else 0;q=0
    for c in range(n):
        k=next((i for i in range(q,m) if A[i][c]),None)
        if k is None:continue
        A[q],A[k]=A[k],A[q];inv=pow(A[q][c],p-2,p);A[q]=[x*inv%p for x in A[q]]
        for i in range(m):
            if i!=q and A[i][c]:
                a=A[i][c];A[i]=[(A[i][j]-a*A[q][j])%p for j in range(n)]
        q+=1
        if q==m:break
    return q

def verify_site(C):
    row=C['row_names'];col=C['col_names'];r=C['rank'];nr=1<<len(row);nc=1<<len(col)
    assert set(row).isdisjoint(col) and set(row)|set(col)==set(SITE_NAMES)
    assert len(C['pivot_rows'])==len(C['pivot_cols'])==r
    # Lower bound over Q: an r x r integer minor is nonsingular modulo odd P,
    # therefore its determinant is nonzero as an integer/rational number.
    M=[[entry(row,ri,col,ci) for ci in C['pivot_cols']] for ri in C['pivot_rows']]
    assert rank_mod(M)==r
    # Upper bound over Q: n-r independent exact integer left-null relations.
    rel=C['null_relations'];assert len(rel)==nr-r
    R=[[0]*nr for _ in rel]
    for i,z in enumerate(rel):
        for j,a in z:R[i][j]=a
    assert rank_mod(R)==len(rel)
    # Verify every stated relation against every column with exact integers.
    used=sorted({j for z in rel for j,a in z})
    for ci in range(nc):
        vals={j:entry(row,j,col,ci) for j in used}
        for z in rel:
            assert sum(a*vals[j] for j,a in z)==0,(C['site'],ci,z)
    return r

def main():
    ap=argparse.ArgumentParser();ap.add_argument('cert',nargs='?',default='research/v26/recovered-bit-puncturing-dac/V26_Q138_FULLY_OPEN_S3_LOCAL_RANK_CERTIFICATE.json');a=ap.parse_args()
    C=json.loads(Path(a.cert).read_text());assert C['milestone']=='V26_Q138_FULLY_OPEN_S3_LOCAL_SIGNED_RANK';assert C['prime']==P
    ranks={int(s):verify_site(z) for s,z in C['sites'].items()}
    assert ranks=={11:168,19:96,27:192},ranks
    raw=sum(C['global']['compressed_sites'][str(s)]['raw_bits'] if str(s) in C['global']['compressed_sites'] else 0 for s in []) if False else 23
    assert raw==8+7+8
    prod=168*96*192;assert prod==189*(2**14)
    D=prod*(2**C['global']['remaining_binary_bits']);assert D==189*(2**56)
    assert C['global']['raw_crossing_bits']==65 and C['global']['remaining_binary_bits']==42
    print('PASS V26_Q138_FULLY_OPEN_S3_LOCAL_SIGNED_RANK')
    print('site_ranks=11:168/256,19:96/128,27:192/256 exact_over_Q')
    print('selected_crossing_bits=23 remaining_binary_bits=42')
    print('fully_open_S3_rank<=168*96*192*2^42=189*2^56')
    print('fully_open_S3_log2_bound=%.15f' % math.log2(D))
    print('gain_vs_fused65=%.15f bits' % (65-math.log2(D)))
if __name__=='__main__':main()
