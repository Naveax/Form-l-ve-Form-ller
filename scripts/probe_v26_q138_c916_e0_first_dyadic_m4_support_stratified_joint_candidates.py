#!/usr/bin/env python3
import hashlib, io, json, math, sys
from collections import Counter
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O
import probe_v26_q138_c916_e0_first_dyadic_singleton_m2_cross_joint_image as X
P, PHYS_N, POS, K = O.P, O.PHYS_N, O.POS, 12
assert PHYS_N == 149


def signed_cells(terms, ambient, icache, mcache):
    terms = tuple(terms); n = len(terms); assert 1 <= n <= 6
    full = (1 << n) - 1
    def exact(active, char):
        total = 0
        for u in X.submasks(full ^ active):
            z = X.character_moment(terms, active | u, char, ambient, icache, mcache)
            total += -z if u.bit_count() & 1 else z
        return total
    out = Counter()
    for active in range(full + 1):
        size = exact(active, 0); assert size >= 0
        if not size: continue
        chars = {c: exact(active, c) for c in X.submasks(active)}
        div = 1 << active.bit_count()
        for neg in X.submasks(active):
            num = sum(-w if (neg & c).bit_count() & 1 else w for c, w in chars.items())
            assert num % div == 0
            pop = num // div; assert pop >= 0
            if pop: out[(active, neg)] += pop
    assert sum(out.values()) == 1 << ambient
    return out


def pair_census(parent, m4, ambient, icache, mcache):
    pt, mt = tuple(parent['terms']), tuple(m4['terms'])
    assert len(pt) == 2 and len(mt) == 4
    terms = pt + mt; assert len({int(t['term_id']) for t in terms}) == 6
    counts = Counter()
    for (active, neg), pop in signed_cells(terms, ambient, icache, mcache).items():
        pv = mv = 0
        for i, t in enumerate(terms):
            if not ((active >> i) & 1): continue
            z = int(t['coefficient']); z = -z if ((neg >> i) & 1) else z
            if i < 2: pv += z
            else: mv += z
        counts[(pv, mv)] += pop
    pm, mm = Counter(), Counter()
    for (pv, mv), pop in counts.items(): pm[pv] += pop; mm[mv] += pop
    return counts, dict(sorted(pm.items())), dict(sorted(mm.items()))


def support_meta(pgid, mgid, census, groups):
    rel, inter = P.support_relation(groups[pgid]['projection_anchor'], groups[mgid]['projection_anchor'], PHYS_N)
    return {'parent_group_id': pgid, 'm4_group_id': mgid,
            'parent_multiplicity': census[pgid]['multiplicity'],
            'parent_image_size': census[pgid]['image_size'],
            'm4_image_size': census[mgid]['image_size'],
            'projection_support_relation': rel,
            'projection_intersection_dimension': None if inter is None else len(inter[2])}


def select(mgid, parents, small_m2, census, groups):
    recs = {p: support_meta(p, mgid, census, groups) for p in parents}; chosen = {}
    def add(p, why):
        if p not in chosen: chosen[p] = dict(recs[p], selection_reason=why)
    for p in small_m2: add(p, 'all_3state_m2')
    by = {r: [x for x in recs.values() if x['projection_support_relation'] == r]
          for r in ('equal','left_subset_right','right_subset_left','overlap_incomparable','disjoint')}
    key = lambda x: (x['parent_image_size'], -(x['projection_intersection_dimension'] if x['projection_intersection_dimension'] is not None else -1), x['parent_group_id'])
    for rel in ('equal','left_subset_right','right_subset_left','disjoint'):
        if by[rel]: add(min(by[rel], key=key)['parent_group_id'], rel + '_representative')
    if by['overlap_incomparable']:
        lo = min(by['overlap_incomparable'], key=lambda x: (x['projection_intersection_dimension'], x['parent_image_size'], x['parent_group_id']))
        hi = min(by['overlap_incomparable'], key=lambda x: (-x['projection_intersection_dimension'], x['parent_image_size'], x['parent_group_id']))
        add(lo['parent_group_id'], 'overlap_min_intersection'); add(hi['parent_group_id'], 'overlap_max_intersection')
    pri = {'equal':0,'left_subset_right':1,'right_subset_left':1,'overlap_incomparable':2,'disjoint':3}
    fill = sorted(recs.values(), key=lambda x: (pri[x['projection_support_relation']], x['parent_image_size'], -(x['projection_intersection_dimension'] if x['projection_intersection_dimension'] is not None else -1), x['parent_group_id']))
    for x in fill:
        if len(chosen) >= K: break
        add(x['parent_group_id'], 'structural_fill')
    assert len(chosen) == K
    return tuple(chosen[p] for p in sorted(chosen))


