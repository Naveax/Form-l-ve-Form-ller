#!/usr/bin/env python3
import io, json, os, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C

ZERO_PATH = Path(os.environ.get(
    'C916_ZERO_CROSS_VALUE_AUTHORITY',
    'authorities/zero/c916_e0_first_dyadic_m4_remaining_zero_cross_value_relation_authority.json',
))
EXPECTED_ZERO_VALUE_DIGEST = '5b93c1bae1acb4571690af475439ec9e8539d234d4626935812280eeda401d58'
EXPECTED_ZERO_ROWS = 1125
EXPECTED_EXACT_PAIRWISE_COUNT = C.EXPECTED_EXACT_COUNT


def expected_axis_quotient(rows, cols):
    zr = rows - 1
    zc = cols - 1
    mask = 0
    for i in range(rows):
        for j in range(cols):
            if i == zr or j == zc:
                mask |= 1 << (i * cols + j)
    return mask


def analyze():
    zero = json.loads(ZERO_PATH.read_text())
    assert zero['decision'] == 'M4_REMAINING_ZERO_CROSS_VALUE_RELATIONS_FULL_AUTHORITY'
    assert zero['relation_digest_sha256'] == EXPECTED_ZERO_VALUE_DIGEST
    assert int(zero['remaining_zero_cross_value_pairs']) == EXPECTED_ZERO_ROWS
    assert int(zero['axis_complete_pairs']) == EXPECTED_ZERO_ROWS
    assert int(zero['non_axis_complete_pairs']) == 0
    assert int(zero['independent_sign_reflection_invariant_pairs']) == EXPECTED_ZERO_ROWS
    assert int(zero['non_independent_sign_reflection_pairs']) == 0

    rows = zero['rows']
    assert len(rows) == EXPECTED_ZERO_ROWS
    seen = set()
    qhist = Counter()
    shape = Counter()
    for row in rows:
        u = int(row['left_group_id'])
        v = int(row['right_group_id'])
        key = tuple(sorted((u, v)))
        assert key not in seen
        seen.add(key)
        assert bool(row['axis_complete'])
        assert bool(row['independent_sign_reflection_invariant'])

        nr = int(row['left_image_size'])
        nc = int(row['right_image_size'])
        qr, qc, qm = C.quotient_relation(nr, nc, row['relation_mask_hex'])
        expected = expected_axis_quotient(qr, qc)
        assert qm == expected, (key, nr, nc, qr, qc, hex(qm), hex(expected))
        qhist[(qr, qc, qm)] += 1
        shape[f'{nr}x{nc}'] += 1

    assert shape == Counter({'7x7': 999, '9x7': 97, '7x9': 29})
    assert sum(qhist.values()) == EXPECTED_ZERO_ROWS

    # The older counter constructed these 1,125 quotient factors synthetically as
    # "zero-cross activity" constraints.  The exact value authority above proves
    # that every raw signed relation is the full union of zero axes and descends
    # independently under sign reflection to exactly that same quotient mask.
    # Therefore its integer is not relaxed at the pairwise m4 layer.
    with redirect_stdout(io.StringIO()):
        counted = C.analyze()
    exact_count = int(counted['exact_count'])
    assert exact_count == EXPECTED_EXACT_PAIRWISE_COUNT
    assert int(counted['all_m4_pairs_covered']) == 4005
    assert int(counted['zero_cross_activity_only_relations']) == EXPECTED_ZERO_ROWS

    out = {
        'position': 'C',
        'physical_shared_dimension': C.PHYS_N,
        'exact_pairwise_count': exact_count,
        'exact_pairwise_log2': counted['exact_log2'],
        'state_bits': counted['state_bits'],
        'all_m4_pairs': 4005,
        'subset_exact_value_pairs': 825,
        'equal_exact_value_pairs': 55,
        'overlap_exact_value_pairs': 2000,
        'remaining_zero_cross_exact_value_pairs': EXPECTED_ZERO_ROWS,
        'zero_cross_value_digest_sha256': EXPECTED_ZERO_VALUE_DIGEST,
        'zero_cross_shapes': dict(sorted(shape.items())),
        'zero_cross_all_axis_complete': True,
        'zero_cross_all_independent_sign_reflection': True,
        'pairwise_relaxation_gap': 0,
        'higher_order_constraints_included': False,
        'decision': 'C916_250WAY_WIDTH3_BASE_ALL_4005_M4_PAIRWISE_VALUE_FACTORS_EXACT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_COMPLETE_M4_PAIRWISE_VALUE_EXACT')
    print('theorem=all 1125 formerly activity-only zero-cross factors are exact axis-union value relations and descend to exactly the quotient masks already counted; therefore the frozen integer is exact for all 4005 m4 pairwise value factors')
    print('boundary=projection triples, quadruples, all-order affine constraints, and any higher-order physical-image constraint remain outside this pairwise model')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
