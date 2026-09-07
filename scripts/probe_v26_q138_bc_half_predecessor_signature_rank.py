#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import probe_v26_q138_bc_direct_e1_exact_sector_cancellation as X
import probe_v26_q138_bc_second_residue_fixed_predecessor_specialization as F
import probe_v26_q138_bc_second_residue_reachable_predecessor_geometry as G

PRED_BITS = 128
PRED_MASK = (1 << PRED_BITS) - 1


def restrict_form(mask, null):
    z = 0
    for j, d in enumerate(null):
        if (mask & d).bit_count() & 1:
            z |= 1 << j
    return z


def rank_restricted(masks, null):
    return len(S.row_basis([restrict_form(m, null) for m in masks if m]))


def bilinear(polar, x, y):
    z = 0
    t = x
    while t:
        b = t & -t
        i = b.bit_length() - 1
        t ^= b
        z ^= (polar[i] & y).bit_count() & 1
    return z


def restricted_polar_rank(polar, null):
    rows = []
    for d in null:
        row = 0
        for j, e in enumerate(null):
            if bilinear(polar, d, e):
                row |= 1 << j
        rows.append(row)
    return len(S.row_basis(rows))


def analyze(pos):
    _e0, _e1, half = H.classify_patterns()
    assert len(half) == 4
    cans = []
    sectors = []
    for zs, cls in half:
        assert cls == (128, 0, 0)
        can = H.support_for(pos, zs, cls)
        assert can is not None
        cans.append(can)
        sectors.append((zs, X.full_corrected_phase(pos, D.carries(zs))))
    assert all(can == cans[0] for can in cans)
    can = cans[0]

    cond = G.predecessor_condition(can)
    sol = T.rref(cond, n=PRED_BITS)
    assert sol is not None
    particular, null = sol[1], sol[2]
    assert F.fixed_possible(can, particular)

    support_masks = [row & PRED_MASK for row in can]
    left_masks = []
    right_masks = []
    polar_ranks = []

    for zs, data in sectors:
        c, lin, polar, rank, pr = data
        assert rank == 128 and pr == 0
        left_masks.extend((polar[e] & PRED_MASK) for e in F.LEXT)
        right_masks.extend((polar[e] & PRED_MASK) for e in F.REXT)
        polar_ranks.append(restricted_polar_rank(polar, null))

    support_rank = rank_restricted(support_masks, null)
    left_rank = rank_restricted(left_masks, null)
    right_rank = rank_restricted(right_masks, null)
    phase_linear_rank = rank_restricted(left_masks + right_masks, null)
    full_linear_rank = rank_restricted(support_masks + left_masks + right_masks, null)

    # The four predecessor-only phase constants are quadratic functions on the
    # half-support predecessor affine space. Regardless of their internal
    # quadratic ranks they add at most four Boolean output bits to a complete
    # predecessor signature. This gives a safe finite-state count envelope.
    state_log2_cap = full_linear_rank + 4

    print(
        'position', pos,
        'half_predecessor_constraint_count', len(cond),
        'half_predecessor_affine_nullity', len(null),
        'support_rhs_variation_rank', support_rank,
        'left_phase_frequency_variation_rank', left_rank,
        'right_linear_phase_variation_rank', right_rank,
        'joint_phase_linear_variation_rank', phase_linear_rank,
        'full_linear_signature_rank', full_linear_rank,
        'restricted_constant_quadratic_polar_ranks', polar_ranks,
        'complete_signature_log2_state_cap', state_log2_cap,
        flush=True,
    )

    # Sanity: the chosen particular is genuinely in the projected half support.
    assert all((((m & particular).bit_count() & 1) == rhs) for m, rhs in cond)


def main():
    for pos in 'BC':
        analyze(pos)
    print('PASS V26_Q138_BC_HALF_PREDECESSOR_SIGNATURE_RANK')
    print('scope=half-support predecessor dependence diagnostic only')
    print('next=enumerate exact predecessor signatures only if the printed finite-state cap is tractable')


if __name__ == '__main__':
    main()
