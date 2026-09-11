#!/usr/bin/env python3
import json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_m4_m4_equal_support_full_census as E

EXPECTED_DIGEST='8318ee76821c7ccaa3f83aa292cc354abb83b1602ce3ecf1025cfcf3b0ea2448'
OUT=Path('artifacts/c916_e0_first_dyadic_m4_equal_pair_relation_authority.json')

def analyze():
    src=E.analyze()
    assert src['equal_support_pairs']==55
    assert src['strict_subcartesian_pairs']==52
    assert src['relation_digest_sha256']==EXPECTED_DIGEST
    rows=[]
    for r in src['results']:
        rows.append({
            'left_group_id':int(r['left_group_id']),
            'right_group_id':int(r['right_group_id']),
            'rows':int(r['left_image_size']),
            'cols':int(r['right_image_size']),
            'relation_mask_hex':str(r['relation_mask_hex']),
            'joint_image_size':int(r['joint_image_size']),
            'cartesian_image_size':int(r['cartesian_image_size']),
            'intersection_dimension':int(r['intersection_dimension']),
            'strict':int(r['joint_image_size'])<int(r['cartesian_image_size']),
        })
    assert len(rows)==55 and sum(r['strict'] for r in rows)==52
    authority={
        'position':'C','physical_shared_dimension':149,
        'equal_support_pairs':55,'strict_subcartesian_pairs':52,'full_cartesian_pairs':3,
        'relation_digest_sha256':EXPECTED_DIGEST,
        'relations':rows,
        'decision':'M4_EQUAL_PAIR_RELATION_AUTHORITY_FROZEN',
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(authority,sort_keys=True,separators=(',',':'))+'\n')
    print('result',json.dumps({k:v for k,v in authority.items() if k!='relations'},sort_keys=True),flush=True)
    print('authority_artifact_path',OUT,flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_EQUAL_PAIR_RELATION_AUTHORITY')
    print('ALPHA_PASS=0')
    return authority

if __name__=='__main__': analyze()
