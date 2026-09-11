#!/usr/bin/env python3
import hashlib, io, json, math, sys
from collections import Counter
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_250way_sampled_pair_tree_bound as B
import probe_v26_q138_c916_e0_first_dyadic_250way_sampled_cactus_bound as C
import probe_v26_q138_c916_e0_first_dyadic_250way_disjoint_m4_augmented_tree as U
import probe_v26_q138_c916_e0_first_dyadic_m4_m4_equal_support_full_census as E

T=B.T
PHYS_N=B.PHYS_N
POS=B.POS
N=250
TOP_DENSITY=160
EXPECTED_OLD_TREE_COUNT=104924396549289894551742971384283046304785569891463833858811091198784336666266829156720254565496012800000000
EXPECTED_OLD_TREE_DIGEST='9c9f0cbe546db2bbfaa6d141f08add9ad3da5dce7397b095847eb8b375358433'
EXPECTED_OLD_CACTUS_COUNT=33698866574282151556543773734144910760069765391592566177717221057511121588650436772267259265024000000
EXPECTED_AUG_TREE_COUNT=21967150676357122759096016157776908681021504645166962636813404072948465193906330799702522296320000000000
EXPECTED_AUG_TREE_DIGEST='57a007e878d6a3ac6bd62891dc1a0c4c824d1438b4f13fc4a0c810c84babdf45'
EXPECTED_EQUAL_DIGEST='8318ee76821c7ccaa3f83aa292cc354abb83b1602ce3ecf1025cfcf3b0ea2448'
assert PHYS_N==149

OLD_CACTUS_CHORD_DESCRIPTORS=(
(('s',13),('s',204)),(('s',94),('s',217)),(('s',2),('s',99)),(('s',164),('m2',21)),
(('s',172),('m2',17)),(('m2',0),('m2',142)),(('s',13),('s',218)),(('s',94),('s',174)),
(('s',208),('m2',21)),(('s',210),('m2',226)),(('m2',21),('m2',148)),(('m2',84),('m2',92)),
(('s',103),('s',109)),(('m2',42),('m2',63)),(('s',13),('s',214)),(('s',190),('m2',225)),
(('s',94),('m2',43)),(('m2',75),('m2',128)),(('s',192),('s',211)),(('m2',36),('m2',50)),
(('s',96),('s',215)),(('s',147),('s',162)),(('s',207),('m2',150)),(('s',1),('s',78)),
(('s',94),('m2',170)),(('m2',53),('m4',89)),(('m2',73),('m2',97)),(('s',105),('s',115)),
(('s',108),('s',120)),(('m2',37),('m2',38)),(('m2',64),('m2',65)),(('s',14),('s',95)),
(('m2',34),('m2',41)),(('s',29),('m2',52)),(('s',212),('m2',21)),(('m2',68),('m2',76)),
(('m2',72),('m2',81)),(('s',218),('m2',133)),
)

EXTRA_FROZEN_MASKS={
    (141,247): int('2450cfe61448',16),
    (160,241): int('121418fe30509',16),
    (3,4): int('1affbefefbfeb',16),
    (3,19): int('fbffffffffbe',16),
    (6,18): int('71f7ffffdf1c',16),
    (6,19): int('71f7ffffdf1c',16),
    (19,22): int('12551cfe71549',16),
    (19,24): int('fbffffffffbe',16),
}

def rsize(m):
    return sum(int(x) for row in m for x in row)

def matrix_mask(m):
    z=bit=0
    for row in m:
        for x in row:
            if x: z |= 1<<bit
            bit += 1
    return z

def matrix_from_counts(counts,lvals,rvals):
    return tuple(tuple((a,b) in counts for b in rvals) for a in lvals)

