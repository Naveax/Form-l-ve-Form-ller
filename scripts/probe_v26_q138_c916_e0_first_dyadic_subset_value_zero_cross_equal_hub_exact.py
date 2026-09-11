#!/usr/bin/env python3
import itertools, io, json, math, os, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_subset_value_plus_complete_zero_cross_exact as Z

K=Z.K
PARENT_GIDS=K.PARENT_GIDS
PHYS_N=149
EXPECTED_EQ_DIGEST='8318ee76821c7ccaa3f83aa292cc354abb83b1602ce3ecf1025cfcf3b0ea2448'
EXPECTED_PR209_COUNT=Z.EXPECTED_COUNT
EXPECTED_PR209_LOG2=math.log2(EXPECTED_PR209_COUNT)
EXPECTED_COUNT=252849989918267448087771928068625815321323389449227318713389292661621659113839001600000
EQUAL_PATH=Path(os.environ.get('C916_M4_EQUAL_AUTHORITY','authorities/equal/c916_e0_first_dyadic_m4_equal_pair_relation_authority.json'))


def cross_mask(rows,cols,za,zb):
    out=0
    for i in range(rows):
        for j in range(cols):
            if i==za or j==zb: out|=1<<(i*cols+j)
    return out


def tiny_wis(nodes,adj,zw,ow):
    unseen=set(nodes); total=1
    while unseen:
        root=min(unseen); stack=[root]; comp=set()
        while stack:
            v=stack.pop()
            if v in comp: continue
            comp.add(v); stack.extend(adj[v]-comp)
        unseen-=comp; comp=tuple(sorted(comp)); subtotal=0
        for bits in range(1<<len(comp)):
            selected={comp[k] for k in range(len(comp)) if (bits>>k)&1}
            if any(adj[v]&selected for v in selected): continue
            w=1
            for v in comp: w*=ow[v] if v in selected else zw[v]
            subtotal+=w
        total*=subtotal
    return total


