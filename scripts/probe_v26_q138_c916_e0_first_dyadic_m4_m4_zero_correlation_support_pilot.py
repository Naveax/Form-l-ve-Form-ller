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
K=12
assert PHYS_N==149

def norm2(counts):
    return sum(int(v)*int(v)*int(n) for v,n in counts.items())

def choose_pairs(census,groups):
    m4s=tuple(g for g in range(250) if census[g]['multiplicity']==4)
    cache={}
    rows=[]
    for i,u in enumerate(m4s):
        for v in m4s[i+1:]:
            inner=D.group_inner(groups[u],groups[v],cache)
            if inner != 0:
                continue
            rel,inter=P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
            dim=None if inter is None else len(inter[2])
            rows.append({'left_group_id':u,'right_group_id':v,
                         'left_image_size':census[u]['image_size'],'right_image_size':census[v]['image_size'],
                         'support_relation':rel,'intersection_dimension':dim})
    assert len(rows)==4003
    chosen={}
    def add(row,reason):
        key=(row['left_group_id'],row['right_group_id'])
        if key not in chosen: chosen[key]=dict(row,selection_reason=reason)
    by={}
    for rel in ('equal','left_subset_right','right_subset_left','overlap_incomparable','disjoint'):
        xs=[r for r in rows if r['support_relation']==rel]; by[rel]=xs
        if not xs: continue
        base=lambda r:(r['left_image_size']*r['right_image_size'],r['left_group_id'],r['right_group_id'])
        add(min(xs,key=base),rel+'_representative')
        dims=[r for r in xs if r['intersection_dimension'] is not None]
        if dims:
            add(min(dims,key=lambda r:(r['intersection_dimension'],)+base(r)),rel+'_min_intersection')
            add(min(dims,key=lambda r:(-r['intersection_dimension'],)+base(r)),rel+'_max_intersection')
    pri={'equal':0,'left_subset_right':1,'right_subset_left':1,'overlap_incomparable':2,'disjoint':3}
    fill=sorted(rows,key=lambda r:(pri[r['support_relation']],r['left_image_size']*r['right_image_size'],
                                    -(r['intersection_dimension'] if r['intersection_dimension'] is not None else -1),
                                    r['left_group_id'],r['right_group_id']))
    for r in fill:
        if len(chosen)>=K: break
        add(r,'structural_fill')
    assert len(chosen)==K
    return tuple(chosen[k] for k in sorted(chosen)),len(cache)

def relation_mask(counts,lvals,rvals):
    mask=bit=0
    for a in lvals:
        for b in rvals:
            if (a,b) in counts: mask|=1<<bit
            bit+=1
    return mask

def analyze():
    syn=J.synthetic()
    with redirect_stdout(io.StringIO()):
        census,groups=O.build_authority()
    selected,inner_cache_entries=choose_pairs(census,groups)
    ic,mc={},{}; outrows=[]; digest=[]; strict=0
    for meta in selected:
        u=meta['left_group_id']; v=meta['right_group_id']
        counts,lm,rm=J.pair_census(groups[u],groups[v],PHYS_N,ic,mc)
        assert lm==census[u]['counts'] and rm==census[v]['counts']
        lvals=tuple(sorted(lm)); rvals=tuple(sorted(rm)); cart=len(lvals)*len(rvals); size=len(counts)
        mask=relation_mask(counts,lvals,rvals)
        if size<cart: strict+=1
        row=dict(meta,cartesian_image_size=cart,joint_image_size=size,missing_cartesian_states=cart-size,
                 integer_bit_saving=(len(lvals)-1).bit_length()+(len(rvals)-1).bit_length()-(size-1).bit_length(),
                 exact_cardinality_gain_log2=math.log2(cart)-math.log2(size),relation_mask_hex=f'{mask:x}')
        outrows.append(row); digest.append(f'{u}|{v}|{len(lvals)}x{len(rvals)}|{mask:x}')
    hist=Counter(r['joint_image_size'] for r in outrows); relhist=Counter(r['support_relation'] for r in outrows)
    decision=('M4_M4_ZERO_CORRELATION_SUPPORT_PILOT_SUBCARTESIAN_FOUND' if strict else
              'M4_M4_ZERO_CORRELATION_SUPPORT_PILOT_ALL_CARTESIAN')
    out={'position':POS,'physical_shared_dimension':PHYS_N,'zero_correlation_pairs_available':4003,
         'pilot_pairs':K,'synthetic_eight_term_regression':syn,'pair_marginal_crosschecks':2*K,
         'support_relation_histogram':dict(sorted(relhist.items())),'joint_image_size_histogram':dict(sorted(hist.items())),
         'strict_subcartesian_pairs':strict,'results':outrows,
         'relation_digest_sha256':hashlib.sha256(('\n'.join(digest)+'\n').encode()).hexdigest(),
         'inner_product_cache_entries':inner_cache_entries,'cached_support_intersections':len(ic),
         'cached_character_moments':len(mc),'decision':decision}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_M4_ZERO_CORRELATION_SUPPORT_PILOT')
    print('scope=exact eight-term joint-image census for 12 deterministic zero-correlation m4-m4 pairs stratified by projection-support geometry')
    print('important=this is a pilot sample, not an exhaustive theorem over all 4003 zero-correlation m4-m4 pairs')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
