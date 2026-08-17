#!/usr/bin/env python3
import itertools,sys,math
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S
import verify_v26_q138_signed_block2_explicit_factor as E


def j1_rows(D):
    bits=[13,14,15,16];rows=[]
    for z in itertools.product((0,1),repeat=8):
        A=dict(zip(bits,z[:4]));Bv=dict(zip(bits,z[4:]));r={}
        for s16 in (0,1):
          for uvals in itertools.product((0,1),repeat=4):
           u3=dict(zip(bits,uvals))
           for x13,x14 in itertools.product((0,1),repeat=2):
            vx={13:x13,14:x14};s=s16;c=Fraction(1);ok=True
            for i in (16,15,14,13):
                base=0 if i==16 else 1 if i==15 else vx[i]
                v=base^Bv[i];w=u3[i]^D[i]
                t=s^A[i]^v^w;q=S.T(s,t,A[i],v,w)
                if not q:ok=False;break
                c*=q;s=t
            if ok:
                k=0
                for b in (s16,)+uvals+(x13,x14)+(s,):k=(k<<1)|b
                r[k]=r.get(k,Fraction(0))+c
        rows.append(r)
    return rows

def bit0_rows(D16):
    rows=[]
    for C0 in (0,1):
        r={}
        for s0,u40,v312 in itertools.product((0,1),repeat=3):
            q=S.T0(s0,C0,D16,u40^v312)
            if q:r[(s0<<2)|(u40<<1)|v312]=q
        rows.append(r)
    return rows

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

def add_scaled(out,v,a):
    for j,x in v.items():
        z=out.get(j,Fraction(0))+a*x
        if z:out[j]=z
        elif j in out:out.pop(j)

def main():
    # First use the explicit 3584->2784 retained-column basis.
    V,_=E.product_channels();B=E.echelon(V);assert len(B)==2784
    piv=sorted(B);pidx={p:i for i,p in enumerate(piv)}
    prod=[]
    for v in V:
        c=E.coords(B,v);prod.append({pidx[p]:a for p,a in c.items()})

    # Per-D exact coordinates of the 256 physical j1 rows and two physical C0 rows.
    JC=[];BC=[]
    for ds in itertools.product((0,1),repeat=4):
        D=dict(zip((13,14,15,16),ds))
        jr=j1_rows(D);JE=echelon(jr);assert len(JE)==112
        jp=sorted(JE);jm={p:i for i,p in enumerate(jp)}
        JC.append([{jm[p]:a for p,a in coords(JE,r).items()} for r in jr])
        br=bit0_rows(D[16]);BE=echelon(br);assert len(BE)==2
        bp=sorted(BE);bm={p:i for i,p in enumerate(bp)}
        BC.append([{bm[p]:a for p,a in coords(BE,r).items()} for r in br])

    def physical_coord(d,ab,c0):
        out={}
        for ia,a in JC[d][ab].items():
            for ic,b in BC[d][c0].items():
                q=d*224+ia*2+ic
                add_scaled(out,prod[q],a*b)
        return out

    # Exact greedy echelon directly over all8192 physical block2 rows, while
    # retaining each normalized basis vector as a combination of physical rows.
    PB={};SRC={};selected=[];idx=0
    for d in range(16):
      for ab in range(256):
       for c0 in range(2):
        r=physical_coord(d,ab,c0);coef={idx:Fraction(1)}
        while r:
            c=min(r);a=r[c]
            if c not in PB:
                q=1/a;PB[c]={j:x*q for j,x in r.items()};SRC[c]={j:x*q for j,x in coef.items()};selected.append(idx);break
            b=PB[c];bc=SRC[c]
            for j,x in b.items():
                z=r.get(j,Fraction(0))-a*x
                if z:r[j]=z
                elif j in r:r.pop(j)
            for j,x in bc.items():
                z=coef.get(j,Fraction(0))-a*x
                if z:coef[j]=z
                elif j in coef:coef.pop(j)
        idx+=1
    assert idx==8192 and len(PB)==2784 and len(selected)==2784

    src_nnz=[len(x) for x in SRC.values()]
    assert max(src_nnz)==64
    assert abs(sum(src_nnz)/len(src_nnz)-3.654094827586207)<1e-15

    # Exact coordinates of every physical row in this physical-generated basis.
    umax=utot=0
    for d in range(16):
      for ab in range(256):
       for c0 in range(2):
        c=coords(PB,physical_coord(d,ab,c0));umax=max(umax,len(c));utot+=len(c)
    assert umax==184
    assert abs(utot/8192-11.8597412109375)<1e-15

    print('PASS V26_Q138_SIGNED_BLOCK2_PHYSICAL_ROW_BRIDGE')
    print('physical_rows=8192 exact_physical_row_span_rank=2784 selected_physical_pivots=2784')
    print('normalized_basis_as_physical_rows_nnz_max=64 mean=%.15f' % (sum(src_nnz)/len(src_nnz)))
    print('physical_row_U_coordinate_nnz_max=184 mean=%.15f' % (utot/8192))
    print('consequence=every retained-column basis slice is an exact combination of <=64 ordinary physical block2 rows')
    print('scope=local physical-row bridge for constructive generation; complete double-round structural peak certified separately')
if __name__=='__main__':main()
