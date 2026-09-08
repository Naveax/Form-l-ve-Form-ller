#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_local_group_separator as P

DOMAIN_BITS = P.DOMAIN_BITS
PRED_BITS = P.PRED_BITS
RIGHT_EXT = tuple(P.U.F.REXT)
assert DOMAIN_BITS == PRED_BITS + len(RIGHT_EXT) == 149


def embed_domain(x):
    """Embed 128 predecessor + 21 right-beta bits into the 160 external bits."""
    out = x & ((1 << PRED_BITS) - 1)
    y = x >> PRED_BITS
    j = 0
    while y:
        b = y & -y
        j = b.bit_length() - 1
        out |= 1 << RIGHT_EXT[j]
        y ^= b
    return out


def restrict_polar_rows(full_polar):
    """Restrict the full 160-bit polar matrix to the 149 shared coordinates."""
    rows = []
    pred_mask = (1 << PRED_BITS) - 1
    for ea in list(range(PRED_BITS)) + list(RIGHT_EXT):
        src = full_polar[ea]
        row = src & pred_mask
        for j, eb in enumerate(RIGHT_EXT):
            if (src >> eb) & 1:
                row |= 1 << (PRED_BITS + j)
        rows.append(row)
    assert len(rows) == DOMAIN_BITS
    assert all(((rows[i] >> i) & 1) == 0 for i in range(DOMAIN_BITS))
    assert all(
        ((rows[i] >> j) & 1) == ((rows[j] >> i) & 1)
        for i in range(DOMAIN_BITS)
        for j in range(i + 1, DOMAIN_BITS)
    )
    return tuple(rows)


def scalar_phase(pos, zs):
    c, lin, polar, rank, pr = P.U.X.full_corrected_phase(
        pos, P.U.D.carries(zs)
    )
    return {
        'c': c,
        'lin': lin,
        'polar': polar,
        'restricted_polar_rows': restrict_polar_rows(polar),
        'internal_rank': rank,
        'polar_radical_dim': pr,
    }


def scalar_delta(phase, h):
    """q(h)+q(0) for the scalar restriction q(p,right), with left beta = 0."""
    return P.U.X.q_eval(
        phase['c'], phase['lin'], phase['polar'], embed_domain(h)
    ) ^ phase['c']


def nullspace(rows):
    eqs = [(int(row), 0) for row in rows]
    sol = P.U.T.rref(eqs, n=DOMAIN_BITS)
    assert sol is not None
    rank, x0, kernel = sol
    assert x0 == 0
    assert rank + len(kernel) == DOMAIN_BITS
    return list(kernel), rank


def annihilator_basis(kernel):
    # K^perp is the minimal row space whose kernel is exactly K.
    if not kernel:
        return [1 << i for i in range(DOMAIN_BITS)]
    sol = P.U.T.rref([(h, 0) for h in kernel], n=DOMAIN_BITS)
    assert sol is not None
    rank, x0, out = sol
    assert x0 == 0
    assert rank == len(kernel)
    assert len(out) == DOMAIN_BITS - len(kernel)
    return list(out)


def impose_scalar_invariance(kernel, phase):
    """Intersect a radical-contained kernel with q(h)=q(0)."""
    vals = [scalar_delta(phase, h) for h in kernel]
    pivot = next((i for i, v in enumerate(vals) if v), None)
    if pivot is None:
        return kernel, False

    p = kernel[pivot]
    out = []
    for i, h in enumerate(kernel):
        if i == pivot:
            continue
        if vals[i]:
            h ^= p
        out.append(h)

    # On the polar radical, q(h)+q(0) is linear, so this is exactly its kernel.
    assert len(out) + 1 == len(kernel)
    assert all(scalar_delta(phase, h) == 0 for h in out)
    return out, True


