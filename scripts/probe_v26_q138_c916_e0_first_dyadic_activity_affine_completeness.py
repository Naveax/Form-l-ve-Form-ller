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

EXPECTED_TRANSVERSALS = 4928
EXPECTED_TRANSVERSAL_DIGEST = '0e80bf3927b0ea8d6ade5871d05937db9e1068a83349ccae24bf530811ad3aa7'
EXPECTED_SIZE_HIST = {6: 80, 7: 600, 8: 1392, 9: 1224, 10: 992, 11: 576, 12: 64}


def affine_of(gids, anchors):
    rows = []
    for gid in gids:
        rows.extend(anchors[int(gid)])
    return A.canonical(rows)


def minimal_transversals(edges):
    """Exact antichain DP for all minimal hitting sets of the hypergraph."""
    trans = {frozenset()}
    for edge in edges:
        candidates = set()
        e = set(edge)
        for h in trans:
            if h & e:
                candidates.add(h)
            else:
                for gid in edge:
                    candidates.add(h | {int(gid)})
        ordered = sorted(candidates, key=lambda h: (len(h), tuple(sorted(h))))
        keep = []
        for h in ordered:
            if any(k <= h for k in keep):
                continue
            keep.append(h)
        trans = set(keep)
    return tuple(sorted((tuple(sorted(h)) for h in trans), key=lambda h: (len(h), h)))


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


def analyze():
    m4 = C.load(C.M4_PATH)
    gids = tuple(map(int, m4['m4_group_ids']))
    assert len(gids) == len(set(gids)) == 90
    triples = tuple(tuple(map(int, row)) for row in m4['projection_minimal_empty_triples'])
    quads = tuple(tuple(map(int, row)) for row in H.QUADS)
    assert len(triples) == 5 and len(quads) == 7
    circuits = triples + quads
    assert len(circuits) == 12

    anchors = A.rebuild_anchors(gids)
    assert set(anchors) == set(gids)

    # Re-certify the 12 known obstructions inside the exact all-order affine
    # algebra itself: each full edge is inconsistent and every one-gid deletion
    # is consistent.
    for edge in circuits:
        assert affine_of(edge, anchors) is None, edge
        for gid in edge:
            assert affine_of([g for g in edge if g != gid], anchors) is not None, (edge, gid)

    trans = minimal_transversals(circuits)
    payload = json.dumps(trans, separators=(',', ':'))
    digest = hashlib.sha256(payload.encode()).hexdigest()
    size_hist = dict(sorted(Counter(map(len, trans)).items()))
    assert len(trans) == EXPECTED_TRANSVERSALS
    assert digest == EXPECTED_TRANSVERSAL_DIGEST
    assert size_hist == EXPECTED_SIZE_HIST

    circuit_sets = tuple(frozenset(edge) for edge in circuits)
    bad = None
    checked = 0
    active_size_hist = Counter()
    rank_hist = Counter()
    for hitting in trans:
        h = frozenset(hitting)
        assert all(h & edge for edge in circuit_sets)
        assert all(not all((h - {gid}) & edge for edge in circuit_sets) for gid in h)
        active = tuple(g for g in gids if g not in h)
        # A complement of a minimal hitting set is a maximal activity set that
        # avoids containing any of the 12 forbidden circuits.
        assert all(not edge <= set(active) for edge in circuit_sets)
        aff = affine_of(active, anchors)
        checked += 1
        active_size_hist[len(active)] += 1
        if aff is None:
            bad = minimize_inconsistent(active, anchors)
            break
        rank_hist[len(aff)] += 1

    complete = bad is None
    novel = None
    if bad is not None:
        badset = frozenset(bad)
        assert all(edge != badset for edge in circuit_sets)
        assert all(not edge <= badset for edge in circuit_sets)
        novel = list(bad)

    out = {
        'position': 'C',
        'physical_shared_dimension': A.PHYS_N,
        'global_projection_normal_rank': A.EXPECTED_NORMAL_RANK,
        'm4_outputs': len(gids),
        'known_minimal_affine_conflict_circuits': len(circuits),
        'known_triples': len(triples),
        'known_quadruples': len(quads),
        'minimal_hitting_sets': len(trans),
        'minimal_hitting_set_digest_sha256': digest,
        'minimal_hitting_set_size_histogram': size_hist,
        'maximal_clause_valid_activity_sets_checked': checked,
        'maximal_activity_size_histogram': dict(sorted(active_size_hist.items())),
        'consistent_affine_rank_histogram': dict(sorted(rank_hist.items())),
        'known_12_circuits_globally_complete_for_affine_inconsistency': complete,
        'novel_minimal_affine_conflict_circuit': novel,
        'decision': 'C916_GLOBAL_AFFINE_CONFLICT_COMPLETENESS_BY_MINIMAL_TRANSVERSALS',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    if complete:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_GLOBAL_AFFINE_CONFLICT_COMPLETENESS')
        print('theorem=every gid activity set avoiding the five known affine-inconsistent triples and seven known affine-inconsistent quadruples is affine-consistent: every such set is contained in a maximal clause-valid set, maximal clause-valid sets are exactly complements of the 4928 minimal hitting sets, and every one of those complements has nonempty exact affine intersection')
        print('consequence=for every separator profile and every magnitude assignment, enforcing the 12 finite projection hyperedges is equivalent to the all-order affine-intersection condition because all-order anchors depend only on gid zero/nonzero activity')
    else:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_GLOBAL_AFFINE_CONFLICT_COUNTEREXAMPLE')
        print('theorem=the 12 known projection circuits are not globally complete for all-order affine inconsistency; the emitted novel circuit is independently inclusion-minimal')
    print('boundary=any higher-order physical-image constraint stronger than all-order affine intersection remains outside this theorem')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
