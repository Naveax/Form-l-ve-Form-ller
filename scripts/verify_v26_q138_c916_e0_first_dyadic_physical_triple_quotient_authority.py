#!/usr/bin/env python3
import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_group_output_pair_dependency as D
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T

TARGET = int(os.environ.get('C916_PHYSICAL_QUOTIENT_TARGET', '0'))
TARGETS = (
    {
        'triple': (5, 181, 182),
        'raw_holes': 32,
        'raw_hole_digest': 'a5c27707cf7b94a0e5fee28423ec77c71947edbea75a246d3ff6491bf9be22cf',
        'raw_image_digest': 'a78bbe77cfd6666d644939d828868867e66a7dae31d169e6d084ec742bd7bd89',
    },
    {
        'triple': (11, 12, 24),
        'raw_holes': 24,
        'raw_hole_digest': 'fa58d2d3676608238c8417ae329d137c3adcce2de4e27d492d869d2e6980b426',
        'raw_image_digest': '8c82e69c6a6d514487084e30be631a53f559fb9f96b4641022d324943ecf5b07',
    },
)


def digest_rows(rows):
    payload = json.dumps([list(map(int, row)) for row in rows], separators=(',', ':'))
    return hashlib.sha256(payload.encode()).hexdigest()


def build_groups(triple):
    ordered = T.build_ordered_groups()
    groups = []
    next_tid = 0
    for gid in triple:
        can, sectors = ordered[int(gid)]
        group, next_tid = D.build_group_terms(int(gid), can, sectors, next_tid)
        groups.append(group)
    return groups


def pairwise_closure(image, values):
    p01 = {(a, b) for a, b, _c in image}
    p02 = {(a, c) for a, _b, c in image}
    p12 = {(b, c) for _a, b, c in image}
    out = set()
    for a in values[0]:
        for b in values[1]:
            if (a, b) not in p01:
                continue
            for c in values[2]:
                if (a, c) in p02 and (b, c) in p12:
                    out.add((a, b, c))
    return out


def quotient_map(values):
    maps = []
    for alphabet in values:
        assert len(alphabet) == 7
        assert alphabet[3] == 0
        assert all(alphabet[i] == -alphabet[6 - i] for i in range(7))
        orbits = C.orbit_indices(7)
        assert orbits == ((0, 6), (1, 5), (2, 4), (3,))
        vm = {}
        for oi, indices in enumerate(orbits):
            for idx in indices:
                vm[int(alphabet[idx])] = oi
        assert len(vm) == 7
        maps.append(vm)
    return tuple(maps)


def qtuple(row, maps):
    return tuple(maps[i][int(row[i])] for i in range(3))


def analyze():
    assert 0 <= TARGET < len(TARGETS)
    expected = TARGETS[TARGET]
    triple = tuple(expected['triple'])
    groups = build_groups(triple)
    dist, stats = T.exact_joint_distribution(groups)
    image = set(dist)
    assert sum(dist.values()) == (1 << T.PHYS_N)

    values = tuple(tuple(sorted({row[i] for row in image})) for i in range(3))
    assert tuple(map(len, values)) == (7, 7, 7)
    raw_closure = pairwise_closure(image, values)
    raw_holes = tuple(sorted(raw_closure - image))
    assert len(raw_holes) == int(expected['raw_holes'])
    assert T.digest_rows([list(row) for row in raw_holes]) == expected['raw_hole_digest']
    image_rows = [[list(key), int(dist[key])] for key in sorted(dist)]
    assert T.digest_rows(image_rows) == expected['raw_image_digest']

    maps = quotient_map(values)
    qimage = {qtuple(row, maps) for row in image}
    qvalues = tuple(tuple(sorted({row[i] for row in qimage})) for i in range(3))
    assert qvalues == ((0, 1, 2, 3),) * 3
    qclosure = pairwise_closure(qimage, qvalues)
    qholes = tuple(sorted(qclosure - qimage))

    qhole_rows = []
    for q in qholes:
        raw_candidates = tuple(sorted(row for row in raw_closure if qtuple(row, maps) == q))
        assert raw_candidates
        assert all(row not in image for row in raw_candidates)
        qhole_rows.append({
            'quotient_tuple': list(q),
            'raw_pairwise_closure_tuples_eliminated': len(raw_candidates),
            'raw_tuples': [list(row) for row in raw_candidates],
        })

    out = {
        'position': 'C',
        'physical_shared_dimension': T.PHYS_N,
        'target': TARGET,
        'triple': list(triple),
        'raw_alphabets': [list(v) for v in values],
        'raw_exact_image_size': len(image),
        'raw_pairwise_closure_size': len(raw_closure),
        'raw_holes': len(raw_holes),
        'raw_hole_digest_sha256': expected['raw_hole_digest'],
        'raw_joint_distribution_digest_sha256': expected['raw_image_digest'],
        'quotient_exact_image_size': len(qimage),
        'quotient_pairwise_closure_size': len(qclosure),
        'quotient_holes': len(qholes),
        'quotient_hole_tuples': [list(row) for row in qholes],
        'quotient_hole_digest_sha256': digest_rows(qholes),
        'quotient_hole_details': qhole_rows,
        'support_classes': stats['support_classes'],
        'cells_visited': stats['cells_visited'],
        'leaf_cells': stats['leaf_cells'],
        'walsh_evals': stats['walsh_evals'],
        'decision': (
            'EXACT_PHYSICAL_TERNARY_OBSTRUCTION_DESCENDS_TO_MAGNITUDE_QUOTIENT'
            if qholes
            else 'PHYSICAL_TERNARY_OBSTRUCTION_IS_SIGN_ONLY_AT_MAGNITUDE_QUOTIENT'
        ),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    if qholes:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_QUOTIENT_OBSTRUCTION')
        print('theorem=the exact physical ternary value obstruction contains complete sign-orbit holes and therefore descends to a nontrivial forbidden ternary relation on the existing sign-reflection magnitude quotient states')
    else:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_SIGN_ONLY_OBSTRUCTION')
        print('theorem=the exact physical ternary value obstruction does not forbid any entire magnitude-orbit tuple, so this target requires sign-refined states to propagate globally')
    print('boundary=even when quotient holes exist, this freezes only the emitted ternary physical factor; other physical higher-order factors remain open')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
