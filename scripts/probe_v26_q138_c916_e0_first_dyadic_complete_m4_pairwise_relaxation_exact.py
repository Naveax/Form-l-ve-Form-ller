#!/usr/bin/env python3
import json, math, os
from collections import Counter, defaultdict, deque
from pathlib import Path

PHYS_N=149
BASE_PATH=Path(os.environ.get('C916_BASE_AUTHORITY','authorities/base/c916_e0_first_dyadic_base160_width3_separator_authority.json'))
M4_PATH=Path(os.environ.get('C916_M4_AUTHORITY','authorities/m4/c916_e0_first_dyadic_four_separator_complete_authority.json'))
SUBSET_PATH=Path(os.environ.get('C916_SUBSET_AUTHORITY','authorities/subset/c916_e0_first_dyadic_m4_subset_pair_relation_authority.json'))
EQUAL_PATH=Path(os.environ.get('C916_EQUAL_AUTHORITY','authorities/equal/c916_e0_first_dyadic_m4_equal_pair_relation_authority.json'))
OVERLAP_Q_PATH=Path(os.environ.get('C916_OVERLAP_QUOTIENT_AUTHORITY','authorities/overlap/c916_e0_first_dyadic_m4_full_overlap_sign_reflection_quotient_authority.json'))

EXPECTED_BASE_GRAPH_DIGEST='ca316800fefcba61d7f295c4c3a224aaa724ce5e02ee9a1dda942212ee5724d8'
EXPECTED_BASE_SEPARATOR_DIGEST='bb05d63be837d3a5fc9b2d31653355eba1ecf6d9e059f583dcfbddb206d4fca7'
EXPECTED_FOUR_PARENT_DIGEST='ce8af72024a4fdd2bdbe270e994dd21bef056e4a703a0e1a34235e646b18d32c'
EXPECTED_ZERO_CROSS_DIGEST='7ce0219e86206aeac622bd423b1341cb47f8681564f19319c96823fcb4d4fab1'
EXPECTED_SUBSET_DIGEST='7910db1e1f649be99503988e77fc3092908572416e4535ac7632cc515b68bc0d'
EXPECTED_EQUAL_DIGEST='8318ee76821c7ccaa3f83aa292cc354abb83b1602ce3ecf1025cfcf3b0ea2448'
EXPECTED_OVERLAP_REDUCED_DIGEST='f872b9040562f0fe3d072b1fc28efe3e73d072fb3cd147da9492e3cfa68c4fcd'
EXPECTED_PR212_COUNT=252849989918267448087771928068625815321323389449227318713389292661621659113839001600000
EXPECTED_EXACT_COUNT=667251639197063986752771721653766635157388976602589789841148591163677039001600000
SPECIAL_PAIRS=((141,247),(160,241))


def load(path):
    return json.loads(path.read_text())

def orbit_indices(n):
    assert n in (7,9)
    seen=set(); out=[]
    for i in range(n):
        if i in seen: continue
        o=tuple(sorted({i,n-1-i})); seen.update(o); out.append(o)
    return tuple(out)

def quotient_relation(nr,nc,mask_hex):
    mask=int(mask_hex,16); ro=orbit_indices(nr); co=orbit_indices(nc); q=0
    for a,A in enumerate(ro):
        for b,B in enumerate(co):
            vals={(mask>>(i*nc+j))&1 for i in A for j in B}
            assert len(vals)==1, (nr,nc,mask_hex,a,b)
            if 1 in vals: q|=1<<(a*len(co)+b)
    return len(ro),len(co),q

def transpose_mask(rows,cols,mask):
    out=0
    for i in range(rows):
        for j in range(cols):
            if (mask>>(i*cols+j))&1: out|=1<<(j*rows+i)
    return out

def add_pair(pairq,source,u,v,nr,nc,qmask,src):
    u=int(u); v=int(v); R=len(orbit_indices(int(nr))); C=len(orbit_indices(int(nc))); qmask=int(qmask)
    if u<v:
        pairq[(u,v)]=(R,C,qmask)
    else:
        pairq[(v,u)]=(C,R,transpose_mask(R,C,qmask))
    source[(min(u,v),max(u,v))]=src

def special_states(exception):
    nr=nc=7; raw=int(exception['original_relation_mask_hex'],16); orbs=orbit_indices(7); states=[]; weights=[]
    for a,A in enumerate(orbs):
        for b,B in enumerate(orbs):
            count=sum((raw>>(i*nc+j))&1 for i in A for j in B)
            if count:
                states.append((a,b)); weights.append(count)
    assert states==[(0,0),(0,3),(1,1),(1,3),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)]
    assert weights==[2,2,2,2,2,2,2,2,2,1] and sum(weights)==19
    return tuple(states),tuple(weights)

