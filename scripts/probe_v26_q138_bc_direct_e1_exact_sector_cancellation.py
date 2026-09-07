#!/usr/bin/env python3
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as B
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H

NEXT = 160
MASK = (1 << NEXT) - 1


def add_affine(state, form):
    c, lin, polar = state
    m, b = form
    c ^= b & 1
    lin ^= m
    return c, lin, polar


def add_product(state, f, g):
    # Exact Boolean ANF product of two affine forms on the 160 external bits.
    # polar[i]_j is the symmetric zero-diagonal polar coefficient B(e_i,e_j).
    c, lin, polar = state
    fm, fc = f
    gm, gc = g
    c ^= fc & gc
    if fc:
        lin ^= gm
    if gc:
        lin ^= fm
    # x_i^2=x_i contributes the diagonal product to the linear part.
    lin ^= fm & gm
    x = fm
    while x:
        b = x & -x
        i = b.bit_length() - 1
        polar[i] ^= gm
        x ^= b
    x = gm
    while x:
        b = x & -x
        i = b.bit_length() - 1
        polar[i] ^= fm
        x ^= b
    return c, lin, polar


def full_corrected_phase(pos, Cmask):
    # Same Gauss-completed phase as corrected_phase_data(), but retain also
    # the right-only quadratic/linear terms rather than quotienting them out.
    sol = A.internal_null(pos, Cmask)
    _, _, NB = sol
    dirs, pr = B.radical_directions(pos, NB)
    FF0 = D.full_forms(pos)
    extras = [A.derivative_form(FF0, A.map_internal_to_full(d)) for d in dirs]
    FF, subs, rank, eindex = S.generalized_substitution(pos, Cmask, extras)
    state = (0, 0, [0] * NEXT)
    for j in range(1, 5):
        for i in range(31):
            X = T.xx(FF[j, i, 'u'], FF[j, i, 'w'])
            Y = T.xx(FF[j, i, 'v'], FF[j, i, 'w'])
            xf = A.sub_form(X, subs, eindex)
            yf = A.sub_form(Y, subs, eindex)
            state = add_product(state, xf, yf)
    if pr:
        PP = B.polar_rows(pos, NB)
        mons, coeff, allowed = S.gauss_sign_anf(PP, len(NB))
        forms = []
        for d in NB:
            der = A.derivative_form(FF, A.map_internal_to_full(d))
            forms.append(A.sub_form(der, subs, eindex))
        for k, mo in enumerate(mons):
            if not ((coeff >> k) & 1):
                continue
            if len(mo) == 0:
                c, lin, polar = state
                state = (c ^ 1, lin, polar)
            elif len(mo) == 1:
                state = add_affine(state, forms[mo[0]])
            else:
                state = add_product(state, forms[mo[0]], forms[mo[1]])
    c, lin, polar = state
    assert all(((polar[i] >> i) & 1) == 0 for i in range(NEXT))
    assert all(((polar[i] >> j) & 1) == ((polar[j] >> i) & 1)
               for i in range(NEXT) for j in range(i + 1, NEXT))
    return c, lin, tuple(polar), rank, pr


def polar_mul(polar, x):
    z = 0
    while x:
        b = x & -x
        z ^= polar[b.bit_length() - 1]
        x ^= b
    return z


def q_eval(c, lin, polar, x):
    z = c ^ ((lin & x).bit_count() & 1)
    y = x
    while y:
        b = y & -y
        i = b.bit_length() - 1
        # Count each unordered quadratic pair exactly once.
        hi = x & ~((1 << (i + 1)) - 1)
        z ^= ((polar[i] & hi).bit_count() & 1)
        y ^= b
    return z


def support_param(can):
    eq = [(row & MASK, (row >> NEXT) & 1) for row in can]
    sol = T.rref(eq, n=NEXT)
    assert sol is not None
    rank, x0, basis = sol
    return rank, x0, tuple(basis)


def restricted_phase_signature(phase, x0, basis):
    c, lin, polar, _rank, _pr = phase
    d = len(basis)
    q0 = q_eval(c, lin, polar, x0)
    sig = q0
    bit = 1
    for b in basis:
        bit += 1
        if q_eval(c, lin, polar, x0 ^ b) ^ q0:
            sig |= 1 << (bit - 1)
    pimages = [polar_mul(polar, b) for b in basis]
    for i in range(d):
        for j in range(i + 1, d):
            bit += 1
            if (pimages[i] & basis[j]).bit_count() & 1:
                sig |= 1 << (bit - 1)
    # bit0 is the global sign on this affine support. All other bits specify
    # the restricted nonconstant quadratic phase in a deterministic support
    # coordinate basis.
    return sig, d, bit


