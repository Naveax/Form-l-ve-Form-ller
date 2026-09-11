#!/usr/bin/env python3
import json, math, os, random, sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_m4_subset_k11_75_exact as K

PARENT_GIDS=K.PARENT_GIDS
PHYS_N=149
EXPECTED_PR194_LOG2=317.07255079311204
EXPECTED_PR204_LOG2=330.0302980870019
EXPECTED_PR208_LOG2=296.4445034677639
EXPECTED_COUNT=252911047368380625450925341261258689931591755853405553449491071561221019113839001600000
EXPECTED_ZC_DIGEST='7ce0219e86206aeac622bd423b1341cb47f8681564f19319c96823fcb4d4fab1'

BASE_PATH=K.BASE_PATH
M4_PATH=K.M4_PATH
SUBSET_PATH=K.SUBSET_PATH


def cross_mask(rows,cols,za,zb):
    z=0
    for i in range(rows):
        for j in range(cols):
            if i==za or j==zb: z|=1<<(i*cols+j)
    return z


def tiny_wis(nodes,adj,zw,ow):
    unseen=set(nodes); total=1
    while unseen:
        root=min(unseen); stack=[root]; comp=set()
        while stack:
            v=stack.pop()
            if v in comp: continue
            comp.add(v); stack.extend(adj[v]-comp)
        unseen-=comp
        comp=tuple(sorted(comp))
        if len(comp)==1:
            v=comp[0]; total*=zw[v]+ow[v]; continue
        assert len(comp)<=4
        subtotal=0
        for bits in range(1<<len(comp)):
            selected={comp[k] for k in range(len(comp)) if (bits>>k)&1}
            if any(adj[v]&selected for v in selected): continue
            w=1
            for v in comp: w*=ow[v] if v in selected else zw[v]
            subtotal+=w
        total*=subtotal
    return total


def generic_leaf_wis(domain_masks,leaves,zidx,ladj):
    n=len(leaves); zw=[]; ow=[]
    for i,g in enumerate(leaves):
        z=int(bool((domain_masks[i]>>zidx[g])&1)); zw.append(z); ow.append(domain_masks[i].bit_count()-z)
    memo={}
    def rec(active):
        if not active: return 1
        if active in memo: return memo[active]
        vs=[i for i in range(n) if (active>>i)&1]
        v=max(vs,key=lambda i:((ladj[i]&active).bit_count(),ow[i],-i)); bit=1<<v
        z0=zw[v]*rec(active&~bit) if zw[v] else 0
        nbr=ladj[v]&active; fac=ow[v]; x=nbr
        while x and fac:
            b=x&-x; u=b.bit_length()-1; fac*=zw[u]; x^=b
        z1=fac*rec(active&~bit&~nbr) if fac else 0
        memo[active]=z0+z1; return memo[active]
    return rec((1<<n)-1)


