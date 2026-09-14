#!/usr/bin/env python3
import hashlib, io, json, math, os, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O
import probe_v26_q138_c916_e0_first_dyadic_m4_m4_nonzero_correlation_joint_images as J

P=O.P
PHYS_N=O.PHYS_N
SHARD_INDEX=int(os.environ['C916_SHARD_INDEX'])
SHARD_TOTAL=int(os.environ['C916_SHARD_TOTAL'])
M4_PATH=Path(os.environ.get('C916_M4_AUTHORITY','authorities/m4/c916_e0_first_dyadic_four_separator_complete_authority.json'))
SUBSET_PATH=Path(os.environ.get('C916_SUBSET_AUTHORITY','authorities/subset/c916_e0_first_dyadic_m4_subset_pair_relation_authority.json'))
EQUAL_PATH=Path(os.environ.get('C916_EQUAL_AUTHORITY','authorities/equal/c916_e0_first_dyadic_m4_equal_pair_relation_authority.json'))
EXPECTED_ZC_DIGEST='7ce0219e86206aeac622bd423b1341cb47f8681564f19319c96823fcb4d4fab1'
EXPECTED_SUBSET_DIGEST='7910db1e1f649be99503988e77fc3092908572416e4535ac7632cc515b68bc0d'
EXPECTED_EQUAL_DIGEST='8318ee76821c7ccaa3f83aa292cc354abb83b1602ce3ecf1025cfcf3b0ea2448'
EXPECTED_REMAINING=1125

def pair_key(r):
    return tuple(sorted((int(r['left_group_id']),int(r['right_group_id']))))

def relation_mask(counts,lvals,rvals):
    z=0
    for i,a in enumerate(lvals):
        for j,b in enumerate(rvals):
            if (a,b) in counts:
                z|=1<<(i*len(rvals)+j)
    return z

def analyze():
    assert SHARD_TOTAL>=1 and 0<=SHARD_INDEX<SHARD_TOTAL
    m4=json.loads(M4_PATH.read_text())
    subset=json.loads(SUBSET_PATH.read_text())
    equal=json.loads(EQUAL_PATH.read_text())
    assert m4['zero_cross_pair_digest_sha256']==EXPECTED_ZC_DIGEST
    assert subset['relation_digest_sha256']==EXPECTED_SUBSET_DIGEST
    assert equal['relation_digest_sha256']==EXPECTED_EQUAL_DIGEST
    zc={tuple(sorted(map(int,e))) for e in m4['zero_cross_pairs']}
    sk={pair_key(r) for r in subset['relations']}
    ek={pair_key(r) for r in equal['relations']}
    cand=sorted(zc-sk-ek)
    assert len(zc)==1318 and len(zc&sk)==183 and len(zc&ek)==10
    assert len(cand)==EXPECTED_REMAINING
    selected=cand[SHARD_INDEX::SHARD_TOTAL]
    assert selected

    with redirect_stdout(io.StringIO()):
        census,groups=O.build_authority()
    ic={}
    mc={}
    rows=[]
    sizehist=Counter()
    shapehist=Counter()
    supporthist=Counter()
    maskhist=Counter()
    axis_complete=0
    reflection_independent=0
    dig=[]

    for idx,(u,v) in enumerate(selected,1):
        counts,lm,rm=J.pair_census(groups[u],groups[v],PHYS_N,ic,mc)
        assert lm==census[u]['counts'] and rm==census[v]['counts']
        lvals=tuple(sorted(lm))
        rvals=tuple(sorted(rm))
        assert 0 in lvals and 0 in rvals
        assert all(a==0 or b==0 for a,b in counts), (u,v)
        li=lvals.index(0)
        ri=rvals.index(0)
        mask=relation_mask(counts,lvals,rvals)
        nr=len(lvals)
        nc=len(rvals)
        axis={(a,b) for a in lvals for b in rvals if a==0 or b==0}
        ac=(set(counts)==axis)
        axis_complete+=int(ac)
        rel,inter=P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
        dim=(len(inter[2]) if inter is not None else None)

        indep=True
        for i in range(nr):
            for j in range(nc):
                bit=(mask>>(i*nc+j))&1
                if bit!=((mask>>((nr-1-i)*nc+j))&1) or bit!=((mask>>(i*nc+(nc-1-j)))&1):
                    indep=False
                    break
            if not indep:
                break
        reflection_independent+=int(indep)

        size=len(counts)
        shape=f'{nr}x{nc}'
        shapehist[shape]+=1
        supporthist[rel]+=1
        sizehist[size]+=1
        maskhist[f'{mask:x}']+=1
        dig.append(f'{u}|{v}|{shape}|{mask:x}')
        rows.append({
            'left_group_id':u,'right_group_id':v,
            'left_image_size':nr,'right_image_size':nc,
            'left_zero_index':li,'right_zero_index':ri,
            'cartesian_image_size':nr*nc,'joint_image_size':size,
            'relation_mask_hex':f'{mask:x}',
            'axis_complete':ac,
            'independent_sign_reflection_invariant':indep,
            'support_relation':rel,
            'intersection_dimension':dim,
        })
        if idx%30==0 or idx==len(selected):
            print('progress',idx,'/',len(selected),'axis_complete',axis_complete,flush=True)

    out={
        'position':O.POS,'physical_shared_dimension':PHYS_N,
        'source_complete_zero_cross_pairs':1318,
        'subset_zero_cross_pairs_already_frozen':183,
        'equal_zero_cross_pairs_already_frozen':10,
        'remaining_zero_cross_value_pairs':EXPECTED_REMAINING,
        'shard_index':SHARD_INDEX,'shard_total':SHARD_TOTAL,'shard_pairs':len(selected),
        'axis_complete_pairs':axis_complete,
        'non_axis_complete_pairs':len(selected)-axis_complete,
        'independent_sign_reflection_invariant_pairs':reflection_independent,
        'shape_histogram':dict(sorted(shapehist.items())),
        'support_relation_histogram':dict(sorted(supporthist.items())),
        'joint_image_size_histogram':dict(sorted(sizehist.items())),
        'relation_mask_histogram':dict(sorted(maskhist.items())),
        'cached_support_intersections':len(ic),'cached_character_moments':len(mc),
        'rows':rows,
        'shard_digest_sha256':hashlib.sha256(('\n'.join(dig)+'\n').encode()).hexdigest(),
        'decision':'M4_REMAINING_ZERO_CROSS_VALUE_RELATION_SHARD_EXACT'
    }
    outdir=Path('artifacts/shards')
    outdir.mkdir(parents=True,exist_ok=True)
    path=outdir/f'c916_m4_remaining_zero_cross_value_shard{SHARD_INDEX}of{SHARD_TOTAL}.json'
    path.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print('result',json.dumps({k:v for k,v in out.items() if k!='rows'},sort_keys=True),flush=True)
    print('artifact_path',path,flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_REMAINING_ZERO_CROSS_VALUE_SHARD')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':
    analyze()
