#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_group_output_pair_dependency as D
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T
import probe_v26_q138_c916_e0_first_dyadic_physical_quad_value_image as QD
import verify_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_authority as Q

TARGET = int(os.environ.get('C916_PHYSICAL_QUAD_QUOTIENT_TARGET', '0'))
TARGETS = (
    {
        'quadruple': (4, 5, 8, 9),
        'raw_holes': 32,
        'raw_hole_digest': '3dd70a9499c74730d646a0f1ec8b7a752fe79890cab6de4a6b0a0f689fc387c1',
        'raw_image_digest': '7906623f16d6f7a840c91d1db4c5cd77966ed054a704df017ae22b788ac6c06b',
    },
    {
        'quadruple': (4, 5, 8, 114),
        'raw_holes': 344,
        'raw_hole_digest': '21969419c455a29089a41c592766ff1faecec921884919530c2e80da088c9243',
        'raw_image_digest': '6d179ba26a36ca3e66808f6302836ddb8af38ee47ffc870d9c0cbfd07aedf94b',
    },
    {
        'quadruple': (4, 5, 9, 114),
        'raw_holes': 344,
        'raw_hole_digest': '21969419c455a29089a41c592766ff1faecec921884919530c2e80da088c9243',
        'raw_image_digest': '6d179ba26a36ca3e66808f6302836ddb8af38ee47ffc870d9c0cbfd07aedf94b',
    },
    {
        'quadruple': (4, 8, 9, 114),
        'raw_holes': 64,
        'raw_hole_digest': 'ba8305a5e4434662d0ad59cc54a7cd2157d9c506d4b452119e91232313edce0e',
        'raw_image_digest': '7f60f670887ca3f0cb303596511068267103a123ba17e453cb9427c974eff818',
    },
    {
        'quadruple': (5, 8, 9, 114),
        'raw_holes': 128,
        'raw_hole_digest': '4e1c6a618ffb9bfd5b39db17212bb840b0208b3f4b9e7232e6b64aca4cae4384',
        'raw_image_digest': '4ac8b187d3e99a5ba1002f96853825bb0ee00fad974b41bd6ab0751d1e3d8246',
    },
)


def build_groups(target):
    ordered = T.build_ordered_groups()
    groups = []
    next_tid = 0
    for gid in target:
        can, sectors = ordered[int(gid)]
        group, next_tid = D.build_group_terms(int(gid), can, sectors, next_tid)
        groups.append(group)
    return groups


def qtuple(row, maps):
    return tuple(maps[i][int(row[i])] for i in range(4))


def analyze():
    assert 0 <= TARGET < len(TARGETS)
    expected = TARGETS[TARGET]
    target = tuple(expected['quadruple'])
    groups = build_groups(target)
    dist, stats = QD.exact_joint_distribution(groups)
    image = set(dist)
    assert sum(dist.values()) == (1 << QD.PHYS_N)

    values = tuple(tuple(sorted({row[i] for row in image})) for i in range(4))
    assert tuple(map(len, values)) == (7, 7, 7, 7)
    raw_closure = set(QD.pairwise_closure(image, values))
    raw_holes = tuple(sorted(raw_closure - image))
    assert len(raw_holes) == int(expected['raw_holes'])
    assert T.digest_rows([list(row) for row in raw_holes]) == expected['raw_hole_digest']
    image_rows = [[list(key), int(dist[key])] for key in sorted(dist)]
    assert T.digest_rows(image_rows) == expected['raw_image_digest']

    maps = Q.quotient_map(values)
    qimage = {qtuple(row, maps) for row in image}
    qvalues = tuple(tuple(sorted({row[i] for row in qimage})) for i in range(4))
    assert qvalues == ((0, 1, 2, 3),) * 4
    qclosure = set(QD.pairwise_closure(qimage, qvalues))
    qholes = tuple(sorted(qclosure - qimage))

    qhole_rows = []
    for qrow in qholes:
        raw_candidates = tuple(sorted(row for row in raw_closure if qtuple(row, maps) == qrow))
        assert raw_candidates
        assert all(row not in image for row in raw_candidates)
        qhole_rows.append({
            'quotient_tuple': list(qrow),
            'raw_pairwise_closure_tuples_eliminated': len(raw_candidates),
            'raw_tuples': [list(row) for row in raw_candidates],
        })

    out = {
        'position': 'C',
        'physical_shared_dimension': QD.PHYS_N,
        'target': TARGET,
        'quadruple': list(target),
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
            'EXACT_PHYSICAL_QUAD_OBSTRUCTION_DESCENDS_TO_MAGNITUDE_QUOTIENT'
            if qholes
            else 'PHYSICAL_QUAD_OBSTRUCTION_IS_SIGN_ONLY_AT_MAGNITUDE_QUOTIENT'
        ),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    if qholes:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_QUAD_QUOTIENT_OBSTRUCTION')
        print('theorem=the exact physical quaternary value obstruction contains complete sign-orbit holes and descends to a nontrivial forbidden quaternary relation on the existing magnitude quotient')
    else:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_QUAD_SIGN_ONLY_OBSTRUCTION')
        print('theorem=the exact physical quaternary obstruction forbids no complete magnitude-orbit tuple and therefore requires sign-refined states for global propagation')
    print('boundary=this freezes only the selected quaternary factor; other physical higher-order factors remain open')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
