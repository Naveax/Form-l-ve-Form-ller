#!/usr/bin/env python3
import hashlib, io, json, math, os, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O
import probe_v26_q138_c916_e0_first_dyadic_m4_m4_nonzero_correlation_joint_images as J

P=O.P; PHYS_N=O.PHYS_N
DIM=int(os.environ['C916_DIM']); SHARD_INDEX=int(os.environ['C916_SHARD_INDEX']); SHARD_TOTAL=int(os.environ['C916_SHARD_TOTAL'])
M4_PATH=Path(os.environ.get('C916_M4_AUTHORITY','authorities/m4/c916_e0_first_dyadic_four_separator_complete_authority.json'))
EXPECTED_ZC_DIGEST='7ce0219e86206aeac622bd423b1341cb47f8681564f19319c96823fcb4d4fab1'
EXPECTED_TOTAL_BY_DIM={139:427,140:986,141:558}

def relation_mask(counts,lvals,rvals):
    z=0; bit=0
    for a in lvals:
        for b in rvals:
            if (a,b) in counts:z|=1<<bit
            bit+=1
    return z

def analyze():
    assert DIM in EXPECTED_TOTAL_BY_DIM and 0<=SHARD_INDEX<SHARD_TOTAL
    m4=json.loads(M4_PATH.read_text()); assert m4['zero_cross_pair_digest_sha256']==EXPECTED_ZC_DIGEST
    zc={tuple(sorted(map(int,e))) for e in m4['zero_cross_pairs']}
    with redirect_stdout(io.StringIO()): census,groups=O.build_authority()
    gids=tuple(g for g in range(250) if census[g]['multiplicity']==4); cand=[]
    for i,u in enumerate(gids):
        for v in gids[i+1:]:
            if (u,v) in zc or census[u]['image_size']!=7 or census[v]['image_size']!=7: continue
            rel,inter=P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
            if rel=='overlap_incomparable' and inter is not None and len(inter[2])==DIM: cand.append((u,v))
    assert len(cand)==EXPECTED_TOTAL_BY_DIM[DIM], (DIM,len(cand))
    selected=cand[SHARD_INDEX::SHARD_TOTAL]; assert selected
    ic={}; mc={}; rows=[]; strict=0; sizehist=Counter(); maskhist=Counter(); gainhist=Counter(); dig=[]
    for idx,(u,v) in enumerate(selected,1):
        counts,lm,rm=J.pair_census(groups[u],groups[v],PHYS_N,ic,mc); assert lm==census[u]['counts'] and rm==census[v]['counts']
        lvals=tuple(sorted(lm)); rvals=tuple(sorted(rm)); assert len(lvals)==len(rvals)==7
        size=len(counts); mask=relation_mask(counts,lvals,rvals); isstrict=size<49; strict+=int(isstrict); gain=math.log2(49)-math.log2(size)
        sizehist[size]+=1; maskhist[f'{mask:x}']+=1; gainhist[round(gain,12)]+=1; dig.append(f'{u}|{v}|7x7|{mask:x}')
        rows.append({'left_group_id':u,'right_group_id':v,'intersection_dimension':DIM,'left_image_size':7,'right_image_size':7,'cartesian_image_size':49,'joint_image_size':size,'strict_subcartesian':isstrict,'exact_cardinality_gain_log2':gain,'relation_mask_hex':f'{mask:x}'})
        if idx%40==0 or idx==len(selected): print('progress',idx,'/',len(selected),'strict',strict,flush=True)
    out={'position':O.POS,'physical_shared_dimension':PHYS_N,'intersection_dimension':DIM,'dimension_total_pairs':len(cand),'shard_index':SHARD_INDEX,'shard_total':SHARD_TOTAL,'shard_pairs':len(selected),'strict_subcartesian_pairs':strict,'full_cartesian_pairs':len(selected)-strict,'joint_image_size_histogram':dict(sorted(sizehist.items())),'relation_mask_histogram':dict(sorted(maskhist.items())),'gain_histogram_rounded_12':dict(sorted(gainhist.items())),'rows':rows,'shard_digest_sha256':hashlib.sha256(('\n'.join(dig)+'\n').encode()).hexdigest(),'cached_support_intersections':len(ic),'cached_character_moments':len(mc),'decision':'M4_OVERLAP_NONZERO_CROSS_7X7_SHARD_EXACT'}
    outdir=Path('artifacts/shards'); outdir.mkdir(parents=True,exist_ok=True); path=outdir/f'c916_m4_overlap_7x7_dim{DIM}_shard{SHARD_INDEX}of{SHARD_TOTAL}.json'; path.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print('result',json.dumps({k:v for k,v in out.items() if k!='rows'},sort_keys=True),flush=True); print('artifact_path',path,flush=True); print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_OVERLAP_7X7_SHARD'); print('ALPHA_PASS=0'); return out

if __name__=='__main__': analyze()
