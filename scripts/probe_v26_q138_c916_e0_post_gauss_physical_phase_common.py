#!/usr/bin/env python3
import io
import json
import sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_local_gauss_transform_quotient_geometry as L
import probe_v26_q138_c916_e0_same_support_integer_coefficients as C
import probe_v26_q138_c916_e0_complete_first_dyadic_fiber_geometry as G
import probe_v26_q138_c916_e0_first_dyadic_pair_residual as R
import probe_v26_q138_c916_e0_first_dyadic_transformed_pair_compatibility as P

POS = 'C'
PHYS_N = len(G.SHARED_EXT)
assert PHYS_N == 149


def parity(x):
    return int(x).bit_count() & 1


def xor_combine(coeff, basis):
    out = 0
    y = int(coeff)
    while y:
        b = y & -y
        out ^= basis[b.bit_length() - 1]
        y ^= b
    return out


def compress_shared(full):
    out = 0
    for i, ext in enumerate(G.SHARED_EXT):
        if (full >> ext) & 1:
            out |= 1 << i
    return out


def coordinate_solver(basis):
    pivots = {}
    for i, vec in enumerate(basis):
        y = int(vec)
        coeff = 1 << i
        while y:
            p = y.bit_length() - 1
            if p not in pivots:
                pivots[p] = (y, coeff)
                break
            pv, pc = pivots[p]
            y ^= pv
            coeff ^= pc
        assert y != 0, 'basis must be independent'
    assert len(pivots) == len(basis)
    return pivots


def solve_coordinates(solver, vec):
    y = int(vec)
    coeff = 0
    while y:
        p = y.bit_length() - 1
        item = solver.get(p)
        if item is None:
            return None
        pv, pc = item
        y ^= pv
        coeff ^= pc
    return coeff


def affine_constraints_from_param(x0, basis, n):
    sol = C.P.U.T.rref([(b, 0) for b in basis], n=n)
    assert sol is not None
    rank, zero, normals = sol
    assert zero == 0
    assert rank == len(basis)
    constraints = tuple((m, parity(m & x0)) for m in normals)
    assert len(constraints) == n - len(basis)
    return constraints


def affine_subset(anchor, constraints):
    if any(parity(m & anchor['physical_support_x0']) != rhs for m, rhs in constraints):
        return False
    for m, _rhs in constraints:
        if any(parity(m & b) for b in anchor['physical_support_basis']):
            return False
    return True


def support_relation(left, right, n):
    lc = left['physical_support_constraints']
    rc = right['physical_support_constraints']
    inter = C.P.U.T.rref(list(lc) + list(rc), n=n)
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


def restrict_anchor_sign(anchor, ix0, ibasis):
    solver = anchor['_coordinate_solver']
    z0 = solve_coordinates(solver, ix0 ^ anchor['physical_support_x0'])
    assert z0 is not None
    mapped = []
    for b in ibasis:
        z = solve_coordinates(solver, b)
        assert z is not None
        mapped.append(z)
    return L.restrict_form(
        anchor['normalized_sign_constant'],
        anchor['normalized_sign_linear'],
        anchor['normalized_sign_rows'],
        z0,
        tuple(mapped),
    )


def compare_phases(left, right, n=PHYS_N):
    relation, inter = support_relation(left, right, n)
    rec = {
        'support_relation': relation,
        'intersection_constraint_rank': None,
        'intersection_dimension': None,
        'sign_difference_type': None,
        'sign_difference_constant_bit': None,
        'sign_difference_linear_weight': None,
        'sign_difference_polar_rank': None,
    }
    if inter is None:
        return rec

    irank, ix0, ibasis = inter
    lc, llin, lrows = restrict_anchor_sign(left, ix0, ibasis)
    rc, rlin, rrows = restrict_anchor_sign(right, ix0, ibasis)
    drows = tuple(a ^ b for a, b in zip(lrows, rrows))
    drank = R.gf2_rank(drows)
    assert drank % 2 == 0
    dlin = llin ^ rlin
    dc = lc ^ rc
    if drank == 0 and dlin == 0:
        dtype = 'constant'
    elif drank == 0:
        dtype = 'affine_nonconstant'
    else:
        dtype = 'quadratic_nonconstant'

    rec.update({
        'intersection_constraint_rank': irank,
        'intersection_dimension': len(ibasis),
        'sign_difference_type': dtype,
        'sign_difference_constant_bit': dc if dtype == 'constant' else None,
        'sign_difference_linear_weight': dlin.bit_count(),
        'sign_difference_polar_rank': drank,
    })
    return rec


def make_synthetic_anchor(constraints, n, form_kind):
    sol = C.P.U.T.rref(constraints, n=n)
    assert sol is not None
    _rank, x0, basis = sol
    basis = tuple(basis)
    d = len(basis)
    c = 0
    lin = 0
    rows = [0] * d
    if form_kind == 'one':
        c = 1
    elif form_kind == 'linear':
        if d:
            lin = 1
        else:
            c = 1
    elif form_kind == 'quadratic':
        if d >= 2:
            rows[0] |= 1 << 1
            rows[1] |= 1 << 0
        elif d:
            lin = 1
        else:
            c = 1
    elif form_kind != 'zero':
        raise AssertionError(form_kind)

    return {
        'physical_support_x0': x0,
        'physical_support_basis': basis,
        'physical_support_constraints': tuple(constraints),
        'normalized_sign_constant': c,
        'normalized_sign_linear': lin,
        'normalized_sign_rows': tuple(rows),
        '_coordinate_solver': coordinate_solver(basis),
    }


