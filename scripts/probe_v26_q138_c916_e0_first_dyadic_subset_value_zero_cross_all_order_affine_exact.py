#!/usr/bin/env python3
import io, json, math, os, sys
from collections import Counter, defaultdict
from functools import lru_cache
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_subset_value_plus_complete_zero_cross_exact as Z
import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O

D, P = O.D, O.P
PARENT_GIDS = Z.PARENT_GIDS
PHYS_N = 149
EXPECTED_PR209_COUNT = Z.EXPECTED_COUNT
EXPECTED_PR209_LOG2 = math.log2(EXPECTED_PR209_COUNT)
EXPECTED_CODIM = {6: 12, 7: 46, 8: 32}
EXPECTED_M4_NORMAL_RANK = 92

BASE_PATH = Z.BASE_PATH
M4_PATH = Z.M4_PATH
SUBSET_PATH = Z.SUBSET_PATH

_INTERSECTIONS = {}

def canonical_affine(rows):
    rows = [int(x) for x in rows if int(x)]
    rank = 0
    mask = (1 << PHYS_N) - 1
    for p in range(PHYS_N - 1, -1, -1):
        pivot = next((i for i in range(rank, len(rows)) if (rows[i] >> p) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pr = rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> p) & 1):
                rows[i] ^= pr
        rank += 1
    for x in rows:
        if (x & mask) == 0 and ((x >> PHYS_N) & 1):
            return None
    return tuple(sorted((x for x in rows if x & mask), reverse=True))


def inter(a, b, stats=None):
    if not a: return b
    if not b: return a
    key = (a, b) if a <= b else (b, a)
    if key in _INTERSECTIONS:
        if stats is not None: stats['intersection_cache_hits'] += 1
        return _INTERSECTIONS[key]
    z = canonical_affine(a + b)
    _INTERSECTIONS[key] = z
    if stats is not None: stats['intersection_cache_misses'] += 1
    return z


def rebuild_anchors(gids):
    e0, _e1, _half = P.C.P.U.H.classify_patterns()
    grouped = defaultdict(list); raw = 0
    for zc in range(4):
        for zs, cls in e0[zc]:
            can = P.C.P.U.H.support_for(O.POS, zs, cls)
            if can is None: continue
            raw += 1; grouped[can].append((zs, cls))
    ordered = list(sorted(grouped.items(), key=lambda kv: kv[0]))
    assert raw == 577 and len(ordered) == 250
    anchors, codim, normals = {}, Counter(), []
    for gid in gids:
        can, sectors = ordered[gid]
        assert len(sectors) == 4
        _prank, _local, anchor = D.projection_anchor(can)
        rows = tuple((int(m), int(rhs)) for m, rhs in anchor['physical_support_constraints'])
        codim[len(rows)] += 1; normals.extend(m for m, _ in rows)
        aug = tuple(m | (rhs << PHYS_N) for m, rhs in rows)
        canaug = canonical_affine(aug)
        assert canaug is not None
        anchors[gid] = canaug
    assert dict(sorted(codim.items())) == EXPECTED_CODIM
    assert P.R.gf2_rank(normals) == EXPECTED_M4_NORMAL_RANK
    return anchors, dict(sorted(codim.items()))


