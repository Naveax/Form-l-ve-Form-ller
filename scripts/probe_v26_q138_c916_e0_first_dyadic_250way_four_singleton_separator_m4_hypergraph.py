#!/usr/bin/env python3
import hashlib, io, json, math, sys
from collections import Counter
from contextlib import redirect_stdout
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_singleton_m2_160way_joint_tree_bound as A
import probe_v26_q138_c916_e0_first_dyadic_m4_support_stratified_joint_candidates as M

T=A.T; PHYS_N=A.PHYS_N; POS=A.POS
PARENT_GIDS=(1,2,13,14)
EXPECTED_BASE_COUNT=3554017933804264224365028336898853306322124800000
EXPECTED_BASE_DIGEST='7deca3ac2fa0e6eb498fd6b2b111927787c158d4afe751e9c59c4fc3cb459118'
EXPECTED_TRIPLE_DIGEST='3dd086974c55e495828bff85119cb542435b7498c69decc7fe5e9247316452a4'
EXPECTED_PR197_M4_COUNT=40592012551537592125547898479898982680883667155799077313900181337605
assert PHYS_N==149

def tree_fixed_count(n,edges,rel,states,fixed):
    adj=[[] for _ in range(n)]
    for u,v in edges: adj[u].append(v); adj[v].append(u)
    def dfs(u,p):
        incoming=[dfs(v,u) for v in adj[u] if v!=p]
        own=[0]*states[u]
        vals=(fixed[u],) if u in fixed else range(states[u])
        for su in vals:
            w=1
            for child,vec in incoming:
                m=T.relation_matrix(rel,u,child)
                w*=sum(vec[sv] for sv in range(states[child]) if m[su][sv])
            own[su]=w
        return u,tuple(own)
    return sum(dfs(0,-1)[1])

def canonical(edges):
    out=[]
    for e in sorted(set(int(x) for x in edges if x),key=lambda x:(x.bit_count(),x)):
        if not any((k&e)==k for k in out): out.append(e)
    return tuple(out)

def weighted_count(n,zw,ow,edges):
    zw=tuple(map(int,zw)); ow=tuple(map(int,ow)); memo={}; calls=0
    def rec(active,eds):
        nonlocal calls
        calls+=1; eds=canonical(eds); factor=1
        while True:
            singles=0
            for e in eds:
                if e&(e-1)==0: singles|=e
            singles&=active
            if not singles: break
            b=singles&-singles; v=b.bit_length()-1
            factor*=zw[v]
            if factor==0: return 0
            active&=~b; eds=canonical(e for e in eds if not(e&b))
        used=0
        for e in eds: used|=e
        iso=active&~used
        while iso:
            b=iso&-iso; v=b.bit_length()-1
            factor*=zw[v]+ow[v]; iso^=b
        active&=used
        if not active: return factor
        key=(active,eds)
        if key in memo: return factor*memo[key]
        rem=active; comps=[]
        while rem:
            comp=rem&-rem; changed=True
            while changed:
                changed=False
                for e in eds:
                    if e&comp:
                        new=e&active&~comp
                        if new: comp|=new; changed=True
            rem&=~comp; comps.append(comp)
        if len(comps)>1:
            z=1
            for comp in comps: z*=rec(comp,tuple(e for e in eds if e&comp))
            memo[key]=z; return factor*z
        deg=Counter()
        for e in eds:
            x=e
            while x:
                b=x&-x; deg[b.bit_length()-1]+=1; x^=b
        v=max((i for i in range(n) if (active>>i)&1),key=lambda i:(deg[i],zw[i]+ow[i],-i))
        bit=1<<v; rest=active&~bit
        z0=zw[v]*rec(rest,tuple(e for e in eds if not(e&bit)))
        shr=[]
        for e in eds: shr.append(e&~bit if e&bit else e)
        z1=ow[v]*rec(rest,tuple(shr))
        memo[key]=z0+z1
        return factor*(z0+z1)
    total=rec((1<<n)-1,tuple(edges))
    return total,{'memo_states':len(memo),'recursive_calls':calls}

