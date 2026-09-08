#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_same_support_integer_coefficients as C
import probe_v26_q138_c916_e0_first_dyadic_pair_residual as D

POS = 'C'
NEXT = 160
SHARED_EXT = tuple(range(128)) + tuple(C.P.U.F.REXT)
LOCAL_EXT = tuple(C.P.U.F.LEXT)
SHARED_MASK = sum(1 << i for i in SHARED_EXT)
LOCAL_MASK = sum(1 << i for i in LOCAL_EXT)
assert len(SHARED_EXT) == 149 and len(LOCAL_EXT) == 11
assert (SHARED_MASK & LOCAL_MASK) == 0
assert (SHARED_MASK | LOCAL_MASK) == (1 << NEXT) - 1


def signature_form(sig, d):
    linear = (sig >> 1) & ((1 << d) - 1)
    rows = [0] * d
    bit = 1 + d
    for i in range(d):
        for j in range(i + 1, d):
            if (sig >> bit) & 1:
                rows[i] |= 1 << j
                rows[j] |= 1 << i
            bit += 1
    assert bit == 1 + d + d * (d - 1) // 2
    return linear, rows


def polar_apply(rows, x):
    z = 0
    y = x
    while y:
        b = y & -y
        z ^= rows[b.bit_length() - 1]
        y ^= b
    return z


def local_fiber_coeff_basis(support_basis):
    d = len(support_basis)
    eqs = []
    for ext in SHARED_EXT:
        row = 0
        for i, b in enumerate(support_basis):
            if (b >> ext) & 1:
                row |= 1 << i
        eqs.append((row, 0))
    sol = C.P.U.T.rref(eqs, n=d)
    assert sol is not None
    projection_rank, x0, kernel = sol
    assert x0 == 0
    assert projection_rank + len(kernel) == d

    for coeff in kernel:
        full = 0
        y = coeff
        while y:
            bit = y & -y
            full ^= support_basis[bit.bit_length() - 1]
            y ^= bit
        assert (full & SHARED_MASK) == 0
        assert (full & ~LOCAL_MASK) == 0
    return projection_rank, tuple(kernel)


