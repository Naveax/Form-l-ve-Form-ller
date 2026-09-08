#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_local_group_separator as P
import probe_v26_q138_bc_e0_quadratic_scalar_refinement as Q
import probe_v26_q138_bc_direct_e1_exact_sector_cancellation as X

POS = 'C'


def phase_tuple(zs):
    ph = Q.scalar_phase(POS, zs)
    return (
        ph['c'],
        ph['lin'],
        ph['polar'],
        ph['internal_rank'],
        ph['internal_pr'],
    )


def analyze():
    e0, _e1, _half = P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for k in range(4):
        for zs, cls in e0[k]:
            can = P.U.H.support_for(POS, zs, cls)
            if can is None:
                continue
            raw += 1
            grouped[can].append((zs, cls))

    assert raw == 577
    assert len(grouped) == 250
    mult_hist = Counter(len(v) for v in grouped.values())
    assert dict(sorted(mult_hist.items())) == {1: 103, 2: 57, 4: 90}

    coefficient_hist = Counter()
    abs_coefficient_hist = Counter()
    classes_per_group_hist = Counter()
    nonzero_classes_per_group_hist = Counter()
    free_dim_hist = Counter()
    signature_bits_hist = Counter()

    exact_zero_classes = 0
    exact_nonzero_classes = 0
    odd_coefficient_classes = 0
    even_nonzero_coefficient_classes = 0
    zeroed_entire_support_groups = 0
    groups_with_phase_collision = 0
    groups_with_abs_coefficient_gt1 = 0
    total_phase_classes_before_sign_combine = 0
    max_abs_coefficient = 0

    compact_groups = []
    for gid, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        _srank, x0, basis = X.support_param(can)
        free_dim_hist[len(basis)] += 1
        coeffs = Counter()
        max_nbits = 0
        for zs, _cls in sectors:
            sig, d, nbits = X.restricted_phase_signature(
                phase_tuple(zs), x0, basis
            )
            assert d == len(basis)
            max_nbits = max(max_nbits, nbits)
            nonconstant_phase = sig >> 1
            sign = -1 if (sig & 1) else 1
            coeffs[nonconstant_phase] += sign

        signature_bits_hist[max_nbits] += 1
        classes_per_group_hist[len(coeffs)] += 1
        total_phase_classes_before_sign_combine += len(coeffs)
        if len(coeffs) < len(sectors):
            groups_with_phase_collision += 1

        nz = 0
        group_max_abs = 0
        for coeff in coeffs.values():
            coefficient_hist[coeff] += 1
            abs_coefficient_hist[abs(coeff)] += 1
            group_max_abs = max(group_max_abs, abs(coeff))
            max_abs_coefficient = max(max_abs_coefficient, abs(coeff))
            if coeff == 0:
                exact_zero_classes += 1
                continue
            nz += 1
            exact_nonzero_classes += 1
            if coeff & 1:
                odd_coefficient_classes += 1
            else:
                even_nonzero_coefficient_classes += 1

        nonzero_classes_per_group_hist[nz] += 1
        if nz == 0:
            zeroed_entire_support_groups += 1
        if group_max_abs > 1:
            groups_with_abs_coefficient_gt1 += 1

        compact_groups.append({
            'group_id': gid,
            'multiplicity': len(sectors),
            'free_dimension': len(basis),
            'restricted_nonconstant_phase_classes': len(coeffs),
            'nonzero_integer_classes': nz,
            'max_abs_coefficient': group_max_abs,
        })

    singleton_groups = mult_hist[1]
    assert max_abs_coefficient <= 4

    out = {
        'position': POS,
        'raw_e0_sectors': raw,
        'support_groups': len(grouped),
        'support_multiplicity_histogram': dict(sorted(mult_hist.items())),
        'support_free_dimension_histogram': dict(sorted(free_dim_hist.items())),
        'phase_signature_bits_histogram': dict(sorted(signature_bits_hist.items())),
        'restricted_phase_classes_before_sign_combine': total_phase_classes_before_sign_combine,
        'classes_per_group_histogram': dict(sorted(classes_per_group_hist.items())),
        'nonzero_classes_per_group_histogram': dict(sorted(nonzero_classes_per_group_hist.items())),
        'coefficient_histogram': dict(sorted(coefficient_hist.items())),
        'absolute_coefficient_histogram': dict(sorted(abs_coefficient_hist.items())),
        'exact_opposite_zero_classes': exact_zero_classes,
        'exact_nonzero_integer_classes': exact_nonzero_classes,
        'odd_coefficient_classes': odd_coefficient_classes,
        'even_nonzero_coefficient_classes': even_nonzero_coefficient_classes,
        'zeroed_entire_support_groups': zeroed_entire_support_groups,
        'groups_with_restricted_phase_collision': groups_with_phase_collision,
        'groups_with_abs_coefficient_gt1': groups_with_abs_coefficient_gt1,
        'max_abs_coefficient': max_abs_coefficient,
        'singleton_groups': singleton_groups,
        'groups': compact_groups,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_SAME_SUPPORT_INTEGER_COEFFICIENTS')
    print('scope=exact signed-integer combination only among C e0 sectors having identical affine support and identical restricted nonconstant quadratic phase; each constituent contributes +1 or -1 according to the restricted constant phase bit')
    print('important=this is an arithmetic precursor for grouped-e0 carry; different restricted phase classes are not combined and no state-dependent cross-class carry contraction is claimed')
    print('next=use the exact coefficient parity/valuation distribution to define the first dyadic carry residual before separator compression')
    print('not_included=cross-phase integer combination, aggregate e0 carry contraction, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
