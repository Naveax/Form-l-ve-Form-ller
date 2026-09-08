#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_same_support_integer_coefficients as C

POS = 'C'
MATCHINGS4 = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def gf2_rank(rows):
    basis = {}
    for x in rows:
        y = int(x)
        while y:
            p = y.bit_length() - 1
            if p not in basis:
                basis[p] = y
                break
            y ^= basis[p]
    return len(basis)


def difference_data(sig_a, sig_b, d):
    diff = sig_a ^ sig_b
    nonconstant = diff >> 1
    assert nonconstant != 0

    linear = (diff >> 1) & ((1 << d) - 1)
    rows = [0] * d
    bit = 1 + d
    for i in range(d):
        for j in range(i + 1, d):
            if (diff >> bit) & 1:
                rows[i] |= 1 << j
                rows[j] |= 1 << i
            bit += 1
    assert bit == 1 + d + d * (d - 1) // 2
    rank = gf2_rank(rows)
    assert rank % 2 == 0
    return {
        'difference_constant_bit': diff & 1,
        'difference_linear_weight': linear.bit_count(),
        'difference_polar_rank': rank,
        'difference_is_affine_nonconstant': rank == 0,
    }


def verify_pair_identity():
    for qi, qj in product((0, 1), repeat=2):
        ai = -1 if qi else 1
        aj = -1 if qj else 1
        lhs_num = ai + aj
        assert lhs_num % 2 == 0
        lhs = lhs_num // 2
        rhs = ai if (qi ^ qj) == 0 else 0
        assert lhs == rhs


def analyze():
    verify_pair_identity()

    e0, _e1, _half = C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for k in range(4):
        for zs, cls in e0[k]:
            can = C.P.U.H.support_for(POS, zs, cls)
            if can is None:
                continue
            raw += 1
            grouped[can].append((zs, cls))

    assert raw == 577
    assert len(grouped) == 250
    mult_hist = Counter(len(v) for v in grouped.values())
    assert dict(sorted(mult_hist.items())) == {1: 103, 2: 57, 4: 90}

    selected_rank_hist = Counter()
    selected_affine = 0
    selected_quadratic = 0
    selected_pair_count = 0
    matching_choice_hist = Counter()
    mult2_rank_hist = Counter()
    mult4_selected_rank_hist = Counter()
    mult4_selected_max_rank_hist = Counter()
    mult4_all_candidate_rank_hist = Counter()
    multi_support_free_dim_hist = Counter()
    compact_groups = []

    for gid, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        m = len(sectors)
        if m == 1:
            continue

        _srank, x0, basis = C.X.support_param(can)
        d = len(basis)
        multi_support_free_dim_hist[d] += 1
        expected_bits = 1 + d + d * (d - 1) // 2

        sigs = []
        for zs, _cls in sectors:
            sig, sd, nbits = C.X.restricted_phase_signature(C.phase_tuple(zs), x0, basis)
            assert sd == d
            assert nbits == expected_bits
            sigs.append(sig)
        assert len(set(s >> 1 for s in sigs)) == m

        def pair_record(i, j):
            rec = difference_data(sigs[i], sigs[j], d)
            rec['pair'] = [i, j]
            return rec

        if m == 2:
            chosen = [pair_record(0, 1)]
            matching_index = 0
            mult2_rank_hist[chosen[0]['difference_polar_rank']] += 1
        else:
            assert m == 4
            options = []
            for mi, matching in enumerate(MATCHINGS4):
                recs = [pair_record(i, j) for i, j in matching]
                ranks = [r['difference_polar_rank'] for r in recs]
                for r in ranks:
                    mult4_all_candidate_rank_hist[r] += 1
                key = (
                    max(ranks),
                    sum(ranks),
                    tuple(sorted(ranks)),
                    mi,
                )
                options.append((key, mi, recs))
            _key, matching_index, chosen = min(options, key=lambda x: x[0])
            matching_choice_hist[matching_index] += 1
            ranks = [r['difference_polar_rank'] for r in chosen]
            mult4_selected_max_rank_hist[max(ranks)] += 1
            for r in ranks:
                mult4_selected_rank_hist[r] += 1

        for rec in chosen:
            r = rec['difference_polar_rank']
            selected_rank_hist[r] += 1
            selected_pair_count += 1
            if rec['difference_is_affine_nonconstant']:
                selected_affine += 1
            else:
                selected_quadratic += 1

        compact_groups.append({
            'group_id': gid,
            'multiplicity': m,
            'support_free_dimension': d,
            'matching_index': matching_index,
            'selected_pairs': chosen,
            'selected_max_difference_polar_rank': max(
                r['difference_polar_rank'] for r in chosen
            ),
        })

    assert len(compact_groups) == 147
    assert selected_pair_count == 57 + 2 * 90 == 237
    assert selected_affine + selected_quadratic == selected_pair_count

    out = {
        'position': POS,
        'raw_e0_sectors': raw,
        'support_groups': len(grouped),
        'support_multiplicity_histogram': dict(sorted(mult_hist.items())),
        'even_multiplicity_support_groups': len(compact_groups),
        'first_dyadic_pair_residual_terms': selected_pair_count,
        'multi_support_free_dimension_histogram': dict(sorted(multi_support_free_dim_hist.items())),
        'selected_difference_polar_rank_histogram': dict(sorted(selected_rank_hist.items())),
        'selected_affine_nonconstant_difference_pairs': selected_affine,
        'selected_genuinely_quadratic_difference_pairs': selected_quadratic,
        'multiplicity2_difference_polar_rank_histogram': dict(sorted(mult2_rank_hist.items())),
        'multiplicity4_matching_choice_histogram': dict(sorted(matching_choice_hist.items())),
        'multiplicity4_selected_difference_polar_rank_histogram': dict(sorted(mult4_selected_rank_hist.items())),
        'multiplicity4_selected_max_difference_polar_rank_histogram': dict(sorted(mult4_selected_max_rank_hist.items())),
        'multiplicity4_all_matching_candidate_polar_rank_histogram': dict(sorted(mult4_all_candidate_rank_hist.items())),
        'max_selected_difference_polar_rank': max(selected_rank_hist) if selected_rank_hist else 0,
        'groups': compact_groups,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PAIR_RESIDUAL')
    print('identity=(((-1)^qi)+((-1)^qj))/2 = ((-1)^qi) * 1[qi xor qj = 0] pointwise on the common affine support')
    print('scope=exact first-dyadic representation for all 147 even-multiplicity C e0 support groups by pair decomposition; multiplicity-4 groups choose the perfect matching minimizing selected difference-polar rank lexicographically')
    print('important=pairing changes representation complexity but not the exact residual value; this probe measures quadratic equality-condition structure only, not separator message count')
    print('next=lift selected pair residual terms onto the 149-bit separator domain and measure cut-local evaluation state without collapsing the signed phases back to XOR aggregate polynomials')
    print('not_included=separator cost of quadratic equality supports, singleton signed-unit 2-adic lift, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
