#!/usr/bin/env python3
import itertools,sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as B
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H

S=sorted(A.S1)
LEFT=[128+i for i in S]
LEFT_SET=set(LEFT)
RIGHT=[i for i in range(160) if i not in LEFT_SET]
RIDX={e:k for k,e in enumerate(RIGHT)}
ALL=(1<<2048)-1
WALSH=[]
for f in range(1<<11):
    z=0
    for x in range(1<<11):
        if (f&x).bit_count()&1:z|=1<<x
    WALSH.append(z)


def insert(Ba,x):
    y=x
    while y:
        p=y.bit_length()-1
        if p not in Ba:
            Ba[p]=y;return True
        y^=Ba[p]
    return False


def row_basis(rows):
    Ba={}
    for x in rows:insert(Ba,x)
    return list(Ba.values())


def generalized_substitution(pos,Cmask,extras):
    FF=D.full_forms(pos);E=D.equations(FF,Cmask,hom=False)+list(extras)
    rows=[m|((rhs&1)<<D.GN) for m,rhs in E]
    ints=A.internal_cols();r=0;piv=[]
    for col in ints:
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        piv.append(col);r+=1
    ec=A.ext_cols();eindex={col:i for i,col in enumerate(ec)}
    subs={}
    for row,p in zip(rows[:r],piv):
        m=0
        for col,ei in eindex.items():
            if (row>>col)&1:m|=1<<ei
        subs[p]=(m,(row>>D.GN)&1)
    for col in ints:
        if col not in subs:subs[col]=(0,0)
    return FF,subs,r,eindex


def split_left(m):
    z=0
    for q,e in enumerate(LEFT):
        if (m>>e)&1:z|=1<<q
    return z


def add_product(qbits,cols,f,g):
    fm,fc=f;gm,gc=g
    fl=split_left(fm);gl=split_left(gm)
    qbits ^= WALSH[fl]&WALSH[gl]
    if fc:qbits^=WALSH[gl]
    if gc:qbits^=WALSH[fl]
    if fc&gc:qbits^=ALL
    for e in RIGHT:
        if (gm>>e)&1:cols[RIDX[e]]^=fl
        if (fm>>e)&1:cols[RIDX[e]]^=gl
    return qbits,cols


def section_phase_data(pos,Cmask,extras):
    FF,subs,rank,eindex=generalized_substitution(pos,Cmask,extras)
    qbits=0;cols=[0]*len(RIGHT)
    for j in range(1,5):
        for i in range(31):
            X=T.xx(FF[j,i,'u'],FF[j,i,'w'])
            Y=T.xx(FF[j,i,'v'],FF[j,i,'w'])
            xm,xc=A.sub_form(X,subs,eindex);ym,yc=A.sub_form(Y,subs,eindex)
            qbits,cols=add_product(qbits,cols,(xm,xc),(ym,yc))
    return qbits,cols,rank,FF,subs,eindex


