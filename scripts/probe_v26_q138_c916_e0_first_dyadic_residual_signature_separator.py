#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_all_577_exact_template_cover as E
import probe_v26_q138_c916_e0_gauss_radical_augmented_separator as B

Q = E.Q
PHYS_N = E.PHYS_N
POS = 'C'
THRESHOLDS = (2, 4)

assert PHYS_N == B.DOMAIN_BITS == 149


def parity(x):
    return int(x).bit_count() & 1


def gf2_basis(rows):
    return tuple(B.A.L.basis([int(x) for x in rows]))


def gf2_rank(rows):
    return B.A.L.rank([int(x) for x in rows])


def nullspace(rows, n):
    sol = B.C.P.U.T.rref([(int(row), 0) for row in rows], n=n)
    assert sol is not None
    rank, x0, kernel = sol
    assert x0 == 0
    assert rank + len(kernel) == n
    return rank, list(kernel)


def annihilator_basis(kernel, n):
    if not kernel:
        return tuple(1 << i for i in range(n))
    sol = B.C.P.U.T.rref([(int(h), 0) for h in kernel], n=n)
    assert sol is not None
    rank, x0, out = sol
    assert x0 == 0
    assert rank == len(kernel)
    assert len(out) == n - len(kernel)
    return tuple(out)


def q_eval(c, lin, rows, x):
    return Q.L.q_eval(c, lin, rows, x)


def minimal_quadratic_signature(c, lin, rows):
    rows = tuple(int(x) for x in rows)
    d = len(rows)
    polar_rank, kernel = nullspace(rows, d)
    assert polar_rank % 2 == 0

    cut = 0
    vals = [q_eval(c, lin, rows, h) ^ c for h in kernel]
    pivot = next((i for i, v in enumerate(vals) if v), None)
    if pivot is not None:
        p = kernel[pivot]
        out = []
        for i, h in enumerate(kernel):
            if i == pivot:
                continue
            if vals[i]:
                h ^= p
            out.append(h)
        kernel = out
        cut = 1

    for h in kernel:
        assert all(parity(row & h) == 0 for row in rows)
        assert (q_eval(c, lin, rows, h) ^ c) == 0

    sig = annihilator_basis(kernel, d)
    signature_rank = len(sig)
    assert signature_rank == polar_rank + cut
    assert signature_rank in (polar_rank, polar_rank + 1)
    return {
        'polar_rank': polar_rank,
        'scalar_cut': cut,
        'signature_rank': signature_rank,
        'signature_basis': sig,
        'hidden_dimension': len(kernel),
    }


def synthetic_signature_regression():
    tested = 0
    for d in range(5):
        pairs = [(i, j) for i in range(d) for j in range(i + 1, d)]
        total_bits = 1 + d + len(pairs)
        for code in range(1 << total_bits):
            y = code
            c = y & 1
            y >>= 1
            lin = y & ((1 << d) - 1)
            y >>= d
            rows = [0] * d
            for k, (i, j) in enumerate(pairs):
                if (y >> k) & 1:
                    rows[i] |= 1 << j
                    rows[j] |= 1 << i

            rec = minimal_quadratic_signature(c, lin, tuple(rows))
            sig = rec['signature_basis']
            _srank, hidden = nullspace(sig, d)
            generated = {0}
            for h in hidden:
                generated |= {x ^ h for x in tuple(generated)}

            brute = set()
            for h in range(1 << d):
                if all(
                    q_eval(c, lin, tuple(rows), x ^ h)
                    == q_eval(c, lin, tuple(rows), x)
                    for x in range(1 << d)
                ):
                    brute.add(h)
            assert generated == brute

            for x in range(1 << d):
                sx = tuple(parity(f & x) for f in sig)
                for z in range(1 << d):
                    if tuple(parity(f & z) for f in sig) == sx:
                        assert q_eval(c, lin, tuple(rows), z) == q_eval(c, lin, tuple(rows), x)
            tested += 1

    assert tested == 2198
    return tested