def residual_component_count(nodes, adj, zw, ow, anchors, seed_aff, stats):
    active = set(nodes); factor = 1; aff = seed_aff
    while True:
        changed = False
        for v in tuple(sorted(active)):
            if ow[v] == 0:
                if zw[v] == 0: return 0
                factor *= zw[v]; active.remove(v)
                stats['forced_zero_unary'] += 1; changed = True
        if changed: continue
        forced = next((v for v in sorted(active) if zw[v] == 0), None)
        if forced is None: break
        v = forced
        if ow[v] == 0: return 0
        aff = inter(aff, anchors[v], stats)
        if aff is None:
            stats['affine_empty_prunes'] += 1; return 0
        factor *= ow[v]; stats['forced_nonzero_unary'] += 1
        nbr = adj[v] & active
        for u in tuple(sorted(nbr)):
            if zw[u] == 0: return 0
            factor *= zw[u]; active.remove(u); stats['forced_zero_neighbors'] += 1
        active.remove(v)

    comps = []
    unseen = set(active)
    while unseen:
        root = min(unseen); stack = [root]; comp = set()
        while stack:
            v = stack.pop()
            if v in comp: continue
            comp.add(v); stack.extend((adj[v] & unseen) - comp)
        unseen -= comp; comps.append(tuple(sorted(comp)))
    stats['max_residual_component'] = max(stats['max_residual_component'], max(map(len, comps), default=0))
    stats['residual_component_hist'].update(map(len, comps))
    assert max(map(len, comps), default=0) <= 4

    option_maps = []
    for comp in comps:
        cmap = defaultdict(int); k = len(comp)
        for bits in range(1 << k):
            selected = {comp[i] for i in range(k) if (bits >> i) & 1}
            if any((adj[v] & selected) for v in selected):
                continue
            ca = (); w = 1
            for v in comp:
                if v in selected:
                    w *= ow[v]; ca = inter(ca, anchors[v], stats)
                    if ca is None: break
                else:
                    w *= zw[v]
            if ca is not None and w:
                cmap[ca] += w
        if not cmap: return 0
        option_maps.append((comp, dict(cmap)))

    option_maps.sort(key=lambda cc: (-max((len(a) for a in cc[1]), default=0), len(cc[1]), -len(cc[0])))
    dp = {aff: factor}; stats['peak_affine_states'] = max(stats['peak_affine_states'], 1)
    for comp, cmap in option_maps:
        nd = defaultdict(int)
        for a, w in dp.items():
            for b, cw in cmap.items():
                na = inter(a, b, stats)
                if na is None: stats['global_affine_empty_prunes'] += 1
                else: nd[na] += w * cw
        dp = dict(nd)
        stats['peak_affine_states'] = max(stats['peak_affine_states'], len(dp))
        if not dp: return 0
    stats['final_affine_states_sum'] += len(dp)
    return sum(dp.values())


def synthetic_component_affine():
    nodes = (0,1,2)
    adj = {0:{1}, 1:{0}, 2:set()}
    zw = {0:1,1:2,2:1}; ow = {0:2,1:3,2:4}
    anchors = {0:(1,), 1:(2,), 2:(1 | (1 << PHYS_N),)}
    st = Counter(); st['max_residual_component']=0; st['peak_affine_states']=0; st['residual_component_hist']=Counter()
    got = residual_component_count(nodes, adj, zw, ow, anchors, (), st)
    brute = 0
    for bits in range(8):
        sel = {i for i in nodes if (bits>>i)&1}
        if any(adj[v] & sel for v in sel): continue
        a=(); w=1
        for v in nodes:
            if v in sel:
                w*=ow[v]; a=canonical_affine(a+anchors[v])
                if a is None: break
            else: w*=zw[v]
        if a is not None: brute += w
    assert got == brute
    _INTERSECTIONS.clear()
    return brute

