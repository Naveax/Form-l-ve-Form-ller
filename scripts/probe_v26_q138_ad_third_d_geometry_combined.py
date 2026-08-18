#!/usr/bin/env python3
import random,sys
from collections import Counter,defaultdict
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_ad_third_direct_e2_condition_group_rank1 as G
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T

MASK=(1<<128)-1
S=sorted(A.S1);R=A.R1


def eq_on_condition(B,M,U):
    return all(G.implied_zero(B,m^u,b^c) for (m,b),(u,c) in zip(M,U))


def active(cond,x):
    return all((((row&MASK)&x).bit_count()&1)==((row>>128)&1) for row in cond)


def eval_map(M,x):
    z=0
    for j,(m,b) in enumerate(M):z|=((((m&x).bit_count()&1)^b)<<j)
    return z


def linear_image_rank(M,basis):
    rows=[]
    for d in basis:
        z=0
        for j,(m,b) in enumerate(M):z|=(((m&d).bit_count()&1)<<j)
        rows.append(z)
    return T.gf2_rank(rows,11)


def affine_hull_rank(points):
    if not points:return 0
    p0=next(iter(points))
    return T.gf2_rank([x^p0 for x in points],11)


def main():
    raw,_=P.direct_supports('D')
    groups=defaultdict(list)
    for typ,zs,can in raw:
        cond=P.canonical_condition(I.input_condition(can))
        groups[cond].append((tuple(zs),can))
    assert len(groups)==8629

    data=[]; image_dim=Counter(); common=Counter()
    for cond,items in groups.items():
        B=G.affine_basis(cond);M=G.singleton_side_map(items[0][1],S,R)
        for zs,can in items[1:]:assert eq_on_condition(B,G.singleton_side_map(can,S,R),M)
        eq=[(row&MASK,(row>>128)&1) for row in cond]
        sol=T.rref(eq,n=128);assert sol is not None
        _,x0,basis=sol
        image_dim[linear_image_rank(M,basis)]+=1
        U=set().union(*(set(zs) for zs,_ in items));J=set(items[0][0])
        for zs,_ in items[1:]:J&=set(zs)
        common[len(J)]+=1
        data.append((cond,B,M,frozenset(U),frozenset(J),x0,basis))

    print('D_groups',len(data),'left_singleton_image_dimension_distribution',dict(sorted(image_dim.items())),
          'common_zero_intersection_size_distribution',dict(sorted(common.items())),flush=True)

    # One affine template per zero site.
    sites=sorted({z for _,_,_,U,_,_,_ in data for z in U});assert len(sites)==93
    bysite=defaultdict(list)
    for k,x in enumerate(data):
        for z in x[3]:bysite[z].append(k)
    templates={z:data[bysite[z][0]][2] for z in sites}
    one=0
    for cond,B,M,U,J,x0,basis in data:
        if any(eq_on_condition(B,M,templates[z]) for z in U):one+=1
    print('one_global_template_per_zero_site_covered_groups',one,'uncovered',len(data)-one,flush=True)

    # Exact explicit site-local greedy cover diagnostic.
    cc={};total=0
    for z in sites:
        uncovered=set(bysite[z]);n=0
        while uncovered:
            seed=next(iter(uncovered));tm=data[seed][2];n+=1
            drop=[k for k in uncovered if eq_on_condition(data[k][1],data[k][2],tm)]
            for k in drop:uncovered.remove(k)
        cc[z]=n;total+=n
    print('site_local_greedy_template_count_distribution',dict(sorted(Counter(cc.values()).items())),
          'site_local_greedy_total',total,'site_local_max',max(cc.values()),flush=True)

    # Deterministic assembled-row samples. This is diagnostic only.
    rng=random.Random(138131)
    samples=[0,(1<<128)-1]
    samples += [1<<b for b in (0,31,32,63,64,95,96,127)]
    samples += [rng.getrandbits(128) for _ in range(200)]
    hist=Counter();maxrows=0;maxh=0;best=None
    for x in samples:
        rows=set();act=0
        for cond,B,M,U,J,x0,basis in data:
            if active(cond,x):
                act+=1;rows.add(eval_map(M,x))
        h=affine_hull_rank(rows);hist[(len(rows),h)]+=1
        if len(rows)>maxrows or (len(rows)==maxrows and h>maxh):maxrows,maxh,best=len(rows),h,(x,act)
    print('sample_count',len(samples),'sample_max_distinct_left_rows',maxrows,
          'sample_max_row_affine_hull_rank_at_rowmax',maxh,'best_active_groups',best[1] if best else 0,
          'sample_row_hull_hist_top',hist.most_common(20),flush=True)
    print('PASS PROBE V26_Q138_AD_THIRD_D_GEOMETRY_COMBINED')
    print('scope=exact group/image/template geometry plus sampled assembled-row statistics; no uniform row-count theorem claimed')

if __name__=='__main__':main()
