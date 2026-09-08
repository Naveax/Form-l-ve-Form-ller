#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_aggregate_signature_separator as A
import probe_v26_q138_c916_aggregate_e0_scalar_separator as G

POS = 'C'
DOMAIN_BITS = 149
PAIR_BITS = DOMAIN_BITS * (DOMAIN_BITS - 1) // 2


def polar_vector(rows):
    z = 0
    k = 0
    for i in range(DOMAIN_BITS):
        row = rows[i]
        for j in range(i + 1, DOMAIN_BITS):
            if (row >> j) & 1:
                z |= 1 << k
            k += 1
    assert k == PAIR_BITS
    return z


def scalar_polynomial_vector(sectors):
    rows, delta, phases = G.aggregate_scalar_phase(POS, sectors)
    pv = polar_vector(rows)
    lin = 0
    for i in range(DOMAIN_BITS):
        if delta(1 << i):
            lin |= 1 << i
    c = 0
    for ph in phases:
        c ^= ph['c']
    return rows, pv, pv | (lin << PAIR_BITS) | (c << (PAIR_BITS + DOMAIN_BITS))


def span_rank(values):
    return len(A.L.basis(values))


def affine_difference_rank(values):
    values = list(values)
    if not values:
        return 0
    base = values[0]
    return span_rank(v ^ base for v in values[1:])


def recursive_summary(route, groups):
    n = len(route)
    orders = {
        'hybrid_rank_ascending': sorted(
            range(n), key=lambda i: (route[i]['combined_rank'], groups[i]['multiplicity'], i)
        ),
        'hybrid_rank_descending': sorted(
            range(n), key=lambda i: (-route[i]['combined_rank'], groups[i]['multiplicity'], i)
        ),
        'multiplicity_then_hybrid': sorted(
            range(n), key=lambda i: (groups[i]['multiplicity'], route[i]['combined_rank'], i)
        ),
    }
    path = {name: A.L.order_profile(route, order) for name, order in orders.items()}
    half = n // 2
    cuts = []
    for name, order in orders.items():
        st = A.L.cut_stats(route, set(order[:half]))
        st['name'] = name + '_half'
        cuts.append(st)
    cuts.sort(key=lambda x: (x['lambda'], x['name']))

    recursive = {
        name: A.recursive_certificate(route, order)
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
        'best_balanced_cut': cuts[0],
        'path_widths': {name: p['max_lambda'] for name, p in path.items()},
        'recursive_widths': {
            name: data['certificate']['width'] for name, data in recursive.items()
        },
        'best_recursive_order': best_name,
        'best_recursive_width': best['certificate']['width'],
        'best_recursive_depth': best['certificate']['max_depth'],
        'best_recursive_root_children': best['root_children'],
    }


