#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_aggregate_signature_separator as A
import probe_v26_q138_c916_e0_same_support_integer_coefficients as C
import probe_v26_q138_c916_e0_complete_first_dyadic_fiber_geometry as G
import probe_v26_q138_c916_e0_first_dyadic_gauss_radical_control as R

POS = 'C'
DOMAIN_BITS = 149
SHARED_EXT = tuple(range(128)) + tuple(C.P.U.F.REXT)
assert len(SHARED_EXT) == DOMAIN_BITS


def compress_shared(full):
    out = 0
    for j, ext in enumerate(SHARED_EXT):
        if (full >> ext) & 1:
            out |= 1 << j
    return out


def solve_shared_representative(control_coeff, support_basis):
    eqs = []
    projected = []
    for i, b in enumerate(support_basis):
        row = compress_shared(b)
        projected.append(row)
        eqs.append((row, (control_coeff >> i) & 1))
    sol = C.P.U.T.rref(eqs, n=DOMAIN_BITS)
    assert sol is not None
    rank, x0, gauge = sol
    for i, row in enumerate(projected):
        assert ((x0 & row).bit_count() & 1) == ((control_coeff >> i) & 1)
    return rank, x0, tuple(gauge)


def analyze():
    raw, base_groups = A.build_groups(POS)
    assert raw == 577 and len(base_groups) == 250

    e0, _e1, _half = C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    for k in range(4):
        for zs, cls in e0[k]:
            can = C.P.U.H.support_for(POS, zs, cls)
            if can is not None:
                grouped[can].append((zs, cls))
    ordered = list(sorted(grouped.items(), key=lambda kv: kv[0]))
    assert len(ordered) == len(base_groups)

    groups = []
    gauge_contained = 0
    lifted_rank_matches = 0
    for gid, ((can, sectors), base) in enumerate(zip(ordered, base_groups)):
        assert gid == base['group_id']
        _srank, x0, support_basis = C.X.support_param(can)
        d = len(support_basis)
        projection_rank, kernel = G.local_fiber_coeff_basis(support_basis)

        control_rows = []
        for zs, _cls in sectors:
            sig, sd, _nbits = C.X.restricted_phase_signature(
                C.phase_tuple(zs), x0, support_basis
            )
            assert sd == d
            rec = R.sector_radical_controls(sig, d, kernel)
            control_rows.extend(rec['control_basis_pullback'])
        control_coeff_basis = tuple(C.P.U.S.row_basis(control_rows))

        zero_eqs = [(compress_shared(b), 0) for b in support_basis]
        zero_sol = C.P.U.T.rref(zero_eqs, n=DOMAIN_BITS)
        assert zero_sol is not None
        zero_rank, zero_x0, gauge_basis = zero_sol
        assert zero_x0 == 0
        assert zero_rank == projection_rank
        gauge_basis = tuple(gauge_basis)

        gauge_delta = A.L.rank(list(base['support_basis']) + list(gauge_basis)) - base['support_rank']
        if gauge_delta == 0:
            gauge_contained += 1

        lifted = []
        for f in control_coeff_basis:
            rank, rep, gauge2 = solve_shared_representative(f, support_basis)
            assert rank == projection_rank
            assert A.L.rank(list(gauge_basis) + list(gauge2)) == len(gauge_basis)
            assert A.L.rank(list(gauge2) + list(gauge_basis)) == len(gauge2)
            lifted.append(rep)
        lifted_basis = tuple(A.L.basis(lifted))
        if len(lifted_basis) == len(control_coeff_basis):
            lifted_rank_matches += 1

        refined_basis = tuple(A.L.basis(list(base['combined_basis']) + list(lifted_basis)))
        groups.append({
            'group_id': gid,
            'multiplicity': len(sectors),
            'base_rank': base['combined_rank'],
            'radical_control_rank': len(control_coeff_basis),
            'lifted_radical_rank': len(lifted_basis),
            'refined_rank': len(refined_basis),
            'extra_rank': len(refined_basis) - base['combined_rank'],
            'projection_rank': projection_rank,
            'gauge_dimension': len(gauge_basis),
            'gauge_delta_over_base_support': gauge_delta,
            'combined_basis': refined_basis,
        })

    assert gauge_contained == len(groups)
    assert lifted_rank_matches == len(groups)

    global_refined_rank = A.L.union_rank(groups, 'combined_basis')
    assert global_refined_rank == DOMAIN_BITS

    base_order = sorted(
        range(len(groups)),
        key=lambda i: (groups[i]['multiplicity'], groups[i]['base_rank'], i),
    )
    orders = {
        'base_multiplicity_then_rank': base_order,
        'multiplicity_then_refined': sorted(
            range(len(groups)),
            key=lambda i: (groups[i]['multiplicity'], groups[i]['refined_rank'], i),
        ),
        'refined_rank_ascending': sorted(
            range(len(groups)),
            key=lambda i: (groups[i]['refined_rank'], groups[i]['multiplicity'], i),
        ),
        'refined_rank_descending': sorted(
            range(len(groups)),
            key=lambda i: (-groups[i]['refined_rank'], groups[i]['multiplicity'], i),
        ),
        'radical_rank_ascending': sorted(
            range(len(groups)),
            key=lambda i: (groups[i]['radical_control_rank'], groups[i]['multiplicity'], groups[i]['refined_rank'], i),
        ),
    }

    base_rec = A.recursive_certificate(base_groups, base_order)
    recursive = {
        name: A.recursive_certificate(groups, order)
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

    half = len(groups) // 2
    cuts = []
    for name, order in orders.items():
        st = A.L.cut_stats(groups, set(order[:half]))
        st['name'] = name + '_half'
        cuts.append(st)
    cuts.sort(key=lambda x: (x['lambda'], x['name']))

    out = {
        'position': POS,
        'support_groups': len(groups),
        'global_refined_rank': global_refined_rank,
        'all_group_gauges_contained_in_existing_support_basis': gauge_contained == len(groups),
        'all_group_lifted_ranks_match_control_ranks': lifted_rank_matches == len(groups),
        'radical_control_rank_histogram': dict(sorted(Counter(g['radical_control_rank'] for g in groups).items())),
        'base_rank_histogram': dict(sorted(Counter(g['base_rank'] for g in groups).items())),
        'refined_rank_histogram': dict(sorted(Counter(g['refined_rank'] for g in groups).items())),
        'extra_rank_histogram': dict(sorted(Counter(g['extra_rank'] for g in groups).items())),
        'max_extra_rank': max(g['extra_rank'] for g in groups),
        'groups_with_zero_extra_rank': sum(g['extra_rank'] == 0 for g in groups),
        'gauge_dimension_histogram': dict(sorted(Counter(g['gauge_dimension'] for g in groups).items())),
        'base_recursive_width': base_rec['certificate']['width'],
        'base_recursive_depth': base_rec['certificate']['max_depth'],
        'recursive_widths': {
            name: data['certificate']['width'] for name, data in recursive.items()
        },
        'best_recursive_order': best_name,
        'best_recursive_width': best['certificate']['width'],
        'best_recursive_depth': best['certificate']['max_depth'],
        'best_recursive_root_children': best['root_children'],
        'best_balanced_cut': cuts[0],
        'groups': [
            {k: v for k, v in g.items() if k != 'combined_basis'}
            for g in groups
        ],
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_GAUSS_RADICAL_AUGMENTED_SEPARATOR')
    print('scope=exact gauge-invariant augmentation of the existing 149-bit grouped-e0 support/frequency skeleton by all first-dyadic Gauss radical-support controls')
    print('important=every shared representative ambiguity is proved contained in the pre-existing per-group support basis before separator ranks are measured')
    print('not_included=nonzero Gauss sign/phase and amplitude, signed integer first-dyadic arithmetic, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
