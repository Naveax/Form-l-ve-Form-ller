#!/usr/bin/env python3
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_phase_complete_linear_branchwidth as K

M = K.M
D = K.PHYS_N
N = K.GROUPS
FULL = (1 << N) - 1
EXPECTED_DIRECTION_COUNT = 3607
EXPECTED_PAIR_COUNT = EXPECTED_DIRECTION_COUNT * (EXPECTED_DIRECTION_COUNT - 1) // 2
assert D == 149 and N == 250
assert EXPECTED_PAIR_COUNT == 6_503_421


def digest_direction(direction):
    return hashlib.sha256(int(direction).to_bytes(19, 'big')).hexdigest()[:20]


def build_direction_masks():
    records, mult_hist = M.build_closed_spaces()
    assert len(records) == N and all(r['exact'] for r in records)

    coverage_masks = defaultdict(int)
    kernel_dim_hist = Counter()
    rank_hist = Counter()

    for rec in records:
        gid = int(rec['group_id'])
        basis = tuple(int(x) for x in rec['minimal_basis'])
        rank = int(rec['lower_rank'])
        assert rank == rec['upper_rank'] == len(basis)
        rank_hist[rank] += 1

        kbasis = tuple(M.B.homogeneous_kernel(basis, D))
        kernel_dim_hist[len(kbasis)] += 1
        for direction in K.xor_span_nonzero(kbasis):
            coverage_masks[int(direction)] |= 1 << gid

    assert len(coverage_masks) == EXPECTED_DIRECTION_COUNT
    return records, mult_hist, coverage_masks, kernel_dim_hist, rank_hist


def synthetic_pair_cover_regression():
    full = 0b111111
    masks = {
        1: 0b001111,
        2: 0b111100,
        4: 0b000001,
    }
    best = 0
    full_count = 0
    first_full = None
    dirs = sorted(masks)
    for i, a in enumerate(dirs):
        for b in dirs[i + 1:]:
            union = masks[a] | masks[b]
            best = max(best, union.bit_count())
            if union == full:
                full_count += 1
                if first_full is None:
                    first_full = (a, b)
    assert best == 6
    assert full_count == 1 and first_full == (1, 2)
    return {'directions': 3, 'full_pair_count': 1, 'max_union_coverage': 6}


def analyze():
    regression = synthetic_pair_cover_regression()
    _records, mult_hist, coverage_masks, kernel_dim_hist, rank_hist = build_direction_masks()

    directions = sorted(
        coverage_masks,
        key=lambda d: (-coverage_masks[d].bit_count(), d),
    )

    pair_count = 0
    full_cover_count = 0
    first_full_cover_pair = None
    max_union = -1
    max_union_pair = None
    max_union_pair_count = 0
    union_hist = Counter()

    for i, da in enumerate(directions):
        ma = coverage_masks[da]
        for db in directions[i + 1:]:
            pair_count += 1
            union_count = (ma | coverage_masks[db]).bit_count()
            union_hist[union_count] += 1
            if union_count > max_union:
                max_union = union_count
                max_union_pair = (da, db)
                max_union_pair_count = 1
            elif union_count == max_union:
                max_union_pair_count += 1

            if union_count == N:
                full_cover_count += 1
                if first_full_cover_pair is None:
                    first_full_cover_pair = (da, db)

    assert pair_count == EXPECTED_PAIR_COUNT
    assert sum(union_hist.values()) == EXPECTED_PAIR_COUNT

    if full_cover_count:
        decision = 'GLOBAL_TWO_KERNEL_DIRECTION_COVER_EXISTS'
        structural_consequence = (
            'width147 admissible cuts of type k(S)=k(S^c)=1 are possible in principle'
        )
    else:
        decision = 'NO_GLOBAL_TWO_KERNEL_DIRECTION_COVER'
        structural_consequence = (
            'every width147 admissible cut must have kernel dimension at least 2 on one side'
        )

    witness = max_union_pair
    assert witness is not None

    out = {
        'position': 'C',
        'physical_shared_dimension': D,
        'support_groups': N,
        'support_multiplicity_histogram': mult_hist,
        'synthetic_pair_cover_regression': regression,
        'minimal_rank_histogram': dict(sorted(rank_hist.items())),
        'kernel_dimension_histogram': dict(sorted(kernel_dim_hist.items())),
        'unique_nonzero_kernel_directions': len(directions),
        'direction_pair_count': pair_count,
        'max_single_direction_coverage': max(
            coverage_masks[d].bit_count() for d in directions
        ),
        'max_two_direction_union_coverage': max_union,
        'max_two_direction_union_pair_count': max_union_pair_count,
        'max_two_direction_union_example_digests': [
            digest_direction(witness[0]),
            digest_direction(witness[1]),
        ],
        'global_two_direction_cover_count': full_cover_count,
        'global_two_direction_cover_example_digests': (
            [] if first_full_cover_pair is None else [
                digest_direction(first_full_cover_pair[0]),
                digest_direction(first_full_cover_pair[1]),
            ]
        ),
        'two_direction_union_coverage_histogram': dict(sorted(union_hist.items())),
        'structural_consequence': structural_consequence,
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHASE_COMPLETE_WIDTH147_TWO_LINE_COVER')
    print('scope=exact all-pairs test over the 3607 nonzero common-kernel directions')
    print('theorem=if no pair covers all groups, no width147 edge can have kernel split exactly (1,1)')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
