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
EXPECTED_LEFT=312
EXPECTED_RIGHT=513
EXPECTED_TOTAL=825
assert PHYS_N==149

def relation_mask(counts,lvals,rvals):
    mask=bit=0
    for a in lvals:
        for b in rvals:
            if (a,b) in counts: mask |= 1<<bit
            bit += 1
    return mask

def select_subset_pairs(census,groups):
    m4s=tuple(g for g in range(250) if census[g]['multiplicity']==4)
    rows=[]; relhist=Counter(); inner_cache={}; nonzero=[]
    for i,u in enumerate(m4s):
        for v in m4s[i+1:]:
            rel,inter=P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
            if rel not in ('left_subset_right','right_subset_left'):
                continue
            assert inter is not None
            inner=D.group_inner(groups[u],groups[v],inner_cache)
            if inner: nonzero.append((u,v,inner))
            rows.append((u,v,rel,len(inter[2])))
            relhist[rel]+=1
    assert relhist==Counter({'left_subset_right':EXPECTED_LEFT,'right_subset_left':EXPECTED_RIGHT}),relhist
    assert len(rows)==EXPECTED_TOTAL
    assert not nonzero,nonzero
    return tuple(rows),len(inner_cache)

def analyze():
    syn=J.synthetic()
    with redirect_stdout(io.StringIO()):
        census,groups=O.build_authority()
    pairs,inner_cache_entries=select_subset_pairs(census,groups)
    ic={}; mc={}; strict=0; digest=[]
    size_hist=Counter(); shape_hist=Counter(); mask_hist=Counter(); direction_size=Counter(); saving_hist=Counter()
    strongest=[]; full=0
    for idx,(u,v,rel,dim) in enumerate(pairs,1):
        counts,lm,rm=J.pair_census(groups[u],groups[v],PHYS_N,ic,mc)
        assert lm==census[u]['counts'] and rm==census[v]['counts']
        lvals=tuple(sorted(lm)); rvals=tuple(sorted(rm)); cart=len(lvals)*len(rvals); size=len(counts)
        mask=relation_mask(counts,lvals,rvals); shape=f'{len(lvals)}x{len(rvals)}'
        gain=math.log2(cart)-math.log2(size)
        saving=(len(lvals)-1).bit_length()+(len(rvals)-1).bit_length()-(size-1).bit_length()
        digest.append(f'{u}|{v}|{rel}|{dim}|{shape}|{mask:x}')
        size_hist[size]+=1; shape_hist[shape]+=1; mask_hist[(shape,f'{mask:x}')]+=1
        direction_size[(rel,size)]+=1; saving_hist[saving]+=1
        if size<cart: strict+=1
        else: full+=1
        strongest.append((gain,u,v,rel,dim,shape,size,cart,f'{mask:x}'))
        if idx%25==0 or idx==len(pairs):
            print('progress',idx,'/',len(pairs),'strict',strict,'masks',len(mask_hist),flush=True)
    strongest.sort(key=lambda r:(-r[0],r[1],r[2]))
    mask_top=sorted(mask_hist.items(),key=lambda kv:(-kv[1],kv[0]))[:60]
    decision=('M4_M4_SUBSET_SUPPORT_FULL_CENSUS_ALL_SUBCARTESIAN' if strict==len(pairs) else
              'M4_M4_SUBSET_SUPPORT_FULL_CENSUS_MIXED' if strict else
              'M4_M4_SUBSET_SUPPORT_FULL_CENSUS_ALL_CARTESIAN')
    out={'position':POS,'physical_shared_dimension':PHYS_N,'multiplicity4_outputs':90,
         'subset_support_pairs':len(pairs),'left_subset_right_pairs':EXPECTED_LEFT,
         'right_subset_left_pairs':EXPECTED_RIGHT,'strict_subcartesian_pairs':strict,
         'full_cartesian_pairs':full,'pair_marginal_crosschecks':2*len(pairs),
         'synthetic_eight_term_regression':syn,'all_subset_pairs_zero_inner_product':True,
         'shape_histogram':dict(sorted(shape_hist.items())),
         'joint_image_size_histogram':dict(sorted(size_hist.items())),
         'integer_bit_saving_histogram':dict(sorted(saving_hist.items())),
         'direction_joint_size_histogram':[
             {'support_relation':k[0],'joint_image_size':k[1],'count':v}
             for k,v in sorted(direction_size.items())],
         'distinct_relation_masks':len(mask_hist),
         'top_relation_masks':[{'shape':k[0],'mask_hex':k[1],'count':v} for k,v in mask_top],
         'strongest_40':[{'left_group_id':u,'right_group_id':v,'support_relation':rel,
             'intersection_dimension':dim,'shape':shape,'joint_image_size':size,
             'cartesian_image_size':cart,'gain_log2':gain,'relation_mask_hex':mask}
             for gain,u,v,rel,dim,shape,size,cart,mask in strongest[:40]],
         'relation_digest_sha256':hashlib.sha256(('\n'.join(digest)+'\n').encode()).hexdigest(),
         'inner_product_cache_entries':inner_cache_entries,
         'cached_support_intersections':len(ic),'cached_character_moments':len(mc),
         'decision':decision}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_M4_SUBSET_SUPPORT_FULL_CENSUS')
    print('scope=exact eight-term joint-image census for all 825 multiplicity-4 projection-support subset pairs')
    print('important=all 825 subset pairs are exactly zero-correlation; nonlinear joint-image structure is measured directly rather than inferred from correlation')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
