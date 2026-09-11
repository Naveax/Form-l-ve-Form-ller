#!/usr/bin/env python3
import io, json, math, sys
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_singleton_m2_160way_joint_tree_bound as A
import probe_v26_q138_c916_e0_first_dyadic_250way_sampled_cactus_bound as C

T=A.T
PHYS_N=A.PHYS_N
POS=A.POS
N=160
TOP_DENSITY=1200
EXPECTED_TREE_COUNT=3554017933804264224365028336898853306322124800000
EXPECTED_TREE_DIGEST='7deca3ac2fa0e6eb498fd6b2b111927787c158d4afe751e9c59c4fc3cb459118'
assert PHYS_N==149

def rsize(m):
    return sum(int(x) for row in m for x in row)

def candidate_pool(rel, states, tree_set):
    rows=[]; strict=0
    for (u,v),m in rel.items():
        s=rsize(m); cart=states[u]*states[v]
        if s>=cart: continue
        strict+=1
        key=(min(u,v),max(u,v))
        if key in tree_set: continue
        rows.append((Fraction(s,cart),s,u,v))
    rows.sort()
    return tuple((u,v) for _,_,u,v in rows[:TOP_DENSITY]),strict,len(rows)

def score_by_tree(tree_edges, rel, states, pool):
    tadj,msg=C.directed_messages(tree_edges,rel,states)
    tree_count,_=T.tree_count_and_marginals(range(N),tree_edges,rel,states)
    out=[]
    for i,(u,v) in enumerate(pool,1):
        p=C.tree_path(tadj,u,v)
        joint=C.endpoint_joint(p,tadj,msg,rel,states)
        assert sum(map(sum,joint))==tree_count
        m=T.relation_matrix(rel,u,v)
        cc=sum(joint[a][b] for a in range(states[u]) for b in range(states[v]) if m[a][b])
        if cc<tree_count: out.append((cc,len(p)-1,rsize(m),u,v))
        if i%200==0:
            print('progress scored',i,'/',len(pool),'strict_single_chord',len(out),flush=True)
    out.sort(key=lambda x:(x[0],x[1],x[2],x[3],x[4]))
    return tuple(out)

def synthetic():
    syn=C.synthetic_regression()
    assert syn['tree_count']>syn['one_chord_count']
    return syn

def analyze():
    syn=synthetic()
    with redirect_stdout(io.StringIO()):
        base=A.build_real_relations()
    desc=base['descriptors']; states=base['state_counts']; rel=base['relations']; local=base['local']
    assert len(desc)==N and len(rel)==12720
    root=local[('s',94)]
    tree,count,_=T.greedy_growth_tree(root,N,rel,states)
    assert count==EXPECTED_TREE_COUNT
    _,_,dig=A.tree_digest(tree,rel,desc); assert dig==EXPECTED_TREE_DIGEST
    tree_set={tuple(sorted(e)) for e in tree}; assert len(tree_set)==159

    pool,strict_total,strict_non_tree=candidate_pool(rel,states,tree_set)
    scored=score_by_tree(tree,rel,states,pool)
    graph=set(tree_set); accepted=[]; rejected=0
    for cc,plen,rs,u,v in scored:
        key=tuple(sorted((u,v)))
        if key in graph: continue
        trial=set(graph); trial.add(key)
        order,width=C.min_fill_order(N,trial)
        if width<=3:
            graph=trial; accepted.append((cc,plen,rs,u,v,width))
        else: rejected+=1
    order,width=C.min_fill_order(N,graph); assert width<=3
    exact,peak=C.exact_factor_count(N,graph,rel,states,order)
    assert peak<=4 and 0<exact<=count
    elog=math.log2(exact)
    decision=('C916_BASE160_CERTIFIED_WIDTH3_BOUND_BELOW_PHYSICAL_149' if exact < (1<<PHYS_N)
              else 'C916_BASE160_CERTIFIED_WIDTH3_STRICTLY_BEATS_TREE' if exact<count
              else 'C916_BASE160_CERTIFIED_WIDTH3_NO_GAIN')
    out={'position':POS,'physical_shared_dimension':PHYS_N,'outputs':N,'synthetic_regression':syn,
         'pair_relations':len(rel),'strict_pair_relations':strict_total,
         'tree_edges':len(tree_set),'tree_count':count,'tree_log2':math.log2(count),'tree_digest_sha256':dig,
         'candidate_density_pool':len(pool),'strict_non_tree_relations':strict_non_tree,
         'strict_single_chord_candidates':len(scored),'accepted_chords':len(accepted),
         'rejected_by_width_certificate':rejected,'final_edges':len(graph),
         'certified_induced_width':width,'peak_factor_scope':peak,
         'exact_assignment_count':exact,'exact_log2':elog,'state_bits':(exact-1).bit_length(),
         'gain_vs_tree_log2_bits':math.log2(count)-elog,'gap_vs_physical_log2_bits':elog-PHYS_N,
         'accepted_edges':[{'left_kind':desc[u][0],'left_group_id':desc[u][1],
                            'right_kind':desc[v][0],'right_group_id':desc[v][1],
                            'tree_single_chord_count':cc,'tree_path_edges':plen,
                            'relation_size':rs,'width_after_accept':w}
                           for cc,plen,rs,u,v,w in accepted],
         'elimination_order':list(order),'decision':decision}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_BASE160_CERTIFIED_WIDTH3')
    print('scope=exact certified-induced-width<=3 CSP count for all 160 singleton+m2 outputs using the complete 12720 exact pair authority')
    print('important=candidate admission is heuristic, but the final count is exact for the accepted graph and every accepted factor is an exact physical pair relation')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':
    analyze()
