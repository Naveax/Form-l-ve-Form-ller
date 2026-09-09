#!/usr/bin/env python3
import io
import json
import sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from probe_v26_q138_c916_e0_post_gauss_physical_phase_common import *


def analyze():
    synthetic_cases = synthetic_pullback_regression()

    with redirect_stdout(io.StringIO()):
        pair_authority = R.analyze()
    assert pair_authority['first_dyadic_pair_residual_terms'] == 237
    pair_groups = {g['group_id']: g for g in pair_authority['groups']}
    assert len(pair_groups) == 147

    e0, _e1, _half = C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for zc in range(4):
        for zs, cls in e0[zc]:
            can = C.P.U.H.support_for(POS, zs, cls)
            if can is not None:
                raw += 1
                grouped[can].append((zs, cls))
    assert raw == 577 and len(grouped) == 250
    assert dict(sorted(Counter(len(v) for v in grouped.values()).items())) == {
        1: 103, 2: 57, 4: 90,
    }

    all_transforms = []
    term_anchor_ids = set()
    mate_ids = set()
    pair_regression_cases = 0
    pair_regression_relation_hist = Counter()
    pair_regression_rank_hist = Counter()

    for gid, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        m = len(sectors)
        projection_rank, transforms = physical_group_transforms(can, sectors)
        for t in transforms:
            t['group_id'] = gid
            t['multiplicity'] = m
            t['role'] = None
            all_transforms.append(t)

        if m == 1:
            transforms[0]['role'] = 'singleton_anchor'
            term_anchor_ids.add((gid, 0))
            continue

        authority = pair_groups[gid]
        assert authority['multiplicity'] == m
        touched = set()
        for selected in authority['selected_pairs']:
            i, j = selected['pair']
            assert i not in touched and j not in touched
            touched.update((i, j))
            transforms[i]['role'] = 'pair_anchor'
            transforms[j]['role'] = 'pair_mate'
            term_anchor_ids.add((gid, i))
            mate_ids.add((gid, j))

            raw_rec = P.classify_pair(
                transforms[i]['_raw_transform'],
                transforms[j]['_raw_transform'],
                projection_rank,
            )
            phys_rec = compare_phases(transforms[i], transforms[j])
            assert phys_rec['support_relation'] == raw_rec['support_relation']
            if raw_rec['intersection_dimension'] is None:
                assert phys_rec['intersection_dimension'] is None
            else:
                assert phys_rec['intersection_dimension'] == raw_rec['intersection_dimension']
                assert phys_rec['sign_difference_type'] == raw_rec['sign_difference_type']
                assert phys_rec['sign_difference_polar_rank'] == raw_rec['sign_difference_polar_rank']
                if raw_rec['sign_difference_type'] == 'constant':
                    assert phys_rec['sign_difference_constant_bit'] == raw_rec['sign_difference_constant_bit']
                pair_regression_rank_hist[phys_rec['sign_difference_polar_rank']] += 1
            pair_regression_relation_hist[phys_rec['support_relation']] += 1
            pair_regression_cases += 1
        assert touched == set(range(m))

    assert len(all_transforms) == 577
    assert len(term_anchor_ids) == 340
    assert len(mate_ids) == 237
    assert pair_regression_cases == 237
    assert dict(sorted(pair_regression_relation_hist.items())) == {
        'disjoint': 28,
        'equal': 6,
        'left_subset_right': 4,
        'overlap_incomparable': 112,
        'right_subset_left': 87,
    }
    assert dict(sorted(pair_regression_rank_hist.items())) == {0: 203, 2: 6}

    singletons = [t for t in all_transforms if t['role'] == 'singleton_anchor']
    assert len(singletons) == 103
    root = min(singletons, key=lambda t: (t['group_id'], t['sector_index']))
    root_id = (root['group_id'], root['sector_index'])
    assert root_id in term_anchor_ids

    relation_hist = Counter()
    intersection_dim_hist = Counter()
    intersection_codim_hist = Counter()
    diff_type_hist = Counter()
    diff_rank_hist = Counter()
    diff_rank_by_role = defaultdict(Counter)
    diff_type_by_role = defaultdict(Counter)
    relation_by_role = defaultdict(Counter)
    diff_rank_by_mult = defaultdict(Counter)
    term_anchor_rank_hist = Counter()
    term_anchor_relation_hist = Counter()
    mate_rank_hist = Counter()
    mate_relation_hist = Counter()
    constant_bit_hist = Counter()
    worst = []

    compared = 0
    for t in all_transforms:
        tid = (t['group_id'], t['sector_index'])
        if tid == root_id:
            continue
        rec = compare_phases(root, t)
        compared += 1
        role = t['role']
        relation_hist[rec['support_relation']] += 1
        relation_by_role[role][rec['support_relation']] += 1
        if tid in term_anchor_ids:
            term_anchor_relation_hist[rec['support_relation']] += 1
        if tid in mate_ids:
            mate_relation_hist[rec['support_relation']] += 1

        if rec['intersection_dimension'] is None:
            worst.append((10**9, tid, role, t['multiplicity'], 'disjoint'))
            continue

        intersection_dim_hist[rec['intersection_dimension']] += 1
        intersection_codim_hist[PHYS_N - rec['intersection_dimension']] += 1
        rank = rec['sign_difference_polar_rank']
        dtype = rec['sign_difference_type']
        diff_rank_hist[rank] += 1
        diff_type_hist[dtype] += 1
        diff_rank_by_role[role][rank] += 1
        diff_type_by_role[role][dtype] += 1
        diff_rank_by_mult[t['multiplicity']][rank] += 1
        if dtype == 'constant':
            constant_bit_hist[rec['sign_difference_constant_bit']] += 1
        if tid in term_anchor_ids:
            term_anchor_rank_hist[rank] += 1
        if tid in mate_ids:
            mate_rank_hist[rank] += 1
        worst.append((rank, tid, role, t['multiplicity'], dtype))

    assert compared == 576
    overlap_count = sum(diff_rank_hist.values())
    disjoint_count = relation_hist['disjoint']
    assert overlap_count + disjoint_count == compared

    worst_sorted = sorted(
        worst,
        key=lambda x: (-x[0], x[1][0], x[1][1]),
    )[:32]
    worst_compact = [
        {
            'difference_polar_rank': None if rank == 10**9 else rank,
            'group_id': tid[0],
            'sector_index': tid[1],
            'role': role,
            'multiplicity': mult,
            'difference_type': dtype,
        }
        for rank, tid, role, mult, dtype in worst_sorted
    ]

    max_rank = max(diff_rank_hist) if diff_rank_hist else None
    term_anchor_disjoint = term_anchor_relation_hist['disjoint']
    mate_disjoint = mate_relation_hist['disjoint']
    term_anchor_max_rank = max(term_anchor_rank_hist) if term_anchor_rank_hist else None
    mate_max_rank = max(mate_rank_hist) if mate_rank_hist else None

    if disjoint_count == 0 and max_rank is not None and max_rank <= 2:
        decision = 'CANONICAL_SINGLETON_PHASE_ANCHOR_ALL_SECTORS_POLAR_RANK0_2'
    elif term_anchor_disjoint == 0 and term_anchor_max_rank is not None and term_anchor_max_rank <= 2:
        decision = 'CANONICAL_SINGLETON_PHASE_ANCHOR_FIRST_DYADIC_ANCHORS_POLAR_RANK0_2'
    else:
        decision = 'CANONICAL_SINGLETON_PHASE_ANCHOR_REQUIRES_REFINEMENT'

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'synthetic_pullback_regression_cases': synthetic_cases,
        'frozen_pair_physical_pullback_regression_cases': pair_regression_cases,
        'frozen_pair_support_relation_histogram_reproduced': dict(sorted(pair_regression_relation_hist.items())),
        'frozen_pair_overlap_sign_difference_polar_rank_histogram_reproduced': dict(sorted(pair_regression_rank_hist.items())),
        'sector_transforms': len(all_transforms),
        'first_dyadic_term_anchors': len(term_anchor_ids),
        'first_dyadic_pair_mates': len(mate_ids),
        'canonical_root': {
            'group_id': root['group_id'],
            'sector_index': root['sector_index'],
            'multiplicity': root['multiplicity'],
            'role': root['role'],
            'physical_support_dimension': root['physical_support_dimension'],
            'physical_support_codimension': root['physical_support_codimension'],
            'normalized_sign_polar_rank': root['normalized_sign_polar_rank'],
            'log2_abs_nonzero_gauss': root['log2_abs_nonzero_gauss'],
        },
        'root_comparisons': compared,
        'root_support_relation_histogram': dict(sorted(relation_hist.items())),
        'root_intersection_dimension_histogram': dict(sorted(intersection_dim_hist.items())),
        'root_intersection_codimension_histogram': dict(sorted(intersection_codim_hist.items())),
        'root_overlap_sign_difference_type_histogram': dict(sorted(diff_type_hist.items())),
        'root_overlap_sign_difference_polar_rank_histogram': dict(sorted(diff_rank_hist.items())),
        'root_overlap_constant_difference_bit_histogram': dict(sorted(constant_bit_hist.items())),
        'root_support_relation_by_role': {
            role: dict(sorted(h.items())) for role, h in sorted(relation_by_role.items())
        },
        'root_overlap_sign_difference_polar_rank_by_role': {
            role: dict(sorted(h.items())) for role, h in sorted(diff_rank_by_role.items())
        },
        'root_overlap_sign_difference_type_by_role': {
            role: dict(sorted(h.items())) for role, h in sorted(diff_type_by_role.items())
        },
        'root_overlap_sign_difference_polar_rank_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(diff_rank_by_mult.items())
        },
        'first_dyadic_term_anchor_support_relation_histogram': dict(sorted(term_anchor_relation_hist.items())),
        'first_dyadic_term_anchor_overlap_sign_difference_polar_rank_histogram': dict(sorted(term_anchor_rank_hist.items())),
        'first_dyadic_term_anchor_disjoint_from_root': term_anchor_disjoint,
        'first_dyadic_term_anchor_max_overlap_sign_difference_polar_rank': term_anchor_max_rank,
        'pair_mate_support_relation_histogram': dict(sorted(mate_relation_hist.items())),
        'pair_mate_overlap_sign_difference_polar_rank_histogram': dict(sorted(mate_rank_hist.items())),
        'pair_mate_disjoint_from_root': mate_disjoint,
        'pair_mate_max_overlap_sign_difference_polar_rank': mate_max_rank,
        'all_sector_disjoint_from_root': disjoint_count,
        'all_sector_max_overlap_sign_difference_polar_rank': max_rank,
        'worst_or_disjoint_examples': worst_compact,
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_POST_GAUSS_CANONICAL_PHASE_ANCHOR')
    print('identity=each normalized Gauss sign is pulled back only through its own exact physical 149-bit shared-support affine parametrization; pairwise differences are restricted on the true physical support intersection, with no ambient quadratic lift')
    print('scope=canonical singleton-root phase-overlap geometry for all 577 nonzero C e0 transformed sectors, with the 340 first-dyadic term anchors and 237 pair mates reported separately')
    print('regression=the physical pullback reproduces the frozen 237 transformed-pair support-relation histogram and the overlap sign-difference polar-rank histogram {0:203,2:6} exactly')
    print('important=this is a root-anchor diagnostic, not yet a proof that one global phase template extends consistently outside pairwise intersections')
    print('next=if the canonical root is insufficient, build a minimum low-rank overlap cover/forest over the 340 first-dyadic anchors; if it is sufficient, factor the common phase section and assemble the quotient-aware first-dyadic message state')
    print('not_included=complete grouped-e0 carry separator, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
