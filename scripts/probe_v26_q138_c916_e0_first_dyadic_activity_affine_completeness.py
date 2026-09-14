#!/usr/bin/env python3
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_complete_pairwise_all_order_affine_scout as A
import probe_v26_q138_c916_e0_first_dyadic_pr212_plus_projection_triples_quads_exact as H

EXPECTED_ZERO_CROSS_PAIRS = 1318
EXPECTED_GRAPH_MAXIMAL_INDEPENDENT_SETS = 69
EXPECTED_GRAPH_MIS_DIGEST = 'eef9959583725463674c69c0a4abd0635088af735f4f2d5ff90d2066d2559d94'
EXPECTED_GRAPH_MIS_SIZE_HIST = {1: 4, 22: 1, 63: 32, 65: 32}
EXPECTED_COVER_SETS = 9185
EXPECTED_COVER_DIGEST = '78b385d674bb3d6ef2af2d03e655d4d03c230ea58206a5a1f0c59ace2964e94b'
EXPECTED_COVER_SIZE_HIST = {1: 4, 22: 1, 56: 768, 57: 1056, 58: 2520, 59: 2056, 60: 1906, 61: 744, 62: 122, 63: 8}


def affine_of(gids, anchors):
    rows = []
    for gid in gids:
        rows.extend(anchors[int(gid)])
    return A.canonical(rows)


def minimal_transversals(edges):
    """Exact antichain DP for all minimal hitting sets of a small hypergraph."""
    trans = {frozenset()}
    for edge in edges:
        candidates = set()
        e = set(map(int, edge))
        for h in trans:
            if h & e:
                candidates.add(h)
            else:
                for gid in e:
                    candidates.add(h | {gid})
        ordered = sorted(candidates, key=lambda h: (len(h), tuple(sorted(h))))
        keep = []
        for h in ordered:
            if any(k <= h for k in keep):
                continue
            keep.append(h)
        trans = set(keep)
    return tuple(sorted((tuple(sorted(h)) for h in trans), key=lambda h: (len(h), h)))


def maximal_independent_sets(gids, conflicts):
    """Deterministic Bron-Kerbosch on the compatibility graph."""
    gids = tuple(sorted(map(int, gids)))
    n = len(gids)
    pos = {g: i for i, g in enumerate(gids)}
    allmask = (1 << n) - 1
    bad = [0] * n
    for u, v in conflicts:
        i = pos[int(u)]
        j = pos[int(v)]
        assert i != j
        bad[i] |= 1 << j
        bad[j] |= 1 << i
    compat = tuple(allmask ^ bad[i] ^ (1 << i) for i in range(n))
    found = []

    def bronk(r, p, x):
        if not (p | x):
            found.append(tuple(gids[i] for i in range(n) if (r >> i) & 1))
            return
        union = p | x
        pivot = None
        scan = union
        while scan:
            bit = scan & -scan
            i = bit.bit_length() - 1
            scan ^= bit
            score = (p & compat[i]).bit_count()
            cand = (score, -i)
            if pivot is None or cand > pivot[0]:
                pivot = (cand, i)
        u = pivot[1]
        candidates = p & ~compat[u] & allmask
        while candidates:
            bit = candidates & -candidates
            i = bit.bit_length() - 1
            candidates ^= bit
            bronk(r | bit, p & compat[i], x & compat[i])
            p &= ~bit
            x |= bit

    bronk(0, allmask, 0)
    return tuple(sorted(set(found), key=lambda row: (len(row), row)))


def minimize_inconsistent(active, anchors):
    core = list(sorted(map(int, active)))
    assert affine_of(core, anchors) is None
    changed = True
    while changed:
        changed = False
        for gid in tuple(core):
            trial = [g for g in core if g != gid]
            if affine_of(trial, anchors) is None:
                core = trial
                changed = True
    core = tuple(core)
    assert affine_of(core, anchors) is None
    for gid in core:
        assert affine_of([g for g in core if g != gid], anchors) is not None
    return core


def digest_rows(rows):
    return hashlib.sha256(json.dumps(tuple(rows), separators=(',', ':')).encode()).hexdigest()


