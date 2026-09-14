#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T
import verify_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_authority as Q

TRIPLE = (178, 179, 184)
RAW_ALPHABET_SIZES = (7, 7, 7)
RAW_HOLES = 24
RAW_HOLE_DIGEST = '26550add0ec46d20b259f3db3f18beb1bbd4db6a0839e7d7edf7db26c8ccc6db'
RAW_IMAGE_DIGEST = '0a8ef378e6a6b0eacf1a1b76eb8c103c6fa9fb88ea594b34095a6ebd50103f9f'


def generalized_quotient_map(values):
    maps = []
    qvalues = []
    for alphabet in values:
        n = len(alphabet)
        assert n % 2 == 1
        mid = n // 2
        assert alphabet[mid] == 0
        assert all(alphabet[i] == -alphabet[n - 1 - i] for i in range(n))
        orbits = C.orbit_indices(n)
        assert len(orbits) == mid + 1
        vm = {}
        for oi, indices in enumerate(orbits):
            for idx in indices:
                vm[int(alphabet[idx])] = oi
        assert len(vm) == n
        maps.append(vm)
        qvalues.append(tuple(range(len(orbits))))
    return tuple(maps), tuple(qvalues)


def analyze():
    groups = Q.build_groups(TRIPLE)
    dist, stats = T.exact_joint_distribution(groups)
    image = set(dist)
    assert sum(dist.values()) == (1 << T.PHYS_N)

    values = tuple(tuple(sorted({row[i] for row in image})) for i in range(3))
    assert tuple(map(len, values)) == RAW_ALPHABET_SIZES
    raw_closure = Q.pairwise_closure(image, values)
    raw_holes = tuple(sorted(raw_closure - image))
    assert len(raw_holes) == RAW_HOLES
    assert T.digest_rows([list(row) for row in raw_holes]) == RAW_HOLE_DIGEST
    image_rows = [[list(key), int(dist[key])] for key in sorted(dist)]
    assert T.digest_rows(image_rows) == RAW_IMAGE_DIGEST

    maps, expected_qvalues = generalized_quotient_map(values)
    qimage = {Q.qtuple(row, maps) for row in image}
    qvalues = tuple(tuple(sorted({row[i] for row in qimage})) for i in range(3))
    assert qvalues == expected_qvalues
    qclosure = Q.pairwise_closure(qimage, qvalues)
    qholes = tuple(sorted(qclosure - qimage))

    qhole_rows = []
    for q in qholes:
        raw_candidates = tuple(sorted(row for row in raw_closure if Q.qtuple(row, maps) == q))
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
        'source_target_index': 19,
        'triple': list(TRIPLE),
        'raw_alphabets': [list(v) for v in values],
        'raw_exact_image_size': len(image),
        'raw_pairwise_closure_size': len(raw_closure),
        'raw_holes': len(raw_holes),
        'raw_hole_digest_sha256': RAW_HOLE_DIGEST,
        'raw_joint_distribution_digest_sha256': RAW_IMAGE_DIGEST,
        'quotient_alphabet_sizes': [len(v) for v in qvalues],
        'quotient_exact_image_size': len(qimage),
        'quotient_pairwise_closure_size': len(qclosure),
        'quotient_holes': len(qholes),
        'quotient_hole_tuples': [list(row) for row in qholes],
        'quotient_hole_digest_sha256': Q.digest_rows(qholes),
        'quotient_hole_details': qhole_rows,
        'support_classes': stats['support_classes'],
        'cells_visited': stats['cells_visited'],
        'leaf_cells': stats['leaf_cells'],
        'walsh_evals': stats['walsh_evals'],
        'decision': (
            'EXACT_PHYSICAL_TERNARY_OBSTRUCTION_DESCENDS_TO_SIGN_REFLECTION_QUOTIENT'
            if qholes
            else 'PHYSICAL_TERNARY_OBSTRUCTION_IS_SIGN_ONLY_AT_SIGN_REFLECTION_QUOTIENT'
        ),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    if qholes:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_178_179_184_QUOTIENT_OBSTRUCTION')
        print('theorem=the exact target-19 physical ternary obstruction contains complete sign-reflection-orbit holes and descends to a forbidden relation on the existing magnitude quotient')
    else:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_178_179_184_QUOTIENT_SIGN_ONLY')
        print('theorem=the exact target-19 physical ternary obstruction has no complete sign-reflection quotient hole and cannot be propagated on the existing quotient without sign refinement')
    print('boundary=only target 19 is frozen here; other physical higher-order factors remain open')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
