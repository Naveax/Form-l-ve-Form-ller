#!/usr/bin/env python3
import itertools, json, math, os, random
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

PARENT_GIDS=(1,2,13,14)
PHYS_N=149
EXPECTED_BASE_COUNT=103580346297435478039507934992782327762124800000
EXPECTED_GRAPH_DIGEST='ca316800fefcba61d7f295c4c3a224aaa724ce5e02ee9a1dda942212ee5724d8'
EXPECTED_MARG_DIGEST='bb05d63be837d3a5fc9b2d31653355eba1ecf6d9e059f583dcfbddb206d4fca7'
EXPECTED_REL_DIGEST='ce8af72024a4fdd2bdbe270e994dd21bef056e4a703a0e1a34235e646b18d32c'
EXPECTED_SUBSET_DIGEST='7910db1e1f649be99503988e77fc3092908572416e4535ac7632cc515b68bc0d'
EXPECTED_PR194_LOG2=317.07255079311204
EXPECTED_PR204_LOG2=330.0302980870019
EXPECTED_COUNT=173255724728752590119677278354962130446481555888517822288435868975177895302341587763200000

BASE_PATH=Path(os.environ.get('C916_BASE_WIDTH3_AUTHORITY','authorities/base/c916_e0_first_dyadic_base160_width3_separator_authority.json'))
M4_PATH=Path(os.environ.get('C916_M4_AUTHORITY','authorities/m4/c916_e0_first_dyadic_four_separator_complete_authority.json'))
SUBSET_PATH=Path(os.environ.get('C916_M4_SUBSET_AUTHORITY','authorities/subset/c916_e0_first_dyadic_m4_subset_pair_relation_authority.json'))

def load(p):
    assert p.is_file(),p
    return json.loads(p.read_text())

def allowed_parent_row(rec,state):
    cols=int(rec['cols']); mask=int(rec['mask_hex'],16)
    return sum((((mask>>(state*cols+j))&1)<<j) for j in range(cols))

def supports_from_relation(r,hub,leaf,dims):
    a,b=int(r['left_group_id']),int(r['right_group_id'])
    rows,cols=int(r['rows']),int(r['cols']); mask=int(r['relation_mask_hex'],16)
    assert rows==dims[a] and cols==dims[b]
    if a==hub and b==leaf:
        return tuple((mask>>(i*cols))&((1<<cols)-1) for i in range(rows))
    assert a==leaf and b==hub
    out=[]
    for j in range(cols):
        z=0
        for i in range(rows):
            if (mask>>(i*cols+j))&1: z|=1<<i
        out.append(z)
    return tuple(out)

def direct_count(hubs,leaves,isolates,dims,prof,supports):
    domains=[tuple(i for i in range(dims[h]) if (prof[h]>>i)&1) for h in hubs]
    iso=math.prod(prof[g].bit_count() for g in isolates); total=0
    for vals in itertools.product(*domains):
        w=iso
        for leaf in leaves:
            m=prof[leaf]
            for h,x in zip(hubs,vals):
                m &= supports[(h,leaf)][x]
                if not m: break
            if not m:
                w=0; break
            w*=m.bit_count()
        total+=w
    return total

