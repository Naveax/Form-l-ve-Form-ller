#!/usr/bin/env python3
import argparse,itertools,re,sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_right_map_rank_conditioning as R
import verify_v26_qr_q138_width40_left_rank48 as Q

I9=['v4_8','v4_9','v4_10','sig4_18','sig3_10','v3_21','v3_22','aux_j2_i10_k2','sig1_10']
EXPECTED=Counter({216:36,144:12,180:6,174:4,117:2,120:2,177:2})

def support_cf(core,labels):
    labs,data=Q.cf(core,labels)
    return [labs,{a:Fraction(1) for a in data}]

def lin(bits):
    z=0
    for b in bits:z=(z<<1)|b
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('cert',nargs='?',default='research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json')
    a=ap.parse_args();ctx=R.setup(a.cert)
    C,E,B,id2,dims,new2old,A64,B107,extA,inter,extB=ctx
    assert set(I9)<=set(extA) and len(I9)==9

    c4=Q.tt(('t','s','v','u'),{'w':0},[2,3,2])
    c3=Q.tt(('u','t','s','v','w'),{},[2,3,3,2])
    c2={b:Q.tt(('t','w','v','s'),{'u':b},[2,3,2]) for b in (0,1)}
    c1={b:Q.tt(('w','v','s','t'),{'u':b},[2,3,2]) for b in (0,1)}

    supports={}
    for pat in itertools.product((0,1),repeat=6):
        u1=pat[:3];u2=pat[3:];fs=[]
        for nv in sorted(A64):
            ov=new2old[nv];name=B.names[ov]
            labs=[id2[e] for e in B.ops[ov] if B.d[e]>1]
            if name.startswith('P_i'):
                data={z:Fraction(1) for z in itertools.product((0,1),repeat=3) if z[0]^z[1]^z[2]==0}
                fs.append([labs,data]);continue
            m=re.match(r'J([1-4])_i(\d+)_c(\d+)_',name);assert m,name
            j,i,k=map(int,m.groups())
            if j==4:co=c4[k]
            elif j==3:co=c3[k]
            elif j==2:co=c2[u2[i-8]][k]
            else:co=c1[u1[i-8]][k]
            fs.append(support_cf(co,labs))
        H=Q.contract(fs,set(I9),dims);pos={x:i for i,x in enumerate(H[0])}
        ss=frozenset(lin(a[pos[x]] for x in I9) for a,v in H[1].items() if v)
        supports[pat]=ss

    dist=Counter(len(s) for s in supports.values())
    assert dist==EXPECTED,(dist,EXPECTED)
    assert min(dist)==117 and max(dist)==216
    classes={}
    for p,s in supports.items():classes.setdefault(s,[]).append(p)
    assert len(classes)==13
    assert sorted(len(s) for s in classes)==[117,120,144,144,174,174,177,180,180,216,216,216,216]
    union=set().union(*supports.values());intersection=set.intersection(*(set(s) for s in supports.values()))
    assert len(union)==384 and len(intersection)==96

    # No strict subset of the six controls determines exact support-set identity.
    for k in range(6):
        for idx in itertools.combinations(range(6),k):
            seen={};ok=True
            for p,s in supports.items():
                key=tuple(p[i] for i in idx)
                if key in seen and seen[key]!=s:ok=False;break
                seen[key]=s
            assert not ok,(k,idx)

    # Exact rational rank of the 64 x 512 mask/support selector.
    rows=[]
    for p in itertools.product((0,1),repeat=6):
        s=supports[p];rows.append([Fraction(int(i in s)) for i in range(512)])
    rr,_=Q.rref_piv(rows);assert rr==12,rr
    urows=[[Fraction(int(i in s)) for i in range(512)] for s in classes]
    urr,_=Q.rref_piv(urows);assert urr==12,urr

    print('PASS V26_QR_Q138_LEFT_I9_SUPPORT216')
    print('fixed_left_masks=64 support_min=117 support_max=216 distinct_support_classes=13 union=384 intersection=96')
    print('support_size_distribution='+repr(dict(sorted(dist.items()))))
    print('mask_support_selector_exact_rational_rank=12')
    print('epsilon=0: assignments excluded by the support projection are exactly impossible')

if __name__=='__main__':main()
