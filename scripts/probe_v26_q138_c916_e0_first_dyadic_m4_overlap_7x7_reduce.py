#!/usr/bin/env python3
import glob,hashlib,json,math
from collections import Counter
from pathlib import Path

EXPECTED_DIM={139:427,140:986,141:558}

def analyze():
    files=sorted(glob.glob('artifacts/shards/*.json')); assert len(files)==8, files
    rows=[]; shard_meta=[]
    for p in files:
        d=json.loads(Path(p).read_text()); rows.extend(d['rows']); shard_meta.append({k:d[k] for k in ('intersection_dimension','shard_index','shard_total','shard_pairs','shard_digest_sha256')})
    rows=sorted(rows,key=lambda r:(int(r['left_group_id']),int(r['right_group_id'])))
    keys=[(int(r['left_group_id']),int(r['right_group_id'])) for r in rows]; assert len(keys)==len(set(keys))==1971
    dh=Counter(int(r['intersection_dimension']) for r in rows); assert dict(sorted(dh.items()))==EXPECTED_DIM
    assert all(int(r['left_image_size'])==7 and int(r['right_image_size'])==7 for r in rows)
    strict=sum(bool(r['strict_subcartesian']) for r in rows); sizehist=Counter(int(r['joint_image_size']) for r in rows); maskhist=Counter(r['relation_mask_hex'] for r in rows); gainhist=Counter(round(float(r['exact_cardinality_gain_log2']),12) for r in rows)
    dig=''.join(f"{r['left_group_id']}|{r['right_group_id']}|7x7|{r['relation_mask_hex']}\n" for r in rows)
    out={'position':'C','physical_shared_dimension':149,'overlap_nonzero_cross_7x7_pairs':1971,'intersection_dimension_histogram':dict(sorted(dh.items())),'strict_subcartesian_pairs':strict,'full_cartesian_pairs':1971-strict,'joint_image_size_histogram':dict(sorted(sizehist.items())),'relation_mask_histogram':[{'mask_hex':k,'count':v} for k,v in sorted(maskhist.items())],'gain_histogram_rounded_12':[{'gain_log2':k,'count':v} for k,v in sorted(gainhist.items())],'relation_digest_sha256':hashlib.sha256(dig.encode()).hexdigest(),'shards':shard_meta,'rows':rows,'decision':'M4_OVERLAP_NONZERO_CROSS_7X7_FULL_AUTHORITY'}
    path=Path('artifacts/c916_e0_first_dyadic_m4_overlap_nonzero_cross_7x7_full_authority.json'); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print('result',json.dumps({k:v for k,v in out.items() if k!='rows'},sort_keys=True),flush=True); print('authority_artifact_path',path,flush=True); print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_OVERLAP_7X7_FULL_AUTHORITY'); print('ALPHA_PASS=0'); return out

if __name__=='__main__': analyze()