def memo_count(hubs,leaves,isolates,dims,prof,supports,order=None):
    masks=[prof[l] for l in leaves]
    iso=math.prod(prof[g].bit_count() for g in isolates)
    free=[]; domains={}
    for h in hubs:
        vals=tuple(i for i in range(dims[h]) if (prof[h]>>i)&1)
        assert vals; domains[h]=vals
        if len(vals)==1:
            x=vals[0]
            for j,l in enumerate(leaves):
                masks[j] &= supports[(h,l)][x]
                if not masks[j]:
                    return 0,{'memo_states':0,'recursive_calls':0,'free_hubs':0,'order':[]}
        else: free.append(h)
    if order is None:
        def score(h):
            discr=0
            for j,l in enumerate(leaves):
                if len({masks[j]&supports[(h,l)][x] for x in domains[h]})>1: discr+=1
            return (len(domains[h]),-discr,h)
        order=tuple(sorted(free,key=score))
    else:
        order=tuple(order); assert set(order)==set(free)
    calls=0
    @lru_cache(None)
    def rec(k,state):
        nonlocal calls
        calls+=1
        if k==len(order): return math.prod(x.bit_count() for x in state)
        h=order[k]; total=0
        for x in domains[h]:
            arr=[]; ok=True
            for j,l in enumerate(leaves):
                nm=state[j]&supports[(h,l)][x]
                if not nm:
                    ok=False; break
                arr.append(nm)
            if ok: total+=rec(k+1,tuple(arr))
        return total
    ans=iso*rec(0,tuple(masks))
    return ans,{'memo_states':rec.cache_info().currsize,'recursive_calls':calls,'free_hubs':len(order),'order':list(order)}

def synthetic():
    hubs=(0,1); leaves=(2,3); isolates=(); dims={0:2,1:2,2:2,3:2}; prof={g:3 for g in range(4)}
    eq=(1,2); supports={(0,2):eq,(1,2):eq,(0,3):eq,(1,3):eq}
    got,st=memo_count(hubs,leaves,isolates,dims,prof,supports)
    brute=direct_count(hubs,leaves,isolates,dims,prof,supports)
    assert got==brute==2
    return {'count':got,'memo_states':st['memo_states']}

