#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_local_gauss_transform_quotient_geometry as L
import probe_v26_q138_c916_e0_same_support_integer_coefficients as C
import probe_v26_q138_c916_e0_complete_first_dyadic_fiber_geometry as G
import probe_v26_q138_c916_e0_first_dyadic_pair_residual as R

POS = 'C'


def parity(x):
    return int(x).bit_count() & 1


def transform_constraints(t):
    return list(zip(t['support_control_rows'], t['support_control_rhs']))


def affine_subset(t, constraints):
    x0 = t['support_x0']
    basis = t['support_basis']
    for m, rhs in constraints:
        if parity(m & x0) != rhs:
            return False
        if any(parity(m & b) for b in basis):
            return False
    return True


def support_relation(left, right, p):
    lc = transform_constraints(left)
    rc = transform_constraints(right)
    inter = C.P.U.T.rref(lc + rc, n=p)
    if inter is None:
        return 'disjoint', None

    left_in_right = affine_subset(left, rc)
    right_in_left = affine_subset(right, lc)
    if left_in_right and right_in_left:
        relation = 'equal'
    elif left_in_right:
        relation = 'left_subset_right'
    elif right_in_left:
        relation = 'right_subset_left'
    else:
        relation = 'overlap_incomparable'
    return relation, inter


def xor_rows(a, b):
    assert len(a) == len(b)
    return tuple(x ^ y for x, y in zip(a, b))


def classify_pair(left, right, p):
    relation, inter = support_relation(left, right, p)
    e1 = left['log2_abs_nonzero_gauss']
    e2 = right['log2_abs_nonzero_gauss']
    assert e1 is not None and e2 is not None
    naive_min_valuation = min(e1, e2) - 1

    rec = {
        'support_relation': relation,
        'left_support_rank': left['support_control_rank'],
        'right_support_rank': right['support_control_rank'],
        'left_log2_abs': e1,
        'right_log2_abs': e2,
        'amplitude_delta': abs(e1 - e2),
        'intersection_rank': None,
        'intersection_dimension': None,
        'sign_difference_type': None,
        'sign_difference_constant_bit': None,
        'sign_difference_linear_weight': None,
        'sign_difference_polar_rank': None,
        'overlap_arithmetic': None,
        'global_pair_class': None,
        'first_dyadic_min_nonzero_valuation': None,
        'valuation_gain_over_naive': None,
    }

    if inter is None:
        rec['overlap_arithmetic'] = 'no_overlap'
        rec['global_pair_class'] = 'disjoint_support_residual'
        rec['first_dyadic_min_nonzero_valuation'] = naive_min_valuation
        rec['valuation_gain_over_naive'] = 0
        return rec

    irank, ix0, ibasis = inter
    dc, dlin, drows = L.restrict_form(
        left['shared_survivor_constant'] ^ right['shared_survivor_constant'],
        left['shared_survivor_linear'] ^ right['shared_survivor_linear'],
        xor_rows(left['shared_survivor_rows'], right['shared_survivor_rows']),
        ix0,
        ibasis,
    )
    drank = R.gf2_rank(drows)
    assert drank % 2 == 0

    if drank == 0 and dlin == 0:
        dtype = 'constant'
    elif drank == 0:
        dtype = 'affine_nonconstant'
    else:
        dtype = 'quadratic_nonconstant'

    if e1 != e2:
        overlap = 'unequal_amplitude_no_cancellation'
    elif dtype == 'constant':
        overlap = 'equal_amplitude_same_sign' if dc == 0 else 'equal_amplitude_opposite_sign'
    elif dtype == 'affine_nonconstant':
        overlap = 'equal_amplitude_affine_switch'
    else:
        overlap = 'equal_amplitude_quadratic_switch'

    if relation == 'equal' and e1 == e2 and dtype == 'constant':
        global_class = 'exact_equal_transform' if dc == 0 else 'exact_zero_transform'
    else:
        global_class = 'genuine_residual'

    if global_class == 'exact_zero_transform':
        min_val = None
        gain = None
    elif relation == 'equal' and e1 == e2:
        min_val = e1
        gain = 1
    else:
        min_val = naive_min_valuation
        gain = 0

    rec.update({
        'intersection_rank': irank,
        'intersection_dimension': len(ibasis),
        'sign_difference_type': dtype,
        'sign_difference_constant_bit': dc if dtype == 'constant' else None,
        'sign_difference_linear_weight': dlin.bit_count(),
        'sign_difference_polar_rank': drank,
        'overlap_arithmetic': overlap,
        'global_pair_class': global_class,
        'first_dyadic_min_nonzero_valuation': min_val,
        'valuation_gain_over_naive': gain,
    })
    return rec


