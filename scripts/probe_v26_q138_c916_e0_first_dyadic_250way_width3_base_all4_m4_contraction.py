#!/usr/bin/env python3
import json, math, os, sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_250way_four_singleton_separator_m4_hypergraph as S

PHYS_N=149
PARENT_GIDS=(1,2,13,14)
EXPECTED_BASE_WIDTH3_COUNT=103580346297435478039507934992782327762124800000
EXPECTED_TREE_BASE_COUNT=3554017933804264224365028336898853306322124800000
EXPECTED_RELATION_DIGEST='ce8af72024a4fdd2bdbe270e994dd21bef056e4a703a0e1a34235e646b18d32c'
EXPECTED_ZERO_CROSS_DIGEST='7ce0219e86206aeac622bd423b1341cb47f8681564f19319c96823fcb4d4fab1'
EXPECTED_M4_VANILLA_COUNT=19495472833965510180005695777791956451721325192874381801
EXPECTED_PR194_LOG2=317.07255079311204

BASE_PATH=Path(os.environ.get('C916_BASE_WIDTH3_AUTHORITY','authorities/base/c916_e0_first_dyadic_base160_width3_separator_authority.json'))
M4_PATH=Path(os.environ.get('C916_M4_AUTHORITY','authorities/m4/c916_e0_first_dyadic_four_separator_complete_authority.json'))

def load_json(path):
    assert path.is_file(),path
    return json.loads(path.read_text())

def marginal_map(rows):
    out={}
    for rec in rows:
        key=tuple(map(int,rec['states']))
        assert len(key)==4 and all(0<=x<4 for x in key)
        c=int(rec['count'])
        assert c>0 and key not in out
        out[key]=c
    return out

def allowed_row(rec,state):
    cols=int(rec['cols'])
    assert cols in (7,9)
    zi=int(rec['zero_index'])
    assert 0<=zi<cols
    mask=int(rec['mask_hex'],16)
    return tuple(bool((mask>>(state*cols+j))&1) for j in range(cols))

def build_extension_table(m4):
    assert int(m4['physical_shared_dimension'])==PHYS_N
    assert tuple(map(int,m4['separator_group_ids']))==PARENT_GIDS
    assert m4['four_parent_relation_digest_sha256']==EXPECTED_RELATION_DIGEST
    assert m4['zero_cross_pair_digest_sha256']==EXPECTED_ZERO_CROSS_DIGEST
    gids=tuple(map(int,m4['m4_group_ids']))
    assert len(gids)==90 and len(set(gids))==90
    local={g:i for i,g in enumerate(gids)}
    rel={}
    for rec in m4['four_parent_relations']:
        pg=int(rec['parent_group_id']); mg=int(rec['m4_group_id'])
        assert pg in PARENT_GIDS and mg in local and (pg,mg) not in rel
        rel[(pg,mg)]=rec
    assert len(rel)==360
    for mg in gids:
        shape={(int(rel[(pg,mg)]['cols']),int(rel[(pg,mg)]['zero_index'])) for pg in PARENT_GIDS}
        assert len(shape)==1
    hedges=[]
    zpairs=m4['zero_cross_pairs']
    assert len(zpairs)==1318
    for u,v in zpairs:
        u=int(u); v=int(v)
        assert u in local and v in local and u!=v
        hedges.append((1<<local[u])|(1<<local[v]))
    triples=m4['projection_minimal_empty_triples']
    assert len(triples)==5
    for a,b,c in triples:
        a=int(a); b=int(b); c=int(c)
        assert len({a,b,c})==3 and all(x in local for x in (a,b,c))
        hedges.append((1<<local[a])|(1<<local[b])|(1<<local[c]))
    ext={}; profile_cache={}; statsum=Counter()
    for a0 in range(4):
      for a1 in range(4):
       for a2 in range(4):
        for a3 in range(4):
            assn=(a0,a1,a2,a3); state=dict(zip(PARENT_GIDS,assn)); zw=[]; ow=[]
            for mg in gids:
                rows=[allowed_row(rel[(pg,mg)],state[pg]) for pg in PARENT_GIDS]
                assert len({len(x) for x in rows})==1
                allowed=tuple(all(row[j] for row in rows) for j in range(len(rows[0])))
                zi=int(rel[(PARENT_GIDS[0],mg)]['zero_index'])
                zw.append(int(allowed[zi]))
                ow.append(sum(int(allowed[j]) for j in range(len(allowed)) if j!=zi))
            prof=(tuple(zw),tuple(ow))
            if prof not in profile_cache:
                z,st=S.weighted_count(90,prof[0],prof[1],tuple(hedges))
                profile_cache[prof]=(z,st)
                statsum.update(st)
            ext[assn]=profile_cache[prof][0]
    return ext,{'unique_weight_profiles':len(profile_cache),'zero_extension_separator_states':sum(v==0 for v in ext.values()),'positive_extension_separator_states':sum(v>0 for v in ext.values()),'min_positive_extension':min(v for v in ext.values() if v>0),'max_extension':max(ext.values()),'memo_states_summed_over_unique_profiles':statsum['memo_states'],'recursive_calls_summed_over_unique_profiles':statsum['recursive_calls']}