def analyze():
    syn=synthetic(); base,m4,sub=load(BASE_PATH),load(M4_PATH),load(SUBSET_PATH)
    assert int(base['exact_graph_count'])==EXPECTED_BASE_COUNT
    assert base['graph_relation_digest_sha256']==EXPECTED_GRAPH_DIGEST
    assert base['separator_marginal_digest_sha256']==EXPECTED_MARG_DIGEST
    assert m4['four_parent_relation_digest_sha256']==EXPECTED_REL_DIGEST
    assert sub['relation_digest_sha256']==EXPECTED_SUBSET_DIGEST
    assert int(sub['subset_support_pairs'])==825
    assert int(sub['strict_subcartesian_pairs'])==820 and int(sub['full_cartesian_pairs'])==5

    gids=tuple(map(int,m4['m4_group_ids'])); assert len(gids)==90
    rel={(int(r['parent_group_id']),int(r['m4_group_id'])):r for r in m4['four_parent_relations']}
    dims={g:int(rel[(PARENT_GIDS[0],g)]['cols']) for g in gids}
    assert Counter(dims.values())==Counter({7:88,9:2})
    for g in gids: assert all(int(rel[(p,g)]['cols'])==dims[g] for p in PARENT_GIDS)

    relation={}; adj={g:set() for g in gids}
    for r in sub['relations']:
        a,b=int(r['left_group_id']),int(r['right_group_id'])
        assert a<b and (a,b) not in relation
        relation[(a,b)]=r; adj[a].add(b); adj[b].add(a)
    assert len(relation)==825
    hubs=tuple(sorted(g for g in gids if len(adj[g])==75))
    leaves=tuple(sorted(g for g in gids if len(adj[g])==11))
    isolates=tuple(sorted(g for g in gids if len(adj[g])==0))
    assert len(hubs)==11 and len(leaves)==75 and len(isolates)==4
    assert all(adj[h]==set(leaves) for h in hubs)
    assert all(adj[l]==set(hubs) for l in leaves)
    assert hubs==(19,20,23,61,83,129,134,139,140,157,232)
    assert isolates==(158,180,236,238)

    supports={}
    for h in hubs:
        for l in leaves:
            r=relation[(min(h,l),max(h,l))]
            supports[(h,l)]=supports_from_relation(r,h,l,dims)
            assert len(supports[(h,l)])==dims[h]

    bm={tuple(map(int,r['states'])):int(r['count']) for r in base['separator_positive_marginal']}
    assert len(bm)==36 and sum(bm.values())==EXPECTED_BASE_COUNT
    profile_mass=Counter(); profile_states=defaultdict(list)
    for assn,mass in bm.items():
        smap=dict(zip(PARENT_GIDS,assn)); prof={}
        for g in gids:
            d=(1<<dims[g])-1
            for p in PARENT_GIDS: d &= allowed_parent_row(rel[(p,g)],smap[p])
            prof[g]=d
        key=tuple(prof[g] for g in gids); profile_mass[key]+=mass; profile_states[key].append(assn)
    assert len(profile_mass)==10

    total=0; profile_rows=[]; hard_order_checks=0; direct_checks=0
    for key,mass in profile_mass.items():
        prof=dict(zip(gids,key)); states=profile_states[key]
        if not all(prof.values()):
            cnt=0; st={'memo_states':0,'recursive_calls':0,'free_hubs':0,'order':[]}
        else:
            cnt,st=memo_count(hubs,leaves,isolates,dims,prof,supports)
            hub_product=math.prod(prof[h].bit_count() for h in hubs)
            if hub_product<=100000:
                assert direct_count(hubs,leaves,isolates,dims,prof,supports)==cnt; direct_checks+=1
            else:
                free=[h for h in hubs if prof[h].bit_count()>1]
                alt1,_=memo_count(hubs,leaves,isolates,dims,prof,supports,tuple(free))
                alt2,_=memo_count(hubs,leaves,isolates,dims,prof,supports,tuple(reversed(free)))
                z=free[:]; random.Random(123).shuffle(z)
                alt3,_=memo_count(hubs,leaves,isolates,dims,prof,supports,tuple(z))
                assert alt1==alt2==alt3==cnt; hard_order_checks+=1
        total+=mass*cnt
        profile_rows.append({'separator_states':[list(x) for x in states],'base_mass':mass,'m4_exact_count':cnt,
                             'm4_log2':None if not cnt else math.log2(cnt),
                             'hub_domain_product':math.prod(prof[h].bit_count() for h in hubs),
                             'memo_states':st['memo_states'],'free_hubs':st['free_hubs'],'hub_order':st['order']})
    assert total==EXPECTED_COUNT
    tlog=math.log2(total)
    out={'position':'C','physical_shared_dimension':PHYS_N,'synthetic_regression':syn,
         'base_positive_separator_states':36,'unique_all4_domain_profiles':len(profile_mass),
         'subset_graph':'K_11_75_plus_4_isolates','subset_treewidth_exact':11,
         'hub_group_ids':list(hubs),'leaf_outputs':len(leaves),'isolate_group_ids':list(isolates),
         'subset_relations':825,'strict_subset_relations':820,'full_cartesian_subset_relations':5,
         'direct_bruteforce_profile_crosschecks':direct_checks,'hard_profile_multi_order_crosschecks':hard_order_checks,
         'profile_rows':profile_rows,'exact_count':total,'exact_log2':tlog,'state_bits':(total-1).bit_length(),
         'gap_vs_physical_log2_bits':tlog-PHYS_N,'gain_vs_pr194_log2_bits':EXPECTED_PR194_LOG2-tlog,
         'gain_vs_pr204_log2_bits':EXPECTED_PR204_LOG2-tlog,
         'decision':'C916_250WAY_WIDTH3_BASE_ALL4_M4_SUBSET_K11_75_EXACT_BEST_BOUND'}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_SUBSET_K11_75_EXACT')
    print('scope=exact contraction of the frozen PR200/203 width3 base separator marginal with all-four singleton-to-m4 unary intersections and all 825 exact PR206 subset-support m4 value relations, exploiting the PR207 K11,75 factor graph')
    print('important=the complete non-subset zero-cross graph and higher-order affine constraints are not included in this factor model, so the count remains a rigorous upper bound')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
