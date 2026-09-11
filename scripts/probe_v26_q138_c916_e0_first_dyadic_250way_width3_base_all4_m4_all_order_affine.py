#!/usr/bin/env python3
import json, math, os, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_250way_four_singleton_separator_m4_hypergraph as S
import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O

D, P = O.D, O.P
PHYS_N = 149
PARENT_GIDS = (1, 2, 13, 14)
EXPECTED_BASE_COUNT = 103580346297435478039507934992782327762124800000
EXPECTED_PR204_COUNT = 2233670981288892478072240015308024902860886517440882932538367850057011239577059386904123759001600000
EXPECTED_PR194_LOG2 = 317.07255079311204
EXPECTED_REL_DIGEST = 'ce8af72024a4fdd2bdbe270e994dd21bef056e4a703a0e1a34235e646b18d32c'
EXPECTED_ZERO_DIGEST = '7ce0219e86206aeac622bd423b1341cb47f8681564f19319c96823fcb4d4fab1'
EXPECTED_GRAPH_DIGEST = 'ca316800fefcba61d7f295c4c3a224aaa724ce5e02ee9a1dda942212ee5724d8'
EXPECTED_MARG_DIGEST = 'bb05d63be837d3a5fc9b2d31653355eba1ecf6d9e059f583dcfbddb206d4fca7'
EXPECTED_CODIM = {6: 12, 7: 46, 8: 32}
BASE_PATH = Path(os.environ.get('C916_BASE_WIDTH3_AUTHORITY', 'authorities/base/c916_e0_first_dyadic_base160_width3_separator_authority.json'))
M4_PATH = Path(os.environ.get('C916_M4_AUTHORITY', 'authorities/m4/c916_e0_first_dyadic_four_separator_complete_authority.json'))


def load(path):
    assert path.is_file(), path
    return json.loads(path.read_text())


def marg(rows):
    out = {}
    for r in rows:
        s, c = tuple(map(int, r['states'])), int(r['count'])
        assert len(s) == 4 and c > 0 and s not in out
        out[s] = c
    return out


def allowed_row(rec, state):
    cols, zi = int(rec['cols']), int(rec['zero_index'])
    assert cols in (7, 9) and 0 <= zi < cols
    mask = int(rec['mask_hex'], 16)
    return tuple(bool((mask >> (state * cols + j)) & 1) for j in range(cols))


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


def rebuild_anchors(gids):
    e0, _e1, _half = P.C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for zc in range(4):
        for zs, cls in e0[zc]:
            can = P.C.P.U.H.support_for(O.POS, zs, cls)
            if can is None:
                continue
            raw += 1
            grouped[can].append((zs, cls))
    ordered = list(sorted(grouped.items(), key=lambda kv: kv[0]))
    assert raw == 577 and len(ordered) == 250
    anchors, codim, normals = [], Counter(), []
    for gid in gids:
        can, sectors = ordered[gid]
        assert len(sectors) == 4
        _prank, _local, anchor = D.projection_anchor(can)
        rows = tuple((int(m), int(rhs)) for m, rhs in anchor['physical_support_constraints'])
        codim[len(rows)] += 1
        normals.extend(m for m, _ in rows)
        aug = tuple(m | (rhs << PHYS_N) for m, rhs in rows)
        assert canonical_affine(aug) is not None
        anchors.append(aug)
    assert dict(sorted(codim.items())) == EXPECTED_CODIM
    assert P.R.gf2_rank(normals) == 92
    return tuple(anchors), dict(sorted(codim.items()))


