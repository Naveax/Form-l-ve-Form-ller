#!/usr/bin/env python3
import glob, hashlib, json
from collections import Counter
from pathlib import Path

EXPECTED_TOTAL=1125
EXPECTED_SHARDS=8

def analyze():
    files=sorted(glob.glob('artifacts/shards/*.json'))
    assert len(files)==EXPECTED_SHARDS, files
    rows=[]
    shard_meta=[]
    for p in files:
        d=json.loads(Path(p).read_text())
        rows.extend(d['rows'])
        shard_meta.append({k:d[k] for k in ('shard_index','shard_total','shard_pairs','shard_digest_sha256')})
    rows=sorted(rows,key=lambda r:(int(r['left_group_id']),int(r['right_group_id'])))
    keys=[(int(r['left_group_id']),int(r['right_group_id'])) for r in rows]
    assert len(keys)==len(set(keys))==EXPECTED_TOTAL
    assert all(bool(r['axis_complete']) or int(r['joint_image_size']) < int(r['left_image_size'])+int(r['right_image_size'])-1 for r in rows)
    assert all(int(r['joint_image_size']) <= int(r['left_image_size'])+int(r['right_image_size'])-1 for r in rows)

    shape=Counter(f"{int(r['left_image_size'])}x{int(r['right_image_size'])}" for r in rows)
    support=Counter(r['support_relation'] for r in rows)
    sizehist=Counter(int(r['joint_image_size']) for r in rows)
    maskhist=Counter(r['relation_mask_hex'] for r in rows)
    axis=sum(bool(r['axis_complete']) for r in rows)
    refl=sum(bool(r['independent_sign_reflection_invariant']) for r in rows)
    dig=''.join(f"{r['left_group_id']}|{r['right_group_id']}|{r['left_image_size']}x{r['right_image_size']}|{r['relation_mask_hex']}\n" for r in rows)
    out={
      'position':'C','physical_shared_dimension':149,
      'remaining_zero_cross_value_pairs':EXPECTED_TOTAL,
      'axis_complete_pairs':axis,'non_axis_complete_pairs':EXPECTED_TOTAL-axis,
      'independent_sign_reflection_invariant_pairs':refl,
      'non_independent_sign_reflection_pairs':EXPECTED_TOTAL-refl,
      'shape_histogram':dict(sorted(shape.items())),
      'support_relation_histogram':dict(sorted(support.items())),
      'joint_image_size_histogram':dict(sorted(sizehist.items())),
      'relation_mask_histogram':[{'mask_hex':k,'count':v} for k,v in sorted(maskhist.items())],
      'relation_digest_sha256':hashlib.sha256(dig.encode()).hexdigest(),
      'shards':shard_meta,'rows':rows,
      'decision':'M4_REMAINING_ZERO_CROSS_VALUE_RELATIONS_FULL_AUTHORITY'
    }
    path=Path('artifacts/c916_e0_first_dyadic_m4_remaining_zero_cross_value_relation_authority.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print('result',json.dumps({k:v for k,v in out.items() if k!='rows'},sort_keys=True),flush=True)
    print('authority_artifact_path',path,flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_REMAINING_ZERO_CROSS_VALUE_RELATIONS')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':
    analyze()