def analyze():
    syn = synthetic_component_affine()
    base, m4, sub = Z.K.load(BASE_PATH), Z.K.load(M4_PATH), Z.K.load(SUBSET_PATH)
    assert int(base['exact_graph_count']) == Z.K.EXPECTED_BASE_COUNT
    assert base['graph_relation_digest_sha256'] == Z.K.EXPECTED_GRAPH_DIGEST
    assert base['separator_marginal_digest_sha256'] == Z.K.EXPECTED_MARG_DIGEST
    assert m4['four_parent_relation_digest_sha256'] == Z.K.EXPECTED_REL_DIGEST
    assert m4['zero_cross_pair_digest_sha256'] == Z.EXPECTED_ZC_DIGEST
    assert sub['relation_digest_sha256'] == Z.K.EXPECTED_SUBSET_DIGEST

    gids = tuple(map(int, m4['m4_group_ids']))
    rel = {(int(r['parent_group_id']), int(r['m4_group_id'])): r for r in m4['four_parent_relations']}
    dims = {g: int(rel[(PARENT_GIDS[0], g)]['cols']) for g in gids}
    zidx = {g: int(rel[(PARENT_GIDS[0], g)]['zero_index']) for g in gids}
    anchors, codim = rebuild_anchors(gids)

    for triple in m4['projection_minimal_empty_triples']:
        a = ()
        for g in map(int, triple): a = inter(a, anchors[g])
        assert a is None

    srel = {}; sadj = {g: set() for g in gids}
    for r in sub['relations']:
        a, b = int(r['left_group_id']), int(r['right_group_id'])
        srel[(a, b)] = r; sadj[a].add(b); sadj[b].add(a)
    hubs = tuple(sorted(g for g in gids if len(sadj[g]) == 75))
    leaves = tuple(sorted(g for g in gids if len(sadj[g]) == 11))
    isolates = tuple(sorted(g for g in gids if not sadj[g]))
    assert hubs == (19,20,23,61,83,129,134,139,140,157,232)
    assert isolates == (158,180,236,238) and len(leaves) == 75
    supports = {(h,l): Z.K.supports_from_relation(srel[(min(h,l),max(h,l))], h, l, dims) for h in hubs for l in leaves}

    H,L,I = set(hubs), set(leaves), set(isolates)
    hpos = {g:i for i,g in enumerate(hubs)}; hh = {h:0 for h in hubs}
    residual_nodes = leaves + isolates
    radj = {g:set() for g in residual_nodes}
    cats = Counter()
    zcpairs = {tuple(sorted(map(int,e))) for e in m4['zero_cross_pairs']}
    for a,b in zcpairs:
        ta = 'h' if a in H else 'l' if a in L else 'i'; tb = 'h' if b in H else 'l' if b in L else 'i'
        cats[''.join(sorted((ta,tb)))] += 1
        if a in H and b in H:
            hh[a] |= 1 << hpos[b]; hh[b] |= 1 << hpos[a]
        if a in radj and b in radj:
            radj[a].add(b); radj[b].add(a)
    assert cats == Counter({'ll':775,'il':300,'hl':183,'hi':44,'hh':10,'ii':6})
    for h in hubs:
        for i in isolates:
            assert tuple(sorted((h,i))) in zcpairs

    bm = {tuple(map(int,r['states'])): int(r['count']) for r in base['separator_positive_marginal']}
    profiles = {}
    for assn, mass in bm.items():
        smap = dict(zip(PARENT_GIDS, assn)); prof = {}
        for g in gids:
            d = (1 << dims[g]) - 1
            for p in PARENT_GIDS: d &= Z.K.allowed_parent_row(rel[(p,g)], smap[p])
            prof[g] = d
        key = tuple(prof[g] for g in gids)
        profiles.setdefault(key, {'prof':prof,'mass':0,'states':[]})
        profiles[key]['mass'] += mass; profiles[key]['states'].append(assn)
    assert len(profiles) == 10

    with redirect_stdout(io.StringIO()):
        zres = Z.analyze()
    assert int(zres['exact_count']) == EXPECTED_PR209_COUNT
    old_by_states = {tuple(sorted(tuple(map(int,x)) for x in r['separator_states'])): int(r['m4_exact_count']) for r in zres['profile_rows']}
    assert len(old_by_states) == 10

    def profile_count(prof):
        domains = {h: tuple(i for i in range(dims[h]) if (prof[h] >> i) & 1) for h in hubs}
        if any(not x for x in domains.values()) or any(not prof[g] for g in isolates):
            return 0, {'memo_states':0,'terminal_profiles':0}
        lm0 = tuple(prof[l] for l in leaves)
        def score(h):
            discr = sum(len({lm0[j] & supports[(h,l)][x] for x in domains[h]}) > 1 for j,l in enumerate(leaves))
            return (len(domains[h]), -discr, h)
        order = tuple(sorted(hubs, key=score))
        memo = {}; terminal_cache = {}; stats = Counter(); stats['max_residual_component'] = 0; stats['peak_affine_states'] = 0
        stats['residual_component_hist'] = Counter()

        def terminal(lm, nzmask, aff):
            key = (lm, nzmask, aff)
            if key in terminal_cache: return terminal_cache[key]
            masks = {l: lm[j] for j,l in enumerate(leaves)}
            for g in isolates: masks[g] = prof[g]
            if nzmask:
                for g in isolates: masks[g] &= 1 << zidx[g]
            zw = {}; ow = {}
            for g in residual_nodes:
                z = int(bool((masks[g] >> zidx[g]) & 1)); zw[g] = z; ow[g] = masks[g].bit_count() - z
            ans = residual_component_count(residual_nodes, radj, zw, ow, anchors, aff, stats)
            terminal_cache[key] = ans; return ans

        def rec(k, lm, nzmask, aff):
            key = (k, lm, nzmask, aff)
            if key in memo: return memo[key]
            if k == len(order):
                ans = terminal(lm, nzmask, aff)
                memo[key] = ans; return ans
            h = order[k]; hp = hpos[h]; total = 0
            for x in domains[h]:
                nz = x != zidx[h]
                if nz and (hh[h] & nzmask): continue
                na = aff
                if nz:
                    na = inter(aff, anchors[h], stats)
                    if na is None:
                        stats['hub_affine_empty_prunes'] += 1; continue
                arr = []; ok = True
                for j,l in enumerate(leaves):
                    nm = lm[j] & supports[(h,l)][x]
                    if not nm: ok = False; break
                    arr.append(nm)
                if ok: total += rec(k+1, tuple(arr), nzmask | ((1 << hp) if nz else 0), na)
            memo[key] = total; return total

        ans = rec(0, lm0, 0, ())
        outstats = {k:(dict(v) if isinstance(v, Counter) else v) for k,v in stats.items()}
        outstats.update({'memo_states':len(memo),'terminal_profiles':len(terminal_cache),'hub_order':list(order)})
        return ans, outstats

    baseline_total = 0; affine_total = 0; rows = []; agg = Counter(); comp_hist = Counter(); maxcomp = 0
    for pi,rec in enumerate(profiles.values(),1):
        prof = rec['prof']
        skey = tuple(sorted(tuple(map(int,x)) for x in rec['states']))
        old = old_by_states[skey]
        new, st = profile_count(prof)
        assert 0 <= new <= old
        baseline_total += rec['mass'] * old; affine_total += rec['mass'] * new
        for k,v in st.items():
            if k == 'residual_component_hist': comp_hist.update({int(a):int(b) for a,b in v.items()})
            elif k == 'max_residual_component': maxcomp = max(maxcomp, int(v))
            elif isinstance(v,int): agg[k] += v
        rows.append({'separator_states':[list(x) for x in rec['states']], 'base_mass':rec['mass'], 'm4_pr209_count':old,
                     'm4_all_order_affine_count':new, 'gain_log2':None if not new or not old else math.log2(old)-math.log2(new),
                     'stats':st})
        print('progress profile',pi,'/',len(profiles),'old',old,'new',new,flush=True)
    assert baseline_total == EXPECTED_PR209_COUNT
    assert 0 < affine_total <= baseline_total
    tlog = math.log2(affine_total)
    out = {
        'position':'C','physical_shared_dimension':PHYS_N,'synthetic_component_affine_count':syn,
        'pr209_baseline_count_crosscheck':baseline_total,
        'exact_count':affine_total,'exact_log2':tlog,'state_bits':(affine_total-1).bit_length(),
        'gain_vs_pr209_log2_bits':EXPECTED_PR209_LOG2-tlog,
        'gap_vs_physical_log2_bits':tlog-PHYS_N,
        'm4_projection_codimension_histogram':codim,'m4_projection_normal_span_rank':EXPECTED_M4_NORMAL_RANK,
        'complete_zero_cross_pairs':1318,'subset_value_relations':825,
        'frozen_projection_triples_crosschecked':len(m4['projection_minimal_empty_triples']),
        'max_residual_component':maxcomp,
        'residual_component_histogram_summed':dict(sorted(comp_hist.items())),
        'intersection_cache_entries':len(_INTERSECTIONS),
        'profile_rows':rows,
        'decision':'C916_250WAY_SUBSET_VALUE_ZERO_CROSS_ALL_ORDER_AFFINE_EXACT',
    }
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_SUBSET_VALUE_ZERO_CROSS_ALL_ORDER_AFFINE_EXACT')
    print('scope=exact contraction of width3 base + all-four unary domains + all 825 exact subset-support value relations + all 1318 zero-cross relations + exact all-order common projection-anchor intersection')
    print('important=generic non-subset non-zero-cross value-level m4 relations remain outside this factor model')
    print('ALPHA_PASS=0')
    return out

if __name__ == '__main__': analyze()
