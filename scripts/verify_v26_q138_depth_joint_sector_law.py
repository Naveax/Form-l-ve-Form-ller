#!/usr/bin/env python3
import itertools, math, sys
from fractions import Fraction
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_depth_signed434_law as A


def basis(rows):
    return A.basis(rows)
T=A.T


def blockA_basis():
    vec=[]
    for dv in itertools.product((0,1),repeat=3):
        D=dict(zip((27,28,29),dv));B1=A.j1_basis(D);B2=A.j2_basis(D)
        for a in B1:
          for b in B2:
            vec.append({ia*32+ib:va*vb for ia,va in a.items() for ib,vb in b.items()})
    B=basis(vec);assert len(B)==434
    return B


def blockB_j1(D):
    # j1 bits13..11, row A/B, interfaces s13,u3_11..13,v3_23..25,s10
    rows=[]
    for z in itertools.product((0,1),repeat=6):
        Aa=dict(zip((11,12,13),z[:3]));Bb=dict(zip((11,12,13),z[3:]));r={}
        for s13 in (0,1):
          for u0 in itertools.product((0,1),repeat=3):
           for x0 in itertools.product((0,1),repeat=3):
            u=dict(zip((11,12,13),u0));x=dict(zip((11,12,13),x0));s=s13;c=Fraction(1);ok=True
            for i in (13,12,11):
                v=x[i]^Bb[i];w=u[i]^D[i];t=s^Aa[i]^v^w;q=T(s,t,Aa[i],v,w)
                if not q:ok=False;break
                c*=q;s=t
            if ok:
                k=0
                for bit in (s13,)+u0+x0+(s,):k=(k<<1)|bit
                r[k]=c
        rows.append(r)
    B=basis(rows);assert len(B)==64
    return B


def blockB_j2(D):
    # j2 bits29..27, row C27..29; v=(1 xor D11,D12,D13), w=v3_7..9
    rows=[]
    for cv in itertools.product((0,1),repeat=3):
        C=dict(zip((27,28,29),cv));r={}
        for s29 in (0,1):
          for w0 in itertools.product((0,1),repeat=3):
            w=dict(zip((27,28,29),w0));s=s29;c=Fraction(1);ok=True
            for i in (29,28,27):
                v=(1^D[11]) if i==27 else D[i-16]
                t=s^C[i]^v^w[i];q=T(s,t,C[i],v,w[i])
                if not q:ok=False;break
                c*=q;s=t
            if ok:
                k=0
                for bit in (s29,)+w0+(s,):k=(k<<1)|bit
                r[k]=c
        rows.append(r)
    B=basis(rows);assert len(B)==8
    return B


def blockB_basis():
    vec=[]
    for dv in itertools.product((0,1),repeat=3):
        D=dict(zip((11,12,13),dv));B1=blockB_j1(D);B2=blockB_j2(D)
        for a in B1:
          for b in B2:
            vec.append({ia*32+ib:va*vb for ia,va in a.items() for ib,vb in b.items()})
    B=basis(vec);assert len(B)==1792
    return B


def proj_A(v,sec):
    sx=(sec>>3)&7;sy=sec&7;out={}
    for idx,val in v.items():
        ia=idx>>5;ib=idx&31
        if ((ia>>1)&7)!=sx or ((ib>>1)&7)!=sy:continue
        r=(((ia>>4)&1)<<3)|((ia&1)<<2)|(((ib>>4)&1)<<1)|(ib&1)
        out[r]=val
    return out


def proj_B(v,sec):
    sx=(sec>>3)&7;sy=sec&7;out={}
    for idx,val in v.items():
        ia=idx>>5;ib=idx&31
        if ((ib>>1)&7)!=sx or ((ia>>1)&7)!=sy:continue
        bits=((ia>>7)&1,(ia>>6)&1,(ia>>5)&1,(ia>>4)&1,ia&1,(ib>>4)&1,ib&1)
        r=0
        for b in bits:r=(r<<1)|b
        out[r]=val
    return out


def generic_pair_basis():
    # Generic occurrence-closed pair: j1 two bits on A/B/D and j2 two bits on C/D.
    vec=[]
    for dv in itertools.product((0,1),repeat=2):
        D={0:dv[0],1:dv[1]}
        R1=[]
        for z in itertools.product((0,1),repeat=4):
            Aa={0:z[0],1:z[1]};Bb={0:z[2],1:z[3]};r={}
            for s1 in (0,1):
              for u0 in itertools.product((0,1),repeat=2):
               for x0 in itertools.product((0,1),repeat=2):
                u={0:u0[0],1:u0[1]};x={0:x0[0],1:x0[1]};s=s1;c=Fraction(1);ok=True
                for i in (1,0):
                    v=x[i]^Bb[i];w=u[i]^D[i];t=s^Aa[i]^v^w;q=T(s,t,Aa[i],v,w)
                    if not q:ok=False;break
                    c*=q;s=t
                if ok:
                    k=0
                    for b in (s1,)+u0+x0+(s,):k=(k<<1)|b
                    r[k]=c
            R1.append(r)
        B1=basis(R1);assert len(B1)==16
        R2=[]
        for cv in itertools.product((0,1),repeat=2):
            C={0:cv[0],1:cv[1]};r={}
            for s1 in (0,1):
              for w0 in itertools.product((0,1),repeat=2):
                w={0:w0[0],1:w0[1]};s=s1;c=Fraction(1);ok=True
                for i in (1,0):
                    t=s^C[i]^D[i]^w[i];q=T(s,t,C[i],D[i],w[i])
                    if not q:ok=False;break
                    c*=q;s=t
                if ok:
                    k=0
                    for b in (s1,)+w0+(s,):k=(k<<1)|b
                    r[k]=c
            R2.append(r)
        B2=basis(R2);assert len(B2)==4
        for a in B1:
          for b in B2:
            vec.append({ia*16+ib:va*vb for ia,va in a.items() for ib,vb in b.items()})
    B=basis(vec);assert len(B)==192
    return B


