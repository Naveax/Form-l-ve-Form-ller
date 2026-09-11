#!/usr/bin/env python3
import hashlib, io, json, math, sys
from collections import Counter, defaultdict, deque
from contextlib import redirect_stdout
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_m4_m4_nonzero_correlation_joint_images as J
import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O

P=O.P
D=O.D
PHYS_N=O.PHYS_N
POS=O.POS
assert PHYS_N==149

def relation_mask(counts,lvals,rvals):
    mask=bit=0
    for a in lvals:
        for b in rvals:
            if (a,b) in counts:
                mask |= 1 << bit
            bit += 1
    return mask

def disjoint_pairs(census,groups):
    m4s=tuple(g for g in range(250) if census[g]['multiplicity']==4)
    inner_cache={}
    rows=[]
    adj={g:set() for g in m4s}
    for i,u in enumerate(m4s):
        for v in m4s[i+1:]:
            rel,inter=P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
            if rel!='disjoint':
                continue
            assert inter is None
            assert D.group_inner(groups[u],groups[v],inner_cache)==0
            rows.append((u,v))
            adj[u].add(v); adj[v].add(u)
    assert len(rows)==359
    comps=[]
    seen=set()
    for g in m4s:
        if g in seen: continue
        q=deque([g]); seen.add(g); comp=[]
        while q:
            x=q.popleft(); comp.append(x)
            for y in sorted(adj[x]):
                if y not in seen:
                    seen.add(y); q.append(y)
        comps.append(tuple(sorted(comp)))
    return tuple(rows),adj,tuple(sorted(comps,key=lambda c:(-len(c),c))),len(inner_cache)

def analyze():
    syn=J.synthetic()
    with redirect_stdout(io.StringIO()):
        census,groups=O.build_authority()
    pairs,adj,components,inner_cache_entries=disjoint_pairs(census,groups)

    ic,mc={},{}
    rows=[]
    digest=[]
    strict=0
    mask_by_shape=defaultdict(Counter)
    size_by_shape=defaultdict(Counter)
    for idx,(u,v) in enumerate(pairs,1):
        counts,lm,rm=J.pair_census(groups[u],groups[v],PHYS_N,ic,mc)
        assert lm==census[u]['counts'] and rm==census[v]['counts']
        lvals=tuple(sorted(lm)); rvals=tuple(sorted(rm))
        cart=len(lvals)*len(rvals); size=len(counts)
        mask=relation_mask(counts,lvals,rvals)
        if size<cart: strict+=1
        shape=f'{len(lvals)}x{len(rvals)}'
        mask_by_shape[shape][f'{mask:x}']+=1
        size_by_shape[shape][size]+=1
        row={
            'left_group_id':u,'right_group_id':v,
            'left_image_size':len(lvals),'right_image_size':len(rvals),
            'cartesian_image_size':cart,'joint_image_size':size,
            'missing_cartesian_states':cart-size,
            'integer_bit_saving':(len(lvals)-1).bit_length()+(len(rvals)-1).bit_length()-(size-1).bit_length(),
            'exact_cardinality_gain_log2':math.log2(cart)-math.log2(size),
            'relation_mask_hex':f'{mask:x}',
        }
        rows.append(row)
        digest.append(f'{u}|{v}|{shape}|{mask:x}')
        if idx%25==0 or idx==len(pairs):
            print(f'progress exact_pairs={idx}/{len(pairs)} support_cache={len(ic)} moment_cache={len(mc)}',flush=True)

    joint_hist=Counter(r['joint_image_size'] for r in rows)
    cart_hist=Counter(r['cartesian_image_size'] for r in rows)
    gain_hist=Counter(round(r['exact_cardinality_gain_log2'],12) for r in rows)
    deg_hist=Counter(len(adj[g]) for g in adj)
    mask_shapes={shape:dict(sorted(c.items())) for shape,c in sorted(mask_by_shape.items())}
    size_shapes={shape:dict(sorted(c.items())) for shape,c in sorted(size_by_shape.items())}
    uniform_masks={shape:(len(c)==1) for shape,c in mask_by_shape.items()}
    decision=('M4_M4_DISJOINT_SUPPORT_FULL_CENSUS_ALL_SUBCARTESIAN'
              if strict==len(pairs)
              else 'M4_M4_DISJOINT_SUPPORT_FULL_CENSUS_MIXED')
    out={
        'position':POS,'physical_shared_dimension':PHYS_N,
        'multiplicity4_outputs':len(adj),
        'disjoint_support_pairs':len(pairs),
        'disjoint_graph_degree_histogram':dict(sorted(deg_hist.items())),
        'disjoint_graph_component_sizes':[len(c) for c in components],
        'disjoint_graph_largest_component':list(components[0]),
        'synthetic_eight_term_regression':syn,
        'pair_marginal_crosschecks':2*len(pairs),
        'strict_subcartesian_pairs':strict,
        'cartesian_image_size_histogram':dict(sorted(cart_hist.items())),
        'joint_image_size_histogram':dict(sorted(joint_hist.items())),
        'cardinality_gain_log2_histogram':{str(k):v for k,v in sorted(gain_hist.items())},
        'joint_size_histogram_by_shape':size_shapes,
        'relation_mask_histogram_by_shape':mask_shapes,
        'uniform_relation_mask_within_shape':dict(sorted(uniform_masks.items())),
        'relation_digest_sha256':hashlib.sha256(('\n'.join(digest)+'\n').encode()).hexdigest(),
        'inner_product_cache_entries':inner_cache_entries,
        'cached_support_intersections':len(ic),
        'cached_character_moments':len(mc),
        'decision':decision,
    }
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_M4_DISJOINT_SUPPORT_FULL_CENSUS')
    print('scope=exact eight-term joint-image census for all 359 disjoint-projection-support m4-m4 pairs')
    print('theorem=every reported relation is exact on the full 149-bit physical domain; no 2^149 enumeration is used')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':
    analyze()
