#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_ad_third_direct_e2_condition_group_rank1 as G
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T

MASK=(1<<128)-1
FULLN=129
S=sorted(A.S1); R=A.R1


def span_basis(rows):
    B={}
    for x in rows:
        y=x
        while y:
            p=y.bit_length()-1
            if p in B:y^=B[p]
            else:B[p]=y;break
    return tuple(B[p] for p in sorted(B,reverse=True))


def reduce_vec(x,basis):
    B={v.bit_length()-1:v for v in basis}; y=x
    for p in sorted(B,reverse=True):
        if (y>>p)&1:y^=B[p]
    return y


def solve_span(vectors,target):
    B={}
    for i,v0 in enumerate(vectors):
        y=v0; tag=1<<i
        while y:
            p=y.bit_length()-1
            if p in B:
                v,t=B[p]; y^=v; tag^=t
            else:B[p]=(y,tag); break
    y=target; tag=0
    while y:
        p=y.bit_length()-1
        if p not in B:return None
        v,t=B[p]; y^=v; tag^=t
    return tag


def intersection_basis(W,U):
    W=tuple(W); U=span_basis(U)
    if not W or not U:return ()
    q=[reduce_vec(w,U) for w in W]
    eq=[]
    for b in range(FULLN):
        m=0
        for i,z in enumerate(q):
            if (z>>b)&1:m|=1<<i
        if m:eq.append((m,0))
    sol=T.rref(eq,n=len(W)); assert sol is not None
    _rank,_x0,kernel=sol
    out=[]
    for c in kernel:
        z=0
        for i,w in enumerate(W):
            if (c>>i)&1:z^=w
        if z:out.append(z)
    return span_basis(out)


def affine_intersect(repW,W,repU,U):
    W=tuple(W); U=tuple(U)
    tag=solve_span(W+U,repW^repU)
    if tag is None:return None
    w=0
    for i,z in enumerate(W):
        if (tag>>i)&1:w^=z
    rep=repW^w
    II=intersection_basis(W,U)
    assert reduce_vec(rep^repW,W)==0
    assert reduce_vec(rep^repU,U)==0
    return rep,II


def full_map(M):
    return tuple(m|((b&1)<<128) for m,b in M)


def map_pairs(F):
    return tuple((z&MASK,(z>>128)&1) for z in F)


def try_add(state,U,F):
    out=[]
    for (rep,W),f in zip(state,F):
        z=affine_intersect(rep,W,f,U)
        if z is None:return None
        out.append(z)
    return tuple(out)


def eq_on_condition(B,M,U):
    return all(G.implied_zero(B,m^u,b^c) for (m,b),(u,c) in zip(M,U))


def canonical_map_on_condition(B,M):
    out=[]
    for m,b in M:
        y=m; bb=b
        while y:
            p=y.bit_length()-1
            if p not in B:break
            rr=B[p]; y^=rr&MASK; bb^=(rr>>128)&1
        out.append((y,bb))
    return tuple(out)


def make_data(pos):
    raw,stats=P.direct_supports(pos)
    keep,elim=(R,S) if pos=='A' else (S,R)
    data_by_key={}
    cutdist=Counter(); typed=Counter()
    for typ,zs,can in raw:
        cut=A.cut_intersection(can); cutdist[cut]+=1
        assert cut==0,(pos,typ,zs,cut)
        cond=P.canonical_condition(I.input_condition(can))
        B=G.affine_basis(cond)
        M=G.singleton_side_map(can,keep,elim)
        U=span_basis(cond); F=full_map(M)
        key=(cond,canonical_map_on_condition(B,M))
        if key not in data_by_key:
            data_by_key[key]=(B,U,F,M,1,Counter({typ:1}))
        else:
            B0,U0,F0,M0,n,ct=data_by_key[key]
            assert eq_on_condition(B0,M0,M)
            ct=ct.copy(); ct[typ]+=1
            data_by_key[key]=(B0,U0,F0,M0,n+1,ct)
        typed[typ]+=1
    data=list(data_by_key.values())
    return raw,stats,cutdist,typed,data


def greedy_cover(pos,data):
    uncovered=set(range(len(data)))
    templates=[]; cluster_sizes=[]; raw_mult_covered=[]
    while uncovered:
        seed=min(uncovered)
        _B,U,F,_M,_n,_ct=data[seed]
        state=tuple((f,U) for f in F)
        cluster=[seed]
        for k in sorted(uncovered-{seed}):
            _Bk,Uk,Fk,_Mk,_nk,_ctk=data[k]
            ns=try_add(state,Uk,Fk)
            if ns is not None:
                state=ns; cluster.append(k)
        Tfull=tuple(rep for rep,_W in state)
        Tmap=map_pairs(Tfull)
        covered=[]
        for k in sorted(uncovered):
            Bk,_Uk,_Fk,Mk,_nk,_ctk=data[k]
            if eq_on_condition(Bk,Mk,Tmap):covered.append(k)
        assert set(cluster)<=set(covered)
        templates.append(Tmap)
        cluster_sizes.append(len(covered))
        raw_mult_covered.append(sum(data[k][4] for k in covered))
        uncovered.difference_update(covered)
        q=len(templates)
        if q<=20 or q%100==0:
            print('position',pos,'templates',q,'last_cover_classes',len(covered),
                  'last_cover_raw_sectors',raw_mult_covered[-1],
                  'remaining_classes',len(uncovered),flush=True)
    return templates,cluster_sizes,raw_mult_covered


def main():
    for pos in 'AD':
        raw,stats,cutdist,typed,data=make_data(pos)
        print('position',pos,'raw_reachable_e2_sectors',len(raw),
              'sector_stats',dict(stats),'type_distribution',dict(typed),
              'cut_intersection_distribution',dict(cutdist),
              'distinct_condition_map_classes',len(data),
              'class_raw_multiplicity_distribution',dict(sorted(Counter(x[4] for x in data).items())),flush=True)
        templates,cs,rm=greedy_cover(pos,data)
        print('position',pos,'raw_e2_global_interpolated_template_cover_size',len(templates),
              'cover_class_size_distribution',dict(sorted(Counter(cs).items())),
              'cover_raw_sector_size_distribution',dict(sorted(Counter(rm).items())),flush=True)
        print('position',pos,'interpretation=every raw reachable e2 signed sector has singleton side and is covered by one fixed global affine singleton-template family; exact signed raw-e2 aggregate rank is at most template count')
    print('PASS PROBE V26_Q138_AD_RAW_E2_GLOBAL_INTERPOLATED_MAP_COVER')
    print('scope=raw exact-signed e2 singleton-template cover diagnostic; no higher-residue theorem until lift/correction semantics are separately certified')

if __name__=='__main__':
    main()