def synthetic():
    zw=(1,2,1,0,3); ow=(2,1,3,4,0); edges=((1<<0)|(1<<1),(1<<1)|(1<<2)|(1<<3))
    got,_=weighted_count(5,zw,ow,edges); brute=0
    for mask in range(32):
        if any((mask&e)==e for e in edges): continue
        w=1
        for i in range(5): w*=ow[i] if (mask>>i)&1 else zw[i]
        brute+=w
    assert got==brute
    return got

def projection_hyperedges(m4s,groups,local):
    pairset=set(); pairs=[]; triples=[]; tg=[]
    for i,u in enumerate(m4s):
        for v in m4s[i+1:]:
            rel,_=M.P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
            if rel=='disjoint':
                pairset.add((u,v)); pairs.append((1<<local[u])|(1<<local[v]))
    assert len(pairs)==359
    for a,b,c in combinations(m4s,3):
        if (a,b) in pairset or (a,c) in pairset or (b,c) in pairset: continue
        cons=(list(groups[a]['projection_anchor']['physical_support_constraints'])+
              list(groups[b]['projection_anchor']['physical_support_constraints'])+
              list(groups[c]['projection_anchor']['physical_support_constraints']))
        if M.P.C.P.U.T.rref(cons,n=PHYS_N) is None:
            tg.append((a,b,c)); triples.append((1<<local[a])|(1<<local[b])|(1<<local[c]))
    dig=hashlib.sha256((''.join(f'{a}|{b}|{c}\n' for a,b,c in tg)).encode()).hexdigest()
    assert len(triples)==5 and dig==EXPECTED_TRIPLE_DIGEST
    return tuple(pairs),tuple(triples)

def mask_of(m):
    z=bit=0
    for row in m:
        for x in row:
            if x: z|=1<<bit
            bit+=1
    return z

