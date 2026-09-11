#!/usr/bin/env python3
import hashlib, io, json, math, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_250way_sampled_pair_tree_bound as B
import probe_v26_q138_c916_e0_first_dyadic_m4_m4_disjoint_support_full_census as F

T=B.T
PHYS_N=B.PHYS_N
POS=B.POS
N=250
OLD_TREE_LOG2=355.5156563188368
OLD_CACTUS_LOG2=333.9455095574383
EXPECTED_DISJOINT_DIGEST='8fd11e4da31260abc9c4a1aa71837aa0ad0c9c683d635d39e208e59b71b8b845'
MASK_BY_SHAPE={
    '7x7': int('20408fe20408',16),
    '9x7': int('8102047f1020408',16),
}
assert PHYS_N==149

def matrix_from_mask(mask,nr,nc):
    out=[]; bit=0
    for _ in range(nr):
        row=[]
        for _ in range(nc):
            row.append(bool((mask>>bit)&1)); bit+=1
        out.append(tuple(row))
    assert mask >> bit == 0
    return tuple(out)

def mask_from_matrix(m):
    mask=bit=0
    for row in m:
        for x in row:
            if x: mask |= 1<<bit
            bit += 1
    return mask

def cross_mask(lvals,rvals):
    assert 0 in lvals and 0 in rvals
    m=tuple(tuple(a==0 or b==0 for b in rvals) for a in lvals)
    return mask_from_matrix(m),m

def augment_relations():
    with redirect_stdout(io.StringIO()):
        c=B.build_combined()
    rel=dict(c['rel'])
    states=tuple(c['states'])
    desc=tuple(c['desc'])
    census=c['census']
    groups=c['groups']
    assert len(rel)==13800 and len(states)==len(desc)==N

    pairs,adj,components,inner_cache_entries=F.disjoint_pairs(census,groups)
    assert len(pairs)==359 and tuple(len(x) for x in components)==(90,)
    local={d:i for i,d in enumerate(desc)}
    digest=[]
    shape_hist=Counter()
    for gu,gv in pairs:
        nu=local[('m4',gu)]; nv=local[('m4',gv)]
        assert nu<nv and (nu,nv) not in rel
        lvals=tuple(sorted(census[gu]['counts']))
        rvals=tuple(sorted(census[gv]['counts']))
        shape=f'{len(lvals)}x{len(rvals)}'
        assert shape in MASK_BY_SHAPE, (gu,gv,shape)
        frozen=MASK_BY_SHAPE[shape]
        structural,mat=cross_mask(lvals,rvals)
        assert structural==frozen, (gu,gv,shape,hex(structural),hex(frozen))
        assert len(mat)==states[nu] and len(mat[0])==states[nv]
        rel[(nu,nv)]=mat
        digest.append(f'{gu}|{gv}|{shape}|{frozen:x}')
        shape_hist[shape]+=1
    got=hashlib.sha256(('\n'.join(digest)+'\n').encode()).hexdigest()
    assert got==EXPECTED_DISJOINT_DIGEST
    assert shape_hist==Counter({'7x7':351,'9x7':8})
    assert len(rel)==14159
    deg={g:len(adj[g]) for g in adj}
    assert Counter(deg.values())==Counter({4:70,5:15,7:1,89:4})
    return c,rel,states,desc,pairs,adj,components,deg,inner_cache_entries

