#!/usr/bin/env python3
import probe_v26_q138_c916_bottleneck_parent_split_scan as P


def main():
    out = P.analyze()
    assert out['position'] == 'C'
    assert out['order'] == 'multiplicity_then_function'
    assert out['splits_scanned'] == 83
    assert out['target_bits'] == 64
    assert out['parent'] == {
        'lo': 166,
        'hi': 250,
        'size': 84,
        'safe_evaluation_bits': 40,
        'generic_safe_evaluation_bits': 40,
        'function_lambda': 44,
        'quadratic_residual_dim': 6,
        'fiber_affine_residual': True,
        'exact_override': False,
        'digest': 'eba0751e307b560c',
    }
    assert out['splits_with_max_child_safe_le_64'] == 36
    assert out['splits_with_max_child_safe_lt_65'] == 36
    assert out['max_child_safe_histogram'] == {
        41: 1, 42: 1, 43: 1, 44: 1, 46: 2, 47: 2, 48: 1,
        49: 3, 50: 1, 51: 2, 52: 1, 53: 1, 54: 2, 55: 1,
        56: 1, 57: 3, 59: 2, 61: 2, 62: 2, 63: 2, 64: 4,
        65: 7, 66: 3, 67: 4, 68: 6, 69: 4, 70: 5, 71: 2,
        72: 2, 73: 1, 74: 2, 75: 7, 76: 1, 77: 3,
    }
    best = out['best_split']
    assert best['split'] == 167
    assert best['max_child_safe_bits'] == 41
    assert best['left']['safe_evaluation_bits'] == 12
    assert best['right']['safe_evaluation_bits'] == 41
    assert best['left']['digest'] == 'c75de23d89df36ba'
    assert best['right']['digest'] == '7130ab82b29c03e1'
    old = out['old_split']
    assert old['split'] == 199
    assert old['max_child_safe_bits'] == 65
    assert old['left']['safe_evaluation_bits'] == 65
    assert old['right']['safe_evaluation_bits'] == 63
    assert old['left']['exact_override'] is True
    assert old['left']['digest'] == '50a4b970f7f85916'
    print('PASS V26_Q138_C916_BOTTLENECK_PARENT_SPLIT_SCAN_RESULT')
    print('exact=83 contiguous splits scanned; 36 admit both direct children <=64; best split 167 has child widths 12 and 41')
    print('decision=proceed to exact threshold64 recursive interval feasibility on [166,250)')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