def form_geometry(sig, d, local_coeffs):
    linear, rows = signature_form(sig, d)
    total_rank = D.gf2_rank(rows)
    assert total_rank % 2 == 0

    local_to_all = [polar_apply(rows, x) for x in local_coeffs]
    local_to_all_rank = D.gf2_rank(local_to_all)

    local_local_rows = []
    for x in local_coeffs:
        px = polar_apply(rows, x)
        row = 0
        for j, y in enumerate(local_coeffs):
            if (px & y).bit_count() & 1:
                row |= 1 << j
        local_local_rows.append(row)
    local_local_rank = D.gf2_rank(local_local_rows)
    assert local_local_rank % 2 == 0
    assert local_local_rank <= local_to_all_rank <= total_rank

    local_linear_rank = int(any((linear & x).bit_count() & 1 for x in local_coeffs))

    if local_local_rank:
        category = 'local_quadratic'
    elif local_to_all_rank:
        category = 'shared_local_bilinear'
    elif local_linear_rank:
        category = 'local_affine_only'
    else:
        category = 'descends_to_shared_quotient'

    return {
        'polar_rank': total_rank,
        'local_to_all_polar_rank': local_to_all_rank,
        'local_local_polar_rank': local_local_rank,
        'local_linear_rank': local_linear_rank,
        'category': category,
    }


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
            if can is not None:
                raw += 1
                grouped[can].append((zs, cls))
    assert raw == 577 and len(grouped) == 250

    projection_by_mult = defaultdict(Counter)
    fiber_dim_by_mult = defaultdict(Counter)
    singleton_polar_hist = Counter()
    singleton_local_to_all_hist = Counter()
    singleton_local_local_hist = Counter()
    singleton_local_linear_hist = Counter()
    singleton_category_hist = Counter()
    pair_local_to_all_hist = Counter()
    pair_local_local_hist = Counter()
    pair_local_linear_hist = Counter()
    pair_category_hist = Counter()
    pair_category_by_mult = defaultdict(Counter)
    compact = []
    singleton_count = pair_count = 0

    for gid, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        m = len(sectors)
        _srank, x0, support_basis = C.X.support_param(can)
        d = len(support_basis)
        projection_rank, local_coeffs = local_fiber_coeff_basis(support_basis)
        local_dim = len(local_coeffs)
        projection_by_mult[m][projection_rank] += 1
        fiber_dim_by_mult[m][local_dim] += 1

        sigs = []
        for zs, _cls in sectors:
            sig, sd, _nbits = C.X.restricted_phase_signature(C.phase_tuple(zs), x0, support_basis)
            assert sd == d
            sigs.append(sig)

        if m == 1:
            rec = form_geometry(sigs[0], d, local_coeffs)
            assert rec['polar_rank'] in (142, 144)
            singleton_count += 1
            singleton_polar_hist[rec['polar_rank']] += 1
            singleton_local_to_all_hist[rec['local_to_all_polar_rank']] += 1
            singleton_local_local_hist[rec['local_local_polar_rank']] += 1
            singleton_local_linear_hist[rec['local_linear_rank']] += 1
            singleton_category_hist[rec['category']] += 1
            compact.append({
                'group_id': gid, 'multiplicity': 1, 'support_free_dimension': d,
                'shared_projection_rank': projection_rank, 'local_fiber_dimension': local_dim,
                'singleton': rec,
            })
            continue

        pg = pair_groups[gid]
        assert pg['multiplicity'] == m
        records = []
        cat = Counter()
        for selected in pg['selected_pairs']:
            i, j = selected['pair']
            rec = form_geometry(sigs[i] ^ sigs[j], d, local_coeffs)
            assert rec['polar_rank'] == selected['difference_polar_rank'] == 2
            rec['pair'] = [i, j]
            records.append(rec)
            pair_count += 1
            pair_local_to_all_hist[rec['local_to_all_polar_rank']] += 1
            pair_local_local_hist[rec['local_local_polar_rank']] += 1
            pair_local_linear_hist[rec['local_linear_rank']] += 1
            pair_category_hist[rec['category']] += 1
            pair_category_by_mult[m][rec['category']] += 1
            cat[rec['category']] += 1
        compact.append({
            'group_id': gid, 'multiplicity': m, 'support_free_dimension': d,
            'shared_projection_rank': projection_rank, 'local_fiber_dimension': local_dim,
            'pair_category_histogram': dict(sorted(cat.items())), 'pairs': records,
        })

    assert singleton_count == 103
    assert pair_count == 237
    assert singleton_polar_hist == Counter({142: 74, 144: 29})
    assert sum(singleton_category_hist.values()) == 103
    assert sum(pair_category_hist.values()) == 237
    assert len(compact) == 250

    out = {
        'position': POS,
        'support_groups': len(compact),
        'singleton_terms': singleton_count,
        'pair_terms': pair_count,
        'total_first_dyadic_terms': singleton_count + pair_count,
        'shared_projection_rank_histogram_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(projection_by_mult.items())
        },
        'local_fiber_dimension_histogram_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(fiber_dim_by_mult.items())
        },
        'singleton_polar_rank_histogram': dict(sorted(singleton_polar_hist.items())),
        'singleton_local_to_all_polar_rank_histogram': dict(sorted(singleton_local_to_all_hist.items())),
        'singleton_local_local_polar_rank_histogram': dict(sorted(singleton_local_local_hist.items())),
        'singleton_local_linear_rank_histogram': dict(sorted(singleton_local_linear_hist.items())),
        'singleton_fiber_category_histogram': dict(sorted(singleton_category_hist.items())),
        'pair_local_to_all_polar_rank_histogram': dict(sorted(pair_local_to_all_hist.items())),
        'pair_local_local_polar_rank_histogram': dict(sorted(pair_local_local_hist.items())),
        'pair_local_linear_rank_histogram': dict(sorted(pair_local_linear_hist.items())),
        'pair_fiber_category_histogram': dict(sorted(pair_category_hist.items())),
        'pair_fiber_category_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(pair_category_by_mult.items())
        },
        'singleton_descends_to_shared_quotient': singleton_category_hist['descends_to_shared_quotient'],
        'pair_descends_to_shared_quotient': pair_category_hist['descends_to_shared_quotient'],
        'groups': compact,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_COMPLETE_FIRST_DYADIC_FIBER_GEOMETRY')
    print('scope=coordinate-free shared/local fiber classification for all 103 singleton and 237 selected pair terms in the complete first dyadic C e0 residual')
    print('important=classifies exact dependence on the local-fiber kernel of the common support projection; still not a separator message-count theorem')
    print('next=build separate exact evaluation-state representations for the singleton and pair regimes using the measured fiber categories')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