def add_m4_authorities(c, rel):
    census,groups=c['census'],c['groups']
    desc=c['desc']; local={d:i for i,d in enumerate(desc)}
    ic={}; mc={}; new_strict=set(); eq_digest=[]; eq_hist=Counter(); strict_eq=0
    pairs,_=E.select_equal_pairs(census,groups)
    assert len(pairs)==55
    for gu,gv,dim in pairs:
        counts,lm,rm=E.J.pair_census(groups[gu],groups[gv],PHYS_N,ic,mc)
        assert lm==census[gu]['counts'] and rm==census[gv]['counts']
        lvals=tuple(sorted(lm)); rvals=tuple(sorted(rm)); mat=matrix_from_counts(counts,lvals,rvals)
        mask=matrix_mask(mat); eq_digest.append(f'{gu}|{gv}|{len(lvals)}x{len(rvals)}|{mask:x}')
        eq_hist[rsize(mat)]+=1
        if rsize(mat) < len(lvals)*len(rvals):
            u,v=local[('m4',gu)],local[('m4',gv)]
            key=(min(u,v),max(u,v)); assert key not in rel
            rel[key]=mat if u<v else tuple(zip(*mat))
            new_strict.add(key); strict_eq+=1
    got=hashlib.sha256(('\n'.join(eq_digest)+'\n').encode()).hexdigest()
    assert got==EXPECTED_EQUAL_DIGEST and strict_eq==52

    extra_rows=[]
    for (gu,gv),expected in sorted(EXTRA_FROZEN_MASKS.items()):
        counts,lm,rm=E.J.pair_census(groups[gu],groups[gv],PHYS_N,ic,mc)
        assert lm==census[gu]['counts'] and rm==census[gv]['counts']
        lvals=tuple(sorted(lm)); rvals=tuple(sorted(rm)); mat=matrix_from_counts(counts,lvals,rvals)
        mask=matrix_mask(mat); assert mask==expected,(gu,gv,hex(mask),hex(expected))
        u,v=local[('m4',gu)],local[('m4',gv)]; key=(min(u,v),max(u,v)); assert key not in rel
        rel[key]=mat if u<v else tuple(zip(*mat))
        new_strict.add(key)
        extra_rows.append({'left_group_id':gu,'right_group_id':gv,'joint_image_size':rsize(mat),'mask_hex':f'{mask:x}'})
    return new_strict,dict(sorted(eq_hist.items())),extra_rows,len(ic),len(mc)

def reconstruct_foundations(c, rel_aug, states, desc):
    old_rel=c['rel']; local={d:i for i,d in enumerate(desc)}
    old_adj=B.adj_from_rel(N,old_rel); root=local[('s',94)]
    old_tree,old_count,_,_=B.sparse_greedy((root,),(),N,old_rel,states,old_adj)
    assert old_count==EXPECTED_OLD_TREE_COUNT
    old_summary=B.tree_summary(old_tree,old_rel,states,desc)
    assert old_summary['edge_relation_digest_sha256']==EXPECTED_OLD_TREE_DIGEST
    old_set={tuple(sorted(e)) for e in old_tree}
    for a,b in OLD_CACTUS_CHORD_DESCRIPTORS:
        u,v=local[a],local[b]; key=tuple(sorted((u,v))); assert key in old_rel
        old_set.add(key)
    assert len(old_set)==287
    order,width=C.min_fill_order(N,old_set); assert width<=2
    cactus_count,peak=C.exact_factor_count(N,old_set,old_rel,states,order)
    assert cactus_count==EXPECTED_OLD_CACTUS_COUNT and peak<=3

    aug_adj=B.adj_from_rel(N,rel_aug)
    aug_tree,aug_count,_,_=B.sparse_greedy((root,),(),N,rel_aug,states,aug_adj)
    assert aug_count==EXPECTED_AUG_TREE_COUNT
    aug_summary=B.tree_summary(aug_tree,rel_aug,states,desc)
    assert aug_summary['edge_relation_digest_sha256']==EXPECTED_AUG_TREE_DIGEST
    aug_set={tuple(sorted(e)) for e in aug_tree}; assert len(aug_set)==249
    return dict(old_tree=tuple(old_tree),old_cactus=old_set,old_cactus_count=cactus_count,
                aug_tree=tuple(aug_tree),aug_set=aug_set,aug_count=aug_count)

def candidate_pool(rel, states, foundation, priority_edges):
    rows=[]
    for (u,v),m in rel.items():
        key=tuple(sorted((u,v)))
        if key in foundation: continue
        s=rsize(m); cart=states[u]*states[v]
        if s>=cart: continue
        rows.append((Fraction(s,cart),s,u,v))
    rows.sort()
    chosen={(u,v) for _,_,u,v in rows[:TOP_DENSITY]}
    chosen |= {e for e in priority_edges if e not in foundation}
    return tuple(sorted(chosen)),len(rows)

def score_by_tree(tree_edges, rel, states, pool):
    tadj,msg=C.directed_messages(tree_edges,rel,states)
    tree_count,_=T.tree_count_and_marginals(range(N),tree_edges,rel,states)
    out=[]
    for u,v in pool:
        p=C.tree_path(tadj,u,v)
        joint=C.endpoint_joint(p,tadj,msg,rel,states)
        assert sum(map(sum,joint))==tree_count
        m=T.relation_matrix(rel,u,v)
        cc=sum(joint[a][b] for a in range(states[u]) for b in range(states[v]) if m[a][b])
        if cc < tree_count:
            out.append((cc,len(p)-1,rsize(m),u,v))
    out.sort(key=lambda x:(x[0],x[1],x[2],x[3],x[4]))
    return tuple(out),tree_count

