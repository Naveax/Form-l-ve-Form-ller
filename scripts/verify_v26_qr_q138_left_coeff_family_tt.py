#!/usr/bin/env python3
import itertools,re,sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_right_map_rank_conditioning as R
import verify_v26_qr_q138_width40_left_rank48 as Q

MASK_NAMES=('u1_8','u1_9','u1_10','u2_8','u2_9','u2_10')


def add_basis(B,row):
    r={j:Fraction(v) for j,v in row.items() if v}
    while r:
        c=min(r)
        if c not in B:
            z=1/r[c];B[c]={j:x*z for j,x in r.items()};return True
        a=r[c];b=B[c]
        for j,x in b.items():
            r[j]=r.get(j,Fraction(0))-a*x
            if not r[j]:r.pop(j,None)
    return False


def reduce(row,B,pindex):
    r={j:Fraction(v) for j,v in row.items() if v};out={}
    while r:
        c=min(r);assert c in B,c;a=r[c];out[pindex[c]]=out.get(pindex[c],Fraction(0))+a
        for j,x in B[c].items():
            r[j]=r.get(j,Fraction(0))-a*x
            if not r[j]:r.pop(j,None)
    return {j:x for j,x in out.items() if x}


def left_flat(ctx,pat):
    C,E,B,id2,dims,new2old,A64,B107,extA,inter,extB=ctx;u1=pat[:3];u2=pat[3:]
    c4=Q.tt(('t','s','v','u'),{'w':0},[2,3,2]);c3=Q.tt(('u','t','s','v','w'),{},[2,3,3,2])
    c2={b:Q.tt(('t','w','v','s'),{'u':b},[2,3,2]) for b in(0,1)};c1={b:Q.tt(('w','v','s','t'),{'u':b},[2,3,2]) for b in(0,1)}
    fs=[]
    for nv in sorted(A64):
        ov=new2old[nv];name=B.names[ov];labs=[id2[e] for e in B.ops[ov] if B.d[e]>1]
        if name.startswith('P_i'):
            fs.append([labs,{z:Fraction(1) for z in itertools.product((0,1),repeat=3) if z[0]^z[1]^z[2]==0}]);continue
        m=re.match(r'J([1-4])_i(\d+)_c(\d+)_',name);assert m,name
        j,i,k=map(int,m.groups());co=c4[k] if j==4 else c3[k] if j==3 else c2[u2[i-8]][k] if j==2 else c1[u1[i-8]][k]
        fs.append(Q.cf(co,labs))
    H=Q.contract(fs,set(extA+inter),dims);pos={x:i for i,x in enumerate(H[0])}
    def enc(names,a):
        z=0
        for x in names:z=(z<<1)|a[pos[x]]
        return z
    flat={};rowbasis={}
    for a,v in H[1].items():
        r=enc(extA,a);c=enc(inter,a);flat[(r<<6)|c]=flat.get((r<<6)|c,Fraction(0))+v
        rowbasis.setdefault(r,{})[c]=rowbasis.setdefault(r,{}).get(c,Fraction(0))+v
    assert Q.rank_rows(rowbasis.values())==48
    return {j:x for j,x in flat.items() if x}


def rank_rows(rows):
    B={}
    for r in rows:add_basis(B,r)
    return len(B)


def tt_profile(D,dim):
    out=[]
    for k in range(1,7):
        B={};ns=1<<(6-k)
        for pref in range(1<<k):
            row={}
            for suff in range(ns):
                base=suff*dim
                for q,x in D[(pref<<(6-k))|suff].items():row[base+q]=x
            add_basis(B,row)
        out.append(len(B))
    return tuple(out)


def main():
    cert=sys.argv[1] if len(sys.argv)>1 else 'research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json'
    ctx=R.setup(cert);pats=list(itertools.product((0,1),repeat=6));F={};mats=[]
    for n,p in enumerate(pats,1):
        M=left_flat(ctx,p);mats.append(M);add_basis(F,M);print('mask',n,'family_dim',len(F),'nnz',len(M),flush=True)
    dim=len(F);pindex={p:i for i,p in enumerate(sorted(F))};D=[reduce(M,F,pindex) for M in mats]
    assert rank_rows(D)==dim
    profile=tt_profile(D,dim);assert profile[-1]==dim
    sector={}
    for b in (0,1):sector[b]=rank_rows([mats[i] for i,p in enumerate(pats) if p[3]==b])
    print('PASS V26_QR_Q138_LEFT_COEFF_FAMILY_TT')
    print('mask_order='+','.join(MASK_NAMES))
    print('exact_left_matrix_family_rank='+str(dim))
    print('selector_shape=64x'+str(dim)+' selector_nnz='+str(sum(len(x) for x in D)))
    print('exact_tt_profile='+','.join(map(str,profile))+' max='+str(max(profile)))
    print('u2_8_conditioned_family_ranks=0:'+str(sector[0])+',1:'+str(sector[1]))
    print('each_left_map_interface_row_rank=48')
if __name__=='__main__':main()