def refine_group(info, phases):
    original = list(info['combined_basis'])
    original_rank = len(original)

    # First require every hidden direction to lie in the radical of every
    # sector scalar quadratic. Then derivative along such a direction is a
    # constant bit q(h)+q(0), which is removed by one additional linear
    # constraint exactly when nonzero.
    rows = list(original)
    for phase in phases:
        rows.extend(phase['restricted_polar_rows'])
    kernel, radical_refined_rank = nullspace(rows)

    scalar_linear_cuts = 0
    for phase in phases:
        kernel, cut = impose_scalar_invariance(kernel, phase)
        scalar_linear_cuts += int(cut)

    # Exact invariance verification for a basis of the final hidden subgroup.
    for h in kernel:
        assert all(
            ((row & h).bit_count() & 1) == 0
            for phase in phases
            for row in phase['restricted_polar_rows']
        )
        assert all(scalar_delta(phase, h) == 0 for phase in phases)

    refined_basis = annihilator_basis(kernel)
    refined_basis = P.basis(refined_basis)
    refined_rank = len(refined_basis)
    assert refined_rank == DOMAIN_BITS - len(kernel)
    assert P.rank(refined_basis + original) == refined_rank
    assert refined_rank >= radical_refined_rank >= original_rank
    assert refined_rank - radical_refined_rank == scalar_linear_cuts

    return {
        **info,
        'original_combined_rank': original_rank,
        'radical_refined_rank': radical_refined_rank,
        'scalar_linear_cuts': scalar_linear_cuts,
        'refined_rank': refined_rank,
        'extra_rank': refined_rank - original_rank,
        'hidden_invariance_dim': len(kernel),
        'refined_basis': refined_basis,
    }


def route_projection(groups):
    return [
        {
            'combined_basis': g['refined_basis'],
            'combined_rank': g['refined_rank'],
            'multiplicity': g['multiplicity'],
        }
        for g in groups
    ]


