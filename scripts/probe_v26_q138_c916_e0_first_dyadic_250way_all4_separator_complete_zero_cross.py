#!/usr/bin/env python3
import hashlib, io, json, math, sys
from collections import Counter
from contextlib import redirect_stdout
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_250way_four_singleton_separator_m4_hypergraph as S
import probe_v26_q138_c916_e0_first_dyadic_m4_complete_zero_cross_graph as Z

A=S.A; M=S.M; T=S.T
PHYS_N=S.PHYS_N
POS=S.POS
PARENT_GIDS=S.PARENT_GIDS
EXPECTED_BASE_COUNT=S.EXPECTED_BASE_COUNT
EXPECTED_BASE_DIGEST=S.EXPECTED_BASE_DIGEST
EXPECTED_RELATION_DIGEST='ce8af72024a4fdd2bdbe270e994dd21bef056e4a703a0e1a34235e646b18d32c'
EXPECTED_ZERO_CROSS_DIGEST='7ce0219e86206aeac622bd423b1341cb47f8681564f19319c96823fcb4d4fab1'
EXPECTED_PR197_COUNT=40592012551537592125547898479898982680883667155799077313900181337605
EXPECTED_PR198_COUNT=19495472833965510180005695777791956451721325192874381801
EXPECTED_PR199_COUNT=17833260475848895092642290377069816337734834772319728519138194714969107472119996130985999230481203200000
assert PHYS_N==149

def all_m4_zero_cross(m4s,groups,local):
    icache={}; zero_pairs=[]; pair_disjoint=set(); nonzero=0; support_hist=Counter()
    for i,(u,v) in enumerate(combinations(m4s,2),1):
        rel,_=Z.P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
        support_hist[rel]+=1
        if rel=='disjoint':
            pair_disjoint.add((u,v)); zero_pairs.append((u,v))
        else:
            has,_=Z.has_simultaneous_nonzero(groups[u],groups[v],PHYS_N,icache)
            if has: nonzero+=1
            else: zero_pairs.append((u,v))
        if i%500==0:
            print('progress zero-cross',i,'/',math.comb(90,2),'edges',len(zero_pairs),flush=True)
    dig=hashlib.sha256((''.join(f'{u}|{v}\n' for u,v in zero_pairs)).encode()).hexdigest()
    assert len(zero_pairs)==1318 and dig==EXPECTED_ZERO_CROSS_DIGEST
    pairs=tuple((1<<local[u])|(1<<local[v]) for u,v in zero_pairs)
    triples_gid=Z.projection_minimal_empty_triples(m4s,groups,pair_disjoint)
    triples=tuple((1<<local[a])|(1<<local[b])|(1<<local[c]) for a,b,c in triples_gid)
    assert len(triples)==5
    return tuple(zero_pairs),pairs,tuple(triples_gid),triples,dict(sorted(support_hist.items())),nonzero,len(icache)

def relation_authority(census,groups,m4s):
    ic={}; mc={}; pdata={}; dig=[]; rows=[]
    for pg in PARENT_GIDS:
        pvals=tuple(sorted(census[pg]['counts'])); assert len(pvals)==4
        for mg in m4s:
            counts,pm,mm=M.pair_census(groups[pg],groups[mg],PHYS_N,ic,mc)
            assert pm==census[pg]['counts'] and mm==census[mg]['counts']
            mvals=tuple(sorted(mm)); zi=mvals.index(0)
            mat=tuple(tuple((pv,mv) in counts for mv in mvals) for pv in pvals)
            size=sum(int(x) for row in mat for x in row); mask=S.mask_of(mat)
            pdata[(pg,mg)]=(mat,mvals,zi,size,mask)
            dig.append(f'{pg}|{mg}|4x{len(mvals)}|{mask:x}')
            rows.append({'parent_group_id':pg,'m4_group_id':mg,'cols':len(mvals),'zero_index':zi,'mask_hex':f'{mask:x}'})
    rd=hashlib.sha256(('\n'.join(dig)+'\n').encode()).hexdigest(); assert rd==EXPECTED_RELATION_DIGEST
    return pdata,rd,rows,len(ic),len(mc)

