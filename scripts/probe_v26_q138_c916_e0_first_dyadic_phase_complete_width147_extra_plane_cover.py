#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_phase_complete_width147_forced_five_plane_dp as F

P = F.P
W = F.W
M = F.M
N = F.N
D = F.D
FULL_GROUP_MASK = (1 << N) - 1
assert N == 250 and D == 149


def groups_from_mask(mask):
    return tuple(g for g in range(N) if (mask >> g) & 1)


def kernel_dim(nonzero_kernel):
    return W.kernel_dimension_from_nonzero(nonzero_kernel)


def build_geometry():
    records, mult_hist = M.build_closed_spaces()
    assert len(records) == N and all(r['exact'] for r in records)

    kernel_sets = []
    line_coverage = defaultdict(int)
    rank_hist = Counter()
    rank147_groups = []

    for rec in records:
        gid = int(rec['group_id'])
        basis = tuple(int(x) for x in rec['minimal_basis'])
        rank = int(rec['lower_rank'])
        assert rank == rec['upper_rank'] == len(basis)
        rank_hist[rank] += 1

        kbasis = tuple(M.B.homogeneous_kernel(basis, D))
        assert len(kbasis) == D - rank
        ks = W.xor_span_nonzero(kbasis)
        kernel_sets.append(ks)
        for direction in ks:
            line_coverage[direction] |= 1 << gid
        if rank == 147:
            rank147_groups.append(gid)

    assert len(kernel_sets) == N
    assert len(rank147_groups) == 16

    forced_by_group = {}
    for gid in rank147_groups:
        planes = P.planes_of_kernel(kernel_sets[gid])
        assert len(planes) == 1
        forced_by_group[gid] = planes[0]

    forced_planes = tuple(sorted(set(forced_by_group.values())))
    assert len(forced_planes) == 5

    forced_plane_masks = {
        plane: P.coverage_from_plane(plane, line_coverage)
        for plane in forced_planes
    }
    forced_union = 0
    for plane in forced_planes:
        forced_union |= forced_plane_masks[plane]

    uncovered_mask = FULL_GROUP_MASK & ~forced_union
    uncovered_groups = groups_from_mask(uncovered_mask)
    assert len(uncovered_groups) == 27

    return {
        'records': records,
        'mult_hist': mult_hist,
        'kernel_sets': tuple(kernel_sets),
        'line_coverage': line_coverage,
        'rank_hist': rank_hist,
        'rank147_groups': tuple(rank147_groups),
        'forced_planes': forced_planes,
        'forced_plane_masks': forced_plane_masks,
        'forced_union': forced_union,
        'uncovered_mask': uncovered_mask,
        'uncovered_groups': uncovered_groups,
    }


def build_extra_plane_candidates(geometry):
    kernel_sets = geometry['kernel_sets']
    line_coverage = geometry['line_coverage']
    uncovered_mask = geometry['uncovered_mask']
    forced = set(geometry['forced_planes'])

    # For the exact set-cover question on the 27 groups, two planes with the
    # same restricted coverage are interchangeable. Keep the lexicographically
    # smallest representative only. This is exact for cover existence/minimum.
    representative = {}
    full_mask_for_restricted = {}

    for gid in geometry['uncovered_groups']:
        for plane in P.planes_of_kernel(kernel_sets[gid]):
            if plane in forced:
                continue
            full_mask = P.coverage_from_plane(plane, line_coverage)
            restricted = full_mask & uncovered_mask
            if not restricted:
                continue
            old = representative.get(restricted)
            if old is None or plane < old:
                representative[restricted] = plane
                full_mask_for_restricted[restricted] = full_mask

    candidates = []
    for restricted, plane in representative.items():
        candidates.append({
            'plane': plane,
            'restricted_mask': restricted,
            'full_mask': full_mask_for_restricted[restricted],
        })
    candidates.sort(
        key=lambda x: (-x['restricted_mask'].bit_count(), x['plane'])
    )
    assert candidates
    return tuple(candidates)


def exact_min_extra_cover(target_mask, candidates, max_depth=3):
    by_group = defaultdict(list)
    for idx, rec in enumerate(candidates):
        mask = rec['restricted_mask']
        for gid in groups_from_mask(mask):
            by_group[gid].append(idx)

    for gid in groups_from_mask(target_mask):
        assert by_group[gid], f'uncovered group {gid} has no 2D-plane candidate'

    stats = Counter()

    def maximal_options(rem, gid):
        # Exact dominance pruning for pure set-cover existence: at a fixed
        # state, a candidate whose newly covered target subset is contained in
        # another candidate's newly covered subset cannot be necessary.
        raw = []
        seen = set()
        for idx in by_group[gid]:
            cov = candidates[idx]['restricted_mask'] & rem
            if not cov or cov in seen:
                continue
            seen.add(cov)
            raw.append((cov, idx))
        raw.sort(key=lambda x: (-x[0].bit_count(), candidates[x[1]]['plane']))
        kept = []
        for cov, idx in raw:
            if any((cov | old_cov) == old_cov for old_cov, _ in kept):
                stats['dominated_options_pruned'] += 1
                continue
            kept.append((cov, idx))
        return tuple(kept)

    @lru_cache(None)
    def solve(rem, depth):
        stats['states_visited'] += 1
        if rem == 0:
            return ()
        if depth == 0:
            return None

        gids = groups_from_mask(rem)
        gid = min(
            gids,
            key=lambda g: (
                len(maximal_options(rem, g)),
                g,
            ),
        )
        options = maximal_options(rem, gid)
        stats['options_considered'] += len(options)

        # Safe cardinality lower bound: use the largest gain of ANY remaining
        # candidate, not merely candidates covering the selected branching
        # group. The latter can falsely prune a valid solution whose later
        # planes cover much larger portions of the remainder.
        global_max_gain = max(
            (rec['restricted_mask'] & rem).bit_count()
            for rec in candidates
        )
        if global_max_gain * depth < rem.bit_count():
            stats['cardinality_lower_bound_prunes'] += 1
            return None

        for cov, idx in options:
            new_rem = rem & ~cov
            if new_rem == rem:
                continue
            got = solve(new_rem, depth - 1)
            if got is not None:
                return (idx,) + got
        return None

    witness = None
    minimum = None
    for depth in range(1, max_depth + 1):
        stats['depths_tested'] += 1
        got = solve(target_mask, depth)
        if got is not None:
            minimum = depth
            witness = tuple(candidates[i] for i in got)
            break

    return minimum, witness, dict(sorted(stats.items()))