class ExactCounter:
    def __init__(self,variables,var_states,var_weights,pairq):
        self.variables=variables; self.var_states=var_states; self.var_weights=var_weights; self.pairq=pairq
        self.N=len(variables); self.ALL=(1<<self.N)-1; self.relrows={}; self.adj=[0]*self.N
        self._build_relations()
        self.wsum=[]
        for ws in var_weights:
            arr=[0]*(1<<len(ws))
            for mask in range(1,1<<len(ws)):
                lsb=mask&-mask; k=lsb.bit_length()-1; arr[mask]=arr[mask^lsb]+ws[k]
            self.wsum.append(arr)
        self.memo={}; self.calls=0

    def _qallowed(self,u,mu,v,mv):
        a,b=(u,v) if u<v else (v,u); R,C,qm=self.pairq[(a,b)]
        if u<v: return bool((qm>>(mu*C+mv))&1)
        return bool((qm>>(mv*C+mu))&1)

    def _build_relations(self):
        for i in range(self.N):
            for j in range(i+1,self.N):
                rows=[]
                for state_i in self.var_states[i]:
                    mask=0
                    for bj,state_j in enumerate(self.var_states[j]):
                        ok=True
                        for ai,u in enumerate(self.variables[i]):
                            for aj,v in enumerate(self.variables[j]):
                                if not self._qallowed(u,state_i[ai],v,state_j[aj]): ok=False; break
                            if not ok: break
                        if ok: mask|=1<<bj
                    rows.append(mask)
                full=(1<<len(self.var_states[j]))-1
                if all(r==full for r in rows): continue
                self.relrows[(i,j)]=tuple(rows)
                rev=[]
                for b in range(len(self.var_states[j])):
                    m=0
                    for a in range(len(self.var_states[i])):
                        if (rows[a]>>b)&1: m|=1<<a
                    rev.append(m)
                self.relrows[(j,i)]=tuple(rev)
                self.adj[i]|=1<<j; self.adj[j]|=1<<i

    @staticmethod
    def _restrict_supported(di,rows,dj):
        out=0; mask=di
        while mask:
            lsb=mask&-mask; a=lsb.bit_length()-1; mask^=lsb
            if rows[a]&dj: out|=lsb
        return out

    def _arc_closure(self,active,domains):
        dom=list(domains); q=deque(i for i in range(self.N) if (active>>i)&1); inq=set(q)
        while q:
            i=q.popleft(); inq.discard(i); di=dom[i]; neighbors=self.adj[i]&active
            while neighbors:
                lsb=neighbors&-neighbors; j=lsb.bit_length()-1; neighbors^=lsb
                nd=self._restrict_supported(dom[j],self.relrows[(j,i)],di)
                if nd!=dom[j]:
                    if nd==0: return None
                    dom[j]=nd
                    if j not in inq: q.append(j); inq.add(j)
        return tuple(dom)

    def _relevant_neighbors(self,i,active,domains):
        out=0; neighbors=self.adj[i]&active; di=domains[i]
        while neighbors:
            lsb=neighbors&-neighbors; j=lsb.bit_length()-1; neighbors^=lsb; dj=domains[j]; rows=self.relrows[(i,j)]
            mask=di; complete=True
            while mask:
                x=mask&-mask; a=x.bit_length()-1; mask^=x
                if (rows[a]&dj)!=dj: complete=False; break
            if not complete: out|=lsb
        return out

    def solve(self,active,domains):
        self.calls+=1; closed=self._arc_closure(active,domains)
        if closed is None: return 0
        domains=closed; singleton=0; factor=1; scan=active
        while scan:
            lsb=scan&-scan; i=lsb.bit_length()-1; scan^=lsb; d=domains[i]
            if d&(d-1)==0:
                singleton|=lsb; factor*=self.var_weights[i][d.bit_length()-1]
        if singleton:
            rest=active^singleton
            return factor if rest==0 else factor*self.solve(rest,domains)
        key=(active,tuple(domains[i] for i in range(self.N) if (active>>i)&1))
        if key in self.memo: return self.memo[key]

        remain=active; comps=[]; isolated_factor=1
        while remain:
            seed=remain&-remain; i=seed.bit_length()-1
            if self._relevant_neighbors(i,active,domains)==0:
                isolated_factor*=self.wsum[i][domains[i]]; remain^=seed; continue
            comp=0; frontier=seed
            while frontier:
                x=frontier&-frontier; frontier^=x; k=x.bit_length()-1
                if comp&x: continue
                comp|=x; frontier|=self._relevant_neighbors(k,active,domains)&~comp
            comps.append(comp); remain&=~comp
        if not comps:
            self.memo[key]=isolated_factor; return isolated_factor
        if len(comps)>1 or isolated_factor!=1 or comps[0]!=active:
            value=isolated_factor
            for comp in comps: value*=self.solve(comp,domains)
            self.memo[key]=value; return value

        best=None; scan=active
        while scan:
            x=scan&-scan; i=x.bit_length()-1; scan^=x
            score=(domains[i].bit_count(),-self._relevant_neighbors(i,active,domains).bit_count())
            if best is None or score<best[0]: best=(score,i)
        i=best[1]; total=0; mask=domains[i]
        while mask:
            x=mask&-mask; mask^=x; nd=list(domains); nd[i]=x; total+=self.solve(active,tuple(nd))
        self.memo[key]=total; return total

    def count_profile(self,domains):
        self.memo.clear(); self.calls=0; value=self.solve(self.ALL,tuple(domains)); return value,self.calls,len(self.memo)

