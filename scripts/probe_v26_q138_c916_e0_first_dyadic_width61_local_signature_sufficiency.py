#!/usr/bin/env python3
import io
import json
import sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_gauss_radical_augmented_separator as B
import probe_v26_q138_c916_e0_first_dyadic_group_output_pair_dependency as D
import probe_v26_q138_c916_e0_first_dyadic_group_output_modp_rank_witness as W

POS = 'C'
PHYS_N = 149
assert B.DOMAIN_BITS == D.PHYS_N == W.PHYS_N == PHYS_N
assert B.SHARED_EXT == tuple(D.P.G.SHARED_EXT)


def parity(x):
    return int(x).bit_count() & 1


def homogeneous_kernel(rows, n):
    rows = tuple(int(x) for x in rows)
    sol = B.C.P.U.T.rref([(row, 0) for row in rows], n=n)
    assert sol is not None
    rank, x0, kernel = sol
    assert x0 == 0
    assert rank == len(rows)
    assert rank + len(kernel) == n
    return tuple(int(x) for x in kernel)


def support_preserved(anchor, h):
    return all(
        parity(int(mask) & int(h)) == 0
        for mask, _rhs in anchor['physical_support_constraints']
    )


def translate_anchor(anchor, h, n):
    basis = tuple(int(x) for x in anchor['physical_support_basis'])
    x0 = int(anchor['physical_support_x0']) ^ int(h)
    out = dict(anchor)
    out['physical_support_x0'] = x0
    out['physical_support_basis'] = basis
    out['physical_support_constraints'] = D.P.affine_constraints_from_param(
        x0, basis, n
    )
    out['_coordinate_solver'] = D.P.coordinate_solver(basis)
    return out


def translate_group(group, h, n, term_id_offset=1_000_000):
    terms = []
    for term in group['terms']:
        item = dict(term)
        item['term_id'] = term_id_offset + int(term['term_id'])
        item['anchor'] = translate_anchor(term['anchor'], h, n)
        item['ambient_dimension'] = n
        terms.append(item)
    out = dict(group)
    out['terms'] = tuple(terms)
    out['projection_anchor'] = translate_anchor(
        group['projection_anchor'], h, n
    )
    return out


def exact_translation_difference(group, h, n, norm=None, crosscheck_norm=False):
    if norm is None:
        norm = D.group_inner(group, group, {})
    translated = translate_group(group, h, n)
    if crosscheck_norm:
        translated_norm = D.group_inner(translated, translated, {})
        assert translated_norm == norm
    inner = D.group_inner(group, translated, {})
    difference_norm2 = 2 * (int(norm) - int(inner))
    assert difference_norm2 >= 0
    return {
        'invariant': difference_norm2 == 0,
        'norm2': int(norm),
        'translation_inner_product': int(inner),
        'difference_norm2': int(difference_norm2),
    }


def eval_synthetic_group(group, x):
    return D.eval_group(group, x)


def make_synthetic_group(gid, anchors_and_coeffs, n, next_tid):
    terms = []
    tid = next_tid
    for anchor, coefficient in anchors_and_coeffs:
        terms.append({
            'term_id': tid,
            'group_id': gid,
            'kind': 'synthetic',
            'coefficient': int(coefficient),
            'anchor': anchor,
            'ambient_dimension': n,
        })
        tid += 1
    return {
        'group_id': gid,
        'multiplicity': len(terms),
        'projection_anchor': anchors_and_coeffs[0][0],
        'terms': tuple(terms),
    }, tid


def signature_value(rows, x):
    return tuple(parity(int(row) & int(x)) for row in rows)


def brute_factorization(group, rows, n):
    seen = {}
    for x in range(1 << n):
        sig = signature_value(rows, x)
        value = eval_synthetic_group(group, x)
        old = seen.setdefault(sig, value)
        if old != value:
            return False
    return True


def exact_factorization(group, rows, n):
    rows = tuple(B.A.L.basis([int(x) for x in rows]))
    kernel = homogeneous_kernel(rows, n)
    norm = D.group_inner(group, group, {})
    assert norm > 0
    for ki, h in enumerate(kernel):
        rec = exact_translation_difference(
            group, h, n, norm=norm, crosscheck_norm=(ki == 0)
        )
        if not rec['invariant']:
            return False, ki, h, rec
    return True, None, None, None


