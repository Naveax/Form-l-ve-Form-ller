#!/usr/bin/env python3
import hashlib, io, json, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_m4_m4_nonzero_correlation_joint_images as J
import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O

P=O.P; D=O.D; PHYS_N=O.PHYS_N; POS=O.POS
EXPECTED_LEFT=312
EXPECTED_RIGHT=513
EXPECTED_TOTAL=825
EXPECTED_STRICT=820
EXPECTED_FULL=5
EXPECTED_DIGEST='7910db1e1f649be99503988e77fc3092908572416e4535ac7632cc515b68bc0d'
assert PHYS_N==149

def relation_mask(counts,lvals,rvals):
    mask=bit=0
    for a in lvals:
        for b in rvals:
            if (a,b) in counts:
                mask |= 1<<bit
            bit += 1
    return mask

def select_pairs(census,groups):
    m4s=tuple(g for g in range(250) if census[g]['multiplicity']==4)
    rows=[]; relhist=Counter(); inner_cache={}
    for i,u in enumerate(m4s):
        for v in m4s[i+1:]:
            rel,inter=P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
            if rel not in ('left_subset_right','right_subset_left'):
                continue
            assert inter is not None
            assert D.group_inner(groups[u],groups[v],inner_cache)==0
            rows.append((u,v,rel,len(inter[2])))
            relhist[rel]+=1
    assert relhist==Counter({'left_subset_right':EXPECTED_LEFT,'right_subset_left':EXPECTED_RIGHT})
    assert len(rows)==EXPECTED_TOTAL
    return tuple(rows),len(inner_cache)

def analyze():
    syn=J.synthetic()
    with redirect_stdout(io.StringIO()):
        census,groups=O.build_authority()
    pairs,inner_cache_entries=select_pairs(census,groups)
    ic={}; mc={}; strict=full=0; digest=[]; authority=[]; shape_hist=Counter(); size_hist=Counter()
    for idx,(u,v,rel,dim) in enumerate(pairs,1):
        counts,lm,rm=J.pair_census(groups[u],groups[v],PHYS_N,ic,mc)
        assert lm==census[u]['counts'] and rm==census[v]['counts']
        lvals=tuple(sorted(lm)); rvals=tuple(sorted(rm)); rows=len(lvals); cols=len(rvals)
        size=len(counts); cart=rows*cols; mask=relation_mask(counts,lvals,rvals)
        shape=f'{rows}x{cols}'
        digest.append(f'{u}|{v}|{rel}|{dim}|{shape}|{mask:x}')
        shape_hist[shape]+=1; size_hist[size]+=1
        strict += int(size<cart); full += int(size==cart)
        authority.append({'left_group_id':u,'right_group_id':v,'support_relation':rel,
                          'intersection_dimension':dim,'rows':rows,'cols':cols,
                          'joint_image_size':size,'cartesian_image_size':cart,
                          'relation_mask_hex':f'{mask:x}','strict':bool(size<cart)})
        if idx%25==0 or idx==len(pairs):
            print('progress',idx,'/',len(pairs),'strict',strict,flush=True)
    dg=hashlib.sha256(('\n'.join(digest)+'\n').encode()).hexdigest()
    assert dg==EXPECTED_DIGEST
    assert strict==EXPECTED_STRICT and full==EXPECTED_FULL
    artifact={'position':POS,'physical_shared_dimension':PHYS_N,'m4_outputs':90,
              'subset_support_pairs':len(pairs),'left_subset_right_pairs':EXPECTED_LEFT,
              'right_subset_left_pairs':EXPECTED_RIGHT,'strict_subcartesian_pairs':strict,
              'full_cartesian_pairs':full,'relation_digest_sha256':dg,
              'relations':authority}
    ap=Path('artifacts/c916_e0_first_dyadic_m4_subset_pair_relation_authority.json')
    ap.parent.mkdir(parents=True,exist_ok=True)
    ap.write_text(json.dumps(artifact,sort_keys=True,separators=(',',':'))+'\n')
    out={'position':POS,'physical_shared_dimension':PHYS_N,'subset_support_pairs':len(pairs),
         'strict_subcartesian_pairs':strict,'full_cartesian_pairs':full,
         'shape_histogram':dict(sorted(shape_hist.items())),
         'joint_image_size_histogram':dict(sorted(size_hist.items())),
         'relation_digest_sha256':dg,'authority_artifact_path':str(ap),
         'inner_product_cache_entries':inner_cache_entries,
         'cached_support_intersections':len(ic),'cached_character_moments':len(mc),
         'synthetic_eight_term_regression':syn,
         'decision':'M4_SUBSET_PAIR_RELATION_AUTHORITY_FROZEN'}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_SUBSET_PAIR_RELATION_AUTHORITY')
    print('scope=frozen exact relation masks for all 825 m4 projection-support subset pairs')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
