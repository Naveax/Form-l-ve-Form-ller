#!/usr/bin/env python3
import itertools, re, sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_right_map_reachable_hull197 as H
import verify_v26_qr_q138_right_map_rank_conditioning as R
import verify_v26_qr_q138_width40_left_rank48 as Q

PHYS=list(itertools.product((0,1),repeat=2))
START='aux_j4_i11_k0'


def site7_factors(ctx,u1_7,u2_7,u2_8,u2_31):
    C,E,B,new2old,id2,dims,intA,extB,site=ctx
    K=H.core_cache()
    T331=Q.tt(('u','t','v','w'),{'s':0},[2,2,2])
    T231={b:Q.tt(('t','w','v'),{'u':b,'s':0},[1,1]) for b in (0,1)}
    out=[]
    for nv in sorted(site[7]):
        ov=new2old[nv]; name=B.names[ov]
        labs=[id2[e] for e in B.ops[ov] if B.d[e]>1]
        if name.startswith('P_i'):
            data={z:Fraction(1) for z in itertools.product((0,1),repeat=3) if z[0]^z[1]^z[2]==0}
            out.append([labs,data]); continue
        m=re.match(r'J([1-4])_i(\d+)_c(\d+)_',name); assert m,name
        j,i,k=map(int,m.groups())
        if j==4:
            co=K['T4_1' if i==3 else 'T4_0'][k]
        elif j==3:
            co=(T331 if i==31 else K['T3'])[k]
        elif j==2:
            if i==31: co=T231[u2_31][k]
            elif i==8: co=K[f'T2_{u2_8}'][k]
            else: co=K[f'T2_{u2_7}'][k]
        else:
            co=K[f'T1_{u1_7}'][k]
        out.append(Q.cf(co,labs))
    return out


def closure7(ctx,u1_7,u2_7,u2_8,u2_31):
    intA=ctx[6]
    close=[x for x in intA if x!=START]
    left,_=H.states(7)
    F=site7_factors(ctx,u1_7,u2_7,u2_8,u2_31)
    T=H.doubled(ctx,F,left+close)
    pos={x:i for i,x in enumerate(T[0])}
    rows=defaultdict(dict)
    for a,v in T[1].items():
        st=(H.enc(left,a,pos)<<5)|H.enc([x+'__b' for x in left],a,pos)
        z=H.enc(close,a,pos); zb=H.enc([x+'__b' for x in close],a,pos)
        o=(z<<5)|zb
        rows[st][o]=rows[st].get(o,Fraction(0))+v
    return rows,close


def apply_closure(v,C):
    out={}
    for st,a in v.items():
        for o,b in C.get(st,{}).items():
            out[o]=out.get(o,Fraction(0))+a*b
            if not out[o]: out.pop(o,None)
    return out


def iface_index(startbit,closebits,intA,close):
    vals={START:startbit}
    for i,n in enumerate(close): vals[n]=(closebits>>(len(close)-1-i))&1
    z=0
    for n in intA: z=(z<<1)|vals[n]
    return z


def gram_rows(intA,close,vecs,C):
    rows=[{} for _ in range(64)]
    for z0,v in vecs.items():
        out=apply_closure(v,C)
        a0=(z0>>1)&1; b0=z0&1
        for oo,x in out.items():
            za=(oo>>5)&31; zb=oo&31
            i=iface_index(a0,za,intA,close); j=iface_index(b0,zb,intA,close)
            rows[i][j]=rows[i].get(j,Fraction(0))+x
            if not rows[i][j]: rows[i].pop(j,None)
    return rows


def row_basis(rows):
    B={}
    for r0 in rows:
        r={j:Fraction(v) for j,v in r0.items() if v}
        while r:
            c=min(r)
            if c not in B:
                q=1/r[c]; B[c]={j:x*q for j,x in r.items()}; break
            q=r[c]; b=B[c]
            for j,x in b.items():
                r[j]=r.get(j,Fraction(0))-q*x
                if not r[j]: r.pop(j,None)
    return list(B.values())


def parent_rows(L,G):
    out=[]
    for lr in L:
        y={}
        for k,a in lr.items():
            for j,g in G[k].items():
                y[j]=y.get(j,Fraction(0))+a*g
                if not y[j]: y.pop(j,None)
        out.append(y)
    return out


def parent_rank(L,G):
    return len(row_basis(parent_rows(L,G)))


