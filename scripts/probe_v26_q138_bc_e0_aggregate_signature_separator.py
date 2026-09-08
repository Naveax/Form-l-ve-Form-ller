#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_direct_e1_exact_sector_cancellation as X
import probe_v26_q138_bc_e0_local_group_separator as L
import probe_v26_q138_bc_e0_recursive_separator_tree as T
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S

DOMAIN_BITS = len(S.RIGHT)
LEFT_BITS = len(S.LEFT)
assert DOMAIN_BITS == 149
assert LEFT_BITS == 11


def compress_shared(mask):
    z = 0
    for j, ext in enumerate(S.RIGHT):
        if (mask >> ext) & 1:
            z |= 1 << j
    return z


def support_basis(can):
    # For fixed shared coordinates r, the left support is the solution set of
    # L x_left = b(r). Two reachable RHS vectors give the same support mask iff
    # they are equal, so these restricted equation rows are the exact linear
    # shared-state information needed to select the affine left support.
    return L.basis(compress_shared(row) for row in can)


def frequency_basis(cols):
    assert len(cols) == DOMAIN_BITS
    return L.basis(L.transpose_columns(cols, LEFT_BITS))


def left_truth_from_full_phase(c, lin, polar):
    qbits = S.ALL if c else 0
    for a, ext in enumerate(S.LEFT):
        if (lin >> ext) & 1:
            qbits ^= S.WALSH[1 << a]
    for a, ea in enumerate(S.LEFT):
        for b in range(a + 1, LEFT_BITS):
            eb = S.LEFT[b]
            if (polar[ea] >> eb) & 1:
                qbits ^= S.WALSH[1 << a] & S.WALSH[1 << b]
    return qbits


def cross_columns_from_full_phase(polar):
    cols = []
    for er in S.RIGHT:
        f = 0
        for a, el in enumerate(S.LEFT):
            if (polar[er] >> el) & 1:
                f |= 1 << a
        cols.append(f)
    return tuple(cols)


def verify_sector_projection(pos, zs):
    Cmask = L.U.D.carries(zs)
    qbits, cols, rank, meta = S.corrected_phase_data(pos, Cmask)
    c, lin, polar, full_rank, full_pr = X.full_corrected_phase(pos, Cmask)
    assert rank == full_rank
    assert meta['pr'] == full_pr
    assert qbits == left_truth_from_full_phase(c, lin, polar)
    assert tuple(cols) == cross_columns_from_full_phase(polar)
    return qbits, tuple(cols), rank, full_pr


def aggregate_group(pos, can, sectors, group_id):
    qbits = 0
    cols = [0] * DOMAIN_BITS
    rank_hist = Counter()
    pr_hist = Counter()

    for zs, _cls in sectors:
        q, c, rank, pr = verify_sector_projection(pos, zs)
        qbits ^= q
        cols = [a ^ b for a, b in zip(cols, c)]
        rank_hist[rank] += 1
        pr_hist[pr] += 1

    sb = support_basis(can)
    fb = frequency_basis(cols)
    cb = L.basis(sb + fb)

    # This is exactly the shared-state dependence of the canonical local
    # sign-span generator after same-support XOR aggregation. The omitted
    # right-only scalar s(r) can only complement the entire 2048-bit left
    # truth vector. S.grouped_e0_basis() explicitly includes S.ALL in every
    # local span, hence that complement is a gauge action for this target.
    return {
        'group_id': group_id,
        'multiplicity': len(sectors),
        'qbits_weight': qbits.bit_count(),
        'support_rank': len(sb),
        'aggregate_frequency_rank': len(fb),
        'combined_rank': len(cb),
        'support_basis': sb,
        'frequency_basis': fb,
        'combined_basis': cb,
        'sector_internal_rank_histogram': dict(sorted(rank_hist.items())),
        'sector_internal_pr_histogram': dict(sorted(pr_hist.items())),
    }