def synthetic_regression():
    n = 4
    full_linear = D.P.make_synthetic_anchor((), n, 'linear')
    x1_zero = D.P.make_synthetic_anchor(((2, 0),), n, 'zero')
    x2_one_quad = D.P.make_synthetic_anchor(((4, 1),), n, 'quadratic')

    groups = []
    tid = 0
    specs = (
        ((full_linear, 1),),
        ((x1_zero, 2),),
        ((x2_one_quad, 1),),
        ((full_linear, 1), (x1_zero, 1)),
    )
    for gid, spec in enumerate(specs):
        group, tid = make_synthetic_group(gid, spec, n, tid)
        groups.append(group)

    row_families = (
        (),
        (1,),
        (2,),
        (4,),
        (1, 2),
        (1, 4),
        (2, 4),
        (1, 2, 4),
        (1, 2, 4, 8),
    )

    tested = 0
    for group in groups:
        for rows in row_families:
            exact, _ki, _h, _rec = exact_factorization(group, rows, n)
            brute = brute_factorization(group, rows, n)
            assert exact == brute, (group['group_id'], rows, exact, brute)
            tested += 1

    # Translation implementation itself is pointwise checked independently.
    for group in groups:
        for h in (1, 2, 4, 8, 3, 5, 10, 15):
            translated = translate_group(group, h, n, term_id_offset=10000)
            for x in range(1 << n):
                assert eval_synthetic_group(translated, x) == eval_synthetic_group(
                    group, x ^ h
                )
            tested += 1

    assert tested == 68
    return tested


def build_refined_groups():
    raw, base_groups = B.A.build_groups(POS)
    assert raw == 577 and len(base_groups) == 250

    e0, _e1, _half = B.C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    for k in range(4):
        for zs, cls in e0[k]:
            can = B.C.P.U.H.support_for(POS, zs, cls)
            if can is not None:
                grouped[can].append((zs, cls))
    ordered = list(sorted(grouped.items(), key=lambda kv: kv[0]))
    assert len(ordered) == 250

    groups = []
    for gid, ((can, sectors), base) in enumerate(zip(ordered, base_groups)):
        assert gid == base['group_id']
        _srank, x0, support_basis = B.C.X.support_param(can)
        d = len(support_basis)
        projection_rank, kernel = B.G.local_fiber_coeff_basis(support_basis)

        control_rows = []
        for zs, _cls in sectors:
            sig, sd, _nbits = B.C.X.restricted_phase_signature(
                B.C.phase_tuple(zs), x0, support_basis
            )
            assert sd == d
            rec = B.R.sector_radical_controls(sig, d, kernel)
            control_rows.extend(rec['control_basis_pullback'])
        control_coeff_basis = tuple(B.C.P.U.S.row_basis(control_rows))

        lifted = []
        for f in control_coeff_basis:
            rank, rep, _gauge = B.solve_shared_representative(f, support_basis)
            assert rank == projection_rank
            lifted.append(rep)
        refined_basis = tuple(
            B.A.L.basis(list(base['combined_basis']) + list(lifted))
        )
        groups.append({
            'group_id': gid,
            'multiplicity': len(sectors),
            'base_rank': base['combined_rank'],
            'radical_control_rank': len(control_coeff_basis),
            'refined_rank': len(refined_basis),
            'combined_basis': refined_basis,
        })

    assert B.A.L.union_rank(groups, 'combined_basis') == PHYS_N
    order = sorted(
        range(len(groups)),
        key=lambda i: (
            groups[i]['multiplicity'],
            groups[i]['refined_rank'],
            i,
        ),
    )
    oracle = B.A.T.RankOracle(groups)
    tree = B.A.T.build_tree(groups, order, oracle)
    cert = B.A.T.verify_tree(tree, order, oracle)
    assert cert == {
        'width': 61,
        'max_depth': 11,
        'leaves': 250,
        'internal_nodes': 249,
    }
    return groups, order, tree, cert


def witness_mechanism(group, h):
    if not support_preserved(group['projection_anchor'], h):
        return 'projection_support_shift'
    gauss_terms = [
        term for term in group['terms']
        if term['kind'] == 'gauss_sector'
    ]
    assert gauss_terms
    if any(not support_preserved(term['anchor'], h) for term in gauss_terms):
        return 'gauss_support_shift_within_projection'
    return 'all_supports_preserved_phase_only'