def analyze():
    c,rel,states,desc,pairs,m4adj,components,m4deg,inner_cache_entries=augment_relations()
    adj=B.adj_from_rel(N,rel)
    assert all(adj)

    candidates={}
    kedges=B.sparse_kruskal(N,rel,states)
    kcount,_=T.tree_count_and_marginals(range(N),kedges,rel,states)
    candidates['augmented_kruskal']=(kcount,kedges,None)

    local={d:i for i,d in enumerate(desc)}
    root_desc=[('s',94)]
    universal=sorted(((-m4deg[g],g) for g in m4deg))[:4]
    assert all(-d==89 for d,_ in universal)
    root_desc.extend(('m4',g) for _,g in universal)
    nine=sorted(g for g in m4deg if states[local[('m4',g)]]==9)
    assert len(nine)==2
    root_desc.extend(('m4',g) for g in nine if ('m4',g) not in root_desc)
    root_desc=tuple(root_desc)

    root_rows=[]
    for d in root_desc:
        root=local[d]
        edges,count,_marg,_hist=B.sparse_greedy((root,),(),N,rel,states,adj)
        key=f'augmented_root_{d[0]}_{d[1]}'
        candidates[key]=(count,edges,root)
        root_rows.append({'kind':d[0],'group_id':d[1],'tree_count':count,'tree_log2':math.log2(count)})

    method,(bound,edges,root)=min(candidates.items(),key=lambda kv:(kv[1][0],kv[0]))
    check,marg=T.tree_count_and_marginals(range(N),edges,rel,states)
    assert check==bound and len(edges)==N-1
    summary=B.tree_summary(edges,rel,states,desc)
    blog=math.log2(bound)
    fam=summary['edge_family_histogram']
    m4m4=int(fam.get('m4_m4',0))
    decision=('C916_250WAY_DISJOINT_M4_AUGMENTED_TREE_BELOW_PHYSICAL_149'
              if bound < (1<<PHYS_N)
              else 'C916_250WAY_DISJOINT_M4_AUGMENTED_TREE_STRICTLY_BEATS_OLD_TREE'
              if blog < OLD_TREE_LOG2
              else 'C916_250WAY_DISJOINT_M4_AUGMENTED_TREE_NO_LOG2_IMPROVEMENT')
    poshist=Counter(sum(int(w>0) for w in ws) for ws in marg.values())
    out={
        'position':POS,'physical_shared_dimension':PHYS_N,'outputs':N,
        'old_sampled_relation_edges':13800,
        'exact_disjoint_m4_m4_edges_added':len(pairs),
        'augmented_relation_edges':len(rel),
        'disjoint_relation_digest_sha256':EXPECTED_DISJOINT_DIGEST,
        'disjoint_relation_shape_histogram':{'7x7':351,'9x7':8},
        'disjoint_relation_masks':{k:f'{v:x}' for k,v in MASK_BY_SHAPE.items()},
        'disjoint_relation_structural_cross_mask_verified':True,
        'disjoint_m4_component_sizes':[len(x) for x in components],
        'disjoint_m4_degree_histogram':dict(sorted(Counter(m4deg.values()).items())),
        'candidate_tree_counts':{k:v[0] for k,v in candidates.items()},
        'root_greedy_results':sorted(root_rows,key=lambda r:(r['tree_count'],r['kind'],r['group_id'])),
        'selected_tree_method':method,
        'selected_tree_root':None if root is None else {'kind':desc[root][0],'group_id':desc[root][1]},
        'selected_tree_count':bound,
        'selected_tree_log2':blog,
        'selected_tree_state_bits':(bound-1).bit_length(),
        'gain_vs_pr184_tree_log2_bits':OLD_TREE_LOG2-blog,
        'gain_vs_pr187_cactus_log2_bits':OLD_CACTUS_LOG2-blog,
        'gap_vs_physical_log2_bits':blog-PHYS_N,
        'selected_m4_m4_tree_edges':m4m4,
        'selected_tree':dict(summary,node_marginal_positive_state_count_histogram=dict(sorted(poshist.items()))),
        'disjoint_inner_product_cache_entries':inner_cache_entries,
        'decision':decision,
    }
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_250WAY_DISJOINT_M4_AUGMENTED_TREE')
    print('scope=rigorous exact tree-consistency upper bound on the 14159-edge graph: PR184 13800 relations plus all 359 PR190 disjoint-support m4-m4 relations')
    print('theorem=PR190 masks are reconstructed from frozen shape masks, re-hashed to the exact PR190 digest, and independently matched to the structural Y_u=0 OR Y_v=0 cross relation')
    print('next=use the selected augmented tree as the foundation for a new exact cactus/junction-tree pass')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':
    analyze()