def eval_anchor_sign(anchor, physical):
    if any(parity(m & physical) != rhs for m, rhs in anchor['physical_support_constraints']):
        return None
    z = solve_coordinates(
        anchor['_coordinate_solver'],
        physical ^ anchor['physical_support_x0'],
    )
    assert z is not None
    return L.q_eval(
        anchor['normalized_sign_constant'],
        anchor['normalized_sign_linear'],
        anchor['normalized_sign_rows'],
        z,
    )


def synthetic_pullback_regression():
    n = 5
    systems = (
        (),
        ((1, 0),),
        ((1, 1),),
        ((2, 0),),
        ((1, 0), (2, 1)),
        ((3, 0),),
    )
    kinds = ('zero', 'one', 'linear', 'quadratic')
    anchors = [
        make_synthetic_anchor(system, n, kind)
        for system in systems
        for kind in kinds
    ]
    tested = 0
    for left in anchors:
        for right in anchors:
            rec = compare_phases(left, right, n=n)
            relation, inter = support_relation(left, right, n=n)
            assert rec['support_relation'] == relation
            if inter is None:
                assert not any(
                    eval_anchor_sign(left, x) is not None
                    and eval_anchor_sign(right, x) is not None
                    for x in range(1 << n)
                )
                tested += 1
                continue

            _irank, ix0, ibasis = inter
            lc, llin, lrows = restrict_anchor_sign(left, ix0, ibasis)
            rc, rlin, rrows = restrict_anchor_sign(right, ix0, ibasis)
            dc = lc ^ rc
            dlin = llin ^ rlin
            drows = tuple(a ^ b for a, b in zip(lrows, rrows))
            for w in range(1 << len(ibasis)):
                physical = ix0 ^ xor_combine(w, ibasis)
                lq = eval_anchor_sign(left, physical)
                rq = eval_anchor_sign(right, physical)
                assert lq is not None and rq is not None
                predicted = L.q_eval(dc, dlin, drows, w)
                assert predicted == (lq ^ rq)
            tested += 1
    assert tested == len(anchors) ** 2 == 576
    return tested


def physical_group_transforms(can, sectors):
    _srank, full_x0, support_basis = C.X.support_param(can)
    support_basis = tuple(support_basis)
    d = len(support_basis)
    projection_rank, kernel = G.local_fiber_coeff_basis(support_basis)
    quotient = L.complement_to_kernel(kernel, d)
    adapted = tuple(quotient) + tuple(kernel)
    assert len(adapted) == d
    assert R.gf2_rank(adapted) == d

    shared_origin = compress_shared(full_x0)
    shared_qbasis = []
    for coeff in quotient:
        full = xor_combine(coeff, support_basis)
        shared_qbasis.append(compress_shared(full))
    shared_qbasis = tuple(shared_qbasis)
    assert len(shared_qbasis) == projection_rank
    assert R.gf2_rank(shared_qbasis) == projection_rank

    transforms = []
    for sector_index, (zs, _cls) in enumerate(sectors):
        sig, sd, _nbits = C.X.restricted_phase_signature(
            C.phase_tuple(zs), full_x0, support_basis
        )
        assert sd == d
        tc, tlin, trows = L.transform_signature(sig, d, adapted)
        got = L.partial_gauss_eliminate(
            tc, tlin, trows, projection_rank, len(kernel)
        )
        assert not got['identically_zero']

        physical_x0 = shared_origin ^ xor_combine(
            got['support_x0'], shared_qbasis
        )
        physical_basis = tuple(
            xor_combine(v, shared_qbasis)
            for v in got['support_basis']
        )
        assert R.gf2_rank(physical_basis) == len(physical_basis)
        assert len(physical_basis) == got['support_free_dimension']
        constraints = affine_constraints_from_param(
            physical_x0, physical_basis, PHYS_N
        )
        expected_codim = PHYS_N - projection_rank + got['support_control_rank']
        assert len(constraints) == expected_codim

        transforms.append({
            'sector_index': sector_index,
            'shared_projection_rank': projection_rank,
            'physical_support_x0': physical_x0,
            'physical_support_basis': physical_basis,
            'physical_support_constraints': constraints,
            'physical_support_dimension': len(physical_basis),
            'physical_support_codimension': len(constraints),
            'log2_abs_nonzero_gauss': got['log2_abs_nonzero_gauss'],
            'normalized_sign_constant': got['normalized_sign_constant'],
            'normalized_sign_linear': got['normalized_sign_linear'],
            'normalized_sign_rows': tuple(got['normalized_sign_rows']),
            'normalized_sign_polar_rank': got['normalized_sign_polar_rank'],
            '_coordinate_solver': coordinate_solver(physical_basis),
            '_raw_transform': got,
        })
    return projection_rank, transforms