def analyze():
    raw, canonical_groups = A.build_groups(POS)
    assert raw == 577 and len(canonical_groups) == 250

    e0, _e1, _half = A.L.U.H.classify_patterns()
    grouped = defaultdict(list)
    for k in range(4):
        for zs, cls in e0[k]:
            can = A.L.U.H.support_for(POS, zs, cls)
            if can is not None:
                grouped[can].append((zs, cls))
    ordered = list(sorted(grouped.items(), key=lambda kv: kv[0]))
    assert len(ordered) == len(canonical_groups)

    groups = []
    singleton_polar = []
    singleton_poly = []
    multi_polar = []
    multi_poly = []

    for gid, ((can, sectors), info) in enumerate(zip(ordered, canonical_groups)):
        assert gid == info['group_id']
        assert len(sectors) == info['multiplicity']
        refined = G.refine_group(info, sectors)
        rows, pv, poly = scalar_polynomial_vector(sectors)
        assert A.L.rank(rows) == refined['aggregate_scalar_polar_rank']

        rec = {
            'group_id': gid,
            'multiplicity': info['multiplicity'],
            'original_rank': info['combined_rank'],
            'refined_rank': refined['refined_rank'],
            'extra_rank': refined['extra_rank'],
            'polar_rank': refined['aggregate_scalar_polar_rank'],
            'original_basis': info['combined_basis'],
            'refined_basis': refined['refined_basis'],
        }
        groups.append(rec)
        if rec['multiplicity'] == 1:
            singleton_polar.append(pv)
            singleton_poly.append(poly)
        else:
            multi_polar.append(pv)
            multi_poly.append(poly)

    assert len(singleton_polar) == 103
    assert len(multi_polar) == 147

    singleton_rank_hist = Counter(g['polar_rank'] for g in groups if g['multiplicity'] == 1)
    multi_rank_hist = Counter(g['polar_rank'] for g in groups if g['multiplicity'] > 1)
    assert set(singleton_rank_hist) == {136, 138, 140, 142}
    assert set(multi_rank_hist) == {2, 4, 6, 8, 10, 12}
    assert all(g['polar_rank'] >= 136 for g in groups if g['multiplicity'] == 1)
    assert all(g['polar_rank'] <= 12 for g in groups if g['multiplicity'] > 1)

    # Hybrid linear skeleton: exact-linearize only the 147 low-polar-rank
    # multi-sector aggregate scalars. Keep each singleton high-rank quadratic
    # scalar nonlinear and therefore do not charge its 124..127-dimensional
    # linear refinement to the separator state here.
    hybrid_route = []
    baseline_route = []
    for g in groups:
        baseline_route.append({
            'combined_basis': g['original_basis'],
            'combined_rank': g['original_rank'],
            'multiplicity': g['multiplicity'],
        })
        if g['multiplicity'] == 1:
            b = g['original_basis']
            r = g['original_rank']
        else:
            b = g['refined_basis']
            r = g['refined_rank']
        hybrid_route.append({
            'combined_basis': b,
            'combined_rank': r,
            'multiplicity': g['multiplicity'],
        })

    assert A.L.union_rank(baseline_route, 'combined_basis') == DOMAIN_BITS
    assert A.L.union_rank(hybrid_route, 'combined_basis') == DOMAIN_BITS

    baseline_order = sorted(
        range(len(groups)),
        key=lambda i: (groups[i]['multiplicity'], groups[i]['original_rank'], i),
    )
    baseline_tree = A.recursive_certificate(baseline_route, baseline_order)
    assert baseline_tree['certificate']['width'] == 58

    hs = recursive_summary(hybrid_route, groups)

    out = {
        'position': POS,
        'raw_e0_sectors': raw,
        'support_groups': len(groups),
        'singleton_groups': len(singleton_polar),
        'multi_sector_groups': len(multi_polar),
        'singleton_polar_rank_histogram': dict(sorted(singleton_rank_hist.items())),
        'multi_sector_polar_rank_histogram': dict(sorted(multi_rank_hist.items())),
        'polar_rank_split_exact': True,
        'baseline_unrefined_recursive_width': baseline_tree['certificate']['width'],
        'hybrid_linear_global_rank': A.L.union_rank(hybrid_route, 'combined_basis'),
        'hybrid_linear_best_balanced_cut': hs['best_balanced_cut'],
        'hybrid_linear_path_widths': hs['path_widths'],
        'hybrid_linear_recursive_widths': hs['recursive_widths'],
        'hybrid_linear_best_recursive_order': hs['best_recursive_order'],
        'hybrid_linear_best_recursive_width': hs['best_recursive_width'],
        'hybrid_linear_best_recursive_depth': hs['best_recursive_depth'],
        'hybrid_linear_best_recursive_root_children': hs['best_recursive_root_children'],
        'singleton_polar_span_rank': span_rank(singleton_polar),
        'singleton_polar_affine_difference_rank': affine_difference_rank(singleton_polar),
        'singleton_full_quadratic_polynomial_span_rank': span_rank(singleton_poly),
        'singleton_full_quadratic_polynomial_affine_difference_rank': affine_difference_rank(singleton_poly),
        'multi_sector_polar_span_rank': span_rank(multi_polar),
        'multi_sector_full_quadratic_polynomial_span_rank': span_rank(multi_poly),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_HYBRID_AGGREGATE_SCALAR_SEPARATOR')
    print('scope=diagnostic split of C same-support aggregate scalar family: exact linear refinement for low-polar-rank multi-sector groups, high-rank singleton quadratics deliberately retained as unresolved nonlinear labels')
    print('important=hybrid linear width excludes the cost of representing/evaluating the 103 singleton quadratic labels; it is not a complete separator or carry bound')
    print('next=use singleton quadratic-family ranks to choose a nonlinear/Gauss representation before attempting all-group aggregate carry contraction')
    print('not_included=exact nonlinear singleton contraction cost, aggregate e0 carry, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


def main():
    analyze()


if __name__ == '__main__':
    main()