def build_radical_support_groups():
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
    assert len(ordered) == len(base_groups)

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
            'base_rank_before_radical': base['combined_rank'],
            'radical_control_rank': len(control_coeff_basis),
            'combined_rank': len(refined_basis),
            'combined_basis': refined_basis,
        })

    assert len(groups) == 250
    assert B.A.L.union_rank(groups, 'combined_basis') == PHYS_N

    orders = {
        'base_multiplicity_then_rank': sorted(
            range(len(groups)),
            key=lambda i: (
                groups[i]['multiplicity'],
                groups[i]['combined_rank'],
                i,
            ),
        ),
        'rank_ascending': sorted(
            range(len(groups)),
            key=lambda i: (
                groups[i]['combined_rank'],
                groups[i]['multiplicity'],
                i,
            ),
        ),
        'rank_descending': sorted(
            range(len(groups)),
            key=lambda i: (
                -groups[i]['combined_rank'],
                groups[i]['multiplicity'],
                i,
            ),
        ),
        'radical_rank_ascending': sorted(
            range(len(groups)),
            key=lambda i: (
                groups[i]['radical_control_rank'],
                groups[i]['multiplicity'],
                groups[i]['combined_rank'],
                i,
            ),
        ),
    }
    recursive = {
        name: B.A.recursive_certificate(groups, order)
        for name, order in orders.items()
    }
    baseline_width = min(
        data['certificate']['width'] for data in recursive.values()
    )
    assert baseline_width == 61, baseline_width
    return groups, baseline_width


def solve_threshold_assignment(geo, threshold):
    transforms = geo['transforms']
    ids = geo['ids']
    classes = geo['classes']
    children_by_class = geo['children_by_class']
    residual_rank = geo['residual_rank']

    chosen_by_class = {}
    chosen_global = []

    for ci, cls in enumerate(classes):
        children = tuple(sorted(children_by_class[ci], key=lambda i: ids[i]))
        pos = {i: p for p, i in enumerate(children)}
        full = (1 << len(children)) - 1
        covers = []
        for root in cls:
            mask = 0
            for i in children:
                if residual_rank[(i, root)] <= threshold:
                    mask |= 1 << pos[i]
            covers.append(mask)
        solved = E.exact_pivot_dp(tuple(covers), full)
        assert solved['feasible']
        roots = tuple(cls[j] for j in solved['chosen_candidate_indices'])
        chosen_by_class[ci] = roots
        chosen_global.extend(roots)

    expected = 39 if threshold == 2 else 22
    assert len(chosen_global) == expected

    assignment = {}
    assignment_rank_hist = Counter()
    for ci, children in children_by_class.items():
        roots = chosen_by_class[ci]
        for i in children:
            opts = sorted(
                (residual_rank[(i, root)], ids[root], root)
                for root in roots
                if residual_rank[(i, root)] <= threshold
            )
            assert opts
            rank, _rid, root = opts[0]
            assignment[i] = root
            assignment_rank_hist[rank] += 1

    assert len(assignment) == 577
    expected_hist = (
        {0: 361, 2: 216}
        if threshold == 2
        else {0: 259, 2: 267, 4: 51}
    )
    assert dict(sorted(assignment_rank_hist.items())) == expected_hist

    return {
        'chosen_global': tuple(sorted(chosen_global, key=lambda i: ids[i])),
        'chosen_by_class': chosen_by_class,
        'assignment': assignment,
        'assignment_rank_hist': assignment_rank_hist,
    }


def residual_form(child, root):
    relation, inter = Q.support_relation(child, root, PHYS_N)
    assert relation in ('equal', 'left_subset_right')
    assert inter is not None
    _irank, ix0, ibasis = inter
    ibasis = tuple(ibasis)
    assert len(ibasis) == len(child['physical_support_basis'])

    lc, llin, lrows = Q.restrict_anchor_sign(child, ix0, ibasis)
    rc, rlin, rrows = Q.restrict_anchor_sign(root, ix0, ibasis)
    dc = lc ^ rc
    dlin = llin ^ rlin
    drows = tuple(a ^ b for a, b in zip(lrows, rrows))
    return dc, dlin, drows, ix0, ibasis