def analyze():
    m4 = C.load(C.M4_PATH)
    gids = tuple(map(int, m4['m4_group_ids']))
    assert len(gids) == len(set(gids)) == 90
    triples = tuple(tuple(map(int, row)) for row in m4['projection_minimal_empty_triples'])
    quads = tuple(tuple(map(int, row)) for row in H.QUADS)
    assert len(triples) == 5 and len(quads) == 7
    higher = triples + quads

    zero_cross = tuple(sorted({tuple(sorted(map(int, pair))) for pair in m4['zero_cross_pairs']}))
    assert len(zero_cross) == EXPECTED_ZERO_CROSS_PAIRS
    zero_cross_set = set(zero_cross)

    # The 12 higher clauses are genuinely beyond the exact pairwise activity
    # conflicts: none contains one of the 1,318 zero-cross forbidden pairs.
    for edge in higher:
        assert not any(tuple(sorted((edge[i], edge[j]))) in zero_cross_set for i in range(len(edge)) for j in range(i + 1, len(edge))), edge

    anchors = A.rebuild_anchors(gids)
    assert set(anchors) == set(gids)

    # Re-certify all 12 higher obstructions in the exact affine algebra.
    for edge in higher:
        assert affine_of(edge, anchors) is None, edge
        for gid in edge:
            assert affine_of([g for g in edge if g != gid], anchors) is not None, (edge, gid)

    # The earlier 12-only global scout found {240,246}; pin down why that was a
    # relaxation artifact rather than a finite-model gap.
    assert (240, 246) in zero_cross_set
    assert affine_of((240, 246), anchors) is None

    # Any exact pairwise assignment has an activity support independent in the
    # zero-cross graph. Every such support extends to one of these maximal graph
    # independent sets.
    graph_maximal = maximal_independent_sets(gids, zero_cross)
    graph_digest = digest_rows(graph_maximal)
    graph_hist = dict(sorted(Counter(map(len, graph_maximal)).items()))
    assert len(graph_maximal) == EXPECTED_GRAPH_MAXIMAL_INDEPENDENT_SETS
    assert graph_digest == EXPECTED_GRAPH_MIS_DIGEST
    assert graph_hist == EXPECTED_GRAPH_MIS_SIZE_HIST

    # Within each maximal graph-independent set M, the only remaining known
    # support clauses are whichever triples/quads lie wholly in M. If S subset M
    # avoids them, M\S is a hitting set and therefore contains a minimal hitting
    # set H. Hence S subseteq M\H. Checking all M\H gives an exact finite cover of
    # every support admitted by the 1,318 pair conflicts plus 12 higher clauses.
    cover = set()
    local_transversal_hist = Counter()
    for maximal in graph_maximal:
        mset = set(maximal)
        contained = tuple(edge for edge in higher if set(edge) <= mset)
        trans = minimal_transversals(contained) if contained else ((),)
        local_transversal_hist[(len(maximal), len(contained), len(trans))] += 1
        for hitting in trans:
            candidate = tuple(sorted(mset - set(hitting)))
            assert all(tuple(sorted((candidate[i], candidate[j]))) not in zero_cross_set for i in range(len(candidate)) for j in range(i + 1, len(candidate)))
            cset = set(candidate)
            assert all(not set(edge) <= cset for edge in higher)
            cover.add(candidate)

    cover = tuple(sorted(cover, key=lambda row: (len(row), row)))
    cover_digest = digest_rows(cover)
    cover_hist = dict(sorted(Counter(map(len, cover)).items()))
    assert len(cover) == EXPECTED_COVER_SETS
    assert cover_digest == EXPECTED_COVER_DIGEST
    assert cover_hist == EXPECTED_COVER_SIZE_HIST

    bad = None
    checked = 0
    rank_hist = Counter()
    for active in cover:
        aff = affine_of(active, anchors)
        checked += 1
        if aff is None:
            bad = minimize_inconsistent(active, anchors)
            break
        rank_hist[len(aff)] += 1

    complete = bad is None
    novel = None
    if bad is not None:
        badset = set(bad)
        assert not any(set(pair) <= badset for pair in zero_cross)
        assert all(not set(edge) <= badset for edge in higher)
        novel = list(bad)

    out = {
        'position': 'C',
        'physical_shared_dimension': A.PHYS_N,
        'global_projection_normal_rank': A.EXPECTED_NORMAL_RANK,
        'm4_outputs': len(gids),
        'exact_pairwise_activity_conflicts': len(zero_cross),
        'higher_projection_clauses': len(higher),
        'known_triples': len(triples),
        'known_quadruples': len(quads),
        'twelve_only_counterexample_already_pairwise_forbidden': [240, 246],
        'graph_maximal_independent_sets': len(graph_maximal),
        'graph_maximal_independent_set_digest_sha256': graph_digest,
        'graph_maximal_independent_set_size_histogram': graph_hist,
        'finite_support_cover_sets': len(cover),
        'finite_support_cover_digest_sha256': cover_digest,
        'finite_support_cover_size_histogram': cover_hist,
        'local_transversal_shape_histogram': {str(k): v for k, v in sorted(local_transversal_hist.items())},
        'cover_sets_checked_for_affine_consistency': checked,
        'consistent_affine_rank_histogram': dict(sorted(rank_hist.items())),
        'pairwise_plus_12_support_constraints_imply_all_order_affine': complete,
        'novel_minimal_affine_conflict_not_implied_by_known_support_constraints': novel,
        'decision': 'C916_PAIRWISE_PLUS_12_SUPPORT_AFFINE_COMPLETENESS_COVER',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    if complete:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PAIRWISE_PLUS_12_AFFINE_COMPLETENESS')
        print('theorem=every gid activity support admitted by the exact 1,318 zero-cross pair conflicts plus the five projection triples and seven projection quadruples is affine-consistent: 69 maximal zero-cross-independent supports reduce to a frozen exact cover of 9,185 higher-clause-valid supersets, and every cover set has nonempty exact affine intersection')
        print('consequence=within the complete exact 4,005-pair value model, adding the 12 frozen projection hyperedges is sufficient for the all-order affine-intersection condition because affine anchors depend only on gid zero/nonzero activity')
    else:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PAIRWISE_PLUS_12_AFFINE_COUNTEREXAMPLE')
        print('theorem=the emitted inclusion-minimal affine conflict is not implied by any exact zero-cross pair conflict or by the 12 frozen higher projection clauses')
    print('boundary=any physical-image constraint stronger than all-order affine intersection remains outside this theorem')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