def build_profiles(m4, states):
    gids = tuple(map(int, m4['m4_group_ids']))
    assert len(gids) == 90 and len(set(gids)) == 90
    rel = {}
    for rec in m4['four_parent_relations']:
        key = (int(rec['parent_group_id']), int(rec['m4_group_id']))
        assert key not in rel
        rel[key] = rec
    assert len(rel) == 360
    profiles, state_profile = {}, {}
    for assn in states:
        smap = dict(zip(PARENT_GIDS, assn))
        zw, ow = [], []
        for mg in gids:
            rows = [allowed_row(rel[(pg, mg)], smap[pg]) for pg in PARENT_GIDS]
            allowed = tuple(all(r[j] for r in rows) for j in range(len(rows[0])))
            zi = int(rel[(PARENT_GIDS[0], mg)]['zero_index'])
            zw.append(int(allowed[zi]))
            ow.append(sum(int(allowed[j]) for j in range(len(allowed)) if j != zi))
        prof = (tuple(zw), tuple(ow))
        profiles.setdefault(prof, []).append(assn)
        state_profile[assn] = prof
    return gids, profiles, state_profile


def build_adj(gids, m4):
    local = {g: i for i, g in enumerate(gids)}
    adj = [0] * 90
    assert len(m4['zero_cross_pairs']) == 1318
    for a, b in m4['zero_cross_pairs']:
        u, v = local[int(a)], local[int(b)]
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    assert sum(x.bit_count() for x in adj) == 2636
    return tuple(adj), local


def count_affine(zw, ow, adj, anchors):
    memo = {}
    stats = Counter()

    def rec(active, aff):
        stats['recursive_calls'] += 1
        if not active:
            return 1
        key = (active, aff)
        if key in memo:
            return memo[key]
        vs = [i for i in range(90) if (active >> i) & 1]
        v = max(vs, key=lambda i: ((adj[i] & active).bit_count(), len(anchors[i]), zw[i] + ow[i], -i))
        bit = 1 << v
        z0 = zw[v] * rec(active & ~bit, aff) if zw[v] else 0
        z1 = 0
        if ow[v]:
            na = canonical_affine(aff + anchors[v])
            if na is None:
                stats['affine_empty_prunes'] += 1
            else:
                stats['max_affine_rank'] = max(stats['max_affine_rank'], len(na))
                nbr = adj[v] & active
                factor = 1
                x = nbr
                while x:
                    b = x & -x
                    u = b.bit_length() - 1
                    factor *= zw[u]
                    if not factor:
                        break
                    stats['forced_zero_neighbors'] += 1
                    x ^= b
                if factor:
                    z1 = ow[v] * factor * rec(active & ~bit & ~nbr, na)
        memo[key] = z0 + z1
        return memo[key]

    total = rec((1 << 90) - 1, tuple())
    stats['memo_states'] = len(memo)
    return total, dict(stats)


def synthetic():
    anchors = (
        (1,),
        (2,),
        (3 | (1 << PHYS_N),),
        (4,),
    )
    zw, ow, adj = (1, 1, 1, 1), (2, 3, 4, 2), (0, 0, 0, 0)
    got, _st = count_affine(zw + (1,) * 86, ow + (0,) * 86, adj + (0,) * 86, anchors + ((),) * 86)
    brute = 0
    for sel in range(16):
        aug, w = [], 1
        for i in range(4):
            if (sel >> i) & 1:
                aug += list(anchors[i]); w *= ow[i]
            else:
                w *= zw[i]
        if canonical_affine(tuple(aug)) is not None:
            brute += w
    assert got == brute
    return brute


