#!/usr/bin/env python3
import hashlib, io, json, math, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_m4_m4_nonzero_correlation_joint_images as J
import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O

P=O.P
D=O.D
PHYS_N=O.PHYS_N
POS=O.POS
K=24
ANCHOR=(3,158)
assert PHYS_N==149

def relation_mask(counts,lvals,rvals):
    mask=bit=0
    for a in lvals:
        for b in rvals:
            if (a,b) in counts:
                mask |= 1 << bit
            bit += 1
    return mask

def choose_pairs(census,groups):
    m4s=tuple(g for g in range(250) if census[g]['multiplicity']==4)
    inner_cache={}
    rows=[]
    for i,u in enumerate(m4s):
        for v in m4s[i+1:]:
            rel,inter=P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
            if rel != 'disjoint':
                continue
            assert inter is None
            inner=D.group_inner(groups[u],groups[v],inner_cache)
            assert inner == 0
            rows.append((u,v,census[u]['image_size']*census[v]['image_size']))
    assert len(rows)==359
    assert any((u,v)==ANCHOR for u,v,_ in rows)

    selected=[next(r for r in rows if (r[0],r[1])==ANCHOR)]
    chosen={(ANCHOR[0],ANCHOR[1])}
    deg=Counter(ANCHOR)
    while len(selected)<K:
        candidates=[r for r in rows if (r[0],r[1]) not in chosen]
        assert candidates
        u,v,cart=min(
            candidates,
            key=lambda r:(
                max(deg[r[0]],deg[r[1]]),
                deg[r[0]]+deg[r[1]],
                r[2],
                r[0],
                r[1],
            ),
        )
        selected.append((u,v,cart))
        chosen.add((u,v))
        deg[u]+=1; deg[v]+=1
    return tuple(selected),len(rows),len(inner_cache),deg

def analyze():
    syn=J.synthetic()
    with redirect_stdout(io.StringIO()):
        census,groups=O.build_authority()
    selected,available,inner_cache_entries,seldeg=choose_pairs(census,groups)

    ic,mc={},{}
    outrows=[]
    digest=[]
    strict=0
    for u,v,cart0 in selected:
        counts,lm,rm=J.pair_census(groups[u],groups[v],PHYS_N,ic,mc)
        assert lm==census[u]['counts'] and rm==census[v]['counts']
        lvals=tuple(sorted(lm)); rvals=tuple(sorted(rm))
        cart=len(lvals)*len(rvals)
        assert cart==cart0
        size=len(counts)
        mask=relation_mask(counts,lvals,rvals)
        if size<cart:
            strict += 1
        if (u,v)==ANCHOR:
            assert cart==49 and size==13 and mask==int('20408fe20408',16)
        outrows.append({
            'left_group_id':u,'right_group_id':v,
            'left_image_size':len(lvals),'right_image_size':len(rvals),
            'cartesian_image_size':cart,'joint_image_size':size,
            'missing_cartesian_states':cart-size,
            'integer_bit_saving':(len(lvals)-1).bit_length()+(len(rvals)-1).bit_length()-(size-1).bit_length(),
            'exact_cardinality_gain_log2':math.log2(cart)-math.log2(size),
            'relation_mask_hex':f'{mask:x}',
        })
        digest.append(f'{u}|{v}|{len(lvals)}x{len(rvals)}|{mask:x}')

    hist=Counter(r['joint_image_size'] for r in outrows)
    gains=sorted(outrows,key=lambda r:(-r['exact_cardinality_gain_log2'],r['left_group_id'],r['right_group_id']))
    selected_nodes=sorted(set(x for u,v,_ in selected for x in (u,v)))
    degree_hist=Counter(seldeg.values())
    decision=('M4_M4_DISJOINT_SUPPORT_BALANCED_SAMPLE_SUBCARTESIAN_FOUND'
              if strict else 'M4_M4_DISJOINT_SUPPORT_BALANCED_SAMPLE_ALL_CARTESIAN')
    out={
        'position':POS,'physical_shared_dimension':PHYS_N,
        'disjoint_support_pairs_available':available,
        'sample_pairs':K,
        'sample_unique_m4_nodes':len(selected_nodes),
        'sample_node_degree_histogram':dict(sorted(degree_hist.items())),
        'synthetic_eight_term_regression':syn,
        'pair_marginal_crosschecks':2*K,
        'strict_subcartesian_pairs':strict,
        'joint_image_size_histogram':dict(sorted(hist.items())),
        'strongest_pairs_top10':gains[:10],
        'results':outrows,
        'relation_digest_sha256':hashlib.sha256(('\n'.join(digest)+'\n').encode()).hexdigest(),
        'inner_product_cache_entries':inner_cache_entries,
        'cached_support_intersections':len(ic),
        'cached_character_moments':len(mc),
        'decision':decision,
    }
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_M4_DISJOINT_SUPPORT_BALANCED_SAMPLE')
    print('scope=exact eight-term joint-image census for 24 deterministically endpoint-balanced disjoint-support m4-m4 pairs')
    print('important=the sample is a candidate layer, not an exhaustive theorem over all 359 disjoint-support m4-m4 pairs')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':
    analyze()