def synthetic_cover_regression():
    target = 0b111111
    candidates = (
        {'plane': (1, 2, 3), 'restricted_mask': 0b000111, 'full_mask': 0b000111},
        {'plane': (4, 8, 12), 'restricted_mask': 0b011100, 'full_mask': 0b011100},
        {'plane': (16, 32, 48), 'restricted_mask': 0b110000, 'full_mask': 0b110000},
    )

    old_n = globals()['N']
    try:
        globals()['N'] = 6
        minimum, witness, _stats = exact_min_extra_cover(target, candidates, 3)
    finally:
        globals()['N'] = old_n

    assert minimum == 3
    assert witness is not None and len(witness) == 3
    covered = 0
    for rec in witness:
        covered |= rec['restricted_mask']
    assert covered == target
    return {'target_groups': 6, 'minimum_cover': 3}


def analyze():
    regression = synthetic_cover_regression()
    geometry = build_geometry()
    candidates = build_extra_plane_candidates(geometry)

    minimum, witness, search_stats = exact_min_extra_cover(
        geometry['uncovered_mask'], candidates, max_depth=3
    )

    max_single = max(x['restricted_mask'].bit_count() for x in candidates)
    max_single_recs = [
        x for x in candidates if x['restricted_mask'].bit_count() == max_single
    ]

    if witness is None:
        decision = 'NO_COMMON_2D_PLANE_COVER_WITH_AT_MOST_EIGHT_TOTAL_PLANES'
        witness_digests = []
        witness_restricted_coverages = []
        witness_full_coverages = []
        witness_total_cover_count = None
        witness_remaining = geometry['uncovered_mask']
    else:
        covered = 0
        for rec in witness:
            covered |= rec['restricted_mask']
        witness_remaining = geometry['uncovered_mask'] & ~covered
        assert witness_remaining == 0
        witness_digests = [P.plane_digest(x['plane']) for x in witness]
        witness_restricted_coverages = [
            x['restricted_mask'].bit_count() for x in witness
        ]
        witness_full_coverages = [x['full_mask'].bit_count() for x in witness]
        witness_total_cover_count = len(geometry['forced_planes']) + minimum
        decision = 'FORCED_FIVE_PLUS_EXACT_EXTRA_2D_PLANE_COVER_FOUND'

    out = {
        'position': 'C',
        'physical_shared_dimension': D,
        'support_groups': N,
        'support_multiplicity_histogram': geometry['mult_hist'],
        'synthetic_cover_regression': regression,
        'minimal_rank_histogram': dict(sorted(geometry['rank_hist'].items())),
        'rank147_groups': list(geometry['rank147_groups']),
        'forced_plane_count': len(geometry['forced_planes']),
        'forced_plane_digests': [
            P.plane_digest(x) for x in geometry['forced_planes']
        ],
        'forced_plane_coverages': [
            geometry['forced_plane_masks'][x].bit_count()
            for x in geometry['forced_planes']
        ],
        'forced_plane_union_coverage': geometry['forced_union'].bit_count(),
        'forced_plane_uncovered_count': len(geometry['uncovered_groups']),
        'forced_plane_uncovered_groups': list(geometry['uncovered_groups']),
        'unique_extra_plane_restricted_coverages': len(candidates),
        'max_single_extra_plane_uncovered_coverage': max_single,
        'max_single_extra_plane_count': len(max_single_recs),
        'max_single_extra_plane_example_digest': P.plane_digest(
            max_single_recs[0]['plane']
        ),
        'exact_minimum_extra_plane_cover_with_cap3': minimum,
        'witness_extra_plane_digests': witness_digests,
        'witness_extra_plane_restricted_coverages': witness_restricted_coverages,
        'witness_extra_plane_full_coverages': witness_full_coverages,
        'witness_total_plane_cover_count': witness_total_cover_count,
        'witness_remaining_uncovered_count': witness_remaining.bit_count(),
        'search_stats': search_stats,
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHASE_COMPLETE_WIDTH147_EXTRA_PLANE_COVER')
    print('scope=exact extension of the five forced 2D kernel planes by at most three extra planes')
    print('important=cover existence is not by itself a width147 tree certificate')
    print('important=no-cover up to eight total 2D planes does not rule out general width147 trees with (1,1) cuts')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