def lift_signature_row(coeff, ibasis):
    eqs = [
        (int(b), (int(coeff) >> j) & 1)
        for j, b in enumerate(ibasis)
    ]
    sol = B.C.P.U.T.rref(eqs, n=PHYS_N)
    assert sol is not None
    rank, rep, gauge = sol
    assert rank == len(ibasis)
    for j, b in enumerate(ibasis):
        assert parity(rep & b) == ((int(coeff) >> j) & 1)
    return int(rep), tuple(int(x) for x in gauge)


def recursive_profiles(groups):
    n = len(groups)
    orders = {
        'multiplicity_then_augmented': sorted(
            range(n),
            key=lambda i: (
                groups[i]['multiplicity'],
                groups[i]['combined_rank'],
                groups[i]['extra_rank'],
                i,
            ),
        ),
        'extra_then_augmented': sorted(
            range(n),
            key=lambda i: (
                groups[i]['extra_rank'],
                groups[i]['combined_rank'],
                groups[i]['multiplicity'],
                i,
            ),
        ),
        'augmented_rank_ascending': sorted(
            range(n),
            key=lambda i: (
                groups[i]['combined_rank'],
                groups[i]['multiplicity'],
                groups[i]['extra_rank'],
                i,
            ),
        ),
        'augmented_rank_descending': sorted(
            range(n),
            key=lambda i: (
                -groups[i]['combined_rank'],
                groups[i]['multiplicity'],
                groups[i]['extra_rank'],
                i,
            ),
        ),
    }
    recursive = {
        name: B.A.recursive_certificate(groups, order)
        for name, order in orders.items()
    }
    best_name, best = min(
        recursive.items(),
        key=lambda kv: (
            kv[1]['certificate']['width'],
            kv[1]['certificate']['max_depth'],
            kv[0],
        ),
    )
    return {
        'recursive_widths': {
            name: data['certificate']['width']
            for name, data in recursive.items()
        },
        'best_recursive_order': best_name,
        'best_recursive_width': best['certificate']['width'],
        'best_recursive_depth': best['certificate']['max_depth'],
        'best_recursive_root_children': best['root_children'],
    }


