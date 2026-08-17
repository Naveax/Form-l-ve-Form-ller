#!/usr/bin/env python3
import itertools,re,sys
from collections import Counter,defaultdict
from fractions import Fraction
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_right_map_rank_conditioning as R
import verify_v26_qr_q138_width40_left_rank48 as Q
import verify_v26_qr_q138_left_i9_support216 as S


def left_factors(ctx,pat):
    C,E,B,id2,dims,new2old,A64,B107,extA,inter,extB=ctx
    u1=pat[:3];u2=pat[3:]
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
    return fs


def gram_support(ctx,pat):
    C,E,B,id2,dims,new2old,A64,B107,extA,inter,extB=ctx
    boundary=set(extA+inter);fs=left_factors(ctx,pat);alllabs=set(x for l,d in fs for x in l)
    internal=alllabs-boundary
    dims2=dict(dims)
    for x in internal:dims2[x+'__b']=dims[x]
    doubled=[[list(l),dict(d)] for l,d in fs]
    for l,d in fs:doubled.append([[x if x in boundary else x+'__b' for x in l],dict(d)])
    H=Q.contract(doubled,set(S.I9),dims2);assert set(H[0])==set(S.I9),H[0]
    pos={x:i for i,x in enumerate(H[0])};ss=set();vals={}
    for a,v in H[1].items():
        i=S.lin(a[pos[x]] for x in S.I9);vals[i]=vals.get(i,Fraction(0))+v
    for i,v in vals.items():
        assert v>=0,(pat,i,v)
        if v:ss.add(i)
    return frozenset(ss),vals


def main():
    cert=sys.argv[1] if len(sys.argv)>1 else 'research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json'
    ctx=R.setup(cert);pats=list(itertools.product((0,1),repeat=6));supports={}
    for n,p in enumerate(pats,1):
        s,_=gram_support(ctx,p);supports[p]=s;print('mask',n,'support',len(s),flush=True)
    dist=Counter(len(s) for s in supports.values());classes={}
    for p,s in supports.items():classes.setdefault(s,[]).append(p)
    union=set().union(*supports.values());inter=set.intersection(*(set(s) for s in supports.values()))
    rows=[[Fraction(int(i in supports[p])) for i in range(512)] for p in pats];rr=Q.rref_piv(rows)[0]
    print('PASS V26_QR_Q138_LEFT_I9_GRAM_SUPPORT')
    print('support_min='+str(min(dist))+' support_max='+str(max(dist)))
    print('support_size_distribution='+repr(dict(sorted(dist.items()))))
    print('distinct_support_classes='+str(len(classes))+' union='+str(len(union))+' intersection='+str(len(inter)))
    print('mask_support_selector_exact_rational_rank='+str(rr))
    print('method=exact Gram diagonal sum_rest L(i,rest)^2; no Booleanized TT-path approximation')

if __name__=='__main__':main()
