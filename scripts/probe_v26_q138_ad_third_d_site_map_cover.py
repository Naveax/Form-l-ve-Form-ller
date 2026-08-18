#!/usr/bin/env python3
import sys
from collections import Counter,defaultdict
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_ad_third_direct_e2_condition_group_rank1 as G

S=sorted(A.S1);R=A.R1


def eq_on_condition(B,M,T):
    for (m,b),(u,c) in zip(M,T):
        if not G.implied_zero(B,m^u,b^c):return False
    return True


def main():
    raw,_=P.direct_supports('D')
    groups=defaultdict(list)
    for typ,zs,can in raw:
        cond=P.canonical_condition(I.input_condition(can))
        groups[cond].append((tuple(zs),can))
    assert len(groups)==8629

    data=[]
    for cond,items in groups.items():
        B=G.affine_basis(cond)
        M=G.singleton_side_map(items[0][1],S,R)
        # rank-one group theorem guarantees the representative map is valid
        # for every support in this predecessor-condition group.
        for zs,can in items[1:]:
            MM=G.singleton_side_map(can,S,R)
            assert eq_on_condition(B,MM,M)
        union=set().union(*(set(zs) for zs,_ in items))
        inter=set(items[0][0])
        for zs,_ in items[1:]:inter &= set(zs)
        data.append((cond,B,M,frozenset(union),frozenset(inter),items))

    print('D_groups',len(data),
          'common_zero_site_count',sum(bool(x[4]) for x in data),
          'no_common_zero_site_count',sum(not x[4] for x in data),
          'union_label_size_distribution',dict(sorted(Counter(len(x[3]) for x in data).items())),
          'intersection_label_size_distribution',dict(sorted(Counter(len(x[4]) for x in data).items())))

    sites=sorted({z for x in data for z in x[3]})
    assert len(sites)==93
    bysite=defaultdict(list)
    for k,x in enumerate(data):
        for z in x[3]:bysite[z].append(k)

    # First test: one global affine template per zero site, chosen from the
    # first group carrying that site label.
    templates={z:data[bysite[z][0]][2] for z in sites}
    covered=[]
    site_cover=Counter()
    for k,(cond,B,M,U,J,items) in enumerate(data):
        ok=[]
        for z in U:
            if eq_on_condition(B,M,templates[z]):ok.append(z)
        covered.append(bool(ok))
        for z in ok:site_cover[z]+=1
    print('one_template_per_site_covered_groups',sum(covered),
          'uncovered_groups',len(data)-sum(covered),
          'site_template_coverage_minmax',(min(site_cover.values() or [0]),max(site_cover.values() or [0])))

    # Stronger diagnostic: for every site, greedily add templates from groups
    # carrying that site until all groups carrying the site are covered on
    # their own predecessor conditions. This gives an explicit site-local map
    # cover, not yet a globally minimal cover.
    class_count={}; total=0
    for z in sites:
        ids=bysite[z]; uncovered=set(ids); T=[]
        while uncovered:
            seed=next(iter(uncovered)); tm=data[seed][2]; T.append(tm)
            drop=[]
            for k in uncovered:
                _,B,M,_,_,_=data[k]
                if eq_on_condition(B,M,tm):drop.append(k)
            for k in drop:uncovered.remove(k)
        class_count[z]=len(T);total+=len(T)
    print('site_local_greedy_template_count_distribution',dict(sorted(Counter(class_count.values()).items())))
    print('site_local_greedy_total_templates',total,'max_per_site',max(class_count.values()))
    print('PASS PROBE V26_Q138_AD_THIRD_D_SITE_MAP_COVER')
    print('scope=exact affine-map cover diagnostics; greedy template count is an explicit upper cover, not a minimality theorem')

if __name__=='__main__':main()