def synthetic():
    zw=(0,1); ow=(2,3); edge=((1<<0)|(1<<1),)
    got,_=S.weighted_count(2,zw,ow,edge); brute=0
    for mask in range(4):
        if (mask&3)==3: continue
        w=1
        for i in range(2): w*=ow[i] if (mask>>i)&1 else zw[i]
        brute+=w
    assert got==brute==2
    return got

def analyze():
    syn=synthetic(); base=load_json(BASE_PATH); m4=load_json(M4_PATH)
    assert int(base['physical_shared_dimension'])==PHYS_N
    assert int(base['base_outputs'])==160
    assert int(base['exact_graph_count'])==EXPECTED_BASE_WIDTH3_COUNT
    assert len(base['graph_edges'])==242
    assert tuple(map(int,base['separator_group_ids']))==PARENT_GIDS
    bm=marginal_map(base['separator_positive_marginal'])
    assert sum(bm.values())==EXPECTED_BASE_WIDTH3_COUNT
    tm=marginal_map(m4['separator_positive_marginal'])
    assert sum(tm.values())==EXPECTED_TREE_BASE_COUNT
    ext,est=build_extension_table(m4)
    old_total=sum(tm.get(s,0)*ext[s] for s in ext)
    new_total=sum(bm.get(s,0)*ext[s] for s in ext)
    assert 0<new_total<=old_total
    base_support=set(bm); tree_support=set(tm)
    assert base_support<=tree_support
    killed_tree_mass=sum(c for s,c in tm.items() if ext[s]==0)
    killed_width3_mass=sum(c for s,c in bm.items() if ext[s]==0)
    vanilla_log=math.log2(EXPECTED_M4_VANILLA_COUNT)
    independent_log=math.log2(EXPECTED_BASE_WIDTH3_COUNT)+vanilla_log
    nlog=math.log2(new_total)
    out={'position':'C','physical_shared_dimension':PHYS_N,'synthetic_weighted_recursion':syn,'base_width3_count':EXPECTED_BASE_WIDTH3_COUNT,'base_width3_log2':math.log2(EXPECTED_BASE_WIDTH3_COUNT),'base_graph_edges':242,'base_graph_relation_digest_sha256':base['graph_relation_digest_sha256'],'base_separator_marginal_digest_sha256':base['separator_marginal_digest_sha256'],'tree_separator_positive_entries':len(tm),'width3_separator_positive_entries':len(bm),'separator_states_removed_by_width3':len(tree_support-base_support),'m4_four_parent_relation_digest_sha256':m4['four_parent_relation_digest_sha256'],'m4_zero_cross_pair_digest_sha256':m4['zero_cross_pair_digest_sha256'],'m4_zero_cross_pairs':len(m4['zero_cross_pairs']),'m4_projection_minimal_empty_triples':len(m4['projection_minimal_empty_triples']),'extension_stats':est,'old_tree_authority_contraction_count':old_total,'old_tree_authority_contraction_log2':math.log2(old_total),'width3_base_contraction_count':new_total,'width3_base_contraction_log2':nlog,'width3_base_contraction_state_bits':(new_total-1).bit_length(),'gain_from_width3_base_at_fixed_m4_factor_bits':math.log2(old_total)-nlog,'independent_width3_base_x_m4_log2':independent_log,'separator_coupling_gain_bits':independent_log-nlog,'gap_vs_physical_log2_bits':nlog-PHYS_N,'gain_vs_pr194_width3_log2_bits':EXPECTED_PR194_LOG2-nlog,'killed_tree_assignment_mass':killed_tree_mass,'killed_width3_assignment_mass':killed_width3_mass,'decision':('C916_250WAY_WIDTH3_BASE_ALL4_M4_CONTRACTION_BELOW_PHYSICAL_149' if new_total<(1<<PHYS_N) else 'C916_250WAY_WIDTH3_BASE_ALL4_M4_CONTRACTION_BEATS_PR194' if nlog<EXPECTED_PR194_LOG2 else 'C916_250WAY_WIDTH3_BASE_ALL4_M4_CONTRACTION_EXACT')}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_250WAY_WIDTH3_BASE_ALL4_M4_CONTRACTION')
    print('scope=exact contraction of the frozen PR200 base160 width3 separator marginal with the PR201 all-four m4 label-intersection plus complete zero-cross+projection-triple factor')
    print('important=exact for the selected factor model; still an upper bound on the true 250-output image')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
