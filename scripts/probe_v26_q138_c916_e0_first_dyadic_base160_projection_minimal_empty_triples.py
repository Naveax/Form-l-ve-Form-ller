#!/usr/bin/env python3
import hashlib, io, json, math, sys
from collections import Counter
from contextlib import redirect_stdout
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_base160_projection_disjoint_activity as B

P=B.P
PHYS_N=B.PHYS_N
POS=B.POS
EXPECTED_NORMAL_RANK=35
EXPECTED_PAIR_DIGEST='55b3e361b4eb532139f5d2660c465195cebb7d0208e14419c5409d09cd007954'
assert PHYS_N==149


def analyze():
    with redirect_stdout(io.StringIO()):
        gids,groups,census,family=B.build_base_authority()
    assert len(gids)==160
    assert B.normal_rank(groups,gids)==EXPECTED_NORMAL_RANK

    pair_disjoint=set(); pair_rows=[]; support_hist=Counter()
    for u,v in combinations(gids,2):
        rel,_=P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
        support_hist[rel]+=1
        if rel=='disjoint':
            pair_disjoint.add((u,v)); pair_rows.append(f'{u}|{v}\n')
    pair_digest=hashlib.sha256(''.join(pair_rows).encode()).hexdigest()
    assert len(pair_disjoint)==2 and pair_digest==EXPECTED_PAIR_DIGEST

    minimal=[]; fam_hist=Counter(); vertex_degree=Counter(); tested=0
    for idx,(a,b,c) in enumerate(combinations(gids,3),1):
        if ((a,b) in pair_disjoint or (a,c) in pair_disjoint or (b,c) in pair_disjoint):
            continue
        tested+=1
        cons=(list(groups[a]['projection_anchor']['physical_support_constraints'])+
              list(groups[b]['projection_anchor']['physical_support_constraints'])+
              list(groups[c]['projection_anchor']['physical_support_constraints']))
        if P.C.P.U.T.rref(cons,n=PHYS_N) is None:
            minimal.append((a,b,c))
            fam_hist['+'.join(sorted((family[a],family[b],family[c])))]+=1
            vertex_degree[a]+=1; vertex_degree[b]+=1; vertex_degree[c]+=1
        if idx%100000==0:
            print('progress',idx,'minimal_empty',len(minimal),flush=True)

    digest=hashlib.sha256((''.join(f'{a}|{b}|{c}\n' for a,b,c in minimal)).encode()).hexdigest()
    out={
        'position':POS,
        'physical_shared_dimension':PHYS_N,
        'outputs':len(gids),
        'projection_normal_span_rank':EXPECTED_NORMAL_RANK,
        'all_triples':math.comb(len(gids),3),
        'projection_disjoint_pairs':len(pair_disjoint),
        'projection_disjoint_pair_digest_sha256':pair_digest,
        'pairwise_intersecting_triples_tested':tested,
        'minimal_empty_projection_triples':len(minimal),
        'minimal_empty_projection_triple_digest_sha256':digest,
        'minimal_empty_projection_triple_family_histogram':dict(sorted(fam_hist.items())),
        'minimal_empty_projection_triple_vertex_degree_histogram':dict(sorted(Counter(vertex_degree.values()).items())),
        'minimal_empty_projection_triple_top_vertices':[{'group_id':g,'family':family[g],'degree':d} for g,d in sorted(vertex_degree.items(),key=lambda kv:(-kv[1],kv[0]))[:30]],
        'minimal_empty_projection_triple_list':[list(x) for x in minimal],
        'support_relation_histogram':dict(sorted(support_hist.items())),
        'decision':'C916_BASE160_PROJECTION_MINIMAL_EMPTY_TRIPLES_EXACT',
    }
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_BASE160_PROJECTION_MINIMAL_EMPTY_TRIPLES')
    print('scope=exact census of every minimal order-3 affine projection-anchor obstruction in the 160 singleton+m2 output family')
    print('important=value-level pair restrictions are not used; this is a structural affine-obstruction authority only')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