def q2(t,P,n):
    z=0
    for i in range(n):
        if (t>>i)&1:
            for j in range(i+1,n):
                if ((t>>j)&1) and ((P[i]>>j)&1:z^=1
    return z


def gauss_sign_anf(P,n):
    allowed=[]
    for L in range(1<<n):
        s=0
        for t in range(1<<n):
            e=((L&t).bit_count()&1)^q2(t,P,n)
            s += -1 if e else 1
        if s:allowed.append((L,1 if s<0 else 0,abs(s)))
    mons=[()]+[(i,) for i in range(n)]+[(i,j) for i in range(n) for j in range(i+1,n)]
    eq=[]
    for L,sg,_ in allowed:
        m=0
        for k,mo in enumerate(mons):
            v=1
            for i in mo:v&=(L>>i)&1
            if v:m|=1<<k
        eq.append((m,sg))
    sol=T.rref(eq,n=len(mons));assert sol is not None
    coeff=sol[1]
    for L,sg,_ in allowed:
        v=0
        for k,mo in enumerate(mons):
            if not ((coeff>>k)&1):continue
            z=1
            for i in mo:z&=(L>>i)&1
            v^=z
        assert v==sg
    return mons,coeff,allowed


def add_affine(qbits,form):
    m,c=form;lm=split_left(m)
    if lm:qbits^=WALSH[lm]
    if c:qbits^=ALL
    return qbits


def corrected_phase_data(pos,Cmask):
    sol=A.internal_null(pos,Cmask);ir,_,NB=sol
    dirs,pr=B.radical_directions(pos,NB)
    FF0=D.full_forms(pos)
    extras=[A.derivative_form(FF0,A.map_internal_to_full(d)) for d in dirs]
    qbits,cols,rank,FF,subs,eindex=section_phase_data(pos,Cmask,extras)
    meta={'basis':NB,'pr':pr,'extras':extras,'FF':FF,'subs':subs,'eindex':eindex,'mons':None,'coeff':0}
    if pr:
        P=B.polar_rows(pos,NB);mons,coeff,allowed=gauss_sign_anf(P,len(NB))
        L=[]
        for d in NB:
            der=A.derivative_form(FF,A.map_internal_to_full(d))
            L.append(A.sub_form(der,subs,eindex))
        for k,mo in enumerate(mons):
            if not ((coeff>>k)&1):continue
            if len(mo)==0:qbits^=ALL
            elif len(mo)==1:qbits=add_affine(qbits,L[mo[0]])
            else:qbits,cols=add_product(qbits,cols,L[mo[0]],L[mo[1]])
        meta.update({'mons':mons,'coeff':coeff,'allowed':allowed})
    return qbits,cols,rank,meta


def left_basis(can):
    rows=[]
    for row in can:
        v=0
        for q,i in enumerate(S):
            if (row>>(128+i))&1:v|=1<<q
        if v:rows.append(v)
    return row_basis(rows)


def coset_masks(lb):
    out=[]
    for bits in range(1<<len(lb)):
        z=ALL
        for j,f in enumerate(lb):
            w=WALSH[f]
            z &= w if ((bits>>j)&1) else (w^ALL)
        if z:out.append(z)
    return out


def grouped_e0_basis(pos):
    e0,_,_=H.classify_patterns();groups={};raw=0
    for k in range(4):
        for zs,cls in e0[k]:
            can=H.support_for(pos,zs,cls)
            if can is None:continue
            raw+=1
            qbits,cols,rank,meta=corrected_phase_data(pos,D.carries(zs))
            if can not in groups:groups[can]=[0,[0]*len(cols),0]
            g=groups[can];g[0]^=qbits;g[1]=[a^b for a,b in zip(g[1],cols)];g[2]+=1
    expected=581 if pos=='B' else 577
    mult=Counter({1:103,4:91,2:57}) if pos=='B' else Counter({1:103,4:90,2:57})
    assert raw==expected and Counter(g[2] for g in groups.values())==mult
    GB={};cross=Counter();left=Counter()
    for can,(qbits,cols,n) in groups.items():
        cb=row_basis(cols);cross[len(cb)]+=1
        lb=left_basis(can);left[len(lb)]+=1
        local=[qbits,ALL]+[WALSH[f] for f in cb]
        for s in coset_masks(lb):
            for g in local:insert(GB,s&g)
    expect=272 if pos=='B' else 388
    assert len(GB)==expect,(pos,len(GB))
    print('position',pos,'raw_e0',raw,'support_groups',len(groups),
          'group_cross_rank_distribution',dict(sorted(cross.items())),
          'group_left_support_rank_distribution',dict(sorted(left.items())),
          'uniform_grouped_e0_rank_F2<=',len(GB),flush=True)
    return GB


def half_basis(pos):
    _,_,half=H.classify_patterns();assert len(half)==4
    cans=[];Q=[];AS=[]
    for zs,cls in half:
        assert cls==(128,0,0)
        can=H.support_for(pos,zs,cls);cans.append(can)
        qbits,cols,rank,meta=corrected_phase_data(pos,D.carries(zs))
        assert rank==128 and meta['pr']==0
        cb=row_basis(cols);Q.append(qbits)
        AS.append(row_basis([ALL]+[WALSH[f] for f in cb]))
    assert all(x==cans[0] for x in cans)
    gens=[ALL]
    for i in range(4):gens.append(Q[i]);gens.extend(AS[i])
    for i in range(4):
        for j in range(i+1,4):
            gens.append(Q[i]&Q[j])
            gens.extend(a&Q[j] for a in AS[i])
            gens.extend(Q[i]&b for b in AS[j])
            gens.extend(a&b for a in AS[i] for b in AS[j])
    core=row_basis(gens);HB={}
    for s in coset_masks(left_basis(cans[0])):
        for g in core:insert(HB,s&g)
    expect=252 if pos=='B' else 280
    assert len(HB)==expect,(pos,len(HB))
    print('position',pos,'half_core_span',len(core),'uniform_half_rank_F2<=',len(HB),flush=True)
    return HB


def union_basis(*Bs):
    out={}
    for B0 in Bs:
        for v in B0.values():insert(out,v)
    return out


def ext_words(x):return tuple((x>>(32*k))&0xffffffff for k in range(5))


def section_internal(subs,e):
    out=0
    for g,fo,io in (('U3',D.GBASE['U3'],T.BASE['U3']),('V3',D.GBASE['V3'],T.BASE['V3']),
                    ('U4',D.GBASE['U4'],T.BASE['U4']),('V4',D.GBASE['V4'],T.BASE['V4'])):
        for i in range(32):
            m,c=subs[fo+i];v=((m&e).bit_count()&1)^c
            if v:out|=1<<(io+i)
    return out


def eval_anf(L,mons,coeff):
    z=0
    for k,mo in enumerate(mons):
        if not ((coeff>>k)&1):continue
        v=1
        for i in mo:v&=(L>>i)&1
        z^=v
    return z


def validate_completion(pos,zs,cls):
    can=H.support_for(pos,zs,cls);assert can is not None
    eq=[(row&((1<<160)-1),(row>>160)&1) for row in can]
    es=T.rref(eq,n=160);assert es is not None
    qbits,cols,rank,meta=corrected_phase_data(pos,D.carries(zs))
    assert meta['pr']==2
    tests=[es[1]]+[es[1]^b for b in es[2][:3]]
    for e in tests:
        F=T.forms(pos,ext_words(e));ins=T.rref(D.equations(F,D.carries(zs),hom=False));assert ins is not None
        ss=0
        for t in range(1<<len(ins[2])):
            x=ins[1]
            for i,b in enumerate(ins[2]):
                if (t>>i)&1:x^=b
            ss += -1 if T.sign_phase(F,x) else 1
        assert ss!=0
        xsec=section_internal(meta['subs'],e);qsec=T.sign_phase(F,xsec);L=0
        for i,d in enumerate(meta['basis']):
            if T.sign_phase(F,xsec^d)^qsec:L|=1<<i
        pred=qsec^eval_anf(L,meta['mons'],meta['coeff'])
        assert pred==(1 if ss<0 else 0),(pos,zs,cls,L,ss)


def main():
    e0,_,_=H.classify_patterns()
    for pos in 'BC':
        validate_completion(pos,e0[0][0][0],e0[0][0][1])
        zs,cls=next((z,c) for z,c in e0[1] if c==(125,3,2))
        validate_completion(pos,zs,cls)
        E0=grouped_e0_basis(pos);HH=half_basis(pos);U=union_basis(E0,HH)
        expect=348 if pos=='B' else 432
        assert len(U)==expect,(pos,len(U))
        print('position',pos,'e0_plus_half_uniform_rank_F2<=',len(U),
              'overlap_dimension',len(E0)+len(HH)-len(U),flush=True)
    print('PASS V26_Q138_PREDECESSOR_LEAF_BC_SECOND_RESIDUE_SIGN_SPAN348_432')
    print('B_e0_rank_F2<=272; B_half_rank_F2<=252; B_union_rank_F2<=348')
    print('C_e0_rank_F2<=388; C_half_rank_F2<=280; C_union_rank_F2<=432')
    print('Gauss_completion_pr2_direct_fiber_validation=PASS')
    print('scope=sign-dependent part of B/C second dyadic residue; support-only lifts remain separate')

if __name__=='__main__':main()