def synthetic():
    n = 4
    anchors = [P.make_synthetic_anchor((), n, 'linear'), P.make_synthetic_anchor(((1,0),), n, 'quadratic'),
               P.make_synthetic_anchor(((2,1),), n, 'one'), P.make_synthetic_anchor(((4,0),), n, 'linear'),
               P.make_synthetic_anchor(((8,1),), n, 'quadratic'), P.make_synthetic_anchor(((1,1),(4,0)), n, 'one')]
    def term(i, a, c): return {'term_id':i,'group_id':-1,'kind':'synthetic','coefficient':c,'anchor':a,'ambient_dimension':n}
    p = {'terms': (term(1,anchors[0],1), term(2,anchors[1],2))}
    m = {'terms': tuple(term(3+i, anchors[2+i], (1,-1,2,-2)[i]) for i in range(4))}
    got, _, _ = pair_census(p, m, n, {}, {})
    brute = Counter((X.eval_group(p,x), X.eval_group(m,x)) for x in range(1 << n))
    assert got == brute
    return {'cases':1,'domain_points_checked':1 << n}


def mask(counts, pvals, mvals):
    out = bit = 0
    for pv in pvals:
        for mv in mvals:
            if (pv,mv) in counts: out |= 1 << bit
            bit += 1
    return out


