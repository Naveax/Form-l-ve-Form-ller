#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_aggregate_signature_separator as A
import probe_v26_q138_bc_e0_quadratic_scalar_refinement as Q

POS = 'C'
DOMAIN_BITS = 149


def aggregate_scalar_phase(pos, sectors):
    phases = [Q.scalar_phase(pos, zs) for zs, _cls in sectors]
    polar_rows = [0] * DOMAIN_BITS
    for ph in phases:
        for i, row in enumerate(ph['restricted_polar_rows']):
            polar_rows[i] ^= row

    assert all(((polar_rows[i] >> i) & 1) == 0 for i in range(DOMAIN_BITS))
    assert all(
        ((polar_rows[i] >> j) & 1) == ((polar_rows[j] >> i) & 1)
        for i in range(DOMAIN_BITS)
        for j in range(i + 1, DOMAIN_BITS)
    )

    def delta(h):
        z = 0
        for ph in phases:
            z ^= Q.scalar_delta(ph, h)
        return z

    return tuple(polar_rows), delta, phases


def impose_aggregate_scalar_invariance(kernel, delta):
    vals = [delta(h) for h in kernel]
    pivot = next((i for i, v in enumerate(vals) if v), None)
    if pivot is None:
        return list(kernel), False
    p = kernel[pivot]
    out = []
    for i, h in enumerate(kernel):
        if i == pivot:
            continue
        if vals[i]:
            h ^= p
        out.append(h)
    assert all(delta(h) == 0 for h in out)
    return out, True