def analyze():
    syn = synthetic()
    base, m4 = load(BASE_PATH), load(M4_PATH)
    assert int(base['exact_graph_count']) == EXPECTED_BASE_COUNT
    assert base['graph_relation_digest_sha256'] == EXPECTED_GRAPH_DIGEST
    assert base['separator_marginal_digest_sha256'] == EXPECTED_MARG_DIGEST
    assert m4['four_parent_relation_digest_sha256'] == EXPECTED_REL_DIGEST
    assert m4['zero_cross_pair_digest_sha256'] == EXPECTED_ZERO_DIGEST
    assert tuple(map(int, base['separator_group_ids'])) == PARENT_GIDS
    assert tuple(map(int, m4['separator_group_ids'])) == PARENT_GIDS
    bm = marg(base['separator_positive_marginal'])
    assert len(bm) == 36 and sum(bm.values()) == EXPECTED_BASE_COUNT
    gids, profiles, state_profile = build_profiles(m4, tuple(bm))
    anchors, codim = rebuild_anchors(gids)
    adj, local = build_adj(gids, m4)
    for triple in m4['projection_minimal_empty_triples']:
        aug = ()
        for g in triple:
            aug += anchors[local[int(g)]]
        assert canonical_affine(aug) is None
    old_edges = []
    for a, b in m4['zero_cross_pairs']:
        old_edges.append((1 << local[int(a)]) | (1 << local[int(b)]))
    for a, b, c in m4['projection_minimal_empty_triples']:
        old_edges.append((1 << local[int(a)]) | (1 << local[int(b)]) | (1 << local[int(c)]))
    state_old, selected = {}, {}
    for prof, ss in profiles.items():
        old, _ = S.weighted_count(90, prof[0], prof[1], tuple(old_edges))
        for s in ss:
            state_old[s] = old
        if old:
            selected[prof] = (ss, old)
    assert sum(bm[s] * state_old[s] for s in bm) == EXPECTED_PR204_COUNT
    assert len(selected) == 7
    new_profile, statsum = {}, Counter()
    for i, (prof, (ss, old)) in enumerate(selected.items(), 1):
        new, st = count_affine(prof[0], prof[1], adj, anchors)
        assert 0 <= new <= old
        new_profile[prof] = new
        statsum.update(st)
        print('progress profile', i, '/', len(selected), 'states', len(ss), 'old', old, 'new', new, flush=True)
    total = sum(bm[s] * new_profile.get(state_profile[s], 0) for s in bm)
    assert 0 < total <= EXPECTED_PR204_COUNT
    tlog = math.log2(total)
    decision = ('C916_250WAY_WIDTH3_BASE_ALL4_M4_ALL_ORDER_AFFINE_BELOW_PHYSICAL_149' if total < (1 << PHYS_N)
                else 'C916_250WAY_WIDTH3_BASE_ALL4_M4_ALL_ORDER_AFFINE_BEATS_PR194' if tlog < EXPECTED_PR194_LOG2
                else 'C916_250WAY_WIDTH3_BASE_ALL4_M4_ALL_ORDER_AFFINE_STRICTLY_BEATS_PR204' if total < EXPECTED_PR204_COUNT
                else 'C916_250WAY_WIDTH3_BASE_ALL4_M4_ALL_ORDER_AFFINE_NO_GAIN')
    out = {
        'position': 'C', 'physical_shared_dimension': PHYS_N,
        'synthetic_regression_count': syn,
        'base_width3_count': EXPECTED_BASE_COUNT,
        'base_positive_separator_states': len(bm),
        'm4_outputs': 90,
        'm4_projection_codimension_histogram': codim,
        'm4_projection_normal_span_rank': 92,
        'complete_zero_cross_pairs': 1318,
        'frozen_projection_triples_crosschecked': 5,
        'base_supported_unique_weight_profiles': len(profiles),
        'old_positive_unique_weight_profiles': len(selected),
        'exact_assignment_count': total,
        'exact_log2': tlog,
        'state_bits': (total - 1).bit_length(),
        'gain_vs_pr204_bits': math.log2(EXPECTED_PR204_COUNT) - tlog,
        'gain_vs_pr194_width3_bits': EXPECTED_PR194_LOG2 - tlog,
        'gap_vs_physical_log2_bits': tlog - PHYS_N,
        'dp_stats_summed': dict(statsum),
        'decision': decision,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_250WAY_WIDTH3_BASE_ALL4_M4_ALL_ORDER_AFFINE')
    print('scope=exact selected-factor count using PR203 width3 base marginal, all-four singleton-to-m4 label intersections, all 1318 exact zero-cross pairs, and exact all-order common projection-anchor intersection')
    print('theorem=every nonzero m4 output requires membership in its projection anchor, so every simultaneously nonzero selected set must have a nonempty common affine-anchor intersection')
    print('important=this enforces all higher-order projection-support incompatibilities but still does not enforce generic non-zero-cross m4 value relations')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