def analyze():
    base,m4,sub=K.load(BASE_PATH),K.load(M4_PATH),K.load(SUBSET_PATH)
    assert int(base['exact_graph_count'])==K.EXPECTED_BASE_COUNT
    assert base['graph_relation_digest_sha256']==K.EXPECTED_GRAPH_DIGEST
    assert base['separator_marginal_digest_sha256']==K.EXPECTED_MARG_DIGEST
    assert m4['four_parent_relation_digest_sha256']==K.EXPECTED_REL_DIGEST
    assert m4['zero_cross_pair_digest_sha256']==EXPECTED_ZC_DIGEST
    assert sub['relation_digest_sha256']==K.EXPECTED_SUBSET_DIGEST

    gids=tuple(map(int,m4['m4_group_ids'])); rel={(int(r['parent_group_id']),int(r['m4_group_id'])):r for r in m4['four_parent_relations']}
    dims={g:int(rel[(PARENT_GIDS[0],g)]['cols']) for g in gids}
    zidx={g:int(rel[(PARENT_GIDS[0],g)]['zero_index']) for g in gids}
    srel={}; sadj={g:set() for g in gids}
    for r in sub['relations']:
        a,b=int(r['left_group_id']),int(r['right_group_id']); srel[(a,b)]=r; sadj[a].add(b); sadj[b].add(a)
    hubs=tuple(sorted(g for g in gids if len(sadj[g])==75)); leaves=tuple(sorted(g for g in gids if len(sadj[g])==11)); isolates=tuple(sorted(g for g in gids if not sadj[g]))
    assert hubs==(19,20,23,61,83,129,134,139,140,157,232)
    assert isolates==(158,180,236,238) and len(leaves)==75
    supports={(h,l):K.supports_from_relation(srel[(min(h,l),max(h,l))],h,l,dims) for h in hubs for l in leaves}

    H,L,I=set(hubs),set(leaves),set(isolates); cats=Counter(); zc=[tuple(map(int,e)) for e in m4['zero_cross_pairs']]
    for a,b in zc:
        ta='h' if a in H else 'l' if a in L else 'i'; tb='h' if b in H else 'l' if b in L else 'i'; cats[''.join(sorted((ta,tb)))]+=1
    assert cats==Counter({'ll':775,'il':300,'hl':183,'hi':44,'hh':10,'ii':6})

    # The 183 hub-leaf zero-cross edges are already exactly represented by PR206 subset masks.
    for a,b in zc:
        if {a,b}&H and {a,b}&L:
            h=a if a in H else b; l=b if b in L else a; r=srel[(min(h,l),max(h,l))]
            rows,cols=int(r['rows']),int(r['cols']); mask=int(r['relation_mask_hex'],16)
            if int(r['left_group_id'])==h:
                assert mask==cross_mask(rows,cols,zidx[h],zidx[l])
            else:
                assert mask==cross_mask(rows,cols,zidx[l],zidx[h])

    hpos={g:i for i,g in enumerate(hubs)}; hh={h:0 for h in hubs}; hi=defaultdict(set)
    leafpos={g:i for i,g in enumerate(leaves)}; ladj=[0]*75
    for a,b in zc:
        if a in H and b in H:
            hh[a]|=1<<hpos[b]; hh[b]|=1<<hpos[a]
        elif a in H and b in I: hi[a].add(b)
        elif b in H and a in I: hi[b].add(a)
        elif a in L and b in L:
            u,v=leafpos[a],leafpos[b]; ladj[u]|=1<<v; ladj[v]|=1<<u
    assert all(hi[h]==I for h in hubs)
    assert Counter(x.bit_count() for x in ladj)==Counter({13:45,14:13,59:13,0:3,16:1})

    A={i for i,x in enumerate(ladj) if x.bit_count()==59}; B=set(range(75))-A; Biso={i for i in B if not ladj[i]}; Bact=B-Biso
    assert len(A)==13 and len(Bact)==59 and len(Biso)==3
    assert tuple(sorted(leaves[i] for i in A))==(31,32,82,87,127,130,131,135,138,229,230,231,233)
    assert tuple(sorted(leaves[i] for i in Biso))==(18,69,132)
    for a in A:
        assert not (ladj[a]&sum(1<<x for x in A))
        assert {j for j in Bact if (ladj[a]>>j)&1}==Bact
    badj={i:set() for i in Bact}; bb=[]
    for i in Bact:
        for j in Bact:
            if i<j and ((ladj[i]>>j)&1): badj[i].add(j); badj[j].add(i); bb.append((leaves[i],leaves[j]))
    assert tuple(sorted(bb))==((5,186),(11,111),(62,154),(111,181),(111,182),(112,183),(141,245),(240,246))

    def leaf_count(dm):
        zw={i:int(bool((dm[i]>>zidx[leaves[i]])&1)) for i in range(75)}; ow={i:dm[i].bit_count()-zw[i] for i in range(75)}
        iso_fac=math.prod(zw[i]+ow[i] for i in Biso); az=math.prod(zw[i] for i in A); aall=math.prod(zw[i]+ow[i] for i in A)
        bz=math.prod(zw[i] for i in Bact); bw=tiny_wis(Bact,badj,zw,ow)
        return iso_fac*(az*bw+(aall-az)*bz)

    # Independent recurrence check on deterministic random real-graph weights.
    rng=random.Random(20260911)
    for _ in range(50):
        dm=tuple(rng.randint(1,(1<<dims[g])-1) for g in leaves)
        assert leaf_count(dm)==generic_leaf_wis(dm,leaves,zidx,ladj)

    bm={tuple(map(int,r['states'])):int(r['count']) for r in base['separator_positive_marginal']}; profiles={}
    for assn,mass in bm.items():
        smap=dict(zip(PARENT_GIDS,assn)); prof={}
        for g in gids:
            d=(1<<dims[g])-1
            for p in PARENT_GIDS: d &= K.allowed_parent_row(rel[(p,g)],smap[p])
            prof[g]=d
        key=tuple(prof[g] for g in gids)
        profiles.setdefault(key,{'prof':prof,'mass':0,'states':[]}); profiles[key]['mass']+=mass; profiles[key]['states'].append(assn)
    assert len(profiles)==10

    def profile_count(prof,order=None):
        domains={h:tuple(i for i in range(dims[h]) if (prof[h]>>i)&1) for h in hubs}
        if any(not v for v in domains.values()) or any(not prof[g] for g in isolates): return 0,{'memo_states':0,'terminal_profiles':0,'raw_hub_space':0}
        lm0=tuple(prof[l] for l in leaves)
        if order is None:
            def score(h):
                discr=sum(len({lm0[j]&supports[(h,l)][x] for x in domains[h]})>1 for j,l in enumerate(leaves))
                return (len(domains[h]),-discr,h)
            order=tuple(sorted(hubs,key=score))
        rc={}; memo={}
        def residual(lm,any_nz):
            key=(lm,any_nz)
            if key in rc: return rc[key]
            lc=leaf_count(lm); zi=[]; oi=[]
            for g in isolates:
                z=int(bool((prof[g]>>zidx[g])&1)); zi.append(z); oi.append(prof[g].bit_count()-z)
            iz=math.prod(zi)
            ans=iz*lc
            if not any_nz:
                lz=math.prod(int(bool((lm[j]>>zidx[l])&1)) for j,l in enumerate(leaves))
                if lz: ans+=sum(oi[i]*math.prod(zi[j] for j in range(4) if j!=i) for i in range(4))
            rc[key]=ans; return ans
        def rec(k,lm,nzmask):
            if k==len(order): return residual(lm,bool(nzmask))
            key=(k,lm,nzmask)
            if key in memo: return memo[key]
            h=order[k]; hp=hpos[h]; total=0
            for x in domains[h]:
                nz=x!=zidx[h]
                if nz and (hh[h]&nzmask): continue
                arr=[]; ok=True
                for j,l in enumerate(leaves):
                    nm=lm[j]&supports[(h,l)][x]
                    if not nm: ok=False; break
                    arr.append(nm)
                if ok: total+=rec(k+1,tuple(arr),nzmask|((1<<hp) if nz else 0))
            memo[key]=total; return total
        ans=rec(0,lm0,0)
        return ans,{'memo_states':len(memo),'terminal_profiles':len(rc),'raw_hub_space':math.prod(len(domains[h]) for h in hubs),'hub_order':list(order)}

    total=0; prows=[]; order_checks=0
    for rec in profiles.values():
        prof=rec['prof']; cnt,st=profile_count(prof)
        if st['raw_hub_space']>100000:
            alt,_=profile_count(prof,tuple(reversed(hubs))); assert alt==cnt; order_checks+=1
        total+=rec['mass']*cnt
        prows.append({'separator_states':[list(x) for x in rec['states']],'base_mass':rec['mass'],'m4_exact_count':cnt,'m4_log2':None if not cnt else math.log2(cnt),**st})
    assert total==EXPECTED_COUNT
    tlog=math.log2(total)
    out={'position':'C','physical_shared_dimension':PHYS_N,'exact_count':total,'exact_log2':tlog,'state_bits':(total-1).bit_length(),
         'zero_cross_category_histogram':dict(sorted(cats.items())),'residual_leaf_graph':'K_13_59_plus_8_B_edges_plus_3_isolates',
         'residual_leaf_high_side_group_ids':list(sorted(leaves[i] for i in A)),'residual_leaf_isolates':list(sorted(leaves[i] for i in Biso)),
         'random_leaf_wis_crosschecks':50,'hard_profile_reverse_order_crosschecks':order_checks,'profile_rows':prows,
         'gain_vs_pr208_log2_bits':EXPECTED_PR208_LOG2-tlog,'gain_vs_pr194_log2_bits':EXPECTED_PR194_LOG2-tlog,
         'gain_vs_pr204_log2_bits':EXPECTED_PR204_LOG2-tlog,'gap_vs_physical_log2_bits':tlog-PHYS_N,
         'decision':'C916_250WAY_SUBSET_VALUE_PLUS_COMPLETE_ZERO_CROSS_EXACT_BEST_BOUND'}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_SUBSET_VALUE_PLUS_COMPLETE_ZERO_CROSS_EXACT')
    print('scope=exact contraction of width3 base + all-four unary m4 domains + all 825 subset value relations + all 1318 complete zero-cross activity relations')
    print('important=higher-order affine projection incompatibilities and generic non-subset non-zero-cross value relations remain outside this factor model')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
