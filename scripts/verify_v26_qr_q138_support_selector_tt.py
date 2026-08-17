#!/usr/bin/env python3
import itertools,re,sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_right_map_rank_conditioning as R
import verify_v26_qr_q138_width40_left_rank48 as Q
import verify_v26_qr_q138_left_i9_support216 as S

MASK_NAMES=('u1_8','u1_9','u1_10','u2_8','u2_9','u2_10')


def rank_dense(rows):
    return Q.rref_piv(rows)[0]


def build_alpha(cert):
    ctx=R.setup(cert)
    C,E,B,id2,dims,new2old,A64,B107,extA,inter,extB=ctx
    c4=Q.tt(('t','s','v','u'),{'w':0},[2,3,2])
    c3=Q.tt(('u','t','s','v','w'),{},[2,3,3,2])
    c2={b:Q.tt(('t','w','v','s'),{'u':b},[2,3,2]) for b in(0,1)}
    c1={b:Q.tt(('w','v','s','t'),{'u':b},[2,3,2]) for b in(0,1)}
    pats=list(itertools.product((0,1),repeat=6)); supports={}
    for pat in pats:
        u1=pat[:3];u2=pat[3:];fs=[]
        for nv in sorted(A64):
            ov=new2old[nv];name=B.names[ov];labs=[id2[e] for e in B.ops[ov] if B.d[e]>1]
            if name.startswith('P_i'):
                fs.append([labs,{z:Fraction(1) for z in itertools.product((0,1),repeat=3) if z[0]^z[1]^z[2]==0}]);continue
            m=re.match(r'J([1-4])_i(\d+)_c(\d+)_',name);assert m,name
            j,i,k=map(int,m.groups())
            co=c4[k] if j==4 else c3[k] if j==3 else c2[u2[i-8]][k] if j==2 else c1[u1[i-8]][k]
            labs0,data=Q.cf(co,labs);fs.append([labs0,{a:Fraction(1) for a in data}])
        H=Q.contract(fs,set(S.I9),dims);pos={x:i for i,x in enumerate(H[0])}
        ss=frozenset(S.lin(a[pos[x]] for x in S.I9) for a,v in H[1].items() if v)
        supports[pat]=ss
    rows=[[Fraction(int(i in supports[p])) for i in range(512)] for p in pats]
    assert rank_dense(rows)==12
    bidx=[pats.index(tuple(map(int,s))) for s in S.BASIS_MASKS];piv=[int(s,2) for s in S.PIVOT_I9]
    basis=[rows[i] for i in bidx]; PM=[[basis[r][c] for c in piv] for r in range(12)]; Pinv=Q.inv(PM)
    alpha=[]
    for row in rows:
        y=[row[c] for c in piv]
        a=[sum(y[k]*Pinv[k][j] for k in range(12)) for j in range(12)]
        assert all(x in (Fraction(-1),Fraction(0),Fraction(1)) for x in a)
        alpha.append(a)
    return pats,alpha


def tt_profile(alpha,perm):
    out=[]
    # Tensor alpha[m0..m5,s], s=12. Reindex rows by chosen bit permutation.
    lookup={tuple(((r>>(5-i))&1) for i in range(6)):alpha[r] for r in range(64)}
    for k in range(1,7):
        rows=[]
        for pref in itertools.product((0,1),repeat=k):
            row=[]
            for suff in itertools.product((0,1),repeat=6-k):
                bits=[0]*6
                for j,b in enumerate(pref):bits[perm[j]]=b
                for j,b in enumerate(suff):bits[perm[k+j]]=b
                row.extend(lookup[tuple(bits)])
            rows.append(row)
        out.append(rank_dense(rows))
    return tuple(out)


def main():
    cert=sys.argv[1] if len(sys.argv)>1 else 'research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json'
    pats,alpha=build_alpha(cert)
    natural=tt_profile(alpha,tuple(range(6)))
    best=None;bestperm=None;bestprof=None
    for perm in itertools.permutations(range(6)):
        prof=tt_profile(alpha,perm);score=(max(prof[:-1]),sum(prof[:-1]),prof)
        if best is None or score<best:best,bestperm,bestprof=score,perm,prof
    # Shared bit with the right coefficient family is u2_8, index 3.
    sector={}
    for b in (0,1):
        sector[b]=rank_dense([alpha[i] for i,p in enumerate(pats) if p[3]==b])
    # Joint rank when keeping u2_8 explicit and summing the other five mask choices into rows.
    # This is simply the span dimension within each shared-bit sector, recorded separately.
    print('PASS V26_QR_Q138_SUPPORT_SELECTOR_TT')
    print('mask_order='+','.join(MASK_NAMES))
    print('selector_rank=12')
    print('natural_tt_profile='+','.join(map(str,natural)))
    print('best_internal_tt_profile='+','.join(map(str,bestprof)))
    print('best_bit_order='+','.join(MASK_NAMES[i] for i in bestperm))
    print('best_internal_max='+str(max(bestprof[:-1])))
    print('u2_8_sector_ranks=0:'+str(sector[0])+',1:'+str(sector[1]))

if __name__=='__main__':main()