def main():
    cert=sys.argv[1] if len(sys.argv)>1 else 'research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json'
    ctx=H.setup(cert)
    intA=ctx[6]
    assert intA==['aux_j2_i8_k0','aux_j4_i11_k0','aux_j4_i16_k0','sig1_7','sig3_7','sig4_7'],intA

    Ks={(u1,u2):H.transfer(ctx,4,(u1,u2,0)) for u1,u2 in PHYS}
    for uv in PHYS:
        assert Ks[uv]==H.transfer(ctx,5,(uv[0],uv[1],0))==H.transfer(ctx,6,(uv[0],uv[1],0))

    prefix={}
    for bits in itertools.product((0,1),repeat=8):
        u13,u23,u14,u24,u15,u25,u16,u26=bits
        vecs=H.boundary(ctx,(u13,u23,0))
        for uv in ((u14,u24),(u15,u25),(u16,u26)):
            vecs={z:H.image(v,Ks[uv]) for z,v in vecs.items()}
        prefix[bits]=vecs

    closures={}
    close_ref=None
    for c in itertools.product((0,1),repeat=4):
        C7,close=closure7(ctx,*c)
        if close_ref is None: close_ref=close
        assert close==close_ref
        closures[c]=C7

    # All 64 left fixed-mask cases have one common exact 48-dimensional row space.
    rctx=R.setup(cert)
    assert rctx[9]==intA
    left={}
    for u1 in itertools.product((0,1),repeat=3):
        for u2 in itertools.product((0,1),repeat=3):
            B=row_basis(R.left_rows(rctx,u1,u2))
            assert len(B)==48
            left[(u1,u2)]=B
    common_left=left[((0,0,0),(0,0,0))]
    for key,B in left.items():
        assert len(row_basis(common_left+B))==48,key

    right={}; parent={}; rd=Counter(); pd=Counter(); common_parent=[]
    for pb,vecs in prefix.items():
        for cb,C7 in closures.items():
            ctrl=pb+cb
            G=gram_rows(intA,close_ref,vecs,C7)
            rr=Q.rank_rows(G)
            P=parent_rows(common_left,G)
            PB=row_basis(P)
            pr=len(PB)
            common_parent=row_basis(common_parent+PB)
            right[ctrl]=rr; parent[ctrl]=pr; rd[rr]+=1; pd[pr]+=1

    expected_r=Counter({11:172,12:34,13:130,15:4,16:4,17:1024,18:396,19:284,22:86,23:28,24:188,25:92,26:64,27:184,28:228,29:168,30:322,33:4,34:4,37:428,38:252})
    expected_p=Counter({5:240,6:100,7:1028,8:680,16:120,17:338,18:410,19:42,20:450,23:8,26:428,27:252})
    assert rd==expected_r,(rd,expected_r)
    assert pd==expected_p,(pd,expected_p)
    assert (min(rd),max(rd))==(11,38)
    assert (min(pd),max(pd))==(5,27)
    assert len(common_parent)==47,len(common_parent)

    # u2_8 is rank-inert for both maps.
    for c in list(right):
        if c[10]==0:
            d=list(c); d[10]=1; d=tuple(d)
            assert right[c]==right[d]
            assert parent[c]==parent[d]

    r0=[right[c] for c in right if c[11]==0]; r1=[right[c] for c in right if c[11]==1]
    p0=[parent[c] for c in parent if c[11]==0]; p1=[parent[c] for c in parent if c[11]==1]
    assert (min(r0),max(r0))==(22,38)
    assert (min(r1),max(r1))==(11,19)
    assert (min(p0),max(p0))==(16,27)
    assert (min(p1),max(p1))==(5,8)

    zero=(0,)*12
    ones=(1,)*12
    bu1=(0,1,1,0,1); bu2=(1,1,0,0,1,0,0)
    high=(bu1[0],bu2[0],bu1[1],bu2[1],bu1[2],bu2[2],bu1[3],bu2[3],bu1[4],bu2[4],bu2[5],bu2[6])
    assert (right[zero],parent[zero])==(34,23)
    assert (right[ones],parent[ones])==(19,8)
    assert (right[high],parent[high])==(37,26)

    print('PASS V26_QR_Q138_PHYSICAL_RANK_ENVELOPE27')
    print('physical_cases=4096 right_rank_min=11 right_rank_max=38 parent_rank_min=5 parent_rank_max=27')
    print('u2_31=0 right=22..38 parent=16..27; u2_31=1 right=11..19 parent=5..8')
    print('all 64 left fixed-mask cases share one exact 48-dimensional row space')
    print('common span of all 4096 parent Schmidt/interface row spaces has exact dimension 47')

if __name__=='__main__': main()