def proj_pair(v,sec,sigma,which):
    hi=(sec>>2)&3;lo=sec&3
    sx,sw=(hi,lo) if which=='C' else (lo,hi);out={}
    for idx,val in v.items():
        ia=idx>>4;ib=idx&15
        if ((ia>>1)&3)!=sx or ((ib>>1)&3)!=sw:continue
        if which=='C':
            if (ib&1)!=sigma:continue
            bits=((ia>>5)&1,(ia>>4)&1,(ia>>3)&1,ia&1,(ib>>3)&1)
        else:
            if (ia&1)!=sigma:continue
            bits=((ia>>5)&1,(ia>>4)&1,(ia>>3)&1,(ib>>3)&1,ib&1)
        r=0
        for b in bits:r=(r<<1)|b
        out[r]=val
    return out


def crossE_basis():
    # Row site19 vs complement site3. Includes both D19 and D3 occurrences and shared v3_15.
    rows=[]
    for A19,B19,C19,D19 in itertools.product((0,1),repeat=4):
        r={}
        for A3,B3,C3,D3 in itertools.product((0,1),repeat=4):
          for v315,u33,u319 in itertools.product((0,1),repeat=3):
           for s119,s203,s103,s219 in itertools.product((0,1),repeat=4):
            t118=s119^A19^B19^(u319^D19);q1=T(s119,t118,A19,B19,u319^D19)
            if not q1:continue
            t202=s203^C3^D19^(1^v315);q2=T(s203,t202,C3,D19,1^v315)
            if not q2:continue
            t102=s103^A3^(v315^B3)^(u33^D3);q3=T(s103,t102,A3,v315^B3,u33^D3)
            if not q3:continue
            t218=s219^C19^D3;q4=T(s219,t218,C19,D3,0)
            if not q4:continue
            bits=(A3,B3,C3,D3,v315,u33,u319,s119,t118,s203,t202,s103,t102,s219,t218)
            k=0
            for b in bits:k=(k<<1)|b
            r[k]=q1*q2*q3*q4
        rows.append(r)
    B=basis(rows);assert len(B)==12
    return B


def proj_E(v,s1,s2):
    out={}
    for idx,val in v.items():
        if ((idx>>7)&1)!=s1 or ((idx>>1)&1)!=s2:continue
        bits=[(idx>>k)&1 for k in range(14,-1,-1) if k not in (7,1)]
        r=0
        for b in bits:r=(r<<1)|b
        out[r]=val
    return out


def central_joint_rank_bound():
    BA=blockA_basis();BB=blockB_basis()
    rA=[];rB=[]
    for sec in range(64):
        rA.append(len(basis([proj_A(v,sec) for v in BA])))
        rB.append(len(basis([proj_B(v,sec) for v in BB])))
    pairs=Counter(zip(rA,rB))
    assert pairs==Counter({(16,120):36,(16,75):12,(11,120):12,(11,75):4}),pairs
    ab=sum(a*b for a,b in zip(rA,rB));assert ab==102660

    P=generic_pair_basis();E=crossE_basis();rC={};rD={};rE={}
    for sec in range(16):
      for s in (0,1):
        rC[(sec,s)]=len(basis([proj_pair(v,sec,s,'C') for v in P]))
        rD[(sec,s)]=len(basis([proj_pair(v,sec,s,'D') for v in P]))
    for s1 in (0,1):
      for s2 in (0,1):rE[(s1,s2)]=len(basis([proj_E(v,s1,s2) for v in E]))
    assert Counter(rC.values())==Counter({28:16,21:8,14:8})
    assert Counter(rD.values())==Counter({23:16,32:16})
    assert rE=={(0,0):4,(0,1):8,(1,0):4,(1,1):8}
    cde=0
    for sec in range(16):
      for s1 in (0,1):
       for s2 in (0,1):cde+=rC[(sec,s2)]*rD[(sec,s1)]*rE[(s1,s2)]
    assert cde==240240
    total=ab*cde
    assert total==24663038400
    return ab,cde,total


def depth_cost(S,d,central_rank):
    m,c,s,f,v=A.caps(S);F=frozenset(S);C=frozenset(set(range(32))-set(F))
    ce=min(float(c),math.log2(central_rank)) if (F==A.S3 or C==A.S3) else float(c)
    return ce+4*s+(8*d-12)*f+4*v


def main():
    ab,cde,R=central_joint_rank_bound()
    root,sets=A.walk(A.TREE,True);assert root==set(range(32))
    vals={d:max(depth_cost(S,d,R) for S in sets) for d in range(2,10)}
    for d,v in vals.items():
        target=520*d-384+math.log2(R)
        assert abs(v-target)<1e-12,(d,v,target)
    print('PASS V26_Q138_DEPTH_JOINT_SECTOR_LAW')
    print('AB_joint_sector_bound=102660')
    print('CDE_joint_sector_bound=240240')
    print('S3_central_rank<=24663038400 log2=%.12f' % math.log2(R))
    print('d>=2 W_repr(d)<=520*d-384+log2(24663038400)')
    print('verified='+','.join(f'{d}:{vals[d]:.12f}' for d in sorted(vals)))
    print('intercept_improvement_vs_520d-340=%.12f bits' % (44-math.log2(R)))
    print('scope=exact representation/message upper bound; no constructive/work/optimality claim')

if __name__=='__main__':main()