def expand_width3(name, foundation, foundation_count, score_tree, rel, states, desc, priority_edges):
    pool,total_strict=candidate_pool(rel,states,foundation,priority_edges)
    scored,score_tree_count=score_by_tree(score_tree,rel,states,pool)
    graph=set(foundation); accepted=[]; rejected_width=0
    initial_order,initial_width=C.min_fill_order(N,graph); assert initial_width<=2
    for cc,plen,rs,u,v in scored:
        key=tuple(sorted((u,v)))
        if key in graph: continue
        trial=set(graph); trial.add(key)
        order,width=C.min_fill_order(N,trial)
        if width<=3:
            graph=trial; accepted.append((cc,plen,rs,u,v,width))
        else:
            rejected_width+=1
    order,width=C.min_fill_order(N,graph); assert width<=3
    count,peak=C.exact_factor_count(N,graph,rel,states,order)
    assert peak<=4 and 0<count<=foundation_count
    return {
        'name':name,'foundation_edges':len(foundation),'foundation_count':foundation_count,
        'foundation_log2':math.log2(foundation_count),'candidate_pool_size':len(pool),
        'strict_nonfoundation_edges_available':total_strict,'tree_scored_strict_candidates':len(scored),
        'score_tree_count':score_tree_count,'accepted_chords':len(accepted),'rejected_by_width_certificate':rejected_width,
        'final_edges':len(graph),'certified_induced_width':width,'peak_factor_scope':peak,
        'exact_assignment_count':count,'exact_log2':math.log2(count),
        'gain_vs_foundation_log2_bits':math.log2(foundation_count)-math.log2(count),
        'gap_vs_physical_log2_bits':math.log2(count)-PHYS_N,
        'accepted_edges':[{'left_kind':desc[u][0],'left_group_id':desc[u][1],
                           'right_kind':desc[v][0],'right_group_id':desc[v][1],
                           'tree_single_chord_count':cc,'tree_path_edges':plen,
                           'relation_size':rs,'width_after_accept':w}
                          for cc,plen,rs,u,v,w in accepted],
    }

def analyze():
    syn=C.synthetic_regression()
    with redirect_stdout(io.StringIO()):
        c,rel_aug,states,desc,pairs,m4adj,components,m4deg,inner_cache=U.augment_relations()
    assert len(rel_aug)==14159
    foundations=reconstruct_foundations(c,rel_aug,states,desc)
    rel=dict(rel_aug)
    new_strict,eq_hist,extra_rows,ic,mc=add_m4_authorities(c,rel)
    assert len(new_strict)==60 and len(rel)==14219

    local={d:i for i,d in enumerate(desc)}
    disjoint_edges={tuple(sorted((local[('m4',gu)],local[('m4',gv)]))) for gu,gv in pairs}
    priority_edges=disjoint_edges | new_strict
    assert len(priority_edges)==419
    old=expand_width3('pr187_cactus_foundation',foundations['old_cactus'],foundations['old_cactus_count'],
                      foundations['old_tree'],rel,states,desc,priority_edges)
    aug=expand_width3('pr191_augmented_tree_foundation',foundations['aug_set'],foundations['aug_count'],
                      foundations['aug_tree'],rel,states,desc,priority_edges)
    best=min((old,aug),key=lambda r:(r['exact_assignment_count'],r['name']))
    decision=('C916_250WAY_CERTIFIED_WIDTH3_BOUND_BELOW_PHYSICAL_149'
              if best['exact_assignment_count'] < (1<<PHYS_N)
              else 'C916_250WAY_CERTIFIED_WIDTH3_STRICTLY_BEATS_PR187_CACTUS'
              if best['exact_log2'] < math.log2(EXPECTED_OLD_CACTUS_COUNT)
              else 'C916_250WAY_CERTIFIED_WIDTH3_NO_GAIN_VS_PR187_CACTUS')
    out={'position':POS,'physical_shared_dimension':PHYS_N,'outputs':N,
         'synthetic_regression':syn,'pr190_augmented_edges':14159,
         'strict_equal_support_edges_added':52,'targeted_other_m4_m4_edges_added':8,
         'enriched_relation_edges':len(rel),'equal_support_joint_size_histogram':eq_hist,
         'targeted_extra_relations':extra_rows,'cached_support_intersections':ic,'cached_character_moments':mc,
         'foundations':[old,aug],'selected_foundation':best['name'],
         'selected_exact_assignment_count':best['exact_assignment_count'],'selected_exact_log2':best['exact_log2'],
         'selected_state_bits':(best['exact_assignment_count']-1).bit_length(),
         'selected_gap_vs_physical_log2_bits':best['gap_vs_physical_log2_bits'],
         'decision':decision}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_250WAY_CERTIFIED_WIDTH3')
    print('scope=exact certified-width<=3 CSP counts from both the PR187 cactus and PR191 augmented-tree foundations over an enriched 14219-edge exact relation authority')
    print('important=candidate admission is heuristic but every reported final count is exact for its accepted graph; rejected edges are not treated as absent physical relations')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
