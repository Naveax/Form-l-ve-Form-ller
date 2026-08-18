#!/usr/bin/env python3
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_ad_third_direct_e2_condition_group_rank1 as G
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T

MASK=(1<<128)-1
FULLN=129
S=sorted(A.S1);R=A.R1


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
    B={v.bit_length()-1:v for v in basis};y=x
    for p in sorted(B,reverse=True):
        if (y>>p)&1:y^=B[p]
    return y


def solve_span(vectors,target):
    B={}
    for i,v0 in enumerate(vectors):
        y=v0;tag=1<<i
        while y:
            p=y.bit_length()-1
            if p in B:
                v,t=B[p];y^=v;tag^=t
            else:B[p]=(y,tag);break
    y=target;tag=0
    while y:
        p=y.bit_length()-1
        if p not in B:return None
        v,t=B[p];y^=v;tag^=t
    return tag


def intersection_basis(W,U):
    W=tuple(W);U=span_basis(U)
    if not W or not U:return ()
    q=[reduce_vec(w,U) for w in W]
    eq=[]
    for b in range(FULLN):
        m=0
        for i,z in enumerate(q):
            if (z>>b)&1:m|=1<<i
        if m:eq.append((m,0))
    sol=T.rref(eq,n=len(W));assert sol is not None
    _rank,_x0,kernel=sol
    out=[]
    for c in kernel:
        z=0
        for i,w in enumerate(W):
            if (c>>i)&1:z^=w
        if z:out.append(z)
    return span_basis(out)


def affine_intersect(repW,W,repU,U):
    W=tuple(W);U=tuple(U)
    tag=solve_span(W+U,repW^repU)
    if tag is None:return None
    w=0
    for i,z in enumerate(W):
        if (tag>>i)&1:w^=z
    rep=repW^w
    I=intersection_basis(W,U)
    assert reduce_vec(rep^repW,W)==0
    assert reduce_vec(rep^repU,U)==0
    return rep,I


def eq_on_condition(B,M,U):
    return all(G.implied_zero(B,m^u,b^c) for (m,b),(u,c) in zip(M,U))


def consistent(rows):
    return T.rref([(r&MASK,(r>>128)&1) for r in rows],n=128) is not None


def full_map(M):return tuple(m|((b&1)<<128) for m,b in M)
def map_pairs(F):return tuple((z&MASK,(z>>128)&1) for z in F)


def try_add(state,U,F):
    out=[]
    for (rep,W),f in zip(state,F):
        z=affine_intersect(rep,W,f,U)
        if z is None:return None
        out.append(z)
    return tuple(out)


def main():
    raw,_=P.direct_supports('A')
    C=Counter(can for _typ,_zs,can in raw)
    odd=[can for can,n in C.items() if n&1]
    assert len(odd)==12098
    groups=defaultdict(list)
    for can in odd:
        cond=P.canonical_condition(I.input_condition(can))
        groups[cond].append(can)
    assert len(groups)==4531
    assert Counter(map(len,groups.values()))==Counter({1:617,2:261,3:3653})

    rows=[]
    for cond,cans in groups.items():
        B=G.affine_basis(cond);M=G.singleton_side_map(cans[0],R,S)
        for can in cans[1:]:assert eq_on_condition(B,G.singleton_side_map(can,R,S),M)
        rows.append((cond,M))

    freq=Counter(r for cond,_M in rows for r in cond)
    core=tuple(r for r,_ in freq.most_common(6))
    assert [freq[r] for r in core]==[4437,4437,4435,4343,4342,4250]

    data=[]
    for cond,M in rows:
        eqrows=core+tuple(cond)
        if not consistent(eqrows):continue
        B=G.affine_basis(eqrows)
        U=span_basis(eqrows)
        F=full_map(M)
        data.append((B,U,F,M))
    assert len(data)==4067
    print('A6_compatible_groups',len(data),
          'condition_direction_rank_distribution',dict(sorted(Counter(len(x[1]) for x in data).items())),flush=True)

    uncovered=set(range(len(data)))
    templates=[];cluster_sizes=[];extra_cover=[]
    while uncovered:
        seed=min(uncovered)
        _B,U,F,_M=data[seed]
        state=tuple((f,U) for f in F)
        cluster=[seed]
        for k in sorted(uncovered-{seed}):
            _Bk,Uk,Fk,_Mk=data[k]
            ns=try_add(state,Uk,Fk)
            if ns is not None:
                state=ns;cluster.append(k)
        Tfull=tuple(rep for rep,_W in state)
        Tmap=map_pairs(Tfull)
        covered=[]
        for k in sorted(uncovered):
            Bk,_Uk,_Fk,Mk=data[k]
            if eq_on_condition(Bk,Mk,Tmap):covered.append(k)
        assert set(cluster)<=set(covered)
        templates.append(Tmap);cluster_sizes.append(len(cluster));extra_cover.append(len(covered)-len(cluster))
        uncovered.difference_update(covered)
        n=len(templates)
        if n<=20 or n%50==0:
            print('interpolated_templates',n,'last_cluster',len(cluster),
                  'last_extra_cover',len(covered)-len(cluster),
                  'remaining_groups',len(uncovered),flush=True)

    inside=len(templates);outside=189;global_upper=max(outside,inside)
    print('A6_interpolated_template_cover_size',inside,
          'cluster_size_distribution',dict(sorted(Counter(cluster_sizes).items())),
          'extra_cover_distribution',dict(sorted(Counter(extra_cover).items())),flush=True)
    print('A_outside_A6_active_group_upper',outside,
          'A_direct_e2_rank_uniform_upper_from_interpolated_cover',global_upper,
          'A_complete_third_rank_sum_upper',min(2048,global_upper+362),flush=True)
    print('PASS PROBE V26_Q138_AD_THIRD_A6_INTERPOLATED_MAP_COVER')
    print('scope=constructive affine-coset interpolation cover for A direct-e2 inside forced A6; inherited e1 correction only added by subadditivity')

if __name__=='__main__':main()
