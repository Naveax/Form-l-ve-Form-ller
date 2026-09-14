#!/usr/bin/env python3
import hashlib, json, os
from collections import Counter
from pathlib import Path

FULL7=Path(os.environ.get('C916_OVERLAP_7X7_AUTHORITY','authorities/full7/c916_e0_first_dyadic_m4_overlap_nonzero_cross_7x7_full_authority.json'))
RARE=Path(os.environ.get('C916_OVERLAP_RARE_AUTHORITY','authorities/rare/c916_e0_first_dyadic_m4_overlap_nonzero_cross_rare_shapes.json'))
SAMPLE=Path(os.environ.get('C916_OVERLAP_SAMPLE_AUTHORITY','authorities/sample/c916_e0_first_dyadic_m4_overlap_nonzero_cross_stratified_sample.json'))
PHYS_N=149
EXPECTED_EXCEPTIONS={(141,247,'2450cfe61448'),(160,241,'121418fe30509')}

def load(p): return json.loads(p.read_text())
def bit(mask,cols,i,j): return (mask>>(i*cols+j))&1

def reflection_orbits(n):
    assert n in (7,9)
    return tuple(tuple(sorted({i,n-1-i})) for i in range((n+1)//2))

def independent_quotient(r):
    nr=int(r['left_image_size']); nc=int(r['right_image_size']); mask=int(r['relation_mask_hex'],16)
    ro,co=reflection_orbits(nr),reflection_orbits(nc); qm=0
    for a,oi in enumerate(ro):
        for b,oj in enumerate(co):
            vals={bit(mask,nc,i,j) for i in oi for j in oj}
            if len(vals)!=1: return None
            if next(iter(vals)): qm|=1<<(a*len(co)+b)
    return len(ro),len(co),qm

def simultaneous_reflection_ok(r):
    nr=int(r['left_image_size']); nc=int(r['right_image_size']); mask=int(r['relation_mask_hex'],16)
    return all(bit(mask,nc,i,j)==bit(mask,nc,nr-1-i,nc-1-j) for i in range(nr) for j in range(nc))

def signed_magnitude_masks_7x7(r):
    assert int(r['left_image_size'])==int(r['right_image_size'])==7 and simultaneous_reflection_ok(r)
    mask=int(r['relation_mask_hex'],16); orb=((0,6),(1,5),(2,4),(3,)); same=opp=0
    for a,oa in enumerate(orb):
        for b,ob in enumerate(orb):
            if len(oa)==2 and len(ob)==2:
                sv={bit(mask,7,oa[0],ob[0]),bit(mask,7,oa[1],ob[1])}; ov={bit(mask,7,oa[0],ob[1]),bit(mask,7,oa[1],ob[0])}
                assert len(sv)==len(ov)==1; s=next(iter(sv)); o=next(iter(ov))
            elif len(oa)==2:
                vv={bit(mask,7,oa[0],ob[0]),bit(mask,7,oa[1],ob[0])}; assert len(vv)==1; s=o=next(iter(vv))
            elif len(ob)==2:
                vv={bit(mask,7,oa[0],ob[0]),bit(mask,7,oa[0],ob[1])}; assert len(vv)==1; s=o=next(iter(vv))
            else:
                s=o=bit(mask,7,oa[0],ob[0])
            p=a*4+b
            if s: same|=1<<p
            if o: opp|=1<<p
    return same,opp

def original_digest(rows):
    text=''.join(f"{int(r['left_group_id'])}|{int(r['right_group_id'])}|{int(r['left_image_size'])}x{int(r['right_image_size'])}|{r['relation_mask_hex']}\n" for r in rows)
    return hashlib.sha256(text.encode()).hexdigest()

def reduced_digest(qrows,exceptions):
    text=''.join(f"Q|{r['left_group_id']}|{r['right_group_id']}|{r['quotient_rows']}x{r['quotient_cols']}|{r['quotient_mask_hex']}\n" for r in qrows)
    text+=''.join(f"E|{r['left_group_id']}|{r['right_group_id']}|{r['same_sign_mask_hex']}|{r['opposite_sign_mask_hex']}\n" for r in exceptions)
    return hashlib.sha256(text.encode()).hexdigest()

def analyze():
    f7,rare,sample=load(FULL7),load(RARE),load(SAMPLE)
    assert int(f7['overlap_nonzero_cross_7x7_pairs'])==1971 and int(rare['rare_shape_overlap_nonzero_cross_pairs'])==29
    allrows=sorted(list(f7['rows'])+list(rare['results']),key=lambda r:(int(r['left_group_id']),int(r['right_group_id'])))
    keys=[(int(r['left_group_id']),int(r['right_group_id'])) for r in allrows]; assert len(keys)==len(set(keys))==2000

    qrows=[]; exceptions=[]; qhist=Counter(); shape=Counter(); strict=0
    for r in allrows:
        nr=int(r['left_image_size']); nc=int(r['right_image_size']); shape[f'{nr}x{nc}']+=1; strict+=int(bool(r['strict_subcartesian']))
        q=independent_quotient(r)
        if q is None:
            same,opp=signed_magnitude_masks_7x7(r)
            exceptions.append({'left_group_id':int(r['left_group_id']),'right_group_id':int(r['right_group_id']),
                               'original_relation_mask_hex':r['relation_mask_hex'],'same_sign_mask_hex':f'{same:x}',
                               'opposite_sign_mask_hex':f'{opp:x}','magnitude_shape':'4x4'})
            continue
        qr,qc,qm=q; qhist[(qr,qc,qm)]+=1
        qrows.append({'left_group_id':int(r['left_group_id']),'right_group_id':int(r['right_group_id']),
                      'left_image_size':nr,'right_image_size':nc,
                      'left_orbit_weights':[len(x) for x in reflection_orbits(nr)],'right_orbit_weights':[len(x) for x in reflection_orbits(nc)],
                      'quotient_rows':qr,'quotient_cols':qc,'quotient_mask_hex':f'{qm:x}',
                      'original_relation_mask_hex':r['relation_mask_hex']})

    eset={(r['left_group_id'],r['right_group_id'],r['original_relation_mask_hex']) for r in exceptions}
    assert eset==EXPECTED_EXCEPTIONS and len(qrows)==1998
    exmap={(r['left_group_id'],r['right_group_id']):r for r in exceptions}
    assert exmap[(141,247)]['same_sign_mask_hex']=='f888' and exmap[(141,247)]['opposite_sign_mask_hex']=='fca9'
    assert exmap[(160,241)]['same_sign_mask_hex']=='fca9' and exmap[(160,241)]['opposite_sign_mask_hex']=='f888'

    amap={(int(r['left_group_id']),int(r['right_group_id'])):r for r in allrows}; checked=0
    for r in sample['results']:
        k=(int(r['left_group_id']),int(r['right_group_id'])); assert k in amap and amap[k]['relation_mask_hex']==r['relation_mask_hex']; checked+=1
    assert checked==64

    odig=original_digest(allrows); qdig=reduced_digest(qrows,exceptions)
    out={'position':'C','physical_shared_dimension':PHYS_N,'overlap_nonzero_cross_relations':2000,
         'full_7x7_relations':1971,'rare_shape_relations':29,'shape_histogram':dict(sorted(shape.items())),
         'strict_subcartesian_relations':strict,'full_cartesian_relations':2000-strict,'sample_rows_crosschecked':checked,
         'reflection_orbit_weights':{'7':[2,2,2,1],'9':[2,2,2,2,1]},
         'independent_sign_reflection_quotient_relations':len(qrows),'simultaneous_sign_reflection_only_relations':len(exceptions),
         'distinct_independent_quotient_masks':len(qhist),
         'independent_quotient_mask_histogram':[{'shape':f'{a}x{b}','mask_hex':f'{m:x}','count':c} for (a,b,m),c in sorted(qhist.items())],
         'signed_magnitude_exceptions':exceptions,'combined_original_relation_digest_sha256':odig,
         'combined_reduced_authority_digest_sha256':qdig,'rows':qrows,
         'decision':'M4_FULL_OVERLAP_VALUE_AUTHORITY_HAS_1998_INDEPENDENT_SIGN_QUOTIENT_FACTORS_AND_TWO_SIGNED_EXCEPTIONS'}
    p=Path('artifacts/c916_e0_first_dyadic_m4_full_overlap_sign_reflection_quotient_authority.json'); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print('result',json.dumps({k:v for k,v in out.items() if k!='rows'},sort_keys=True),flush=True)
    print('authority_artifact_path',p,flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_FULL_OVERLAP_SIGN_REFLECTION_QUOTIENT')
    print('theorem=1998 of the 2000 exact overlap non-zero-cross pair factors descend independently to magnitude orbits; the only two exceptions are the known 49-to-19 pairs, which remain invariant under simultaneous sign flip and reduce exactly to 4x4 same-sign/opposite-sign magnitude masks')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
