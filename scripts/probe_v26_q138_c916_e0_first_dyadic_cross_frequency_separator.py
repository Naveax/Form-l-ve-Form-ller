#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_aggregate_signature_separator as A
import probe_v26_q138_c916_e0_same_support_integer_coefficients as C
import probe_v26_q138_c916_e0_first_dyadic_pair_residual as D

POS = 'C'
SHARED_EXT = tuple(range(128)) + tuple(C.P.U.F.REXT)
LOCAL_EXT = tuple(C.P.U.F.LEXT)
assert len(SHARED_EXT) == 149 and len(LOCAL_EXT) == 11


def xor_phase(a, b):
    return (
        a[0] ^ b[0],
        a[1] ^ b[1],
        tuple(x ^ y for x, y in zip(a[2], b[2])),
        None,
        None,
    )


def cross_control_rows(phase):
    polar = phase[2]
    rows = []
    for le in LOCAL_EXT:
        row = 0
        for si, se in enumerate(SHARED_EXT):
            if (polar[se] >> le) & 1:
                row |= 1 << si
        if row:
            rows.append(row)
    return rows


def analyze():
    raw, base_groups = A.build_groups(POS)
    assert raw == 577 and len(base_groups) == 250

    pair_out = D.analyze()
    pair_groups = {g['group_id']: g for g in pair_out['groups']}
    assert len(pair_groups) == 147

    e0, _e1, _half = C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    for k in range(4):
        for zs, cls in e0[k]:
            can = C.P.U.H.support_for(POS, zs, cls)
            if can is not None:
                grouped[can].append((zs, cls))
    ordered = list(sorted(grouped.items(), key=lambda kv: kv[0]))
    assert len(ordered) == len(base_groups)

    route = []
    groups = []
    for gid, ((_can, sectors), base) in enumerate(zip(ordered, base_groups)):
        assert gid == base['group_id']
        m = len(sectors)
        phases = [C.phase_tuple(zs) for zs, _cls in sectors]

        anchor_rows = []
        difference_rows = []
        if m == 1:
            anchor_rows.extend(cross_control_rows(phases[0]))
        else:
            pg = pair_groups[gid]
            assert pg['multiplicity'] == m
            for selected in pg['selected_pairs']:
                i, j = selected['pair']
                anchor_rows.extend(cross_control_rows(phases[i]))
                difference_rows.extend(cross_control_rows(xor_phase(phases[i], phases[j])))

        anchor_basis = A.L.basis(anchor_rows)
        difference_basis = A.L.basis(difference_rows)
        cross_basis = A.L.basis(anchor_basis + difference_basis)
        refined_basis = A.L.basis(list(base['combined_basis']) + cross_basis)
        assert A.L.rank(refined_basis + list(base['combined_basis'])) == len(refined_basis)

        rec = {
            'group_id': gid,
            'multiplicity': m,
            'base_rank': base['combined_rank'],
            'anchor_cross_rank': len(anchor_basis),
            'difference_cross_rank': len(difference_basis),
            'combined_cross_rank': len(cross_basis),
            'refined_rank': len(refined_basis),
            'extra_rank': len(refined_basis) - base['combined_rank'],
            'combined_basis': refined_basis,
        }
        groups.append(rec)
        route.append({
            'combined_basis': refined_basis,
            'combined_rank': len(refined_basis),
            'multiplicity': m,
        })

    assert A.L.union_rank(route, 'combined_basis') == 149

    n = len(groups)
    orders = {
        'base_multiplicity_then_rank': sorted(
            range(n), key=lambda i: (groups[i]['multiplicity'], groups[i]['base_rank'], i)
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

    half = n // 2
    cuts = []
    for name, order in orders.items():
        st = A.L.cut_stats(route, set(order[:half]))
        st['name'] = name + '_half'
        cuts.append(st)
    cuts.sort(key=lambda x: (x['lambda'], x['name']))

    out = {
        'position': POS,
        'support_groups': n,
        'global_refined_rank': A.L.union_rank(route, 'combined_basis'),
        'base_rank_histogram': dict(sorted(Counter(g['base_rank'] for g in groups).items())),
        'anchor_cross_rank_histogram': dict(sorted(Counter(g['anchor_cross_rank'] for g in groups).items())),
        'difference_cross_rank_histogram': dict(sorted(Counter(g['difference_cross_rank'] for g in groups).items())),
        'combined_cross_rank_histogram': dict(sorted(Counter(g['combined_cross_rank'] for g in groups).items())),
        'refined_rank_histogram': dict(sorted(Counter(g['refined_rank'] for g in groups).items())),
        'extra_rank_histogram': dict(sorted(Counter(g['extra_rank'] for g in groups).items())),
        'groups_with_no_extra_rank': sum(g['extra_rank'] == 0 for g in groups),
        'max_extra_rank': max(g['extra_rank'] for g in groups),
        'best_balanced_cut': cuts[0],
        'recursive_widths': {
            name: data['certificate']['width'] for name, data in recursive.items()
        },
        'best_recursive_order': best_name,
        'best_recursive_width': best['certificate']['width'],
        'best_recursive_depth': best['certificate']['max_depth'],
        'best_recursive_root_children': best['root_children'],
        'groups': [
            {k: v for k, v in g.items() if k != 'combined_basis'} for g in groups
        ],
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_CROSS_FREQUENCY_SEPARATOR')
    print('scope=exact linear refinement of each existing grouped-e0 support/frequency signature sufficient to determine every shared-dependent 11-bit local-frequency shift appearing in a valid full-coordinate representative of the first-dyadic singleton anchors, signed pair anchors, and pair equality differences')
    print('important=this is only the cross-frequency linear skeleton; local-left quadratic blocks, shared-only phase bits, support-gauge reductions, and integer residual arithmetic are not yet charged')
    print('decision=use the refined separator width only as a safe precursor for the complete carry representation')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
