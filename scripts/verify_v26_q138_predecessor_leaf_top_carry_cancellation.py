#!/usr/bin/env python3

# Exact GF(2) verifier for the predecessor-leaf formal carry-weight124 sector.

BASE={'U3':0,'V3':32,'U4':64,'V4':96}
N=128


def vx(name,i):
    return (1 << (BASE[name]+(i%32)), 0)


def xx(*fs):
    m=c=0
    for f in fs:
        if isinstance(f,tuple):
            m ^= f[0]; c ^= f[1]
        else:
            c ^= int(f)&1
    return m,c


def forms(pos,ext):
    A0,B0,C0,D0,beta=ext
    bit=lambda z,i:(z>>(i%32))&1
    def O(letter,k):
        return (0,bit(beta,k)) if pos==letter else (0,0)
    F={}
    for i in range(32):
        F[4,i,'u']=vx('U4',i)
        F[4,i,'v']=vx('V4',i)
        F[4,i,'w']=xx(O('C',i),O('B',i+7))

        F[3,i,'u']=vx('U3',i)
        F[3,i,'v']=vx('V3',i)
        F[3,i,'w']=xx(O('A',i),vx('V4',i+8),O('D',i+8))

        F[2,i,'u']=(0,bit(C0,i))
        F[2,i,'v']=xx(vx('V4',i+8),O('D',i+8),(0,bit(D0,i+16)))
        F[2,i,'w']=xx(vx('U4',i),vx('V3',i+12),O('B',i+19))

        F[1,i,'u']=(0,bit(A0,i))
        F[1,i,'v']=xx((0,bit(B0,i)),vx('V3',i+12),O('B',i+19))
        F[1,i,'w']=xx(vx('U3',i),(0,bit(D0,i)))
    return F


def max124_equations(F,homogeneous=False):
    E=[]
    # Bits1..30: u xor v xor w =0.
    for j in range(1,5):
        for i in range(1,31):
            m,c=xx(F[j,i,'u'],F[j,i,'v'],F[j,i,'w'])
            E.append((m,0 if homogeneous else c))
        # Bit31: u=v=w=1.
        for z in 'uvw':
            m,c=F[j,31,z]
            E.append((m,0 if homogeneous else (c^1)))
    return E


def rref(eqs,n=N):
    rows=[m | ((rhs&1)<<n) for m,rhs in eqs]
    r=0; piv=[]
    for col in range(n):
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:
            continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):
                rows[k]^=rows[r]
        piv.append(col); r+=1
    for row in rows:
        if (row & ((1<<n)-1))==0 and ((row>>n)&1):
            return None
    rows=rows[:r]
    pset=set(piv); free=[i for i in range(n) if i not in pset]
    x0=0
    for row,p in zip(rows,piv):
        if (row>>n)&1:
            x0 |= 1<<p
    basis=[]
    for f in free:
        x=1<<f
        for row,p in zip(rows,piv):
            if (row>>f)&1:
                x |= 1<<p
        basis.append(x)
    return len(piv),x0,basis


def gf2_rank(rows,n):
    R=list(rows); r=0
    for col in range(n):
        p=next((k for k in range(r,len(R)) if (R[k]>>col)&1),None)
        if p is None:
            continue
        R[r],R[p]=R[p],R[r]
        for k in range(len(R)):
            if k!=r and ((R[k]>>col)&1):
                R[k]^=R[r]
        r+=1
    return r


def ev(f,x):
    return ((f[0]&x).bit_count()&1)^f[1]


def sign_phase(F,x):
    q=0
    for j in range(1,5):
        for i in range(31):
            u=ev(F[j,i,'u'],x)
            v=ev(F[j,i,'v'],x)
            w=ev(F[j,i,'w'],x)
            q ^= ((u^w)&(v^w))
    return q


def nullspace_and_polar(pos):
    # Constants do not affect the coefficient matrix or polar form.
    F=forms(pos,(0,0,0,0,0))
    sol=rref(max124_equations(F,homogeneous=True))
    assert sol is not None
    rank,_,B=sol
    assert rank==124 and len(B)==4,(pos,rank,len(B))

    # Polar matrix on the four-dimensional nullspace.
    q0=sign_phase(F,0)
    M=[]
    for a in B:
        row=0
        qa=sign_phase(F,a)
        for j,b in enumerate(B):
            qb=sign_phase(F,b)
            z=sign_phase(F,a^b)^qa^qb^q0
            row |= z<<j
        M.append(row)
    assert gf2_rank(M,4)==2,(pos,M)

    # Any external affine RHS/particular solution changes only affine-linear
    # terms on N. Enumerate all such perturbations; Gauss sums are 0 or +/-8.
    qvals=[]
    for t in range(16):
        x=0
        for k,b in enumerate(B):
            if (t>>k)&1:
                x ^= b
        qvals.append(sign_phase(F,x))
    sums=set()
    for ell in range(16):
        for const in (0,1):
            s=0
            for t in range(16):
                p=qvals[t]^((ell&t).bit_count()&1)^const
                s += -1 if p else 1
            sums.add(s)
    assert sums=={-8,0,8},(pos,sums)
    return M


def main():
    # A/D: j4 bit31 exposes only B/C output occurrences, hence w4_31=0.
    # Weight124 would require j4 bit31 u=v=w=1, impossible.
    for pos in 'AD':
        F=forms(pos,(0,0,0,0,0))
        assert F[4,31,'w']==(0,0)

    witnesses={
        'B':(0x80000000,0x80000000,0x80800000,0x00800000,0x00000040),
        'C':(0x80800000,0x80080000,0x80800000,0x00000000,0x80080080),
    }
    polars=[]
    for pos in 'BC':
        M=nullspace_and_polar(pos); polars.append(M)
        # Explicit consistency witness proves the formal top sector is reachable.
        F=forms(pos,witnesses[pos])
        sol=rref(max124_equations(F,homogeneous=False))
        assert sol is not None
        rank,x0,B=sol
        assert rank==124 and len(B)==4
        # Direct witness-fiber Gauss sum must obey the universal set.
        ss=0
        for t in range(16):
            x=x0
            for k,b in enumerate(B):
                if (t>>k)&1:
                    x ^= b
            ss += -1 if sign_phase(F,x) else 1
        assert ss in (-8,0,8)
    assert polars[0]==polars[1]

    print('PASS V26_Q138_PREDECESSOR_LEAF_TOP_CARRY_CANCELLATION')
    print('formal_max_carry_weight=124')
    print('positions_A_D_weight124=impossible')
    print('positions_B_C_internal_maxcarry_rank=124/128 nullity=4 fiber_size=16')
    print('restricted_sign_polar_rank=2')
    print('all_affine_fiber_Gauss_sums={-8,0,+8}')
    print('uniform_leaf_coefficient_lattice=2^-123 Z')
    print('scaled_2^123_parity_receives_no_weight124_contribution')
    print('next=analyze carry-weight123 parity tensor for small exact 11|21 rank certificate')
    print('scope=exact coefficient arithmetic; no Schmidt-rank or arithmetic-work reduction claimed')


if __name__=='__main__':
    main()
