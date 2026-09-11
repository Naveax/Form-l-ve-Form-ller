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
EXPECTED_PAIRS=55
assert PHYS_N==149

def relation_mask(counts,lvals,rvals):
    mask=bit=0
    for a in lvals:
        for b in rvals:
            if (a,b) in counts:
                mask |= 1<<bit
            bit += 1
    return mask

def select_equal_pairs(census,groups):
    m4s=tuple(g for g in range(250) if census[g]['multiplicity']==4)
    inner_cache={}; rows=[]
    for i,u in enumerate(m4s):
        for v in m4s[i+1:]:
            rel,inter=P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
            if rel!='equal':
                continue
            assert inter is not None
            inner=D.group_inner(groups[u],groups[v],inner_cache)
            assert inner==0, (u,v,inner)
            rows.append((u,v,len(inter[2])))
    assert len(rows)==EXPECTED_PAIRS, len(rows)
    return tuple(rows),len(inner_cache)

def analyze():
    syn=J.synthetic()
    with redirect_stdout(io.StringIO()):
        census,groups=O.build_authority()
    pairs,inner_cache_entries=select_equal_pairs(census,groups)
    ic,mc={},{}
    rows=[]; digest=[]; strict=0; mask_hist=Counter(); size_hist=Counter(); gain_hist=Counter(); shape_hist=Counter()
    for idx,(u,v,dim) in enumerate(pairs,1):
        counts,lm,rm=J.pair_census(groups[u],groups[v],PHYS_N,ic,mc)
        assert lm==census[u]['counts'] and rm==census[v]['counts']
        lvals=tuple(sorted(lm)); rvals=tuple(sorted(rm))
        cart=len(lvals)*len(rvals); size=len(counts)
        mask=relation_mask(counts,lvals,rvals)
        shape=f'{len(lvals)}x{len(rvals)}'
        if size<cart:
            strict+=1
        gain=math.log2(cart)-math.log2(size)
        row={'left_group_id':u,'right_group_id':v,'intersection_dimension':dim,
             'left_image_size':len(lvals),'right_image_size':len(rvals),
             'cartesian_image_size':cart,'joint_image_size':size,
             'missing_cartesian_states':cart-size,
             'integer_bit_saving':(len(lvals)-1).bit_length()+(len(rvals)-1).bit_length()-(size-1).bit_length(),
             'exact_cardinality_gain_log2':gain,'relation_mask_hex':f'{mask:x}'}
        rows.append(row)
        digest.append(f'{u}|{v}|{shape}|{mask:x}')
        mask_hist[(shape,f'{mask:x}')]+=1
        size_hist[size]+=1
        shape_hist[shape]+=1
        gain_hist[round(gain,12)]+=1
        if idx%10==0 or idx==len(pairs):
            print('progress',idx,'/',len(pairs),'strict',strict,flush=True)
    decision=('M4_M4_EQUAL_SUPPORT_FULL_CENSUS_ALL_SUBCARTESIAN' if strict==len(pairs) else
              'M4_M4_EQUAL_SUPPORT_FULL_CENSUS_MIXED' if strict else
              'M4_M4_EQUAL_SUPPORT_FULL_CENSUS_ALL_CARTESIAN')
    out={'position':POS,'physical_shared_dimension':PHYS_N,'multiplicity4_outputs':90,
         'equal_support_pairs':len(pairs),'strict_subcartesian_pairs':strict,
         'pair_marginal_crosschecks':2*len(pairs),'synthetic_eight_term_regression':syn,
         'shape_histogram':dict(sorted(shape_hist.items())),
         'joint_image_size_histogram':dict(sorted(size_hist.items())),
         'relation_mask_histogram':[{'shape':k[0],'mask_hex':k[1],'count':v} for k,v in sorted(mask_hist.items())],
         'gain_histogram_rounded_12':[{'gain_log2':k,'count':v} for k,v in sorted(gain_hist.items())],
         'results':rows,
         'relation_digest_sha256':hashlib.sha256(('\n'.join(digest)+'\n').encode()).hexdigest(),
         'inner_product_cache_entries':inner_cache_entries,
         'cached_support_intersections':len(ic),'cached_character_moments':len(mc),
         'decision':decision}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_M4_EQUAL_SUPPORT_FULL_CENSUS')
    print('scope=exact eight-term joint-image census for all 55 equal-projection-support multiplicity-4 pairs')
    print('important=all selected pairs have exact zero full-domain inner product; correlation is not used as an independence claim')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':
    analyze()
