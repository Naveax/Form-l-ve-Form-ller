#!/usr/bin/env python3
import itertools
from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T


def carries(zeros,ad=False):
    Z=set(zeros)
    return {(j,i):(0 if (ad and j==4) or (j,i) in Z else 1)
            for j in range(1,5) for i in range(31)}


def equations(F,C,hom=False):
    E=[]
    for j in range(1,5):
        for i in range(32):
            u,v,w=F[j,i,'u'],F[j,i,'v'],F[j,i,'w']
            if i==0:
                s=C[j,0]
                if s==0:
                    m,c=T.xx(u,v);E.append((m,0 if hom else c))
                    m,c=T.xx(u,w);E.append((m,0 if hom else c))
            elif i<31:
                s=C[j,i];sp=C[j,i-1]
                m,c=T.xx(u,v,w)
                E.append((m,0 if hom else (c^(sp^s))))
                if s==0:
                    m,c=T.xx(u,v);E.append((m,0 if hom else c))
                    m,c=T.xx(u,w);E.append((m,0 if hom else c))
            else:
                sp=C[j,30]
                m,c=T.xx(u,v);E.append((m,0 if hom else c))
                m,c=T.xx(u,w);E.append((m,0 if hom else c))
                m,c=T.xx(u,v,w);E.append((m,0 if hom else (c^sp)))
    return E


def polar_rank(F,B):
    q0=T.sign_phase(F,0); rows=[]
    for a in B:
        qa=T.sign_phase(F,a); row=0
        for k,b in enumerate(B):
            z=T.sign_phase(F,a^b)^qa^T.sign_phase(F,b)^q0
            row |= z<<k
        rows.append(row)
    return T.gf2_rank(rows,len(B))


def internal_class(pos,C):
    F=T.forms(pos,(0,0,0,0,0))
    sol=T.rref(equations(F,C,hom=True))
    assert sol is not None
    rank,_,B=sol
    return rank,len(B),polar_rank(F,B)

# Full symbolic external system for comparing the four weight122 rank128 sectors.
GBASE={'A0':0,'B0':32,'C0':64,'D0':96,'U3':128,'V3':160,'U4':192,'V4':224,'BETA':256}
GN=288


def gv(name,i):
    return (1<<(GBASE[name]+(i%32)),0)


def full_forms(pos):
    def O(letter,k):return gv('BETA',k) if pos==letter else (0,0)
    F={}
    for i in range(32):
        F[4,i,'u']=gv('U4',i);F[4,i,'v']=gv('V4',i);F[4,i,'w']=T.xx(O('C',i),O('B',i+7))
        F[3,i,'u']=gv('U3',i);F[3,i,'v']=gv('V3',i);F[3,i,'w']=T.xx(O('A',i),gv('V4',i+8),O('D',i+8))
        F[2,i,'u']=gv('C0',i);F[2,i,'v']=T.xx(gv('V4',i+8),O('D',i+8),gv('D0',i+16))
        F[2,i,'w']=T.xx(gv('U4',i),gv('V3',i+12),O('B',i+19))
        F[1,i,'u']=gv('A0',i);F[1,i,'v']=T.xx(gv('B0',i),gv('V3',i+12),O('B',i+19))
        F[1,i,'w']=T.xx(gv('U3',i),gv('D0',i))
    return F


def canonical_external_constraints(pos,C):
    F=full_forms(pos); E=equations(F,C,hom=False)
    rows=[m|((rhs&1)<<GN) for m,rhs in E]
    internal=[]
    for g in ('U3','V3','U4','V4'):
        internal += list(range(GBASE[g],GBASE[g]+32))
    r=0
    for col in internal:
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        r+=1
    assert r==128
    extcols=[]
    for g in ('A0','B0','C0','D0','BETA'):
        extcols += list(range(GBASE[g],GBASE[g]+32))
    residual=[]
    for row in rows[r:]:
        m=0
        for q,col in enumerate(extcols):
            if (row>>col)&1:m|=1<<q
        rhs=(row>>GN)&1
        if m or rhs:residual.append((m,rhs))
    sol=T.rref(residual,n=160)
    assert sol is not None
    rank,_,_=sol
    # Canonicalize once more to return exact reduced pivot rows.
    rr=[m|((rhs&1)<<160) for m,rhs in residual]; r=0; out=[]
    for col in range(160):
        p=next((k for k in range(r,len(rr)) if (rr[k]>>col)&1),None)
        if p is None:continue
        rr[r],rr[p]=rr[p],rr[r]
        for k in range(len(rr)):
            if k!=r and ((rr[k]>>col)&1):rr[k]^=rr[r]
        r+=1
    for row in rr[r:]:
        assert not ((row&((1<<160)-1))==0 and ((row>>160)&1))
    out=tuple(rr[:r])
    assert r==rank
    return out


def main():
    # A/D: j4 output is zero, so all j4 carries are forced zero. The unique
    # top-weight93 pattern has internal rank127 and hence two-point fibers.
    for pos in 'AD':
        F=T.forms(pos,(0,0,0,0,0))
        for i in range(32):assert F[4,i,'w']==(0,0)
        cls=internal_class(pos,carries([],ad=True))
        assert cls[0]==127 and cls[1]==1,(pos,cls)

    # B/C weight123 one-zero sectors.
    sites=[(j,i) for j in range(1,5) for i in range(31)]
    expected=Counter({(124,4,2):95,(125,3,2):14,(125,3,0):7,(126,2,0):8})
    for pos in 'BC':
        d=Counter(internal_class(pos,carries([z])) for z in sites)
        assert d==expected,(pos,d)

    # Internal linear parts are identical for B/C. Enumerate all weight122
    # two-zero sectors once.
    d=Counter(); full=[]
    for z in itertools.combinations(sites,2):
        rank,nullity,_=internal_class('B',carries(z))
        d[rank]+=1
        if rank==128:full.append(z)
    assert d==Counter({124:4465,125:2058,126:1025,127:74,128:4}),d
    expected_full=[
        ((1,0),(2,0)),
        ((1,0),(4,0)),
        ((2,0),(3,0)),
        ((3,0),(4,0)),
    ]
    assert full==expected_full,full

    # The four unique-solution sectors have one identical external consistency
    # subspace for B and one identical subspace for C.
    for pos in 'BC':
        C=[canonical_external_constraints(pos,carries(z)) for z in full]
        assert all(x==C[0] for x in C),pos
        assert len(C[0])==8,(pos,len(C[0]))

    print('PASS V26_Q138_PREDECESSOR_LEAF_DYADIC_DESCENT92_121')
    print('positions_A_D_all_j4_carries_zero; top_weight=93 internal_rank=127 nullity=1')
    print('positions_A_D_uniform_lattice=2^-92 Z')
    print('positions_B_C_weight123_classes='+repr(dict(expected)))
    print('positions_B_C_weight122_rank_distribution=124:4465,125:2058,126:1025,127:74,128:4')
    print('weight122_rank128_pairs='+repr(full))
    print('four_rank128_sectors_share_identical_external_rank8_consistency_system')
    print('positions_B_C_uniform_lattice=2^-121 Z')
    print('next=build position-scaled modulo2 parity tensors for the 11|21 leaf-rank probe')
    print('scope=exact coefficient arithmetic; no Schmidt-rank or arithmetic-work reduction claimed')


if __name__=='__main__':main()
