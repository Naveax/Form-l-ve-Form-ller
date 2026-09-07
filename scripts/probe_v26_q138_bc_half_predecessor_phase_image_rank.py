#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import probe_v26_q138_bc_direct_e1_exact_sector_cancellation as X
import probe_v26_q138_bc_second_residue_fixed_predecessor_specialization as F
import probe_v26_q138_bc_second_residue_reachable_predecessor_geometry as G


def insert(B, x):
    y = x
    while y:
        p = y.bit_length() - 1
        if p not in B:
            B[p] = y
            return True
        y ^= B[p]
    return False


def rank(rows):
    B = {}
    for x in rows:
        insert(B, x)
    return len(B)


def bilinear(polar, a, b):
    z = 0
    y = a
    while y:
        lb = y & -y
        i = lb.bit_length() - 1
        y ^= lb
        z ^= (polar[i] & b).bit_count() & 1
    return z


def xor_dirs(dirs, coeff):
    out = 0
    for i, d in enumerate(dirs):
        if (coeff >> i) & 1:
            out ^= d
    return out


def feature_columns(pos, half_can, null, phases):
    support_width = len(half_can)
    left_width = 4 * len(F.LEXT)
    right_width = 4 * len(F.REXT)
    cols = []
    for d in null:
        z = 0
        shift = 0
        for e, row in enumerate(half_can):
            if (row & d).bit_count() & 1:
                z |= 1 << (shift + e)
        shift += support_width
        for _c, _lin, polar in phases:
            for a, el in enumerate(F.LEXT):
                if (polar[el] & d).bit_count() & 1:
                    z |= 1 << (shift + a)
            shift += len(F.LEXT)
        for _c, _lin, polar in phases:
            for a, er in enumerate(F.REXT):
                if (polar[er] & d).bit_count() & 1:
                    z |= 1 << (shift + a)
            shift += len(F.REXT)
        assert shift == support_width + left_width + right_width
        cols.append(z)
    return cols, support_width, left_width, right_width


def kernel_coeff_basis(cols):
    if not cols:
        return []
    width = max((c.bit_length() for c in cols), default=0)
    rows = []
    for b in range(width):
        r = 0
        for j, c in enumerate(cols):
            if (c >> b) & 1:
                r |= 1 << j
        if r:
            rows.append((r, 0))
    sol = T.rref(rows, n=len(cols))
    assert sol is not None and sol[1] == 0
    return sol[2]


def main():
    _e0, _e1, half = H.classify_patterns()
    assert len(half) == 4

    for pos in 'BC':
        _groups, half_can = G.support_groups(pos)
        cond = G.predecessor_condition(half_can)
        sol = T.rref(cond, n=G.PRED_BITS)
        assert sol is not None
        p0, null = sol[1], sol[2]
        assert F.fixed_possible(half_can, p0)

        phases = []
        for zs, cls in half:
            assert cls == (128, 0, 0)
            can = H.support_for(pos, zs, cls)
            assert can == half_can
            c, lin, polar, irank, pr = X.full_corrected_phase(pos, D.carries(zs))
            assert irank == 128 and pr == 0
            phases.append((c, lin, polar))

        cols, sw, lw, rw = feature_columns(pos, half_can, null, phases)
        fr = rank(cols)
        kcoeff = kernel_coeff_basis(cols)
        kdirs = [xor_dirs(null, v) for v in kcoeff]
        assert len(kdirs) == len(null) - fr
        assert all(feature_columns(pos, half_can, [d], phases)[0][0] == 0 for d in kdirs)

        cross_ranks = []
        derivative_patterns = []
        for d in kdirs:
            pat = 0
            for i, (c, lin, polar) in enumerate(phases):
                if X.q_eval(c, lin, polar, p0 ^ d) ^ X.q_eval(c, lin, polar, p0):
                    pat |= 1 << i
            derivative_patterns.append(pat)

        for _c, _lin, polar in phases:
            rows = []
            for kd in kdirs:
                r = 0
                for j, nd in enumerate(null):
                    if bilinear(polar, kd, nd):
                        r |= 1 << j
                rows.append(r)
            cross_ranks.append(rank(rows))

        pattern_rank = rank(derivative_patterns)
        pattern_set = sorted(set(derivative_patterns))
        print(
            'position', pos,
            'half_predecessor_constraint_count', len(cond),
            'half_predecessor_affine_nullity', len(null),
            'linear_feature_width', sw + lw + rw,
            'support_rhs_width', sw,
            'left_frequency_width', lw,
            'right_scalar_linear_width', rw,
            'linear_feature_rank', fr,
            'linear_feature_kernel_dim', len(kdirs),
            'kernel_to_null_quadratic_cross_ranks', cross_ranks,
            'kernel_phase_derivative_pattern_rank', pattern_rank,
            'kernel_phase_derivative_patterns', pattern_set,
            flush=True,
        )

    print('PASS V26_Q138_BC_HALF_PREDECESSOR_PHASE_IMAGE_RANK')
    print('scope=half-active predecessor dependence rank diagnostic; no uniform second-lift claim')
    print('interpretation=small linear feature rank plus trivial kernel quadratic action would support exact predecessor-signature enumeration')


if __name__ == '__main__':
    main()
