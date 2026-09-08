#!/usr/bin/env python3
import hashlib
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_bc_half_uniform_linear_state_relaxed_scalar as U

PRED_BITS = 128
RIGHT_BITS = len(U.F.RIGHT)
DOMAIN_BITS = PRED_BITS + RIGHT_BITS
RANDOM_BALANCED_CUTS = 32
SEED = 0xBC_E0_149


def basis(rows):
    return S.row_basis(rows)


def rank(rows):
    return len(basis(rows))


def transpose_columns(columns, out_bits):
    """Transpose an out_bits x DOMAIN_BITS GF(2) matrix stored by columns."""
    assert len(columns) == DOMAIN_BITS
    rows = [0] * out_bits
    for j, col in enumerate(columns):
        y = col
        while y:
            lsb = y & -y
            i = lsb.bit_length() - 1
            assert i < out_bits
            rows[i] |= 1 << j
            y ^= lsb
    return rows


def pack_frequency(values):
    z = 0
    shift = 0
    for value in values:
        z |= value << shift
        shift += len(U.F.LEFT)
    return z


def local_group(pos, can, sectors, group_id):
    cond = U.G.predecessor_condition(can)
    sol = U.T.rref(cond, n=PRED_BITS)
    assert sol is not None
    p0 = sol[1]
    assert U.F.fixed_possible(can, p0)

    eqs, toggles, _rhsbits = U.F.support_desc(can, p0)
    syndrome_bits = len(eqs)
    assert len(toggles) == RIGHT_BITS

    polars = []
    crosses = []
    for zs, _cls in sectors:
        _c, _lin, polar, _r, _pr = U.X.full_corrected_phase(
            pos, U.D.carries(zs)
        )
        polars.append(polar)
        _q, cross, _r2, _pr2 = U.F.specialized_phase_data(pos, zs, p0)
        assert len(cross) == RIGHT_BITS
        crosses.append(cross)

    support_columns = []
    frequency_columns = []

    for i in range(PRED_BITS):
        d = 1 << i
        support_columns.append(U.pred_support_delta(can, d))
        frequency_columns.append(
            pack_frequency([U.pred_left_freq(polar, d) for polar in polars])
        )

    for j in range(RIGHT_BITS):
        support_columns.append(toggles[j])
        frequency_columns.append(pack_frequency([cross[j] for cross in crosses]))

    frequency_bits = len(sectors) * len(U.F.LEFT)
    support_rows = transpose_columns(support_columns, syndrome_bits)
    frequency_rows = transpose_columns(frequency_columns, frequency_bits)
    combined_rows = support_rows + frequency_rows

    support_basis = basis(support_rows)
    frequency_basis = basis(frequency_rows)
    combined_basis = basis(combined_rows)

    # Stable digest for certificates without serializing the large support key.
    can_bytes = b''.join(int(x).to_bytes((int(x).bit_length() + 7) // 8 or 1, 'little') + b'\0' for x in can)
    can_digest = hashlib.sha256(can_bytes).hexdigest()[:16]

    return {
        'group_id': group_id,
        'can_digest': can_digest,
        'multiplicity': len(sectors),
        'syndrome_bits': syndrome_bits,
        'frequency_bits': frequency_bits,
        'support_rank': len(support_basis),
        'frequency_rank': len(frequency_basis),
        'combined_rank': len(combined_basis),
        'support_basis': support_basis,
        'frequency_basis': frequency_basis,
        'combined_basis': combined_basis,
    }


def union_rank(groups, field, indices=None):
    if indices is None:
        indices = range(len(groups))
    rows = []
    for i in indices:
        rows.extend(groups[i][field])
    return rank(rows)


def cut_stats(groups, subset):
    left = sorted(subset)
    chosen = set(left)
    right = [i for i in range(len(groups)) if i not in chosen]
    lr = union_rank(groups, 'combined_basis', left)
    rr = union_rank(groups, 'combined_basis', right)
    full = DOMAIN_BITS
    lam = lr + rr - full
    assert 0 <= lam <= DOMAIN_BITS
    return {
        'left_groups': len(left),
        'right_groups': len(right),
        'left_rank': lr,
        'right_rank': rr,
        'lambda': lam,
    }


def order_profile(groups, order):
    n = len(order)
    prefix = [0] * (n + 1)
    suffix = [0] * (n + 1)

    rows = []
    for k, i in enumerate(order, 1):
        rows.extend(groups[i]['combined_basis'])
        prefix[k] = rank(rows)

    rows = []
    for k in range(n - 1, -1, -1):
        rows.extend(groups[order[k]]['combined_basis'])
        suffix[k] = rank(rows)

    profile = []
    max_lambda = -1
    argmax = None
    for k in range(n + 1):
        lam = prefix[k] + suffix[k] - DOMAIN_BITS
        assert 0 <= lam <= DOMAIN_BITS
        if lam > max_lambda:
            max_lambda = lam
            argmax = k
        if k in (0, n // 4, n // 2, (3 * n) // 4, n):
            profile.append(
                {
                    'cut': k,
                    'prefix_rank': prefix[k],
                    'suffix_rank': suffix[k],
                    'lambda': lam,
                }
            )
    return {
        'max_lambda': max_lambda,
        'argmax_cut': argmax,
        'selected_profile': profile,
    }


def analyze(pos):
    e0, _e1, _half = U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for k in range(4):
        for zs, cls in e0[k]:
            can = U.H.support_for(pos, zs, cls)
            if can is None:
                continue
            raw += 1
            grouped[can].append((zs, cls))

    expected_raw = 581 if pos == 'B' else 577
    expected_groups = 251 if pos == 'B' else 250
    assert raw == expected_raw
    assert len(grouped) == expected_groups

    groups = []
    for group_id, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        groups.append(local_group(pos, can, sectors, group_id))

    support_global = union_rank(groups, 'support_basis')
    frequency_global = union_rank(groups, 'frequency_basis')
    combined_global = union_rank(groups, 'combined_basis')
    assert support_global == DOMAIN_BITS
    assert combined_global == DOMAIN_BITS
    assert frequency_global == (149 if pos == 'B' else 147)

    local_hist = Counter(g['combined_rank'] for g in groups)
    support_hist = Counter(g['support_rank'] for g in groups)
    frequency_hist = Counter(g['frequency_rank'] for g in groups)
    multiplicity_hist = Counter(g['multiplicity'] for g in groups)

    # Exact pairwise row-space intersections. These are local overlap data, not
    # a claim about globally optimal branchwidth.
    pair_overlap_hist = Counter()
    max_pair_overlap = -1
    max_pair = None
    for i in range(len(groups)):
        bi = groups[i]['combined_basis']
        ri = groups[i]['combined_rank']
        for j in range(i + 1, len(groups)):
            rj = groups[j]['combined_rank']
            rij = rank(bi + groups[j]['combined_basis'])
            ov = ri + rj - rij
            pair_overlap_hist[ov] += 1
            if ov > max_pair_overlap:
                max_pair_overlap = ov
                max_pair = (i, j)

    orders = {
        'canonical': list(range(len(groups))),
        'local_rank_ascending': sorted(
            range(len(groups)), key=lambda i: (groups[i]['combined_rank'], i)
        ),
        'local_rank_descending': sorted(
            range(len(groups)), key=lambda i: (-groups[i]['combined_rank'], i)
        ),
        'multiplicity_then_rank': sorted(
            range(len(groups)),
            key=lambda i: (groups[i]['multiplicity'], groups[i]['combined_rank'], i),
        ),
    }
    order_profiles = {name: order_profile(groups, order) for name, order in orders.items()}

    # Balanced cuts are only route-search candidates. Every reported lambda is
    # exact for that particular cut; the minimum across samples is NOT claimed
    # to be the optimum branchwidth/min-cut.
    n = len(groups)
    left_size = n // 2
    cut_candidates = []
    canonical_subset = set(range(left_size))
    cut_candidates.append(('canonical_half', canonical_subset))
    rank_order = orders['local_rank_ascending']
    cut_candidates.append(('rank_half', set(rank_order[:left_size])))
    multiplicity_order = orders['multiplicity_then_rank']
    cut_candidates.append(('multiplicity_half', set(multiplicity_order[:left_size])))

    rng = random.Random(SEED + ord(pos))
    base = list(range(n))
    for t in range(RANDOM_BALANCED_CUTS):
        rng.shuffle(base)
        cut_candidates.append((f'random_{t:02d}', set(base[:left_size])))

    balanced = []
    for name, subset in cut_candidates:
        st = cut_stats(groups, subset)
        st['name'] = name
        balanced.append(st)
    balanced.sort(key=lambda x: (x['lambda'], x['name']))

    compact_groups = [
        {
            k: g[k]
            for k in (
                'group_id',
                'can_digest',
                'multiplicity',
                'syndrome_bits',
                'frequency_bits',
                'support_rank',
                'frequency_rank',
                'combined_rank',
            )
        }
        for g in groups
    ]

    out = {
        'position': pos,
        'domain_bits': DOMAIN_BITS,
        'raw_e0_sectors': raw,
        'support_groups': len(groups),
        'global_ranks': {
            'support': support_global,
            'frequency': frequency_global,
            'combined': combined_global,
        },
        'local_combined_rank_histogram': dict(sorted(local_hist.items())),
        'local_support_rank_histogram': dict(sorted(support_hist.items())),
        'local_frequency_rank_histogram': dict(sorted(frequency_hist.items())),
        'multiplicity_histogram': dict(sorted(multiplicity_hist.items())),
        'pair_overlap_histogram': dict(sorted(pair_overlap_hist.items())),
        'max_pair_overlap': {
            'dimension': max_pair_overlap,
            'groups': list(max_pair) if max_pair else None,
        },
        'order_profiles': order_profiles,
        'best_sampled_balanced_cut': balanced[0],
        'sampled_balanced_cut_lambda_histogram': dict(
            sorted(Counter(x['lambda'] for x in balanced).items())
        ),
        'groups': compact_groups,
    }
    print(json.dumps(out, sort_keys=True), flush=True)
    return out


def main():
    out = {pos: analyze(pos) for pos in 'BC'}
    print('result_summary', json.dumps({
        pos: {
            'global_ranks': out[pos]['global_ranks'],
            'local_combined_rank_histogram': out[pos]['local_combined_rank_histogram'],
            'max_pair_overlap': out[pos]['max_pair_overlap'],
            'best_sampled_balanced_cut': out[pos]['best_sampled_balanced_cut'],
            'order_profiles': out[pos]['order_profiles'],
        }
        for pos in 'BC'
    }, sort_keys=True))
    print('PASS V26_Q138_BC_E0_LOCAL_GROUP_SEPARATOR')
    print('scope=exact GF2 local group row spaces, pair overlaps, deterministic path-order profiles, and sampled balanced separator certificates over the 149-bit shared state')
    print('claim=all reported ranks and lambda values are exact for the displayed groups/orders/cuts; sampled minima are upper-bound route diagnostics only, not optimal branchwidth claims')
    print('not_included=grouped-e0 quadratic carry, recursive contraction tree certificate, e0-half cross-carry, complete B2/C2, W_repr, alpha, arithmetic-work, ranking/search, full-round')


if __name__ == '__main__':
    main()
