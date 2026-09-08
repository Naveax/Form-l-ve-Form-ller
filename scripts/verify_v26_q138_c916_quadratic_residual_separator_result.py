#!/usr/bin/env python3
import probe_v26_q138_c916_quadratic_residual_separator as P

out = P.analyze()

assert out['position'] == 'C'
assert out['support_groups'] == 250
assert out['tree_edges_analyzed'] == 498
assert out['function_global_rank'] == 321
assert out['linear_global_rank'] == 149
assert out['scalar_global_rank'] == 199
assert out['polar_global_rank'] == 171
assert out['best_combined_function_tree_width'] == 70
assert out['best_combined_function_tree_depth'] == 10
assert out['max_function_lambda'] == 70
assert out['max_direct_linear_lambda_on_function_tree'] == 58
assert out['max_quadratic_residual_dim'] == 13
assert out['max_affine_from_scalar_combinations'] == 5
assert out['quadratic_residual_histogram'] == {
    0: 175, 1: 203, 2: 57, 3: 25, 4: 15, 5: 7, 6: 7,
    7: 2, 8: 1, 9: 2, 10: 1, 12: 2, 13: 1,
}

for root in out['root_children']:
    assert root['function_lambda'] == 44
    assert root['direct_linear_lambda'] == 33
    assert root['shared_affine_dim'] == 38
    assert root['quadratic_residual_dim'] == 6
    assert root['polar_lambda'] == 6
    assert root['scalar_lambda'] == 8
    assert root['affine_from_scalar_combinations'] == 5

b = out['balanced_cut']
assert b == {
    'size': 125,
    'complement_size': 125,
    'function_lambda': 72,
    'shared_affine_dim': 60,
    'direct_linear_lambda': 55,
    'affine_from_scalar_combinations': 5,
    'quadratic_residual_dim': 12,
    'scalar_lambda': 6,
    'polar_lambda': 12,
}

w = out['worst_function_edges'][0]
assert w['function_lambda'] == 70
assert w['shared_affine_dim'] == 57
assert w['direct_linear_lambda'] == 56
assert w['affine_from_scalar_combinations'] == 1
assert w['quadratic_residual_dim'] == 13
assert w['polar_lambda'] == 13
assert w['scalar_lambda'] == 8
assert w['lo'] == 110 and w['hi'] == 166 and w['size'] == 56

print('PASS V26_Q138_C916_QUADRATIC_RESIDUAL_SEPARATOR_RESULT')
print('C function-tree width=70; max genuine quadratic residual=13; worst edge decomposes as 57 affine + 13 quadratic')
print('root edges=38 affine + 6 quadratic; balanced cut=60 affine + 12 quadratic')
print('ALPHA_PASS=0')