def build_groups(pos):
    e0, _e1, _half = L.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for k in range(4):
        for zs, cls in e0[k]:
            can = L.U.H.support_for(pos, zs, cls)
            if can is None:
                continue
            raw += 1
            grouped[can].append((zs, cls))

    expected_raw = 581 if pos == 'B' else 577
    expected_groups = 251 if pos == 'B' else 250
    expected_mult = {1: 103, 2: 57, 4: 91 if pos == 'B' else 90}
    assert raw == expected_raw
    assert len(grouped) == expected_groups
    assert dict(sorted(Counter(len(v) for v in grouped.values()).items())) == expected_mult

    groups = []
    for group_id, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        groups.append(aggregate_group(pos, can, sectors, group_id))
    return raw, groups


def pair_overlap_summary(groups):
    hist = Counter()
    best = (-1, None)
    for i in range(len(groups)):
        ri = groups[i]['combined_rank']
        bi = groups[i]['combined_basis']
        for j in range(i + 1, len(groups)):
            rj = groups[j]['combined_rank']
            rij = L.rank(bi + groups[j]['combined_basis'])
            ov = ri + rj - rij
            hist[ov] += 1
            if ov > best[0]:
                best = (ov, (i, j))
    return dict(sorted(hist.items())), {
        'dimension': best[0],
        'groups': list(best[1]) if best[1] is not None else None,
    }


def recursive_certificate(groups, order):
    oracle = T.RankOracle(groups)
    tree = T.build_tree(groups, order, oracle)
    cert = T.verify_tree(tree, order, oracle)
    return {
        'certificate': cert,
        'root_children': [
            {
                'size': tree['left']['size'],
                'rank': tree['left']['rank'],
                'complement_rank': tree['left']['complement_rank'],
                'lambda': tree['left']['lambda'],
            },
            {
                'size': tree['right']['size'],
                'rank': tree['right']['rank'],
                'complement_rank': tree['right']['complement_rank'],
                'lambda': tree['right']['lambda'],
            },
        ],
        'worst_nodes': T.worst_nodes(tree),
        'rank_oracle_cache_entries': len(oracle.rank_cache),
    }


def analyze(pos):
    raw, groups = build_groups(pos)
    n = len(groups)

    support_global = L.union_rank(groups, 'support_basis')
    frequency_global = L.union_rank(groups, 'frequency_basis')
    combined_global = L.union_rank(groups, 'combined_basis')
    assert support_global == DOMAIN_BITS
    assert combined_global == DOMAIN_BITS

    support_hist = Counter(g['support_rank'] for g in groups)
    freq_hist = Counter(g['aggregate_frequency_rank'] for g in groups)
    combined_hist = Counter(g['combined_rank'] for g in groups)
    mult_hist = Counter(g['multiplicity'] for g in groups)
    zero_frequency_groups = sum(g['aggregate_frequency_rank'] == 0 for g in groups)

    pair_hist, max_pair = pair_overlap_summary(groups)

    orders = {
        'canonical': list(range(n)),
        'aggregate_rank_ascending': sorted(
            range(n), key=lambda i: (groups[i]['combined_rank'], groups[i]['multiplicity'], i)
        ),
        'aggregate_rank_descending': sorted(
            range(n), key=lambda i: (-groups[i]['combined_rank'], groups[i]['multiplicity'], i)
        ),
        'multiplicity_then_rank': sorted(
            range(n), key=lambda i: (groups[i]['multiplicity'], groups[i]['combined_rank'], i)
        ),
    }
    path_profiles = {name: L.order_profile(groups, order) for name, order in orders.items()}

    half = n // 2
    cuts = []
    for name, order in orders.items():
        st = L.cut_stats(groups, set(order[:half]))
        st['name'] = name + '_half'
        cuts.append(st)
    cuts.sort(key=lambda x: (x['lambda'], x['name']))

    recursive = {}
    for name in ('aggregate_rank_ascending', 'aggregate_rank_descending', 'multiplicity_then_rank'):
        recursive[name] = recursive_certificate(groups, orders[name])
    best_tree_name, best_tree = min(
        recursive.items(),
        key=lambda kv: (
            kv[1]['certificate']['width'],
            kv[1]['certificate']['max_depth'],
            kv[0],
        ),
    )

    out = {
        'position': pos,
        'domain_bits': DOMAIN_BITS,
        'raw_e0_sectors': raw,
        'support_groups': n,
        'global_ranks': {
            'support': support_global,
            'aggregate_frequency': frequency_global,
            'combined': combined_global,
        },
        'multiplicity_histogram': dict(sorted(mult_hist.items())),
        'local_support_rank_histogram': dict(sorted(support_hist.items())),
        'local_aggregate_frequency_rank_histogram': dict(sorted(freq_hist.items())),
        'local_aggregate_combined_rank_histogram': dict(sorted(combined_hist.items())),
        'zero_aggregate_frequency_groups': zero_frequency_groups,
        'pair_overlap_histogram': pair_hist,
        'max_pair_overlap': max_pair,
        'best_deterministic_balanced_cut': cuts[0],
        'balanced_cuts': cuts,
        'path_profiles': path_profiles,
        'recursive_candidates': recursive,
        'best_recursive_order': best_tree_name,
        'best_recursive_width': best_tree['certificate']['width'],
        'best_recursive_depth': best_tree['certificate']['max_depth'],
        'best_recursive_root_children': best_tree['root_children'],
        'groups': [
            {
                'group_id': g['group_id'],
                'multiplicity': g['multiplicity'],
                'support_rank': g['support_rank'],
                'aggregate_frequency_rank': g['aggregate_frequency_rank'],
                'combined_rank': g['combined_rank'],
                'qbits_weight': g['qbits_weight'],
            }
            for g in groups
        ],
    }
    print(json.dumps(out, sort_keys=True), flush=True)
    return out


