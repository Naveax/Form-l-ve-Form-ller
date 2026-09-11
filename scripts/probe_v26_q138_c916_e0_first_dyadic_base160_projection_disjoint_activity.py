#!/usr/bin/env python3
import hashlib, io, json, math, sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_group_output_pair_dependency as D
import probe_v26_q138_c916_e0_first_dyadic_singleton_m2_cross_joint_image as X
import probe_v26_q138_c916_e0_first_dyadic_m4_projection_pair_triple_hypergraph as H

P=D.P
S=X.S
E=X.E
POS=D.POS
PHYS_N=D.PHYS_N
EXPECTED_NORMAL_RANK=35
assert PHYS_N==149

def census_map(record):
    return {int(x['value']):int(x['multiplicity']) for x in record['value_multiplicity']}

def build_base_authority():
    with redirect_stdout(io.StringIO()):
        singleton=S.analyze()
        even=E.analyze()
    sf={int(r['group_id']):census_map(r) for r in singleton['groups']}
    mf={int(r['group_id']):census_map(r) for r in even['groups'] if int(r['multiplicity'])==2}
    assert len(sf)==103 and len(mf)==57
    assert all(0 in z and len(z)==4 for z in sf.values())
    assert Counter(len(z) for z in mf.values())==Counter({3:6,5:51})
    assert all(0 in z for z in mf.values())

    e0,_e1,_half=P.C.P.U.H.classify_patterns()
    grouped=defaultdict(list)
    for zc in range(4):
        for zs,cls in e0[zc]:
            can=P.C.P.U.H.support_for(POS,zs,cls)
            if can is not None:
                grouped[can].append((zs,cls))
    ordered=list(sorted(grouped.items(),key=lambda kv:kv[0]))
    assert len(ordered)==250
    groups={}
    census={}
    family={}
    tid=1
    for gid,(can,sectors) in enumerate(ordered):
        if len(sectors) not in (1,2):
            continue
        group,tid=D.build_group_terms(gid,can,sectors,tid)
        groups[gid]=group
        family[gid]='s' if len(sectors)==1 else 'm2'
        census[gid]=sf[gid] if len(sectors)==1 else mf[gid]
    gids=tuple(sorted(groups))
    assert len(gids)==160
    assert Counter(family[g] for g in gids)==Counter({'s':103,'m2':57})
    return gids,groups,census,family

def normal_rank(groups,gids):
    rows=[]
    for g in gids:
        rows.extend(int(m) for m,_ in groups[g]['projection_anchor']['physical_support_constraints'])
    return P.R.gf2_rank(rows)

def analyze():
    syn=H.synthetic_regression()
    gids,groups,census,family=build_base_authority()
    assert normal_rank(groups,gids)==EXPECTED_NORMAL_RANK
    local={g:i for i,g in enumerate(gids)}
    weights=tuple(len(census[g])-1 for g in gids)
    assert Counter(weights)==Counter({3:103,2:6,4:51})

    term_relation_hist=Counter()
    for g in gids:
        proj=groups[g]['projection_anchor']
        for t in groups[g]['terms']:
            rel,_=P.support_relation(t['anchor'],proj,PHYS_N)
            term_relation_hist[rel]+=1
            assert rel in ('equal','left_subset_right'), (g,t['kind'],rel)

    support_hist=Counter()
    family_edge_hist=Counter()
    edges=[]
    rows=[]
    for i,u in enumerate(gids):
        for v in gids[i+1:]:
            rel,_=P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
            support_hist[rel]+=1
            if rel=='disjoint':
                edges.append((1<<local[u])|(1<<local[v]))
                fkey='_'.join(sorted((family[u],family[v])))
                family_edge_hist[fkey]+=1
                rows.append(f'{u}|{v}\n')
    digest=hashlib.sha256(''.join(rows).encode()).hexdigest()
    exact,stats=H.weighted_hypergraph_count(len(gids),weights,tuple(edges))
    isolated=1
    for w in weights:
        isolated*=1+w
    assert isolated==(4**103)*(3**6)*(5**51)
    assert 0<exact<=isolated
    elog=math.log2(exact)
    decision=('C916_BASE160_PROJECTION_DISJOINT_ACTIVITY_BOUND_BELOW_PHYSICAL_149'
              if exact < (1<<PHYS_N)
              else 'C916_BASE160_PROJECTION_DISJOINT_ACTIVITY_STRICTLY_BEATS_ISOLATED'
              if exact < isolated
              else 'C916_BASE160_PROJECTION_DISJOINT_ACTIVITY_NO_GAIN')
    out={
        'position':POS,'physical_shared_dimension':PHYS_N,'outputs':160,
        'synthetic_weighted_hypergraph_regression':syn,
        'projection_normal_span_rank':EXPECTED_NORMAL_RANK,
        'term_to_projection_support_relation_histogram':dict(sorted(term_relation_hist.items())),
        'support_relation_histogram':dict(sorted(support_hist.items())),
        'projection_disjoint_pair_edges':len(edges),
        'projection_disjoint_family_edge_histogram':dict(sorted(family_edge_hist.items())),
        'projection_disjoint_edge_digest_sha256':digest,
        'isolated_cartesian_count':isolated,'isolated_cartesian_log2':math.log2(isolated),
        'exact_weighted_activity_count':exact,'exact_weighted_activity_log2':elog,
        'state_bits':(exact-1).bit_length(),
        'gain_vs_isolated_log2_bits':math.log2(isolated)-elog,
        'gap_vs_physical_log2_bits':elog-PHYS_N,
        'weighted_dp_stats':stats,'decision':decision,
    }
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_BASE160_PROJECTION_DISJOINT_ACTIVITY')
    print('scope=rigorous base160 activity-support upper bound from exact projection-anchor disjointness and exact isolated nonzero label counts')
    print('theorem=every term support is asserted to lie inside its group projection anchor, so a nonzero group output requires projection-anchor membership; disjoint anchors therefore imply a zero-cross pair')
    print('important=this uses only projection-disjoint activity constraints and ignores stronger nonlinear pair/value restrictions')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':
    analyze()
