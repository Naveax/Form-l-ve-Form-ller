#!/usr/bin/env python3
import hashlib, json, os
from collections import Counter
from pathlib import Path

FULL7=Path(os.environ.get('C916_OVERLAP_7X7_AUTHORITY','authorities/full7/c916_e0_first_dyadic_m4_overlap_nonzero_cross_7x7_full_authority.json'))
RARE=Path(os.environ.get('C916_OVERLAP_RARE_AUTHORITY','authorities/rare/c916_e0_first_dyadic_m4_overlap_nonzero_cross_rare_shapes.json'))
SAMPLE=Path(os.environ.get('C916_OVERLAP_SAMPLE_AUTHORITY','authorities/sample/c916_e0_first_dyadic_m4_overlap_nonzero_cross_stratified_sample.json'))
PHYS_N=149


def load(p): return json.loads(p.read_text())

def bit(mask,cols,i,j): return (mask>>(i*cols+j))&1

def reflection_orbits(n):
    assert n in (7,9)
    return tuple(tuple(sorted({i,n-1-i})) for i in range((n+1)//2))

def verify_and_quotient(r):
    nr=int(r.get('left_image_size',r.get('rows'))); nc=int(r.get('right_image_size',r.get('cols')))
    assert nr in (7,9) and nc in (7,9)
    mask=int(r['relation_mask_hex'],16)
    for i in range(nr):
        for j in range(nc):
            x=bit(mask,nc,i,j)
            assert x==bit(mask,nc,nr-1-i,j)
            assert x==bit(mask,nc,i,nc-1-j)
            assert x==bit(mask,nc,nr-1-i,nc-1-j)
    ro,co=reflection_orbits(nr),reflection_orbits(nc)
    qm=0
    for a,oi in enumerate(ro):
        for b,oj in enumerate(co):
            vals={bit(mask,nc,i,j) for i in oi for j in oj}
            assert len(vals)==1
            if next(iter(vals)): qm|=1<<(a*len(co)+b)
    return nr,nc,ro,co,qm

def canonical_original_digest(rows):
    text=''.join(f"{int(r['left_group_id'])}|{int(r['right_group_id'])}|{int(r.get('left_image_size',r.get('rows')))}x{int(r.get('right_image_size',r.get('cols')))}|{r['relation_mask_hex']}\n" for r in rows)
    return hashlib.sha256(text.encode()).hexdigest()

def canonical_quotient_digest(rows):
    text=''.join(f"{r['left_group_id']}|{r['right_group_id']}|{r['quotient_rows']}x{r['quotient_cols']}|{r['quotient_mask_hex']}\n" for r in rows)
    return hashlib.sha256(text.encode()).hexdigest()

def analyze():
    f7,rare,sample=load(FULL7),load(RARE),load(SAMPLE)
    assert int(f7['overlap_nonzero_cross_7x7_pairs'])==1971
    assert int(rare['rare_shape_overlap_nonzero_cross_pairs'])==29
    allrows=list(f7['rows'])+list(rare['rows'])
    allrows=sorted(allrows,key=lambda r:(int(r['left_group_id']),int(r['right_group_id'])))
    keys=[(int(r['left_group_id']),int(r['right_group_id'])) for r in allrows]
    assert len(keys)==len(set(keys))==2000

    qrows=[]; qhist=Counter(); shape=Counter(); strict=0
    for r in allrows:
        nr,nc,ro,co,qm=verify_and_quotient(r)
        shape[f'{nr}x{nc}']+=1
        strict+=int(bool(r.get('strict_subcartesian',r.get('strict',False))))
        qhist[(len(ro),len(co),qm)]+=1
        qrows.append({'left_group_id':int(r['left_group_id']),'right_group_id':int(r['right_group_id']),
                      'left_image_size':nr,'right_image_size':nc,
                      'left_orbit_weights':[len(x) for x in ro],'right_orbit_weights':[len(x) for x in co],
                      'quotient_rows':len(ro),'quotient_cols':len(co),'quotient_mask_hex':f'{qm:x}',
                      'original_relation_mask_hex':r['relation_mask_hex']})

    amap={(int(r['left_group_id']),int(r['right_group_id'])):r for r in allrows}
    sample_checked=0
    for r in sample['rows']:
        k=(int(r['left_group_id']),int(r['right_group_id']))
        assert k in amap and amap[k]['relation_mask_hex']==r['relation_mask_hex']
        sample_checked+=1
    assert sample_checked==64

    odig=canonical_original_digest(allrows); qdig=canonical_quotient_digest(qrows)
    out={'position':'C','physical_shared_dimension':PHYS_N,
         'overlap_nonzero_cross_relations':2000,'full_7x7_relations':1971,'rare_shape_relations':29,
         'shape_histogram':dict(sorted(shape.items())),'strict_subcartesian_relations':strict,
         'full_cartesian_relations':2000-strict,'sample_rows_crosschecked':sample_checked,
         'reflection_orbit_weights':{'7':[2,2,2,1],'9':[2,2,2,2,1]},
         'distinct_quotient_masks':len(qhist),
         'quotient_mask_histogram':[{'shape':f'{a}x{b}','mask_hex':f'{m:x}','count':c} for (a,b,m),c in sorted(qhist.items())],
         'combined_original_relation_digest_sha256':odig,'combined_quotient_relation_digest_sha256':qdig,
         'rows':qrows,
         'decision':'M4_FULL_OVERLAP_VALUE_AUTHORITY_FACTORS_THROUGH_INDEPENDENT_SIGN_REFLECTION_ORBITS'}
    p=Path('artifacts/c916_e0_first_dyadic_m4_full_overlap_sign_reflection_quotient_authority.json'); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print('result',json.dumps({k:v for k,v in out.items() if k!='rows'},sort_keys=True),flush=True)
    print('authority_artifact_path',p,flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_FULL_OVERLAP_SIGN_REFLECTION_QUOTIENT')
    print('theorem=all 2000 exact overlap-incomparable non-zero-cross m4 pair factors are invariant under independent sign reflection of either endpoint label; each factor therefore descends exactly to the weighted 7-to-4 or 9-to-5 orbit quotient')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