def analyze():
    base,m4,sub,eq=K.load(K.BASE_PATH),K.load(K.M4_PATH),K.load(K.SUBSET_PATH),K.load(EQUAL_PATH)
    assert int(base['exact_graph_count'])==K.EXPECTED_BASE_COUNT
    assert base['graph_relation_digest_sha256']==K.EXPECTED_GRAPH_DIGEST
    assert base['separator_marginal_digest_sha256']==K.EXPECTED_MARG_DIGEST
    assert m4['four_parent_relation_digest_sha256']==K.EXPECTED_REL_DIGEST
    assert m4['zero_cross_pair_digest_sha256']==Z.EXPECTED_ZC_DIGEST
    assert sub['relation_digest_sha256']==K.EXPECTED_SUBSET_DIGEST
    assert eq['relation_digest_sha256']==EXPECTED_EQ_DIGEST
    assert int(eq['equal_support_pairs'])==55 and int(eq['strict_subcartesian_pairs'])==52 and int(eq['full_cartesian_pairs'])==3

    with redirect_stdout(io.StringIO()):
        zres=Z.analyze()
    assert int(zres['exact_count'])==EXPECTED_PR209_COUNT
    old_by_states={tuple(sorted(tuple(map(int,x)) for x in r['separator_states'])):int(r['m4_exact_count']) for r in zres['profile_rows']}

    gids=tuple(map(int,m4['m4_group_ids']))
    rel={(int(r['parent_group_id']),int(r['m4_group_id'])):r for r in m4['four_parent_relations']}
    dims={g:int(rel[(PARENT_GIDS[0],g)]['cols']) for g in gids}
    zidx={g:int(rel[(PARENT_GIDS[0],g)]['zero_index']) for g in gids}

    srel={}; sadj={g:set() for g in gids}
    for r in sub['relations']:
        a,b=int(r['left_group_id']),int(r['right_group_id']); srel[(a,b)]=r; sadj[a].add(b); sadj[b].add(a)
    hubs=tuple(sorted(g for g in gids if len(sadj[g])==75))
    leaves=tuple(sorted(g for g in gids if len(sadj[g])==11))
    isolates=tuple(sorted(g for g in gids if not sadj[g]))
    assert hubs==(19,20,23,61,83,129,134,139,140,157,232)
    assert isolates==(158,180,236,238) and len(leaves)==75
    supports={(h,l):K.supports_from_relation(srel[(min(h,l),max(h,l))],h,l,dims) for h in hubs for l in leaves}

    erel={(int(r['left_group_id']),int(r['right_group_id'])):r for r in eq['relations']}
    assert set(erel)==set(itertools.combinations(hubs,2))
    assert all(int(r['rows'])==7 and int(r['cols'])==7 for r in erel.values())
    eqsupports={(a,b):K.supports_from_relation(erel[(a,b)],a,b,dims) for a,b in itertools.combinations(hubs,2)}
    def pair_allowed(h,u,x):
        if h<u: return eqsupports[(h,u)][x]
        return K.supports_from_relation(erel[(u,h)],h,u,dims)[x]

    H,L,I=set(hubs),set(leaves),set(isolates)
    hpos={g:i for i,g in enumerate(hubs)}; hh={h:0 for h in hubs}
    leafpos={g:i for i,g in enumerate(leaves)}; ladj=[0]*75; hh_pairs=set()
    for a,b in map(lambda e:tuple(map(int,e)),m4['zero_cross_pairs']):
        if a in H and b in H:
            hh[a]|=1<<hpos[b]; hh[b]|=1<<hpos[a]; hh_pairs.add((min(a,b),max(a,b)))
        elif a in L and b in L:
            u,v=leafpos[a],leafpos[b]; ladj[u]|=1<<v; ladj[v]|=1<<u
    assert len(hh_pairs)==10
    exact_cross=set()
    for a,b in itertools.combinations(hubs,2):
        r=erel[(a,b)]; mask=int(r['relation_mask_hex'],16)
        if mask==cross_mask(7,7,zidx[a],zidx[b]): exact_cross.add((a,b))
    assert exact_cross==hh_pairs
    assert sum(bool(r['strict']) for r in eq['relations'] if (int(r['left_group_id']),int(r['right_group_id'])) not in exact_cross)==42

    A={i for i,x in enumerate(ladj) if x.bit_count()==59}; B=set(range(75))-A
    Biso={i for i in B if not ladj[i]}; Bact=B-Biso
    assert len(A)==13 and len(Bact)==59 and len(Biso)==3
    badj={i:set() for i in Bact}
    for i in Bact:
        for j in Bact:
            if i<j and ((ladj[i]>>j)&1): badj[i].add(j); badj[j].add(i)
    def leaf_count(dm):
        zw={i:int(bool((dm[i]>>zidx[leaves[i]])&1)) for i in range(75)}
        ow={i:dm[i].bit_count()-zw[i] for i in range(75)}
        iso_fac=math.prod(zw[i]+ow[i] for i in Biso)
        az=math.prod(zw[i] for i in A); aall=math.prod(zw[i]+ow[i] for i in A)
        bz=math.prod(zw[i] for i in Bact); bw=tiny_wis(Bact,badj,zw,ow)
        return iso_fac*(az*bw+(aall-az)*bz)

    bm={tuple(map(int,r['states'])):int(r['count']) for r in base['separator_positive_marginal']}
    profiles={}
    for assn,mass in bm.items():
        smap=dict(zip(PARENT_GIDS,assn)); prof={}
        for g in gids:
            d=(1<<dims[g])-1
            for p in PARENT_GIDS: d &= K.allowed_parent_row(rel[(p,g)],smap[p])
            prof[g]=d
        key=tuple(prof[g] for g in gids)
        profiles.setdefault(key,{'prof':prof,'mass':0,'states':[]}); profiles[key]['mass']+=mass; profiles[key]['states'].append(assn)
    assert len(profiles)==10

    hhnbr={h:{u for u in hubs if (hh[h]>>hpos[u])&1} for h in hubs}
    def profile_count(prof,order=None):
        dom0={h:prof[h] for h in hubs}
        if any(not dom0[h] for h in hubs) or any(not prof[g] for g in isolates): return 0,{'memo_states':0,'terminal_profiles':0,'raw_hub_space':0,'hub_order':[]}
        lm0=tuple(prof[l] for l in leaves)
        if order is None:
            def score(h):
                vals=tuple(i for i in range(dims[h]) if (dom0[h]>>i)&1)
                eqd=sum(len({dom0[u]&pair_allowed(h,u,x) for x in vals})>1 for u in hubs if u!=h)
                discr=sum(len({lm0[j]&supports[(h,l)][x] for x in vals})>1 for j,l in enumerate(leaves))
                return (len(vals),-eqd,-discr,h)
            order=tuple(sorted(hubs,key=score))
        else:
            order=tuple(order); assert set(order)==set(hubs)
        hdm0=tuple(dom0[h] for h in order); memo={}; terminal_cache={}; calls=0
        def residual(lm,any_nz):
            key=(lm,any_nz)
            if key in terminal_cache:return terminal_cache[key]
            lc=leaf_count(lm); zi=[]; oi=[]
            for g in isolates:
                z=int(bool((prof[g]>>zidx[g])&1)); zi.append(z); oi.append(prof[g].bit_count()-z)
            ans=math.prod(zi)*lc
            if not any_nz:
                lz=math.prod(int(bool((lm[j]>>zidx[l])&1)) for j,l in enumerate(leaves))
                if lz: ans+=sum(oi[i]*math.prod(zi[j] for j in range(4) if j!=i) for i in range(4))
            terminal_cache[key]=ans; return ans
        def rec(k,hdm,lm,nzmask):
            nonlocal calls; calls+=1
            if k==len(order):return residual(lm,bool(nzmask))
            key=(k,hdm[k:],lm,nzmask)
            if key in memo:return memo[key]
            h=order[k]; bits=hdm[k]; total=0
            while bits:
                bit=bits&-bits; x=bit.bit_length()-1; bits^=bit; nz=x!=zidx[h]
                if nz and any(((nzmask>>j)&1) and order[j] in hhnbr[h] for j in range(k)): continue
                arr=[]; ok=True
                for j,l in enumerate(leaves):
                    nm=lm[j]&supports[(h,l)][x]
                    if not nm:ok=False;break
                    arr.append(nm)
                if not ok:continue
                nh=list(hdm)
                for j in range(k+1,len(order)):
                    u=order[j]; nm=nh[j]&pair_allowed(h,u,x)
                    if not nm:ok=False;break
                    nh[j]=nm
                if ok:total+=rec(k+1,tuple(nh),tuple(arr),nzmask|((1<<k) if nz else 0))
            memo[key]=total; return total
        ans=rec(0,hdm0,lm0,0)
        raw=math.prod(dom0[h].bit_count() for h in hubs)
        return ans,{'memo_states':len(memo),'terminal_profiles':len(terminal_cache),'recursive_calls':calls,'raw_hub_space':raw,'hub_order':list(order)}

    def direct_profile(prof):
        ds={h:tuple(i for i in range(dims[h]) if (prof[h]>>i)&1) for h in hubs}; total=0
        for vals in itertools.product(*(ds[h] for h in hubs)):
            amap=dict(zip(hubs,vals)); ok=True
            for a,b in itertools.combinations(hubs,2):
                if not ((pair_allowed(a,b,amap[a])>>amap[b])&1):ok=False;break
            if not ok:continue
            lm=[prof[l] for l in leaves]; any_nz=False
            for h in hubs:
                x=amap[h]; any_nz|=x!=zidx[h]
                for j,l in enumerate(leaves):
                    lm[j]&=supports[(h,l)][x]
                    if not lm[j]:ok=False;break
                if not ok:break
            if not ok:continue
            total+=profile_residual(prof,tuple(lm),any_nz)
        return total
    def profile_residual(prof,lm,any_nz):
        lc=leaf_count(lm); zi=[];oi=[]
        for g in isolates:
            z=int(bool((prof[g]>>zidx[g])&1));zi.append(z);oi.append(prof[g].bit_count()-z)
        ans=math.prod(zi)*lc
        if not any_nz:
            lz=math.prod(int(bool((lm[j]>>zidx[l])&1)) for j,l in enumerate(leaves))
            if lz:ans+=sum(oi[i]*math.prod(zi[j] for j in range(4) if j!=i) for i in range(4))
        return ans

    total=0; rows=[]; direct_checks=0; order_checks=0
    for rec in profiles.values():
        prof=rec['prof']; cnt,st=profile_count(prof); skey=tuple(sorted(tuple(map(int,x)) for x in rec['states'])); old=old_by_states[skey]
        assert 0<=cnt<=old
        if st['raw_hub_space']<=100000:
            assert direct_profile(prof)==cnt; direct_checks+=1
        elif cnt:
            alt,_=profile_count(prof,tuple(reversed(hubs))); assert alt==cnt; order_checks+=1
        total+=rec['mass']*cnt
        rows.append({'separator_states':[list(x) for x in rec['states']],'base_mass':rec['mass'],'m4_pr209_count':old,'m4_equal_exact_count':cnt,**st})
    assert total==EXPECTED_COUNT
    tlog=math.log2(total)
    out={'position':'C','physical_shared_dimension':PHYS_N,'exact_count':total,'exact_log2':tlog,'state_bits':(total-1).bit_length(),
         'gain_vs_pr209_log2_bits':EXPECTED_PR209_LOG2-tlog,'gap_vs_physical_log2_bits':tlog-PHYS_N,
         'equal_support_pairs':55,'strict_equal_relations':52,'new_strict_nonzero_cross_equal_relations':42,
         'equal_relation_digest_sha256':EXPECTED_EQ_DIGEST,'direct_bruteforce_profile_crosschecks':direct_checks,
         'hard_profile_reverse_order_crosschecks':order_checks,'profile_rows':rows,
         'decision':'C916_250WAY_SUBSET_VALUE_ZERO_CROSS_EQUAL_HUB_EXACT'}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_SUBSET_VALUE_ZERO_CROSS_EQUAL_HUB_EXACT')
    print('scope=PR209 exact model plus all 55 exact equal-support hub-hub value relations')
    print('important=higher-order affine constraints and generic overlap-incomparable non-zero-cross value relations remain outside this factor model')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':analyze()