def main():
    _e0, e1, _half = H.classify_patterns()
    assert [len(e1[k]) for k in range(4)] == [0, 102, 2397, 8196]
    for pos in 'BC':
        groups = defaultdict(list)
        raw = unreachable = 0
        byk = Counter()
        for k in range(4):
            for zs, cls in e1[k]:
                can = H.support_for(pos, zs, cls)
                if can is None:
                    unreachable += 1
                    continue
                raw += 1
                byk[k] += 1
                groups[can].append((zs, cls))
        mult = Counter(len(v) for v in groups.values())
        duplicate_groups = {can: arr for can, arr in groups.items() if len(arr) > 1}
        duplicate_sector_count = sum(len(v) for v in duplicate_groups.values())

        exact_zero_classes = 0
        exact_nonzero_classes = 0
        odd_coefficient_classes = 0
        even_nonzero_classes = 0
        zeroed_support_groups = 0
        duplicate_raw = 0
        combined_class_count = 0
        coefficient_hist = Counter()
        free_dim_hist = Counter()
        phase_bits_max = 0

        for can, arr in duplicate_groups.items():
            srank, x0, basis = support_param(can)
            free_dim_hist[len(basis)] += 1
            C = Counter()
            for zs, cls in arr:
                phase = full_corrected_phase(pos, D.carries(zs))
                sig, d, nbits = restricted_phase_signature(phase, x0, basis)
                assert d == len(basis)
                phase_bits_max = max(phase_bits_max, nbits)
                # Same nonconstant restricted phase, constant differing by one,
                # gives exactly opposite signed matrices on the same support.
                nonconst = sig >> 1
                sgn = -1 if (sig & 1) else 1
                C[nonconst] += sgn
            duplicate_raw += len(arr)
            combined_class_count += len(C)
            nz = 0
            for coeff in C.values():
                coefficient_hist[coeff] += 1
                if coeff == 0:
                    exact_zero_classes += 1
                else:
                    nz += 1
                    exact_nonzero_classes += 1
                    if coeff & 1:
                        odd_coefficient_classes += 1
                    else:
                        even_nonzero_classes += 1
            if nz == 0:
                zeroed_support_groups += 1

        singleton_groups = mult.get(1, 0)
        total_exact_nonzero_sector_classes = singleton_groups + exact_nonzero_classes
        # For a K1 integer lift modulo2, even coefficients may be deferred to
        # the next dyadic residual. This count is diagnostic only; no rank sum
        # is admitted from it because one surviving class can itself rank2048.
        total_odd_lift_classes = singleton_groups + odd_coefficient_classes

        print('position', pos,
              'reachable_e1_sectors', raw,
              'unreachable_e1', unreachable,
              'reachable_by_zero_count', dict(sorted(byk.items())),
              'support_groups', len(groups),
              'support_multiplicity_distribution', dict(sorted(mult.items())),
              'duplicate_support_groups', len(duplicate_groups),
              'duplicate_sector_count', duplicate_sector_count,
              flush=True)
        print('position', pos,
              'duplicate_support_free_dimension_distribution', dict(sorted(free_dim_hist.items())),
              'duplicate_restricted_phase_classes_before_sign_combine', combined_class_count,
              'exact_opposite_zero_classes', exact_zero_classes,
              'exact_nonzero_combined_classes', exact_nonzero_classes,
              'odd_coefficient_classes', odd_coefficient_classes,
              'even_nonzero_coefficient_classes', even_nonzero_classes,
              'zeroed_entire_support_groups', zeroed_support_groups,
              'coefficient_histogram', dict(sorted(coefficient_hist.items())),
              'max_restricted_phase_signature_bits', phase_bits_max,
              flush=True)
        print('position', pos,
              'total_exact_nonzero_sector_classes_after_same_support_phase_combine', total_exact_nonzero_sector_classes,
              'total_odd_classes_available_for_mod2_K1_lift', total_odd_lift_classes,
              flush=True)

    print('PASS PROBE V26_Q138_BC_DIRECT_E1_EXACT_SECTOR_CANCELLATION')
    print('theorem_scope=exact whole-sector equality/opposition after restricting the full Gauss-completed quadratic phase to each identical affine support')
    print('important=classes with different affine supports are not combined; partial cross-support cancellation and complete aggregate Schmidt rank remain open')


if __name__ == '__main__':
    main()
