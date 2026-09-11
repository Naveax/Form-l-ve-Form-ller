#!/usr/bin/env python3
import hashlib, io, json, math, sys
from collections import Counter, deque
from contextlib import redirect_stdout
from functools import lru_cache
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_m4_m4_disjoint_support_full_census as F

P=F.P
PHYS_N=F.PHYS_N
POS=F.POS
EXPECTED_DIGEST='8fd11e4da31260abc9c4a1aa71837aa0ad0c9c683d635d39e208e59b71b8b845'
MASK_BY_SHAPE={'7x7':int('20408fe20408',16),'9x7':int('8102047f1020408',16)}
assert PHYS_N==149

def mask_for_cross(lvals,rvals):
    mask=bit=0
    for a in lvals:
        for b in rvals:
            if a==0 or b==0: mask |= 1<<bit
            bit+=1
    return mask

def components(vertices,adj):
    left=set(vertices); out=[]
    while left:
        s=min(left); q=deque([s]); left.remove(s); comp=[]
        while q:
            x=q.popleft(); comp.append(x)
            for y in sorted(adj[x]):
                if y in left:
                    left.remove(y); q.append(y)
        out.append(tuple(sorted(comp)))
    return tuple(sorted(out,key=lambda c:(-len(c),c)))

def weighted_independent_set_count(m4s,adj,weights):
    idx={g:i for i,g in enumerate(m4s)}
    n=len(m4s)
    nbr=[0]*n
    for g in m4s:
        i=idx[g]
        for h in adj[g]:
            nbr[i] |= 1<<idx[h]
    w=tuple(weights[g] for g in m4s)

    @lru_cache(None)
    def z(mask):
        if not mask: return 1
        best=None
        mm=mask
        while mm:
            b=mm & -mm; i=b.bit_length()-1; mm^=b
            d=(nbr[i]&mask).bit_count()
            if d==0:
                return (1+w[i])*z(mask ^ (1<<i))
            key=(d,-i)
            if best is None or key>best[0]: best=(key,i)
        i=best[1]
        without=mask ^ (1<<i)
        return z(without) + w[i]*z(without & ~nbr[i])
    total=z((1<<n)-1)
    return total,z.cache_info().currsize

def analyze():
    with redirect_stdout(io.StringIO()):
        census,groups=F.O.build_authority()
    pairs,adj,all_components,inner_cache_entries=F.disjoint_pairs(census,groups)
    m4s=tuple(sorted(adj))
    assert len(m4s)==90 and len(pairs)==359
    assert tuple(len(c) for c in all_components)==(90,)

    support_subset_checks=0
    for g in m4s:
        grp=groups[g]
        assert grp['multiplicity']==4 and len(grp['terms'])==4
        assert all(t['kind']=='gauss_sector' for t in grp['terms'])
        pc=grp['projection_anchor']['physical_support_constraints']
        for t in grp['terms']:
            assert P.affine_subset(t['anchor'],pc)
            support_subset_checks+=1
        vals=tuple(sorted(census[g]['counts']))
        assert 0 in vals
        assert vals[len(vals)//2]==0

    digest=[]
    shape_hist=Counter()
    for u,v in pairs:
        lv=tuple(sorted(census[u]['counts'])); rv=tuple(sorted(census[v]['counts']))
        shape=f'{len(lv)}x{len(rv)}'
        assert shape in MASK_BY_SHAPE
        mask=mask_for_cross(lv,rv)
        assert mask==MASK_BY_SHAPE[shape]
        digest.append(f'{u}|{v}|{shape}|{mask:x}')
        shape_hist[shape]+=1
    got=hashlib.sha256(('\n'.join(digest)+'\n').encode()).hexdigest()
    assert got==EXPECTED_DIGEST
    assert shape_hist==Counter({'7x7':351,'9x7':8})

    universals=tuple(sorted(g for g in m4s if len(adj[g])==89))
    assert len(universals)==4
    residual=tuple(g for g in m4s if g not in universals)
    radj={g:set(h for h in adj[g] if h in residual) for g in residual}
    residual_edges=sum(len(x) for x in radj.values())//2
    assert residual_edges==9
    rdeg=Counter(len(radj[g]) for g in residual)
    assert rdeg==Counter({0:70,1:15,3:1})
    rcomps=components(residual,radj)
    assert Counter(map(len,rcomps))==Counter({1:70,2:6,4:1})

    state_sizes={g:int(census[g]['image_size']) for g in m4s}
    weights={g:state_sizes[g]-1 for g in m4s}
    assert Counter(state_sizes.values())==Counter({7:88,9:2})
    exact,cache_states=weighted_independent_set_count(m4s,adj,weights)
    isolated=1
    for g in m4s: isolated*=state_sizes[g]
    assert 0<exact<isolated

    elog=math.log2(exact); ilog=math.log2(isolated)
    out={
        'position':POS,'physical_shared_dimension':PHYS_N,
        'multiplicity4_outputs':len(m4s),
        'exact_disjoint_relations':len(pairs),
        'relation_digest_sha256':EXPECTED_DIGEST,
        'relation_shape_histogram':dict(sorted(shape_hist.items())),
        'projection_support_subset_checks':support_subset_checks,
        'all_m4_outputs_zero_outside_projection_anchor':True,
        'disjoint_relation_is_exact_zero_cross':True,
        'disjoint_graph_component_sizes':[len(c) for c in all_components],
        'universal_degree_89_m4_nodes':list(universals),
        'residual_after_universals_nodes':len(residual),
        'residual_after_universals_edges':residual_edges,
        'residual_degree_histogram':dict(sorted(rdeg.items())),
        'residual_component_size_histogram':dict(sorted(Counter(map(len,rcomps)).items())),
        'nine_state_m4_nodes':[g for g in m4s if state_sizes[g]==9],
        'isolated_m4_state_count':isolated,
        'isolated_m4_log2':ilog,
        'exact_disjoint_relation_consistent_m4_assignment_count':exact,
        'exact_disjoint_relation_consistent_m4_log2':elog,
        'exact_disjoint_relation_consistent_m4_state_bits':(exact-1).bit_length(),
        'gain_vs_isolated_m4_log2_bits':ilog-elog,
        'independent_set_dp_cache_states':cache_states,
        'inner_product_cache_entries':inner_cache_entries,
        'decision':'M4_90WAY_DISJOINT_RELATION_CSP_COUNT_EXACT',
    }
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_90WAY_DISJOINT_RELATION_CSP')
    print('scope=exact count of all 90-way m4 state assignments satisfying all 359 PR190 disjoint-support relations')
    print('theorem=each disjoint relation is exactly Y_u=0 OR Y_v=0, so relation-consistent assignments are weighted independent sets with node weight image_size-1')
    print('important=this is exact for the 359-relation m4 CSP, but still only an upper bound on the true 90-output physical joint image')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':
    analyze()