def analyze(pos):
    e0, _e1, _half = P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for k in range(4):
        for zs, cls in e0[k]:
            can = P.U.H.support_for(pos, zs, cls)
            if can is None:
                continue
            raw += 1
            grouped[can].append((zs, cls))

    expected_raw = 581 if pos == 'B' else 577
    expected_groups = 251 if pos == 'B' else 250
    assert raw == expected_raw
    assert len(grouped) == expected_groups

    groups = []
    phase_rank_hist = Counter()
    phase_pr_hist = Counter()
    for group_id, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        info = P.local_group(pos, can, sectors, group_id)
        phases = []
        for zs, _cls in sectors:
            phase = scalar_phase(pos, zs)
            phase_rank_hist[phase['internal_rank']] += 1
            phase_pr_hist[phase['polar_radical_dim']] += 1
            phases.append(phase)
        groups.append(refine_group(info, phases))

    route = route_projection(groups)
    global_rank = P.union_rank(route, 'combined_basis')
    assert global_rank == DOMAIN_BITS

    original_hist = Counter(g['original_combined_rank'] for g in groups)
    radical_hist = Counter(g['radical_refined_rank'] for g in groups)
    refined_hist = Counter(g['refined_rank'] for g in groups)
    extra_hist = Counter(g['extra_rank'] for g in groups)
    hidden_hist = Counter(g['hidden_invariance_dim'] for g in groups)
    scalar_cut_hist = Counter(g['scalar_linear_cuts'] for g in groups)

    n = len(groups)
    orders = {
        'original_rank_ascending': sorted(
            range(n), key=lambda i: (groups[i]['original_combined_rank'], i)
        ),
        'refined_rank_ascending': sorted(
            range(n), key=lambda i: (groups[i]['refined_rank'], i)
        ),
        'refined_rank_descending': sorted(
            range(n), key=lambda i: (-groups[i]['refined_rank'], i)
        ),
        'multiplicity_then_refined': sorted(
            range(n),
            key=lambda i: (groups[i]['multiplicity'], groups[i]['refined_rank'], i),
        ),
    }
    order_profiles = {
        name: P.order_profile(route, order) for name, order in orders.items()
    }

    left_size = n // 2
    cuts = []
    for name, order in orders.items():
        st = P.cut_stats(route, set(order[:left_size]))
        st['name'] = name + '_half'
        cuts.append(st)
    cuts.sort(key=lambda x: (x['lambda'], x['name']))

    compact_groups = [
        {
            'group_id': g['group_id'],
            'multiplicity': g['multiplicity'],
            'original_combined_rank': g['original_combined_rank'],
            'radical_refined_rank': g['radical_refined_rank'],
            'scalar_linear_cuts': g['scalar_linear_cuts'],
            'refined_rank': g['refined_rank'],
            'extra_rank': g['extra_rank'],
            'hidden_invariance_dim': g['hidden_invariance_dim'],
        }
        for g in groups
    ]

    out = {
        'position': pos,
        'domain_bits': DOMAIN_BITS,
        'raw_e0_sectors': raw,
        'support_groups': len(groups),
        'global_refined_rank': global_rank,
        'phase_internal_rank_histogram': dict(sorted(phase_rank_hist.items())),
        'phase_internal_polar_radical_dim_histogram': dict(sorted(phase_pr_hist.items())),
        'original_local_rank_histogram': dict(sorted(original_hist.items())),
        'radical_refined_rank_histogram': dict(sorted(radical_hist.items())),
        'refined_local_rank_histogram': dict(sorted(refined_hist.items())),
        'extra_rank_histogram': dict(sorted(extra_hist.items())),
        'hidden_invariance_dim_histogram': dict(sorted(hidden_hist.items())),
        'scalar_linear_cut_count_histogram': dict(sorted(scalar_cut_hist.items())),
        'groups_already_scalar_determined': sum(g['extra_rank'] == 0 for g in groups),
        'groups_refined_to_full_149': sum(g['refined_rank'] == DOMAIN_BITS for g in groups),
        'max_refined_rank': max(g['refined_rank'] for g in groups),
        'max_extra_rank': max(g['extra_rank'] for g in groups),
        'best_deterministic_balanced_cut': cuts[0],
        'balanced_cuts': cuts,
        'order_profiles': order_profiles,
        'groups': compact_groups,
    }
    print(json.dumps(out, sort_keys=True), flush=True)
    return out


def main():
    out = {pos: analyze(pos) for pos in 'BC'}
    print('result_summary', json.dumps({
        pos: {
            'refined_local_rank_histogram': out[pos]['refined_local_rank_histogram'],
            'extra_rank_histogram': out[pos]['extra_rank_histogram'],
            'groups_already_scalar_determined': out[pos]['groups_already_scalar_determined'],
            'groups_refined_to_full_149': out[pos]['groups_refined_to_full_149'],
            'max_refined_rank': out[pos]['max_refined_rank'],
            'max_extra_rank': out[pos]['max_extra_rank'],
            'best_deterministic_balanced_cut': out[pos]['best_deterministic_balanced_cut'],
            'path_widths': {
                name: profile['max_lambda']
                for name, profile in out[pos]['order_profiles'].items()
            },
        }
        for pos in 'BC'
    }, sort_keys=True))
    print('PASS V26_Q138_BC_E0_QUADRATIC_SCALAR_REFINEMENT')
    print('scope=exact minimal sectorwise linear refinements of PR112 local signatures sufficient to determine each grouped-e0 sector scalar quadratic phase on the 149-bit shared domain')
    print('claim=refinement is minimal among linear signatures extending each local support/frequency signature and determining all sector scalar bits individually; separator values are exact for the displayed refined linear routes')
    print('relaxation=sectorwise scalar determination may be stronger than necessary for the aggregate grouped factor because cross-sector cancellation is not exploited')
    print('not_included=recursive refined tree, grouped-e0 carry values, e0-half cross-carry, complete B2/C2, W_repr, alpha, arithmetic-work, ranking/search, full-round')


if __name__ == '__main__':
    main()
