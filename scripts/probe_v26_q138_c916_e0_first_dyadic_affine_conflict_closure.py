#!/usr/bin/env python3
import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_activity_affine_completeness as Q
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_complete_pairwise_all_order_affine_scout as A
import probe_v26_q138_c916_e0_first_dyadic_pr212_plus_projection_triples_quads_exact as H

KNOWN_FIVE = (4, 5, 8, 9, 114)
MAX_NEW = int(os.environ.get('C916_AFFINE_CLOSURE_MAX_NEW', '64'))


def digest_rows(rows):
    payload = json.dumps(tuple(tuple(map(int, row)) for row in rows), separators=(',', ':'))
    return hashlib.sha256(payload.encode()).hexdigest()


def inclusion_maximal(rows):
    ordered = sorted((tuple(sorted(map(int, row))) for row in rows), key=lambda r: (-len(r), r))
    keep = []
    keep_sets = []
    for row in ordered:
        s = frozenset(row)
        if any(s <= t for t in keep_sets):
            continue
        keep.append(row)
        keep_sets.append(s)
    return tuple(sorted(keep, key=lambda r: (len(r), r)))


def build_cover(graph_maximal, higher, zero_cross_set):
    raw = set()
    local_shapes = Counter()
    for maximal in graph_maximal:
        mset = set(maximal)
        contained = tuple(edge for edge in higher if set(edge) <= mset)
        trans = Q.minimal_transversals(contained) if contained else ((),)
        local_shapes[(len(maximal), len(contained), len(trans))] += 1
        for hitting in trans:
            candidate = tuple(sorted(mset - set(hitting)))
            cset = set(candidate)
            assert all(not set(edge) <= cset for edge in higher)
            assert not any(set(pair) <= cset for pair in zero_cross_set)
            raw.add(candidate)
    raw = tuple(sorted(raw, key=lambda r: (len(r), r)))
    maximal = inclusion_maximal(raw)
    return raw, maximal, local_shapes


def analyze():
    m4 = C.load(C.M4_PATH)
    gids = tuple(map(int, m4['m4_group_ids']))
    assert len(gids) == len(set(gids)) == 90
    triples = tuple(tuple(map(int, row)) for row in m4['projection_minimal_empty_triples'])
    quads = tuple(tuple(map(int, row)) for row in H.QUADS)
    assert len(triples) == 5 and len(quads) == 7

    zero_cross = tuple(sorted({tuple(sorted(map(int, pair))) for pair in m4['zero_cross_pairs']}))
    assert len(zero_cross) == Q.EXPECTED_ZERO_CROSS_PAIRS == 1318
    zero_cross_set = tuple(frozenset(pair) for pair in zero_cross)

    graph_maximal = Q.maximal_independent_sets(gids, zero_cross)
    assert len(graph_maximal) == Q.EXPECTED_GRAPH_MAXIMAL_INDEPENDENT_SETS
    assert Q.digest_rows(graph_maximal) == Q.EXPECTED_GRAPH_MIS_DIGEST

    anchors = A.rebuild_anchors(gids)
    assert set(anchors) == set(gids)

    higher = list(triples + quads + (KNOWN_FIVE,))
    for edge in higher:
        assert Q.affine_of(edge, anchors) is None, edge
        for gid in edge:
            assert Q.affine_of([g for g in edge if g != gid], anchors) is not None, (edge, gid)
        eset = set(edge)
        assert not any(pair <= eset for pair in zero_cross_set), edge

    discovered = []
    rounds = []
    complete = False
    capped = False

    while True:
        raw_cover, maximal_cover, local_shapes = build_cover(graph_maximal, tuple(higher), zero_cross_set)
        rank_hist = Counter()
        bad_cores = set()
        checked = 0
        for active in maximal_cover:
            aff = Q.affine_of(active, anchors)
            checked += 1
            if aff is None:
                core = tuple(Q.minimize_inconsistent(active, anchors))
                cset = set(core)
                assert not any(pair <= cset for pair in zero_cross_set)
                assert all(not set(edge) <= cset for edge in higher)
                bad_cores.add(core)
            else:
                rank_hist[len(aff)] += 1

        novel = tuple(sorted(bad_cores, key=lambda r: (len(r), r)))
        row = {
            'round': len(rounds),
            'known_higher_conflicts_before_round': len(higher),
            'raw_cover_sets': len(raw_cover),
            'maximal_cover_sets': len(maximal_cover),
            'raw_cover_digest_sha256': digest_rows(raw_cover),
            'maximal_cover_digest_sha256': digest_rows(maximal_cover),
            'cover_sets_checked': checked,
            'consistent_affine_rank_histogram': dict(sorted(rank_hist.items())),
            'novel_minimal_conflicts_found': [list(edge) for edge in novel],
            'local_transversal_shape_histogram': {str(k): v for k, v in sorted(local_shapes.items())},
        }
        rounds.append(row)
        print('closure_round', json.dumps(row, sort_keys=True), flush=True)

        if not novel:
            complete = True
            break
        if len(discovered) + len(novel) > MAX_NEW:
            capped = True
            break

        known_sets = {tuple(edge) for edge in higher}
        for edge in novel:
            assert edge not in known_sets
            higher.append(edge)
            discovered.append(edge)

    final_higher = tuple(sorted((tuple(sorted(map(int, edge))) for edge in higher), key=lambda r: (len(r), r)))
    out = {
        'position': 'C',
        'physical_shared_dimension': A.PHYS_N,
        'global_projection_normal_rank': A.EXPECTED_NORMAL_RANK,
        'm4_outputs': len(gids),
        'exact_pairwise_activity_conflicts': len(zero_cross),
        'starting_higher_affine_conflicts': 13,
        'new_conflicts_discovered_in_closure': len(discovered),
        'discovered_conflicts': [list(edge) for edge in discovered],
        'final_known_higher_affine_conflicts': len(final_higher),
        'final_higher_conflicts': [list(edge) for edge in final_higher],
        'final_higher_conflict_digest_sha256': digest_rows(final_higher),
        'rounds': rounds,
        'all_pairwise_admissible_supports_avoiding_final_conflicts_are_affine_consistent': complete,
        'resource_cap_reached': capped,
        'decision': (
            'C916_ALL_ORDER_AFFINE_CONFLICT_CLOSURE_COMPLETE'
            if complete
            else 'C916_ALL_ORDER_AFFINE_CONFLICT_CLOSURE_INCOMPLETE_RESOURCE_CAP'
        ),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    if complete:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_AFFINE_CONFLICT_CLOSURE_COMPLETE')
        print('theorem=starting from all exact pairwise zero-activity conflicts, the five projection triples, seven projection quadruples, and the certified affine 5-conflict (4,5,8,9,114), iterative exact cover certification has reached closure: every remaining admissible activity support is affine-consistent')
        print('consequence=the emitted finite list of higher affine conflict circuits is complete for all-order affine support on the 90 m4 outputs')
    else:
        print('INCOMPLETE V26_Q138_C916_E0_FIRST_DYADIC_AFFINE_CONFLICT_CLOSURE')
        print('reason=the preregistered novel-circuit cap was reached; emitted circuits remain exact individually but completeness is not claimed')
    print('boundary=physical output-value constraints stronger than affine support remain outside this theorem')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