def weights_for_assignment(m4s,pdata,state,chosen=None,all_four=False):
    zw=[]; ow=[]; impossible=forced_nonzero=forced_zero=0
    for mg in m4s:
        if all_four:
            mats=[pdata[(pg,mg)] for pg in PARENT_GIDS]
            mvals=mats[0][1]; zi=mats[0][2]
            assert all(x[1]==mvals and x[2]==zi for x in mats)
            allowed=[all(x[0][state[pg]][j] for pg,x in zip(PARENT_GIDS,mats)) for j in range(len(mvals))]
        else:
            pg=chosen[mg]; mat,mvals,zi,_,_=pdata[(pg,mg)]; allowed=list(mat[state[pg]])
        z=int(allowed[zi]); w=sum(int(allowed[j]) for j in range(len(allowed)) if j!=zi)
        zw.append(z); ow.append(w)
        if z==0 and w==0: impossible+=1
        elif z==0: forced_nonzero+=1
        elif w==0: forced_zero+=1
    return tuple(zw),tuple(ow),impossible,forced_nonzero,forced_zero

def count_model(bmarg,m4s,pdata,hedges,chosen=None,all_four=False):
    total=0; positive_parts=zero_parts=killed_base_mass=0; part_min=None; part_max=0
    impossible_rows=forced_nonzero_rows=forced_zero_rows=memo_states=recursive_calls=0
    for assn,bc in bmarg.items():
        if not bc: continue
        state=dict(zip(PARENT_GIDS,assn))
        zw,ow,imp,fnz,fz=weights_for_assignment(m4s,pdata,state,chosen,all_four)
        part,st=S.weighted_count(90,zw,ow,hedges)
        impossible_rows+=imp; forced_nonzero_rows+=fnz; forced_zero_rows+=fz
        memo_states+=st['memo_states']; recursive_calls+=st['recursive_calls']
        if part:
            positive_parts+=1; total+=bc*part
            part_min=part if part_min is None else min(part_min,part); part_max=max(part_max,part)
        else:
            zero_parts+=1; killed_base_mass+=bc
    assert total>0
    return total,{'positive_separator_partitions':positive_parts,'zero_separator_partitions':zero_parts,
                  'killed_base_tree_assignment_mass':killed_base_mass,'partition_min_positive':part_min,
                  'partition_max':part_max,'impossible_m4_rows':impossible_rows,
                  'forced_nonzero_m4_rows':forced_nonzero_rows,'forced_zero_m4_rows':forced_zero_rows,
                  'memo_states_summed':memo_states,'recursive_calls_summed':recursive_calls}

