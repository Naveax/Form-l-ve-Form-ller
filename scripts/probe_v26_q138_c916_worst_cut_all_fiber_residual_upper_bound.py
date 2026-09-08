#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_worst_cut_fiber_residual_rank_witness as W

DOMAIN_BITS = W.DOMAIN_BITS
assert DOMAIN_BITS == 149


def flatten_matrix(rows, width):
    z = 0
    for i, row in enumerate(rows):
        assert row >> width == 0
        z |= row << (i * width)
    return z


def unflatten_matrix(z, nrows, width):
    mask = (1 << width) - 1
    return [(z >> (i * width)) & mask for i in range(nrows)]


def xor_subset(items, mask):
    z = 0
    x = mask
    while x:
        b = x & -x
        z ^= items[b.bit_length() - 1]
        x ^= b
    return z


def ceil_log2(n):
    assert n > 0
    return (n - 1).bit_length()


def analyze():
    kernel, origin_rows, full_polars = W.context()
    kdim = len(kernel)
    assert kdim == 93
    assert len(origin_rows) == 13
    assert len(full_polars) == 13

    origin_rank = W.A.L.rank(origin_rows)
    assert origin_rank == 4

    effect_rows = []
    effect_matrices = []
    for s in range(DOMAIN_BITS):
        x = 1 << s
        rows = [
            W.functional_on_kernel(full_polars[i], x, kernel)
            for i in range(13)
        ]
        effect_rows.extend(rows)
        effect_matrices.append(flatten_matrix(rows, kdim))

    # The residual polar forms vanish on K x K. Therefore changing a fiber
    # representative by a kernel vector cannot change the residual linear
    # map on K.
    for k in kernel:
        for i in range(13):
            assert W.functional_on_kernel(full_polars[i], k, kernel) == 0

    common_row_span_rank = W.A.L.rank(origin_rows + effect_rows)
    control_basis = W.A.L.basis(effect_matrices)
    translation_matrix_control_rank = len(control_basis)
    varying_affine_label_rank = DOMAIN_BITS - kdim
    assert varying_affine_label_rank == 56
    assert translation_matrix_control_rank <= varying_affine_label_rank

    # For every representative x0, each residual row on the affine fiber
    # x0 + K equals origin_row_i plus a GF(2)-linear combination of the
    # coordinate translation-effect rows. Hence all thirteen residual rows
    # live in this one common K* row space.
    uniform_rank_upper = common_row_span_rank
    uniform_image_upper = 1 << uniform_rank_upper
    exact_max_rank = None
    exact_max_image = None
    shared_evaluation_upper_bits = varying_affine_label_rank + uniform_rank_upper
    shared_evaluation_upper_states = 1 << shared_evaluation_upper_bits

    if common_row_span_rank == origin_rank:
        exact_max_rank = origin_rank
        exact_max_image = 1 << exact_max_rank
        assert exact_max_rank == 4
        assert uniform_image_upper == 16
        assert shared_evaluation_upper_bits == 60

    # The translation map V/K -> Mat(13,K*) is linear. Its image has the
    # exact dimension reported above, so each matrix in the image is attained
    # by exactly 2^(56-d) affine labels. When d is small, enumerate that image
    # exactly and recover the rank distribution over every one of the 2^56
    # affine fibers, not a sample.
    control_rank_hist = None
    all_fiber_rank_hist = None
    exact_shared_evaluation_states = None
    exact_shared_evaluation_ceiling_bits = None
    fiber_labels_per_control_state = None
    control_states = None

    if translation_matrix_control_rank <= 20:
        d = translation_matrix_control_rank
        control_states = 1 << d
        fiber_labels_per_control_state = 1 << (varying_affine_label_rank - d)
        hist = Counter()
        image_size_sum = 0
        for m in range(control_states):
            flat = xor_subset(control_basis, m)
            erows = unflatten_matrix(flat, 13, kdim)
            rows = [origin_rows[i] ^ erows[i] for i in range(13)]
            r = W.A.L.rank(rows)
            hist[r] += 1
            image_size_sum += 1 << r
        control_rank_hist = dict(sorted(hist.items()))
        all_fiber_rank_hist = {
            r: count * fiber_labels_per_control_state
            for r, count in sorted(hist.items())
        }
        assert sum(all_fiber_rank_hist.values()) == 1 << varying_affine_label_rank
        exact_shared_evaluation_states = image_size_sum * fiber_labels_per_control_state
        exact_shared_evaluation_ceiling_bits = ceil_log2(exact_shared_evaluation_states)
        assert exact_shared_evaluation_states <= shared_evaluation_upper_states
        assert max(hist) == exact_max_rank

    out = {
        'position': 'C',
        'edge': {'lo': 110, 'hi': 166, 'size': 56},
        'function_lambda': 70,
        'shared_affine_function_dim': 57,
        'varying_affine_label_rank': varying_affine_label_rank,
        'fiber_kernel_dim': kdim,
        'quadratic_residual_dim': 13,
        'origin_fiber_residual_rank': origin_rank,
        'origin_fiber_image_size': 1 << origin_rank,
        'translation_effect_vectors': len(effect_rows),
        'common_kernel_dual_row_span_rank': common_row_span_rank,
        'translation_matrix_control_rank': translation_matrix_control_rank,
        'translation_matrix_control_states': control_states,
        'fiber_labels_per_control_state': fiber_labels_per_control_state,
        'control_state_residual_rank_histogram': control_rank_hist,
        'all_affine_fiber_residual_rank_histogram': all_fiber_rank_hist,
        'all_fiber_residual_rank_upper_bound': uniform_rank_upper,
        'all_fiber_residual_image_upper_bound': uniform_image_upper,
        'max_fiber_residual_rank_exact': exact_max_rank,
        'max_fiber_residual_image_exact': exact_max_image,
        'shared_evaluation_state_upper_bits': shared_evaluation_upper_bits,
        'shared_evaluation_state_upper_bound': shared_evaluation_upper_states,
        'exact_shared_evaluation_state_count': exact_shared_evaluation_states,
        'exact_shared_evaluation_state_ceiling_bits': exact_shared_evaluation_ceiling_bits,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)

    if exact_max_rank == 4:
        print('PASS V26_Q138_C916_WORST_CUT_ALL_FIBER_RESIDUAL_UPPER_BOUND')
        print('verdict=ALL_FIBER_RESIDUAL_RANK_AT_MOST_4_AND_MAX_EXACTLY_4')
        print('scope=exact all-affine-fiber residual evaluation geometry for the unique width-70 C edge')
        print('method=all origin residual rows and all 149 coordinate translation-effect rows lie in one 4-dimensional subspace of K*; enumerate the exact 4-dimensional translation-matrix image')
        print('important=the unique width-70 edge has at most 2^56 affine labels times 2^4 residual values; when the 4D control image is enumerated, the exact realizable shared-evaluation tuple count is also reported')
    else:
        print('PASS V26_Q138_C916_WORST_CUT_ALL_FIBER_RESIDUAL_DIAGNOSTIC')
        print('verdict=COMMON_ROW_SPAN_EXCEEDS_ORIGIN_RANK')
        print('scope=exact common K* row-span diagnostic for the unique width-70 C edge')
    print('not_included=other tree edges, full-tree evaluation width, aggregate e0 carry, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
