#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_aggregate_scalar_gauss_classes as P


def main():
    out = P.analyze()
    assert out['position'] == 'C'
    assert out['small_quadratic_forms_exhaustively_checked'] == 2196
    assert out['groups'] == 250
    assert out['gauss_zero_groups'] == 248
    assert out['gauss_nonzero_groups'] == 2
    assert out['polar_rank_histogram'] == {
        '2': 8,
        '4': 53,
        '6': 71,
        '8': 11,
        '10': 3,
        '12': 1,
        '136': 6,
        '138': 50,
        '140': 41,
        '142': 6,
    }
    assert out['nonzero_sign_histogram_by_multiplicity'] == {
        '1:-1': 1,
        '1:1': 1,
    }
    assert out['nonzero_log2_abs_histogram_by_multiplicity'] == {
        '1:78': 1,
        '1:79': 1,
    }
    assert all(k.startswith('1:') for k in out['nonzero_log2_abs_histogram_by_multiplicity'])
    print('PASS V26_Q138_C916_AGGREGATE_SCALAR_GAUSS_CLASSES_RESULT')
    print('C aggregate scalar Gauss classes: 248 zero, 2 nonzero singleton groups with |G|=2^78 and 2^79 and opposite signs')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