def refine_group(info, sectors):
    original = list(info['combined_basis'])
    original_rank = len(original)
    polar_rows, delta, phases = aggregate_scalar_phase(POS, sectors)
    polar_rank = A.L.rank(polar_rows)

    # A hidden direction preserves the aggregate quadratic scalar on every
    # fiber iff it lies in the aggregate polar radical and has zero constant
    # derivative. This is exact for the same-support XOR aggregate, unlike the
    # stronger historical sectorwise refinement which required every sector
    # scalar to be individually fixed.
    kernel, radical_refined_rank = Q.nullspace(original + list(polar_rows))
    kernel, scalar_cut = impose_aggregate_scalar_invariance(kernel, delta)

    for h in kernel:
        assert all(((row & h).bit_count() & 1) == 0 for row in original)
        assert all(((row & h).bit_count() & 1) == 0 for row in polar_rows)
        assert delta(h) == 0

    refined_basis = A.L.basis(Q.annihilator_basis(kernel))
    refined_rank = len(refined_basis)
    assert refined_rank == DOMAIN_BITS - len(kernel)
    assert A.L.rank(refined_basis + original) == refined_rank
    assert refined_rank >= radical_refined_rank >= original_rank
    assert refined_rank - radical_refined_rank == int(scalar_cut)

    return {
        'group_id': info['group_id'],
        'multiplicity': info['multiplicity'],
        'original_combined_rank': original_rank,
        'aggregate_scalar_polar_rank': polar_rank,
        'radical_refined_rank': radical_refined_rank,
        'scalar_linear_cut': int(scalar_cut),
        'refined_rank': refined_rank,
        'extra_rank': refined_rank - original_rank,
        'hidden_invariance_dim': len(kernel),
        'refined_basis': refined_basis,
        'sector_count': len(phases),
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
    for gid, ((can, sectors), info) in enumerate(zip(ordered, canonical_groups)):
        assert gid == info['group_id']
        assert len(sectors) == info['multiplicity']
        groups.append(refine_group(info, sectors))

    route = [
        {
            'combined_basis': g['refined_basis'],
            'combined_rank': g['refined_rank'],
            'multiplicity': g['multiplicity'],
        }
        for g in groups
    ]
    global_rank = A.L.union_rank(route, 'combined_basis')
    assert global_rank == DOMAIN_BITS

    original_hist = Counter(g['original_combined_rank'] for g in groups)
    polar_hist = Counter(g['aggregate_scalar_polar_rank'] for g in groups)
    radical_hist = Counter(g['radical_refined_rank'] for g in groups)
    refined_hist = Counter(g['refined_rank'] for g in groups)
    extra_hist = Counter(g['extra_rank'] for g in groups)
    hidden_hist = Counter(g['hidden_invariance_dim'] for g in groups)
    cut_hist = Counter(g['scalar_linear_cut'] for g in groups)

    n = len(groups)
    orders = {
        'original_rank_ascending': sorted(
            range(n), key=lambda i: (groups[i]['original_combined_rank'], groups[i]['multiplicity'], i)
        ),
        'refined_rank_ascending': sorted(
            range(n), key=lambda i: (groups[i]['refined_rank'], groups[i]['multiplicity'], i)
        ),
        'refined_rank_descending': sorted(
            range(n), key=lambda i: (-groups[i]['refined_rank'], groups[i]['multiplicity'], i)
        ),
        'multiplicity_then_refined': sorted(
            range(n), key=lambda i: (groups[i]['multiplicity'], groups[i]['refined_rank'], i)
        ),
    }

    path_profiles = {
        name: A.L.order_profile(route, order) for name, order in orders.items()
    }
    half = n // 2
    cuts = []
    for name, order in orders.items():
        st = A.L.cut_stats(route, set(order[:half]))
        st['name'] = name + '_half'
        cuts.append(st)
    cuts.sort(key=lambda x: (x['lambda'], x['name']))

    recursive = {}
    for name in ('refined_rank_ascending', 'refined_rank_descending', 'multiplicity_then_refined'):
        recursive[name] = A.recursive_certificate(route, orders[name])
    best_name, best = min(
        recursive.items(),
        key=lambda kv: (
            kv[1]['certificate']['width'],
            kv[1]['certificate']['max_depth'],
            kv[0],
        ),
    )

    out = {
        'position': POS,
        'raw_e0_sectors': raw,
        'support_groups': n,
        'global_refined_rank': global_rank,
        'original_combined_rank_histogram': dict(sorted(original_hist.items())),
        'aggregate_scalar_polar_rank_histogram': dict(sorted(polar_hist.items())),
        'radical_refined_rank_histogram': dict(sorted(radical_hist.items())),
        'refined_rank_histogram': dict(sorted(refined_hist.items())),
        'extra_rank_histogram': dict(sorted(extra_hist.items())),
        'hidden_invariance_dim_histogram': dict(sorted(hidden_hist.items())),
        'scalar_linear_cut_histogram': dict(sorted(cut_hist.items())),
        'groups_with_no_extra_rank': sum(g['extra_rank'] == 0 for g in groups),
        'groups_reaching_full_rank': sum(g['refined_rank'] == DOMAIN_BITS for g in groups),
        'max_extra_rank': max(g['extra_rank'] for g in groups),
        'min_refined_rank': min(g['refined_rank'] for g in groups),
        'max_refined_rank': max(g['refined_rank'] for g in groups),
        'best_balanced_cut': cuts[0],
        'path_widths': {name: p['max_lambda'] for name, p in path_profiles.items()},
        'recursive_widths': {
            name: data['certificate']['width'] for name, data in recursive.items()
        },
        'best_recursive_order': best_name,
        'best_recursive_width': best['certificate']['width'],
        'best_recursive_depth': best['certificate']['max_depth'],
        'best_recursive_root_children': best['root_children'],
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_AGGREGATE_E0_SCALAR_SEPARATOR')
    print('scope=C same-support XOR-aggregate scalar only; minimal exact linear refinement making each aggregate right-only quadratic scalar constant on local signature fibers, followed by exact displayed separator certificates')
    print('comparison=historical sectorwise scalar refinement was strictly stronger because it fixed every constituent sector scalar separately')
    print('not_included=grouped-e0 aggregate carry, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


def main():
    analyze()


if __name__ == '__main__':
    main()