def analyze():
    base=load(BASE_PATH); m4=load(M4_PATH); subset=load(SUBSET_PATH); equal=load(EQUAL_PATH); overlap=load(OVERLAP_Q_PATH)
    assert base['graph_relation_digest_sha256']==EXPECTED_BASE_GRAPH_DIGEST
    assert base['separator_marginal_digest_sha256']==EXPECTED_BASE_SEPARATOR_DIGEST
    assert m4['four_parent_relation_digest_sha256']==EXPECTED_FOUR_PARENT_DIGEST
    assert m4['zero_cross_pair_digest_sha256']==EXPECTED_ZERO_CROSS_DIGEST
    assert subset['relation_digest_sha256']==EXPECTED_SUBSET_DIGEST
    assert equal['relation_digest_sha256']==EXPECTED_EQUAL_DIGEST
    assert overlap['combined_reduced_authority_digest_sha256']==EXPECTED_OVERLAP_REDUCED_DIGEST
    assert int(base['exact_graph_count'])==sum(int(r['count']) for r in base['separator_positive_marginal'])

    gids=tuple(map(int,m4['m4_group_ids'])); assert len(gids)==90
    imgsize={}
    for r in m4['four_parent_relations']:
        g=int(r['m4_group_id']); imgsize[g]=int(r['cols'])
    assert Counter(imgsize.values())==Counter({7:88,9:2})

    pairq={}; source={}
    for r in subset['relations']:
        _,_,qm=quotient_relation(int(r['rows']),int(r['cols']),r['relation_mask_hex'])
        add_pair(pairq,source,r['left_group_id'],r['right_group_id'],r['rows'],r['cols'],qm,'subset')
    for r in equal['relations']:
        _,_,qm=quotient_relation(int(r['rows']),int(r['cols']),r['relation_mask_hex'])
        add_pair(pairq,source,r['left_group_id'],r['right_group_id'],r['rows'],r['cols'],qm,'equal')
    for r in overlap['rows']:
        add_pair(pairq,source,r['left_group_id'],r['right_group_id'],r['left_image_size'],r['right_image_size'],int(r['quotient_mask_hex'],16),'overlap')

    exceptions={(min(int(e['left_group_id']),int(e['right_group_id'])),max(int(e['left_group_id']),int(e['right_group_id']))):e for e in overlap['signed_magnitude_exceptions']}
    assert set(exceptions)==set(SPECIAL_PAIRS)
    zero_cross={tuple(sorted(map(int,e))) for e in m4['zero_cross_pairs']}
    remaining=zero_cross-set(pairq)-set(SPECIAL_PAIRS)
    assert len(zero_cross)==1318 and len(remaining)==1125
    for u,v in sorted(remaining):
        R=(imgsize[u]+1)//2; C=(imgsize[v]+1)//2; zu=R-1; zv=C-1; qm=0
        for i in range(R):
            for j in range(C):
                if i==zu or j==zv: qm|=1<<(i*C+j)
        add_pair(pairq,source,u,v,imgsize[u],imgsize[v],qm,'zero_cross_activity')
    allpairs={(u,v) for i,u in enumerate(gids) for v in gids[i+1:]}
    assert set(pairq)|set(SPECIAL_PAIRS)==allpairs and len(pairq)==4003
    assert Counter(source.values())==Counter({'overlap':1998,'zero_cross_activity':1125,'subset':825,'equal':55})

    endpoint={g:p for p in SPECIAL_PAIRS for g in p}; variables=[]
    for g in gids:
        if g in endpoint:
            p=endpoint[g]
            if g==p[0]: variables.append(p)
        else: variables.append((g,))
    assert len(variables)==88
    var_states=[]; var_weights=[]
    for members in variables:
        if len(members)==1:
            orbits=orbit_indices(imgsize[members[0]]); var_states.append(tuple((i,) for i in range(len(orbits)))); var_weights.append(tuple(map(len,orbits)))
        else:
            states,weights=special_states(exceptions[tuple(members)]); var_states.append(states); var_weights.append(weights)

    parents=tuple(map(int,m4['separator_group_ids'])); assert parents==(1,2,13,14)
    pr={(int(r['parent_group_id']),int(r['m4_group_id'])):r for r in m4['four_parent_relations']}; assert len(pr)==360
    def unary_domain(g,sep):
        n=imgsize[g]; allowed=set(range(n))
        for pg,state in zip(parents,sep):
            r=pr[(pg,g)]; cols=int(r['cols']); raw=int(r['mask_hex'],16); row=(raw>>(state*cols))&((1<<cols)-1)
            allowed&={j for j in range(cols) if (row>>j)&1}
        out=0
        for k,O in enumerate(orbit_indices(n)):
            vals={x in allowed for x in O}; assert len(vals)==1
            if True in vals: out|=1<<k
        return out
    def domains_for_sep(sep):
        domains=[]
        for members,states in zip(variables,var_states):
            if len(members)==1: domains.append(unary_domain(members[0],sep)); continue
            d0=unary_domain(members[0],sep); d1=unary_domain(members[1],sep); dm=0
            for k,(a,b) in enumerate(states):
                if ((d0>>a)&1) and ((d1>>b)&1): dm|=1<<k
            domains.append(dm)
        return tuple(domains)

    profiles=defaultdict(lambda:{'base_mass':0,'separator_states':[]})
    for row in base['separator_positive_marginal']:
        sep=tuple(map(int,row['states'])); dom=domains_for_sep(sep); profiles[dom]['base_mass']+=int(row['count']); profiles[dom]['separator_states'].append(list(sep))
    assert len(profiles)==10 and sum(v['base_mass'] for v in profiles.values())==int(base['exact_graph_count'])

    counter=ExactCounter(tuple(variables),tuple(var_states),tuple(var_weights),pairq)
    profile_rows=[]; total=0
    ordered=sorted(profiles.items(),key=lambda kv:sum(d.bit_count() for d in kv[0]))
    for idx,(domains,meta) in enumerate(ordered,1):
        value,calls,memo_states=counter.count_profile(domains); total+=meta['base_mass']*value
        row={'profile_index':idx,'separator_states':meta['separator_states'],'base_mass':meta['base_mass'],'domain_state_sum':sum(d.bit_count() for d in domains),'m4_pairwise_relaxation_count':value,'m4_pairwise_relaxation_log2':math.log2(value) if value else None,'recursive_calls':calls,'memo_states':memo_states}
        profile_rows.append(row); print('profile',idx,'/',len(ordered),json.dumps(row,sort_keys=True),flush=True)

    assert total==EXPECTED_EXACT_COUNT and total<EXPECTED_PR212_COUNT
    log2=math.log2(total)
    out={'position':'C','physical_shared_dimension':PHYS_N,'exact_count':total,'exact_log2':log2,'state_bits':total.bit_length(),'gap_vs_physical_log2_bits':log2-PHYS_N,'gain_vs_pr212_log2_bits':math.log2(EXPECTED_PR212_COUNT)-log2,'m4_outputs':90,'contracted_variables':88,'special_signed_pairs':[list(p) for p in SPECIAL_PAIRS],'exact_subset_pair_relations':825,'exact_equal_pair_relations':55,'exact_overlap_pair_relations':2000,'zero_cross_activity_only_relations':1125,'all_m4_pairs_covered':4005,'unique_separator_domain_profiles':len(profiles),'profile_rows':profile_rows,'decision':'C916_250WAY_WIDTH3_BASE_COMPLETE_M4_PAIRWISE_RELAXATION_EXACT'}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_COMPLETE_M4_PAIRWISE_RELAXATION_EXACT')
    print('scope=width3 base separator + four-parent unary domains + all 825 subset value factors + all 55 equal value factors + all 2000 overlap value factors + remaining 1125 zero-cross activity factors')
    print('important=the 1125 remaining zero-cross factors are intentionally activity-only until their exact value authority completes; projection triples, quadruples and all-order affine constraints are also outside this relaxation')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