def analyze():
    syn=synthetic()
    with redirect_stdout(io.StringIO()):
        base=A.build_real_relations(); census,groups=M.O.build_authority()
    desc=base['descriptors']; states=base['state_counts']; rel=base['relations']; bloc=base['local']
    root=bloc[('s',94)]
    edges,bcount,_=T.greedy_growth_tree(root,160,rel,states)
    assert bcount==EXPECTED_BASE_COUNT
    _,_,bdig=A.tree_digest(edges,rel,desc); assert bdig==EXPECTED_BASE_DIGEST

    sep=tuple(bloc[('s',g)] for g in PARENT_GIDS); assert all(states[x]==4 for x in sep)
    bmarg={}
    for assn in product(range(4),repeat=4): bmarg[assn]=tree_fixed_count(160,edges,rel,states,dict(zip(sep,assn)))
    assert sum(bmarg.values())==bcount

    m4s=tuple(g for g in range(250) if census[g]['multiplicity']==4); assert len(m4s)==90
    ml={g:i for i,g in enumerate(m4s)}
    pairs,triples=projection_hyperedges(m4s,groups,ml); hedges=pairs+triples
    vanilla,_=weighted_count(90,(1,)*90,tuple(census[g]['image_size']-1 for g in m4s),hedges)
    assert vanilla==EXPECTED_PR197_M4_COUNT

    ic,mc={},{}; pdata={}; dig=[]
    for pg in PARENT_GIDS:
        assert census[pg]['multiplicity']==1 and census[pg]['image_size']==4
        pvals=tuple(sorted(census[pg]['counts']))
        for mg in m4s:
            counts,pm,mm=M.pair_census(groups[pg],groups[mg],PHYS_N,ic,mc)
            assert pm==census[pg]['counts'] and mm==census[mg]['counts']
            mvals=tuple(sorted(mm)); zi=mvals.index(0)
            mat=tuple(tuple((pv,mv) in counts for mv in mvals) for pv in pvals)
            size=sum(int(x) for row in mat for x in row)
            pdata[(pg,mg)]=(mat,mvals,zi,size)
            dig.append(f'{pg}|{mg}|4x{len(mvals)}|{mask_of(mat):x}')
    pdig=hashlib.sha256(('\n'.join(dig)+'\n').encode()).hexdigest()

    chosen={}; ph=Counter()
    for mg in m4s:
        pg=min(PARENT_GIDS,key=lambda p:(Fraction(pdata[(p,mg)][3],4*len(pdata[(p,mg)][1])),pdata[(p,mg)][3],p))
        chosen[mg]=pg; ph[pg]+=1
    all_strict=all(pdata[(chosen[g],g)][3] < 4*len(pdata[(chosen[g],g)][1]) for g in m4s)

    total=0; parts=[]; stats=Counter(); zero_disallowed=0
    for assn,bc in bmarg.items():
        state=dict(zip(PARENT_GIDS,assn)); zw=[]; ow=[]
        for mg in m4s:
            pg=chosen[mg]; mat,mvals,zi,_=pdata[(pg,mg)]; row=mat[state[pg]]
            z=int(row[zi]); w=sum(int(row[j]) for j in range(len(row)) if j!=zi)
            zw.append(z); ow.append(w); zero_disallowed+=int(not z)
        part,st=weighted_count(90,tuple(zw),tuple(ow),hedges)
        total+=bc*part; parts.append(part); stats.update(st)
    assert total>0
    tlog=math.log2(total); baseline=math.log2(bcount)+math.log2(vanilla)
    out={'position':POS,'physical_shared_dimension':PHYS_N,'synthetic_weighted_hypergraph_count':syn,
         'base_outputs':160,'m4_outputs':90,'base_tree_count':bcount,'base_tree_log2':math.log2(bcount),'base_tree_digest':bdig,
         'separator_singleton_group_ids':list(PARENT_GIDS),'separator_state_assignments':256,
         'separator_positive_base_marginal_entries':sum(v>0 for v in bmarg.values()),
         'four_parent_m4_pair_relations':360,'four_parent_relation_digest_sha256':pdig,
         'selected_parent_histogram':dict(sorted(ph.items())),'selected_parent_relations_all_strict':all_strict,
         'm4_disjoint_pair_hyperedges':len(pairs),'m4_minimal_empty_triples':len(triples),
         'vanilla_m4_pair_triple_count':vanilla,'vanilla_m4_pair_triple_log2':math.log2(vanilla),
         'independent_product_baseline_log2':baseline,'coupled_exact_assignment_count':total,'coupled_exact_log2':tlog,
         'coupled_state_bits':(total-1).bit_length(),'gain_vs_independent_product_log2_bits':baseline-tlog,
         'gap_vs_physical_log2_bits':tlog-PHYS_N,'gain_vs_width3_log2_bits':317.07255079311204-tlog,
         'partition_min':min(parts),'partition_max':max(parts),'zero_disallowed_row_occurrences':zero_disallowed,
         'support_intersection_cache_entries':len(ic),'character_moment_cache_entries':len(mc),
         'hypergraph_dp_stats_summed':dict(stats),
         'decision':'C916_250WAY_FOUR_SINGLETON_SEPARATOR_M4_HYPERGRAPH_COUPLING_EXACT'}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_250WAY_FOUR_SINGLETON_SEPARATOR_M4_HYPERGRAPH')
    print('scope=exact count for the frozen 160-way base tree, one exact selected relation from one of four singleton parents to each m4 output, and all PR197 m4 projection pair/triple hyperedges')
    print('theorem=fixing four singleton separator states turns each selected base-m4 relation into exact zero/nonzero label weights; the m4 activity hypergraph is then counted exactly')
    print('important=this is a rigorous upper bound on the true 250-output image but retains only one base-m4 relation per m4 output')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