def analyze():
    syn = synthetic()
    with redirect_stdout(io.StringIO()): census, groups = O.build_authority()
    parents = tuple(g for g in range(250) if census[g]['multiplicity'] in (1,2))
    m4s = tuple(g for g in range(250) if census[g]['multiplicity'] == 4)
    small = tuple(g for g in parents if census[g]['multiplicity'] == 2 and census[g]['image_size'] == 3)
    assert len(parents) == 160 and len(m4s) == 90 and len(small) == 6
    selected = {m: select(m, parents, small, census, groups) for m in m4s}
    assert sum(map(len, selected.values())) == 1080
    sel_rel, sel_reason = Counter(), Counter()
    for rows in selected.values():
        for r in rows: sel_rel[r['projection_support_relation']] += 1; sel_reason[r['selection_reason']] += 1
    icache, mcache = {}, {}; joint_hist, cart_hist, miss_hist, save_hist = Counter(), Counter(), Counter(), Counter()
    strict_rel, strict_kind, strict_m4, strongest, best, dig = Counter(), Counter(), set(), [], {}, []
    checks = strict = 0
    for mgid in m4s:
        mcounts = census[mgid]['counts']; mvals = tuple(sorted(mcounts)); b = None
        for meta in selected[mgid]:
            pgid = meta['parent_group_id']; pcounts = census[pgid]['counts']; pvals = tuple(sorted(pcounts))
            counts, pm, mm = pair_census(groups[pgid], groups[mgid], PHYS_N, icache, mcache)
            assert pm == pcounts and mm == mcounts; checks += 2
            cart, size = len(pvals)*len(mvals), len(counts); missing = cart-size
            bits = (len(pvals)-1).bit_length() + (len(mvals)-1).bit_length() - (size-1).bit_length()
            density = Fraction(size, cart); gain = math.log2(cart)-math.log2(size); rm = mask(counts,pvals,mvals)
            dig.append(f'{pgid}|{mgid}|{len(pvals)}x{len(mvals)}|{rm:x}')
            cart_hist[cart] += 1; joint_hist[size] += 1; miss_hist[missing] += 1; save_hist[bits] += 1
            row = dict(meta, cartesian_image_size=cart, joint_image_size=size, missing_cartesian_states=missing,
                       integer_bit_saving=bits, exact_cardinality_gain_log2=gain, relation_mask_hex=f'{rm:x}')
            if size < cart:
                strict += 1; strict_m4.add(mgid); strict_rel[meta['projection_support_relation']] += 1
                strict_kind['singleton' if census[pgid]['multiplicity']==1 else 'm2'] += 1
                strongest.append((density,size,pgid,mgid,row))
            k = (density,size,meta['parent_image_size'],pgid)
            if b is None or k < b[0]: b = (k,row)
        best[mgid] = b[1]
    assert checks == 2160
    strongest.sort(key=lambda x:(x[0],x[1],x[2],x[3]))
    best_joint, best_den, best_kind = Counter(), Counter(), Counter()
    for row in best.values():
        best_joint[row['joint_image_size']] += 1; best_den[f"{row['joint_image_size']}/{row['cartesian_image_size']}"] += 1
        best_kind['singleton' if census[row['parent_group_id']]['multiplicity']==1 else 'm2'] += 1
    decision = ('M4_SUPPORT_STRATIFIED_ALL_OUTPUTS_HAVE_SUBCARTESIAN_PARENT_CANDIDATE' if len(strict_m4)==90 else
                'M4_SUPPORT_STRATIFIED_PARTIAL_SUBCARTESIAN_PARENT_CANDIDATES_FOUND' if strict else
                'M4_SUPPORT_STRATIFIED_NO_SUBCARTESIAN_PARENT_CANDIDATE_IN_SAMPLE')
    out = {'position':POS,'physical_shared_dimension':PHYS_N,'parent_outputs':160,'multiplicity4_outputs':90,
           'three_state_m2_parents':list(small),'target_candidates_per_m4':K,'candidate_pairs':1080,
           'synthetic_six_term_regression':syn,'pair_marginal_crosschecks':checks,
           'selected_support_relation_histogram':dict(sorted(sel_rel.items())),'selection_reason_histogram':dict(sorted(sel_reason.items())),
           'cartesian_pair_image_size_histogram':dict(sorted(cart_hist.items())),'joint_image_size_histogram':dict(sorted(joint_hist.items())),
           'missing_cartesian_state_histogram':dict(sorted(miss_hist.items())),'integer_bit_saving_histogram':dict(sorted(save_hist.items())),
           'subcartesian_candidate_pairs':strict,'m4_outputs_with_subcartesian_candidate':len(strict_m4),
           'm4_outputs_without_subcartesian_candidate':90-len(strict_m4),'strict_support_relation_histogram':dict(sorted(strict_rel.items())),
           'strict_parent_kind_histogram':dict(sorted(strict_kind.items())),'best_candidate_joint_image_histogram':dict(sorted(best_joint.items())),
           'best_candidate_density_histogram':dict(sorted(best_den.items())),'best_candidate_parent_kind_histogram':dict(sorted(best_kind.items())),
           'strongest_candidate_pairs_top40':[x[-1] for x in strongest[:40]],'best_candidate_by_m4':{str(k):v for k,v in best.items()},
           'candidate_relation_digest_sha256':hashlib.sha256(('\n'.join(sorted(dig))+'\n').encode()).hexdigest(),
           'cached_support_intersections':len(icache),'cached_character_moments':len(mcache),'decision':decision}
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_SUPPORT_STRATIFIED_JOINT_CANDIDATES')
    print('scope=exact six-term joint-image census on 12 deterministic support-stratified parents per m4 output, including all six 3-state m2 parents')
    print('important=this is a search layer, not an exhaustive 14400-pair parent-by-m4 theorem; a missing strict relation would be inconclusive')
    print('next=combine these relation matrices with the frozen 160-way tree marginals and attach m4 leaves by exact incremental assignment count')
    print('ALPHA_PASS=0')
    return out

if __name__ == '__main__': analyze()