def analyze():
    regression = synthetic_regression()
    refined_groups, order, tree, cert = build_refined_groups()
    physical_groups, physical_terms, mult_hist = W.build_physical_groups()
    assert len(physical_groups) == len(refined_groups) == 250
    assert len(physical_terms) == 680
    assert mult_hist == {1: 103, 2: 57, 4: 90}

    with redirect_stdout(io.StringIO()):
        frozen_separator = B.analyze()
    assert frozen_separator['best_recursive_order'] == 'multiplicity_then_refined'
    assert frozen_separator['best_recursive_width'] == cert['width'] == 61
    assert frozen_separator['best_recursive_depth'] == cert['max_depth'] == 11

    refined_rank_hist = Counter()
    kernel_dim_hist = Counter()
    result_hist = Counter()
    result_by_mult = defaultdict(Counter)
    mechanism_hist = Counter()
    first_failure_kernel_index_hist = Counter()
    checked_kernel_directions_hist = Counter()
    records = []

    norms = []
    for gid, (refined, physical) in enumerate(zip(refined_groups, physical_groups)):
        assert refined['group_id'] == physical['group_id'] == gid
        assert refined['multiplicity'] == physical['multiplicity']
        norm = D.group_inner(physical, physical, {})
        assert norm > 0
        norms.append(norm)

    for gid, (refined, physical, norm) in enumerate(zip(refined_groups, physical_groups, norms)):
        basis = tuple(refined['combined_basis'])
        kernel = homogeneous_kernel(basis, PHYS_N)
        assert len(kernel) == PHYS_N - refined['refined_rank']
        refined_rank_hist[refined['refined_rank']] += 1
        kernel_dim_hist[len(kernel)] += 1

        factorizes = True
        witness = None
        checked = 0
        for ki, h in enumerate(kernel):
            checked += 1
            rec = exact_translation_difference(
                physical,
                h,
                PHYS_N,
                norm=norm,
                crosscheck_norm=(ki == 0),
            )
            if rec['invariant']:
                continue
            factorizes = False
            mechanism = witness_mechanism(physical, h)
            witness = {
                'kernel_basis_index': ki,
                'translation_hex': format(h, '038x'),
                'translation_weight': int(h).bit_count(),
                'mechanism': mechanism,
                'norm2': rec['norm2'],
                'translation_inner_product': rec['translation_inner_product'],
                'difference_norm2': rec['difference_norm2'],
            }
            mechanism_hist[mechanism] += 1
            first_failure_kernel_index_hist[ki] += 1
            break

        checked_kernel_directions_hist[checked] += 1
        status = 'factorizes' if factorizes else 'refuted'
        result_hist[status] += 1
        result_by_mult[physical['multiplicity']][status] += 1
        records.append({
            'group_id': gid,
            'multiplicity': physical['multiplicity'],
            'base_rank': refined['base_rank'],
            'radical_control_rank': refined['radical_control_rank'],
            'refined_rank': refined['refined_rank'],
            'kernel_dimension': len(kernel),
            'kernel_directions_checked': checked,
            'factorizes_through_refined_linear_signature': factorizes,
            'first_counterexample': witness,
        })

    if result_hist['factorizes'] == 250:
        decision = 'ALL_250_GROUP_OUTPUTS_FACTOR_THROUGH_WIDTH61_REFINED_LOCAL_SIGNATURES'
    elif result_hist['refuted'] == 250:
        decision = 'ALL_250_GROUP_OUTPUTS_REFUTE_WIDTH61_REFINED_LOCAL_SIGNATURE_SUFFICIENCY'
    else:
        decision = (
            'MIXED_WIDTH61_REFINED_LOCAL_SIGNATURE_SUFFICIENCY_'
            f'FACTORIZES{result_hist["factorizes"]}_REFUTED{result_hist["refuted"]}'
        )

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'synthetic_factorization_and_translation_regression_cases': regression,
        'support_groups': 250,
        'support_multiplicity_histogram': mult_hist,
        'physical_term_count': len(physical_terms),
        'frozen_separator_best_order': 'multiplicity_then_refined',
        'frozen_separator_width': cert['width'],
        'frozen_separator_depth': cert['max_depth'],
        'refined_rank_histogram': dict(sorted(refined_rank_hist.items())),
        'refined_kernel_dimension_histogram': dict(sorted(kernel_dim_hist.items())),
        'factorization_status_histogram': dict(sorted(result_hist.items())),
        'factorization_status_by_multiplicity': {
            int(m): dict(sorted(h.items()))
            for m, h in sorted(result_by_mult.items())
        },
        'first_counterexample_mechanism_histogram': dict(sorted(mechanism_hist.items())),
        'first_failure_kernel_basis_index_histogram': dict(
            sorted(first_failure_kernel_index_hist.items())
        ),
        'kernel_directions_checked_per_group_histogram': dict(
            sorted(checked_kernel_directions_hist.items())
        ),
        'groups': records,
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_WIDTH61_LOCAL_SIGNATURE_SUFFICIENCY')
    print('scope=exact factorization test of each of the 250 integer-valued first-dyadic group residual functions through its frozen PR148 width-61 refined local linear signature')
    print('proof=for a local signature row space V, the output factors through V iff it is invariant under every translation in V-perp; invariance of the whole kernel follows from invariance under a kernel basis, while one nonzero L2 translation difference is an exact counterexample')
    print('mechanism=counterexamples distinguish projection-support shifts, Gauss-support shifts inside a preserved projection, and phase-only changes with every affine support preserved')
    print('important=this does not invalidate the PR148 width61 certificate for its original radical-support/frequency target; it tests whether that local state can be promoted unchanged to the exact nonlinear first-dyadic group outputs')
    print('not_included=minimal augmented local signatures, exact nonlinear separator width, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