def analyze_threshold(geo, base_groups, threshold):
    transforms = geo['transforms']
    ids = geo['ids']
    residual_rank = geo['residual_rank']
    solved = solve_threshold_assignment(geo, threshold)

    rows_by_group = defaultdict(list)
    gauge_failures = []
    signature_rank_hist = Counter()
    signature_rank_by_polar = defaultdict(Counter)
    scalar_cut_hist = Counter()
    total_signature_rows_before_union = 0

    for i in range(len(transforms)):
        root_index = solved['assignment'][i]
        child = transforms[i]
        root = transforms[root_index]
        dc, dlin, drows, _ix0, ibasis = residual_form(child, root)

        rec = minimal_quadratic_signature(dc, dlin, drows)
        expected_polar = residual_rank[(i, root_index)]
        assert rec['polar_rank'] == expected_polar
        assert rec['polar_rank'] <= threshold

        signature_rank_hist[rec['signature_rank']] += 1
        signature_rank_by_polar[rec['polar_rank']][rec['signature_rank']] += 1
        scalar_cut_hist[rec['scalar_cut']] += 1
        total_signature_rows_before_union += rec['signature_rank']

        gid = child['group_id']
        existing = base_groups[gid]
        for coeff in rec['signature_basis']:
            rep, gauge = lift_signature_row(coeff, ibasis)
            gauge_delta = (
                gf2_rank(list(existing['combined_basis']) + list(gauge))
                - existing['combined_rank']
            )
            if gauge_delta:
                gauge_failures.append({
                    'transform': list(ids[i]),
                    'template': list(ids[root_index]),
                    'group_id': gid,
                    'polar_rank': rec['polar_rank'],
                    'signature_rank': rec['signature_rank'],
                    'gauge_delta': gauge_delta,
                })
            rows_by_group[gid].append(rep)

    all_gauges_contained = not gauge_failures

    augmented = []
    residual_union_rank_hist = Counter()
    extra_rank_hist = Counter()
    for gid, base in enumerate(base_groups):
        residual_basis = gf2_basis(rows_by_group.get(gid, ()))
        residual_union_rank_hist[len(residual_basis)] += 1
        combined_basis = gf2_basis(
            list(base['combined_basis']) + list(residual_basis)
        )
        extra = len(combined_basis) - base['combined_rank']
        extra_rank_hist[extra] += 1
        augmented.append({
            'group_id': gid,
            'multiplicity': base['multiplicity'],
            'base_rank': base['combined_rank'],
            'residual_signature_union_rank': len(residual_basis),
            'combined_rank': len(combined_basis),
            'extra_rank': extra,
            'combined_basis': combined_basis,
        })

    global_rank = B.A.L.union_rank(augmented, 'combined_basis')
    assert global_rank == PHYS_N

    profiles = None
    if all_gauges_contained:
        profiles = recursive_profiles(augmented)

    return {
        'threshold': threshold,
        'templates': len(solved['chosen_global']),
        'chosen_template_ids': [
            list(ids[i]) for i in solved['chosen_global']
        ],
        'assignment_residual_polar_rank_histogram': dict(
            sorted(solved['assignment_rank_hist'].items())
        ),
        'minimal_signature_rank_histogram': dict(
            sorted(signature_rank_hist.items())
        ),
        'minimal_signature_rank_by_polar_rank': {
            k: dict(sorted(v.items()))
            for k, v in sorted(signature_rank_by_polar.items())
        },
        'scalar_cut_histogram': dict(sorted(scalar_cut_hist.items())),
        'total_signature_rows_before_group_union': total_signature_rows_before_union,
        'all_lift_gauges_contained_in_existing_radical_support_group_basis': all_gauges_contained,
        'gauge_failure_count': len(gauge_failures),
        'first_gauge_failures': gauge_failures[:30],
        'residual_signature_union_rank_histogram': dict(
            sorted(residual_union_rank_hist.items())
        ),
        'extra_rank_over_width61_group_basis_histogram': dict(
            sorted(extra_rank_hist.items())
        ),
        'groups_with_zero_extra_rank': extra_rank_hist.get(0, 0),
        'max_extra_rank': max(extra_rank_hist) if extra_rank_hist else 0,
        'global_augmented_linear_rank': global_rank,
        'recursive_separator_measurement_valid': all_gauges_contained,
        **(profiles or {}),
    }


def analyze():
    regression = synthetic_signature_regression()
    geo = E.build_geometry()
    base_groups, baseline_width = build_radical_support_groups()

    results = {
        threshold: analyze_threshold(geo, base_groups, threshold)
        for threshold in THRESHOLDS
    }

    if all(
        rec['all_lift_gauges_contained_in_existing_radical_support_group_basis']
        for rec in results.values()
    ):
        decision = (
            'RESIDUAL_SIGNATURE_AUGMENTATION_GAUGE_VALID_'
            f'R2_WIDTH{results[2]["best_recursive_width"]}_'
            f'R4_WIDTH{results[4]["best_recursive_width"]}'
        )
    else:
        decision = 'RESIDUAL_SIGNATURE_LIFT_GAUGE_NOT_CONTAINED'

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'synthetic_quadratic_signature_regression_cases': regression,
        'baseline_radical_support_recursive_width': baseline_width,
        'results': results,
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_RESIDUAL_SIGNATURE_SEPARATOR')
    print('scope=exact minimal linear evaluation signatures of deterministic complete-577 child-to-template residual quadratics, lifted into the 149-bit physical shared domain and measured on top of the frozen width-61 Gauss radical-support separator')
    print('minimality=for each residual quadratic the hidden subgroup is exactly the translation stabilizer rad(B) intersect q(h)=q(0), and its annihilator is the minimal linear signature determining that residual sign')
    print('gauge=recursive separator widths are reported only if every ambient lift gauge lies in the pre-existing per-group width-61 radical-support basis')
    print('important=template common high-rank signs are NOT included and are NOT treated as free; this pass measures residual-correction state only')
    print('not_included=template common-sign gluing, complete grouped-e0 separator theorem, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