def main():
    out = {pos: analyze(pos) for pos in 'BC'}
    print('result_summary', json.dumps({
        pos: {
            'global_ranks': out[pos]['global_ranks'],
            'local_aggregate_frequency_rank_histogram': out[pos]['local_aggregate_frequency_rank_histogram'],
            'local_aggregate_combined_rank_histogram': out[pos]['local_aggregate_combined_rank_histogram'],
            'zero_aggregate_frequency_groups': out[pos]['zero_aggregate_frequency_groups'],
            'max_pair_overlap': out[pos]['max_pair_overlap'],
            'best_deterministic_balanced_cut': out[pos]['best_deterministic_balanced_cut'],
            'path_widths': {
                name: profile['max_lambda']
                for name, profile in out[pos]['path_profiles'].items()
            },
            'recursive_widths': {
                name: data['certificate']['width']
                for name, data in out[pos]['recursive_candidates'].items()
            },
            'best_recursive_order': out[pos]['best_recursive_order'],
            'best_recursive_width': out[pos]['best_recursive_width'],
            'best_recursive_depth': out[pos]['best_recursive_depth'],
            'best_recursive_root_children': out[pos]['best_recursive_root_children'],
        }
        for pos in 'BC'
    }, sort_keys=True))
    print('PASS V26_Q138_BC_E0_AGGREGATE_SIGNATURE_SEPARATOR')
    print('scope=exact same-support XOR-aggregated support/frequency dependence of the canonical grouped-e0 sign-span construction on the 149 shared coordinates')
    print('scalar_gauge=the full corrected phase projection is verified sector-by-sector; omitted right-only scalar only complements the whole left truth vector and is absorbed by the explicit ALL generator in the local sign span')
    print('claim=reported ranks/lambdas/tree widths are exact for this canonical grouped-e0 sign-span target and the displayed deterministic decompositions; no optimal branchwidth claim')
    print('not_included=exact grouped-e0 integer coefficients beyond admitted sign-span target, e0-half cross-carry, complete B2/C2, W_repr, alpha, arithmetic-work, ranking/search, full-round')


if __name__ == '__main__':
    main()