def analyze():
    with redirect_stdout(io.StringIO()):
        base=A.build_real_relations(); census,groups=M.O.build_authority()
    desc=base['descriptors']; states=base['state_counts']; rel=base['relations']; bloc=base['local']
    root=bloc[('s',94)]
    tree,bcount,_=T.greedy_growth_tree(root,160,rel,states)
    assert bcount==EXPECTED_BASE_COUNT
    _,_,bdig=A.tree_digest(tree,rel,desc); assert bdig==EXPECTED_BASE_DIGEST
    sep=tuple(bloc[('s',g)] for g in PARENT_GIDS)
    bmarg={}
    for assn in product(range(4),repeat=4): bmarg[assn]=S.tree_fixed_count(160,tree,rel,states,dict(zip(sep,assn)))
    assert sum(bmarg.values())==bcount and sum(v>0 for v in bmarg.values())==36

    m4s=tuple(g for g in range(250) if census[g]['multiplicity']==4); assert len(m4s)==90
    local={g:i for i,g in enumerate(m4s)}
    pdata,rdig,rrows,ic1,mc1=relation_authority(census,groups,m4s)
    chosen={mg:min(PARENT_GIDS,key=lambda p:(Fraction(pdata[(p,mg)][3],4*len(pdata[(p,mg)][1])),pdata[(p,mg)][3],p)) for mg in m4s}

    projection_pairs,projection_triples=S.projection_hyperedges(m4s,groups,local); projection_hedges=projection_pairs+projection_triples
    vanilla_projection,_=S.weighted_count(90,(1,)*90,tuple(census[g]['image_size']-1 for g in m4s),projection_hedges)
    assert vanilla_projection==EXPECTED_PR197_COUNT

    zero_pairs,complete_pairs,triples_gid,complete_triples,shist,nonzero,ic2=all_m4_zero_cross(m4s,groups,local)
    complete_hedges=complete_pairs+complete_triples
    vanilla_complete,_=S.weighted_count(90,(1,)*90,tuple(census[g]['image_size']-1 for g in m4s),complete_hedges)
    assert vanilla_complete==EXPECTED_PR198_COUNT

    single_projection,spstats=count_model(bmarg,m4s,pdata,projection_hedges,chosen=chosen); assert single_projection==EXPECTED_PR199_COUNT
    single_complete,scstats=count_model(bmarg,m4s,pdata,complete_hedges,chosen=chosen)
    all4_projection,a4pstats=count_model(bmarg,m4s,pdata,projection_hedges,all_four=True)
    all4_complete,a4cstats=count_model(bmarg,m4s,pdata,complete_hedges,all_four=True)
    assert 0<all4_complete<=all4_projection<=single_projection
    assert 0<all4_complete<=single_complete<=single_projection
    best_log=math.log2(all4_complete)
    decision=('C916_250WAY_ALL4_SEPARATOR_COMPLETE_ZERO_CROSS_BOUND_BELOW_PHYSICAL_149' if all4_complete < (1<<PHYS_N)
              else 'C916_250WAY_ALL4_SEPARATOR_COMPLETE_ZERO_CROSS_STRICTLY_BEATS_WIDTH3' if best_log < 317.07255079311204
              else 'C916_250WAY_ALL4_SEPARATOR_COMPLETE_ZERO_CROSS_STRICTLY_BEATS_SINGLE_PARENT')

    authority={'position':POS,'physical_shared_dimension':PHYS_N,'separator_group_ids':list(PARENT_GIDS),
               'separator_positive_marginal':[{'states':list(a),'count':c} for a,c in sorted(bmarg.items()) if c],
               'm4_group_ids':list(m4s),'four_parent_relations':rrows,'four_parent_relation_digest_sha256':rdig,
               'zero_cross_pairs':[list(x) for x in zero_pairs],'zero_cross_pair_digest_sha256':EXPECTED_ZERO_CROSS_DIGEST,
               'projection_minimal_empty_triples':[list(x) for x in triples_gid]}
    ap=Path('artifacts/c916_e0_first_dyadic_four_separator_complete_authority.json'); ap.parent.mkdir(parents=True,exist_ok=True)
    ap.write_text(json.dumps(authority,sort_keys=True,separators=(',',':'))+'\n')

    def rec(name,count,stats):
        return {'name':name,'exact_assignment_count':count,'exact_log2':math.log2(count),
                'state_bits':(count-1).bit_length(),'gap_vs_physical_log2_bits':math.log2(count)-PHYS_N,
                'gain_vs_pr194_width3_log2_bits':317.07255079311204-math.log2(count),**stats}
    out={'position':POS,'physical_shared_dimension':PHYS_N,'base_outputs':160,'m4_outputs':90,
         'base_tree_count':bcount,'base_tree_log2':math.log2(bcount),'base_tree_digest':bdig,
         'separator_group_ids':list(PARENT_GIDS),'separator_positive_base_marginal_entries':36,
         'four_parent_relations':360,'four_parent_relation_digest_sha256':rdig,
         'complete_zero_cross_pairs':len(zero_pairs),'complete_zero_cross_pair_digest_sha256':EXPECTED_ZERO_CROSS_DIGEST,
         'complete_zero_cross_support_relation_histogram':shist,'complete_nonzero_witness_pairs':nonzero,
         'projection_minimal_empty_triples':len(triples_gid),'relation_support_intersection_cache_entries':ic1,
         'relation_character_moment_cache_entries':mc1,'zero_cross_support_intersection_cache_entries':ic2,
         'models':[rec('single_parent_projection_graph',single_projection,spstats),
                   rec('single_parent_complete_zero_cross',single_complete,scstats),
                   rec('all_four_intersection_projection_graph',all4_projection,a4pstats),
                   rec('all_four_intersection_complete_zero_cross',all4_complete,a4cstats)],
         'selected_exact_assignment_count':all4_complete,'selected_exact_log2':best_log,
         'selected_state_bits':(all4_complete-1).bit_length(),'selected_gap_vs_physical_log2_bits':best_log-PHYS_N,
         'selected_gain_vs_single_parent_projection_log2_bits':math.log2(single_projection)-best_log,
         'selected_gain_vs_pr194_width3_log2_bits':317.07255079311204-best_log,
         'authority_artifact_path':str(ap),'decision':decision}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_250WAY_ALL4_SEPARATOR_COMPLETE_ZERO_CROSS')
    print('scope=exact count for the frozen 160-way base tree, all four exact singleton-to-m4 relation intersections, the complete 1318-edge m4 zero-cross graph, and five exact projection triple hyperedges')
    print('theorem=fixing the four separator states makes the intersection of all four measured base-m4 label sets exact; the complete activity hypergraph is then counted exactly')
    print('important=this remains a rigorous upper bound because only selected base-tree relations and activity-level m4-m4 constraints are enforced')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
