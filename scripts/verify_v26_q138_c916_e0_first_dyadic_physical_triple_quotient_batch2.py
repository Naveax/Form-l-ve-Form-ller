#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T
import verify_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_authority as Q

TARGET = int(os.environ.get('C916_PHYSICAL_QUOTIENT_BATCH2_TARGET', '0'))
TARGETS = (
    {
        'triple': (62, 67, 104),
        'raw_holes': 16,
        'raw_hole_digest': '8a9d31b52b4a275b906ce15eede95b2296a5d19450d0acb350a7e86f6bb9113a',
        'raw_image_digest': 'e246533146d7539e87bee9fec0f4ce706c36ddeee99373c2076d801b26e8e8e3',
    },
    {
        'triple': (111, 112, 113),
        'raw_holes': 24,
        'raw_hole_digest': '9bde1dec2bab4539fdc7b7448a0b850e5d6b94221442c99083c54443e30f277f',
        'raw_image_digest': 'b8671c6e840c49b56b017362da2198d232e1d2c6944006c72651d6af409ef305',
    },
)


def analyze():
    assert 0 <= TARGET < len(TARGETS)
    expected = TARGETS[TARGET]
    triple = tuple(expected['triple'])
    groups = Q.build_groups(triple)
    dist, stats = T.exact_joint_distribution(groups)
    image = set(dist)
    assert sum(dist.values()) == (1 << T.PHYS_N)

    values = tuple(tuple(sorted({row[i] for row in image})) for i in range(3))
    assert tuple(map(len, values)) == (7, 7, 7)
    raw_closure = Q.pairwise_closure(image, values)
    raw_holes = tuple(sorted(raw_closure - image))
    assert len(raw_holes) == int(expected['raw_holes'])
    assert T.digest_rows([list(row) for row in raw_holes]) == expected['raw_hole_digest']
    image_rows = [[list(key), int(dist[key])] for key in sorted(dist)]
    assert T.digest_rows(image_rows) == expected['raw_image_digest']

    maps = Q.quotient_map(values)
    qimage = {Q.qtuple(row, maps) for row in image}
    qvalues = tuple(tuple(sorted({row[i] for row in qimage})) for i in range(3))
    assert qvalues == ((0, 1, 2, 3),) * 3
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
        'quotient_hole_digest_sha256': Q.digest_rows(qholes),
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
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_QUOTIENT_BATCH2_OBSTRUCTION')
        print('theorem=this second-batch exact physical ternary obstruction contains complete sign-orbit holes and descends to a forbidden ternary relation on the existing magnitude quotient')
    else:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_QUOTIENT_BATCH2_SIGN_ONLY')
        print('theorem=this second-batch exact physical ternary obstruction has no complete magnitude-orbit hole and therefore cannot be propagated on the existing quotient without sign refinement')
    print('boundary=only the emitted second-batch target is frozen; other physical higher-order factors remain open')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
