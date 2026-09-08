#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_same_support_integer_coefficients as C
import probe_v26_q138_c916_e0_first_dyadic_pair_residual as D

POS = 'C'


def polar_rank_from_signature(sig, d):
    rows = [0] * d
    bit = 1 + d
    for i in range(d):
        for j in range(i + 1, d):
            if (sig >> bit) & 1:
                rows[i] |= 1 << j
                rows[j] |= 1 << i
            bit += 1
    assert bit == 1 + d + d * (d - 1) // 2
    rank = D.gf2_rank(rows)
    assert rank % 2 == 0
    return rank


def verify_residual_identity(m, pairs):
    assert m in (1, 2, 4)
    for q in product((0, 1), repeat=m):
        signs = [(-1 if x else 1) for x in q]
        total = sum(signs)
        epsilon = m & 1
        assert (total - epsilon) % 2 == 0
        lhs = (total - epsilon) // 2

        if m == 1:
            rhs = -q[0]
        else:
            used = sorted(i for pair in pairs for i in pair)
            assert used == list(range(m))
            rhs = 0
            for i, j in pairs:
                rhs += signs[i] if (q[i] ^ q[j]) == 0 else 0
        assert lhs == rhs


def analyze():
    pair_out = D.analyze()
    pair_groups = {g['group_id']: g for g in pair_out['groups']}
    assert len(pair_groups) == 147

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

    assert raw == 577 and len(grouped) == 250
    mult_hist = Counter(len(v) for v in grouped.values())
    assert dict(sorted(mult_hist.items())) == {1: 103, 2: 57, 4: 90}

    singleton_phase_polar_rank_hist = Counter()
    singleton_support_free_dim_hist = Counter()
    residual_terms_by_multiplicity = Counter()
    group_residual_term_hist = Counter()
    compact = []

    for gid, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        m = len(sectors)
        _srank, x0, basis = C.X.support_param(can)
        d = len(basis)

        if m == 1:
            verify_residual_identity(1, ())
            zs, _cls = sectors[0]
            sig, sd, nbits = C.X.restricted_phase_signature(C.phase_tuple(zs), x0, basis)
            assert sd == d
            assert nbits == 1 + d + d * (d - 1) // 2
            pr = polar_rank_from_signature(sig, d)
            singleton_phase_polar_rank_hist[pr] += 1
            singleton_support_free_dim_hist[d] += 1
            terms = 1
            rec = {
                'group_id': gid,
                'multiplicity': 1,
                'support_free_dimension': d,
                'residual_terms': 1,
                'residual_kind': 'singleton_minus_phase_bit',
                'singleton_phase_polar_rank': pr,
            }
        else:
            pg = pair_groups[gid]
            assert pg['multiplicity'] == m
            pairs = tuple(tuple(r['pair']) for r in pg['selected_pairs'])
            verify_residual_identity(m, pairs)
            terms = len(pairs)
            assert terms == m // 2
            rec = {
                'group_id': gid,
                'multiplicity': m,
                'support_free_dimension': d,
                'residual_terms': terms,
                'residual_kind': 'paired_signed_equality',
                'matching_index': pg['matching_index'],
                'selected_max_difference_polar_rank': pg['selected_max_difference_polar_rank'],
            }

        residual_terms_by_multiplicity[m] += terms
        group_residual_term_hist[terms] += 1
        compact.append(rec)

    total_terms = sum(residual_terms_by_multiplicity.values())
    assert residual_terms_by_multiplicity == Counter({4: 180, 1: 103, 2: 57})
    assert total_terms == 340
    assert len(compact) == 250

    out = {
        'position': POS,
        'raw_e0_sectors': raw,
        'support_groups': len(grouped),
        'support_multiplicity_histogram': dict(sorted(mult_hist.items())),
        'first_dyadic_group_residual_formula': '(sum_i (-1)^q_i - (m mod 2))/2',
        'residual_terms_by_multiplicity': dict(sorted(residual_terms_by_multiplicity.items())),
        'group_residual_term_count_histogram': dict(sorted(group_residual_term_hist.items())),
        'total_first_dyadic_residual_terms': total_terms,
        'singleton_phase_polar_rank_histogram': dict(sorted(singleton_phase_polar_rank_hist.items())),
        'singleton_support_free_dimension_histogram': dict(sorted(singleton_support_free_dim_hist.items())),
        'pair_selected_difference_polar_rank_histogram': pair_out['selected_difference_polar_rank_histogram'],
        'pair_max_selected_difference_polar_rank': pair_out['max_selected_difference_polar_rank'],
        'pair_affine_nonconstant_difference_terms': pair_out['selected_affine_nonconstant_difference_pairs'],
        'pair_genuinely_quadratic_difference_terms': pair_out['selected_genuinely_quadratic_difference_pairs'],
        'groups': compact,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_COMPLETE_FIRST_DYADIC_GROUP_RESIDUAL')
    print('exact=for every C e0 support group, the signed sector sum is decomposed as parity support plus twice an integer residual; singleton groups contribute -q and even groups use exact paired signed-equality terms')
    print('term_count=103 singleton terms + 57 multiplicity2 pair terms + 180 multiplicity4 pair terms = 340')
    print('important=this is an exact within-support arithmetic representation, not a separator-state or contraction-width certificate')
    print('next=express the 340 residual terms through the existing support/frequency local coordinates and measure cut-local message complexity without replacing them by XOR aggregate scalars')
    print('not_included=separator cost, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
