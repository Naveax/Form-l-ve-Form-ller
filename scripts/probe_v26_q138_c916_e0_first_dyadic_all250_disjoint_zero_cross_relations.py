#!/usr/bin/env python3
import hashlib, io, json, sys
from collections import Counter, deque
from contextlib import redirect_stdout
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O
import probe_v26_q138_c916_e0_first_dyadic_m4_support_stratified_joint_candidates as M

P=O.P
PHYS_N=O.PHYS_N
POS=O.POS
assert PHYS_N==149

def kind(census,g):
    m=census[g]['multiplicity']
    return 's' if m==1 else 'm2' if m==2 else 'm4'

def cross_mask(lvals,rvals):
    mask=bit=0
    for a in lvals:
        for b in rvals:
            if a==0 or b==0: mask |= 1<<bit
            bit+=1
    return mask

def components(n,edges):
    adj=[set() for _ in range(n)]
    for u,v in edges:
        adj[u].add(v); adj[v].add(u)
    left=set(range(n)); out=[]
    while left:
        s=min(left); q=deque([s]); left.remove(s); c=[]
        while q:
            x=q.popleft(); c.append(x)
            for y in sorted(adj[x]):
                if y in left:
                    left.remove(y); q.append(y)
        out.append(tuple(sorted(c)))
    return tuple(sorted(out,key=lambda c:(-len(c),c))),adj

def analyze():
    with redirect_stdout(io.StringIO()):
        census,groups=O.build_authority()
    assert len(census)==len(groups)==250

    checks=0
    term_kind_hist=Counter()
    for g in range(250):
        pc=groups[g]['projection_anchor']['physical_support_constraints']
        vals=tuple(sorted(census[g]['counts']))
        assert 0 in vals
        for t in groups[g]['terms']:
            assert P.affine_subset(t['anchor'],pc)
            checks+=1; term_kind_hist[t['kind']]+=1
    assert checks==680

    parents=tuple(g for g in range(250) if census[g]['multiplicity'] in (1,2))
    m4s=tuple(g for g in range(250) if census[g]['multiplicity']==4)
    small=tuple(g for g in parents if census[g]['multiplicity']==2 and census[g]['image_size']==3)
    selected_base_m4=set()
    for m in m4s:
        for rec in M.select(m,parents,small,census,groups):
            selected_base_m4.add((int(rec['parent_group_id']),m))
    assert len(selected_base_m4)==1080

    disjoint=[]
    family_hist=Counter(); shape_hist=Counter(); size_hist=Counter(); digest=[]
    existing_disjoint=Counter(); new_disjoint=Counter()
    for u in range(250):
        for v in range(u+1,250):
            rel,inter=P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
            if rel!='disjoint': continue
            assert inter is None
            uv=(u,v); disjoint.append(uv)
            ku,kv=kind(census,u),kind(census,v)
            fam='_'.join(sorted((ku,kv)))
            lv=tuple(sorted(census[u]['counts'])); rv=tuple(sorted(census[v]['counts']))
            shape=f'{len(lv)}x{len(rv)}'
            mask=cross_mask(lv,rv)
            rsize=len(lv)+len(rv)-1
            assert mask.bit_count()==rsize
            family_hist[fam]+=1; shape_hist[shape]+=1; size_hist[rsize]+=1
            digest.append(f'{u}|{v}|{ku}:{len(lv)}x{kv}:{len(rv)}|{mask:x}')
            is_base_base=(ku!='m4' and kv!='m4')
            is_sampled_base_m4=((u,v) in selected_base_m4)
            is_exact_m4_m4=(ku=='m4' and kv=='m4')
            if is_base_base or is_sampled_base_m4 or is_exact_m4_m4:
                existing_disjoint[fam]+=1
            else:
                assert 'm4' in (ku,kv)
                new_disjoint[fam]+=1

    comps,adj=components(250,disjoint)
    new_total=sum(new_disjoint.values())
    structural_graph_edges=14159+new_total
    out={
        'position':POS,'physical_shared_dimension':PHYS_N,
        'outputs':250,'physical_terms':checks,
        'term_kind_histogram':dict(sorted(term_kind_hist.items())),
        'all_term_supports_subset_projection_anchor':True,
        'all_outputs_zero_outside_projection_anchor':True,
        'disjoint_projection_pairs':len(disjoint),
        'disjoint_pair_family_histogram':dict(sorted(family_hist.items())),
        'disjoint_pair_state_shape_histogram':dict(sorted(shape_hist.items())),
        'disjoint_cross_relation_size_histogram':dict(sorted(size_hist.items())),
        'disjoint_graph_component_sizes':[len(c) for c in comps],
        'disjoint_graph_degree_histogram':dict(sorted(Counter(len(x) for x in adj).items())),
        'already_covered_disjoint_pair_family_histogram':dict(sorted(existing_disjoint.items())),
        'new_structural_disjoint_pair_family_histogram':dict(sorted(new_disjoint.items())),
        'new_structural_disjoint_edges':new_total,
        'pr191_augmented_edges_before_structural_layer':14159,
        'structurally_augmented_relation_edges':structural_graph_edges,
        'structural_relation_digest_sha256':hashlib.sha256(('\n'.join(digest)+'\n').encode()).hexdigest(),
        'decision':'ALL250_DISJOINT_PROJECTION_ZERO_CROSS_RELATIONS_FROZEN',
    }
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL250_DISJOINT_ZERO_CROSS_RELATIONS')
    print('scope=structural zero-cross pair constraints for every disjoint projection-anchor pair among all 250 first-dyadic outputs')
    print('theorem=every physical term support lies inside its group projection anchor, hence disjoint anchors imply Y_u=0 OR Y_v=0 on every physical input')
    print('important=these structural cross relations are rigorous supersets; they need not equal the exact two-output joint image to be valid for upper-bound CSP counting')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':
    analyze()