def make_synthetic_transform(constraints, p, exponent, c, lin, rows):
    sol = C.P.U.T.rref(constraints, n=p)
    assert sol is not None
    rank, x0, basis = sol
    return {
        'support_control_rank': rank,
        'support_control_rows': tuple(m for m, _rhs in constraints),
        'support_control_rhs': tuple(rhs for _m, rhs in constraints),
        'support_x0': x0,
        'support_basis': tuple(basis),
        'log2_abs_nonzero_gauss': exponent,
        'shared_survivor_constant': c,
        'shared_survivor_linear': lin,
        'shared_survivor_rows': tuple(rows),
    }


def eval_transform(t, s):
    if any(
        parity(m & s) != rhs
        for m, rhs in transform_constraints(t)
    ):
        return 0
    q = L.q_eval(
        t['shared_survivor_constant'],
        t['shared_survivor_linear'],
        t['shared_survivor_rows'],
        s,
    )
    amp = 1 << t['log2_abs_nonzero_gauss']
    return -amp if q else amp


def v2_nonzero(z):
    z = abs(int(z))
    assert z
    return (z & -z).bit_length() - 1


def synthetic_pair_regression():
    p = 3
    systems = (
        (),
        ((1, 0),),
        ((1, 1),),
        ((2, 0),),
        ((1, 0), (2, 0)),
        ((3, 0),),
    )
    zero_rows = (0, 0, 0)
    quad01 = (2, 1, 0)
    forms = (
        (0, 0, zero_rows),
        (1, 0, zero_rows),
        (0, 1, zero_rows),
        (0, 0, quad01),
    )
    tested = 0

    for lc in systems:
        for rc in systems:
            for e1 in (4, 5):
                for e2 in (4, 5):
                    for f1 in forms:
                        for f2 in forms:
                            left = make_synthetic_transform(lc, p, e1, *f1)
                            right = make_synthetic_transform(rc, p, e2, *f2)
                            got = classify_pair(left, right, p)

                            ltruth = tuple(eval_transform(left, s) != 0 for s in range(1 << p))
                            rtruth = tuple(eval_transform(right, s) != 0 for s in range(1 << p))
                            overlap = any(a and b for a, b in zip(ltruth, rtruth))
                            if not overlap:
                                expected_relation = 'disjoint'
                            else:
                                linr = all((not a) or b for a, b in zip(ltruth, rtruth))
                                rinl = all((not b) or a for a, b in zip(ltruth, rtruth))
                                if linr and rinl:
                                    expected_relation = 'equal'
                                elif linr:
                                    expected_relation = 'left_subset_right'
                                elif rinl:
                                    expected_relation = 'right_subset_left'
                                else:
                                    expected_relation = 'overlap_incomparable'
                            assert got['support_relation'] == expected_relation

                            values = []
                            for s in range(1 << p):
                                num = eval_transform(left, s) + eval_transform(right, s)
                                assert num % 2 == 0
                                values.append(num // 2)
                            nz = [z for z in values if z]
                            if not nz:
                                assert got['global_pair_class'] == 'exact_zero_transform'
                                assert got['first_dyadic_min_nonzero_valuation'] is None
                            else:
                                exact_min = min(v2_nonzero(z) for z in nz)
                                assert got['first_dyadic_min_nonzero_valuation'] == exact_min
                                assert got['global_pair_class'] != 'exact_zero_transform'
                            tested += 1
    assert tested == 2304
    return tested


def group_transforms(can, sectors):
    _srank, x0, support_basis = C.X.support_param(can)
    d = len(support_basis)
    projection_rank, kernel = G.local_fiber_coeff_basis(support_basis)
    quotient = L.complement_to_kernel(kernel, d)
    adapted = quotient + tuple(kernel)
    assert len(adapted) == d
    assert R.gf2_rank(adapted) == d

    transforms = []
    for zs, _cls in sectors:
        sig, sd, _nbits = C.X.restricted_phase_signature(
            C.phase_tuple(zs), x0, support_basis
        )
        assert sd == d
        tc, tlin, trows = L.transform_signature(sig, d, adapted)
        got = L.partial_gauss_eliminate(
            tc, tlin, trows, projection_rank, len(kernel)
        )
        assert not got['identically_zero']
        assert got['support_free_dimension'] == (
            projection_rank - got['support_control_rank']
        )
        transforms.append(got)
    return projection_rank, transforms


def analyze():
    regression_cases = synthetic_pair_regression()

    pair_authority = R.analyze()
    assert pair_authority['first_dyadic_pair_residual_terms'] == 237
    pair_groups = {g['group_id']: g for g in pair_authority['groups']}
    assert len(pair_groups) == 147

    e0, _e1, _half = C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for zc in range(4):
        for zs, cls in e0[zc]:
            can = C.P.U.H.support_for(POS, zs, cls)
            if can is None:
                continue
            raw += 1
            grouped[can].append((zs, cls))
    assert raw == 577 and len(grouped) == 250
    assert dict(sorted(Counter(len(v) for v in grouped.values()).items())) == {
        1: 103, 2: 57, 4: 90,
    }

    relation_hist = Counter()
    amplitude_delta_hist = Counter()
    intersection_rank_hist = Counter()
    difference_type_hist = Counter()
    difference_rank_hist = Counter()
    overlap_arithmetic_hist = Counter()
    global_class_hist = Counter()
    min_valuation_hist = Counter()
    valuation_gain_hist = Counter()

    by_mult_relation = defaultdict(Counter)
    by_mult_global = defaultdict(Counter)
    by_mult_difference_rank = defaultdict(Counter)
    by_mult_amplitude_delta = defaultdict(Counter)
    group_records = []
    total_pairs = 0

    for gid, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        m = len(sectors)
        if m == 1:
            continue

        authority = pair_groups[gid]
        assert authority['multiplicity'] == m
        projection_rank, transforms = group_transforms(can, sectors)
        assert len(transforms) == m

        records = []
        for selected in authority['selected_pairs']:
            i, j = selected['pair']
            rec = classify_pair(transforms[i], transforms[j], projection_rank)
            rec['pair'] = [i, j]
            rec['original_difference_polar_rank'] = selected['difference_polar_rank']
            records.append(rec)
            total_pairs += 1

            relation_hist[rec['support_relation']] += 1
            amplitude_delta_hist[rec['amplitude_delta']] += 1
            overlap_arithmetic_hist[rec['overlap_arithmetic']] += 1
            global_class_hist[rec['global_pair_class']] += 1
            by_mult_relation[m][rec['support_relation']] += 1
            by_mult_global[m][rec['global_pair_class']] += 1
            by_mult_amplitude_delta[m][rec['amplitude_delta']] += 1

            if rec['intersection_rank'] is not None:
                intersection_rank_hist[rec['intersection_rank']] += 1
                difference_type_hist[rec['sign_difference_type']] += 1
                difference_rank_hist[rec['sign_difference_polar_rank']] += 1
                by_mult_difference_rank[m][rec['sign_difference_polar_rank']] += 1

            if rec['first_dyadic_min_nonzero_valuation'] is not None:
                min_valuation_hist[rec['first_dyadic_min_nonzero_valuation']] += 1
                valuation_gain_hist[rec['valuation_gain_over_naive']] += 1

        group_records.append({
            'group_id': gid,
            'multiplicity': m,
            'shared_projection_rank': projection_rank,
            'matching_index': authority['matching_index'],
            'pairs': records,
        })

    assert len(group_records) == 147
    assert total_pairs == 237
    assert sum(relation_hist.values()) == total_pairs
    assert sum(global_class_hist.values()) == total_pairs

    out = {
        'position': POS,
        'synthetic_pair_regression_cases': regression_cases,
        'raw_e0_sectors': raw,
        'support_groups': len(grouped),
        'even_multiplicity_support_groups': len(group_records),
        'transformed_first_dyadic_pairs': total_pairs,
        'support_relation_histogram': dict(sorted(relation_hist.items())),
        'amplitude_delta_histogram': dict(sorted(amplitude_delta_hist.items())),
        'intersection_constraint_rank_histogram': dict(sorted(intersection_rank_hist.items())),
        'sign_difference_type_histogram': dict(sorted(difference_type_hist.items())),
        'sign_difference_polar_rank_histogram': dict(sorted(difference_rank_hist.items())),
        'overlap_arithmetic_histogram': dict(sorted(overlap_arithmetic_hist.items())),
        'global_pair_class_histogram': dict(sorted(global_class_hist.items())),
        'first_dyadic_min_nonzero_valuation_histogram': dict(sorted(min_valuation_hist.items())),
        'valuation_gain_over_naive_histogram': dict(sorted(valuation_gain_hist.items())),
        'support_relation_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(by_mult_relation.items())
        },
        'global_pair_class_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(by_mult_global.items())
        },
        'sign_difference_polar_rank_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(by_mult_difference_rank.items())
        },
        'amplitude_delta_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(by_mult_amplitude_delta.items())
        },
        'groups': group_records,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_TRANSFORMED_PAIR_COMPATIBILITY')
    print('identity=after exact local Gauss elimination, each frozen pair is evaluated as H(s)=(G_i(s)+G_j(s))/2 on a common shared-quotient coordinate system')
    print('scope=exact affine-support relation, power-of-two amplitude compatibility, intersection-restricted sign-difference rank, and first-dyadic minimum 2-adic valuation for all 237 frozen C e0 pair terms')
    print('important=the original +/-1 pair cancellation identity is not reused across unequal Gauss amplitudes; unequal amplitudes are handled by exact integer arithmetic after local summation')
    print('next=use the measured transformed-pair classes plus 103 singleton transforms to assemble a quotient-aware first-dyadic message representation before any separator-width claim')
    print('not_included=complete grouped-e0 carry separator, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
