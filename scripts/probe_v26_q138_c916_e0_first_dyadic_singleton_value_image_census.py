#!/usr/bin/env python3
import io
import json
import sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_complete_first_dyadic_group_residual as A
import probe_v26_q138_c916_e0_first_dyadic_pair_value_image_census as V
import probe_v26_q138_c916_e0_first_dyadic_transformed_pair_compatibility as P
import probe_v26_q138_c916_e0_local_gauss_transform_quotient_geometry as L

POS = P.POS
PHYS_N = len(P.G.SHARED_EXT)
assert PHYS_N == 149


def singleton_residual_census(transform, projection_rank, local_dim, domain_dim):
    """Exact census for R(s)=sum_t(-q(s,t))=(G(s)-2^k)/2."""
    assert 0 <= projection_rank <= domain_dim
    assert local_dim >= 1

    domain = 1 << domain_dim
    projection_size = 1 << projection_rank
    local_size = 1 << local_dim
    baseline = -(1 << (local_dim - 1))

    counts = Counter()
    outside_projection = domain - projection_size
    if outside_projection:
        counts[0] += outside_projection

    if transform['identically_zero']:
        counts[baseline] += projection_size
        gauss_support_size = 0
        gauss_sign_moment = 0
    else:
        gauss_support_size = 1 << len(transform['support_basis'])
        assert gauss_support_size <= projection_size
        off_gauss_support = projection_size - gauss_support_size
        if off_gauss_support:
            counts[baseline] += off_gauss_support

        gauss_sign_moment = V.signed_quadratic_moment(
            transform['shared_survivor_constant'],
            transform['shared_survivor_linear'],
            transform['shared_survivor_rows'],
            transform['support_x0'],
            transform['support_basis'],
        )
        assert -gauss_support_size <= gauss_sign_moment <= gauss_support_size
        assert (gauss_support_size + gauss_sign_moment) % 2 == 0
        pos = (gauss_support_size + gauss_sign_moment) // 2
        neg = (gauss_support_size - gauss_sign_moment) // 2
        assert pos >= 0 and neg >= 0 and pos + neg == gauss_support_size

        exponent = transform['log2_abs_nonzero_gauss']
        assert exponent is not None and exponent >= 1
        amp = 1 << exponent
        assert (amp - local_size) % 2 == 0
        assert (-amp - local_size) % 2 == 0
        pos_value = (amp - local_size) // 2
        neg_value = (-amp - local_size) // 2
        if pos:
            counts[pos_value] += pos
        if neg:
            counts[neg_value] += neg

    counts = Counter({int(v): int(n) for v, n in counts.items() if n})
    assert sum(counts.values()) == domain
    assert all(n > 0 for n in counts.values())

    values = tuple(sorted(counts))
    nonzero = tuple(v for v in values if v)
    image_size = len(values)
    state_bits = (image_size - 1).bit_length()
    min_v2 = min(P.v2_nonzero(v) for v in nonzero) if nonzero else None
    normalized = (
        tuple(sorted(v >> min_v2 for v in values))
        if min_v2 is not None
        else (0,)
    )

    return {
        'projection_size': projection_size,
        'outside_projection_size': outside_projection,
        'local_fiber_size': local_size,
        'baseline_residual_value': baseline,
        'identically_zero_gauss': bool(transform['identically_zero']),
        'gauss_support_size': gauss_support_size,
        'gauss_sign_moment': gauss_sign_moment,
        'image_size': image_size,
        'state_bits': state_bits,
        'nonzero_value_count': len(nonzero),
        'minimum_nonzero_valuation': min_v2,
        'normalized_alphabet': list(normalized),
        'value_multiplicity': [
            {'value': v, 'multiplicity': counts[v]}
            for v in values
        ],
    }


def synthetic_singleton_regression(p, k):
    n = p + k
    assert n == 4
    pair_bits = n * (n - 1) // 2
    tested = 0
    for pair_mask in range(1 << pair_bits):
        rows = L.rows_from_pair_mask(n, pair_mask)
        for lin in range(1 << n):
            for c in (0, 1):
                transform = L.partial_gauss_eliminate(c, lin, rows, p, k)
                got = singleton_residual_census(transform, p, k, p)

                brute = Counter()
                for s in range(1 << p):
                    residual = 0
                    for local in range(1 << k):
                        x = s | (local << p)
                        residual -= L.q_eval(c, lin, rows, x)
                    brute[residual] += 1

                exact = {
                    rec['value']: rec['multiplicity']
                    for rec in got['value_multiplicity']
                }
                assert exact == dict(sorted(brute.items())), (
                    p, k, pair_mask, lin, c, got, brute
                )
                tested += 1
    return tested


def analyze():
    regression_cases = (
        synthetic_singleton_regression(2, 2)
        + synthetic_singleton_regression(1, 3)
    )
    assert regression_cases == 4096

    with redirect_stdout(io.StringIO()):
        authority = A.analyze()
    authority_singletons = {
        g['group_id']: g
        for g in authority['groups']
        if g['multiplicity'] == 1
    }
    assert len(authority_singletons) == 103
    assert all(
        g['residual_kind'] == 'singleton_minus_phase_bit'
        and g['residual_terms'] == 1
        for g in authority_singletons.values()
    )

    e0, _e1, _half = P.C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for zc in range(4):
        for zs, cls in e0[zc]:
            can = P.C.P.U.H.support_for(POS, zs, cls)
            if can is None:
                continue
            raw += 1
            grouped[can].append((zs, cls))
    assert raw == 577 and len(grouped) == 250
    assert dict(sorted(Counter(len(v) for v in grouped.values()).items())) == {
        1: 103, 2: 57, 4: 90,
    }

    projection_rank_hist = Counter()
    local_dim_hist = Counter()
    gauss_zero_hist = Counter()
    gauss_control_rank_hist = Counter()
    gauss_exponent_hist = Counter()
    image_size_hist = Counter()
    state_bits_hist = Counter()
    nonzero_count_hist = Counter()
    min_v2_hist = Counter()
    normalized_alphabet_hist = Counter()
    by_local_dim_image = defaultdict(Counter)
    by_projection_rank_image = defaultdict(Counter)

    records = []
    for gid, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        if len(sectors) != 1:
            continue

        assert gid in authority_singletons
        _srank, x0, support_basis = P.C.X.support_param(can)
        d = len(support_basis)
        projection_rank, kernel = P.G.local_fiber_coeff_basis(support_basis)
        local_dim = len(kernel)
        assert projection_rank + local_dim == d

        quotient = L.complement_to_kernel(kernel, d)
        assert len(quotient) == projection_rank
        adapted = quotient + tuple(kernel)
        assert P.R.gf2_rank(adapted) == d

        zs, _cls = sectors[0]
        sig, sd, _nbits = P.C.X.restricted_phase_signature(
            P.C.phase_tuple(zs), x0, support_basis
        )
        assert sd == d
        tc, tlin, trows = L.transform_signature(sig, d, adapted)
        transform = L.partial_gauss_eliminate(
            tc, tlin, trows, projection_rank, local_dim
        )

        census = singleton_residual_census(
            transform, projection_rank, local_dim, PHYS_N
        )

        projection_rank_hist[projection_rank] += 1
        local_dim_hist[local_dim] += 1
        gauss_zero_hist[bool(transform['identically_zero'])] += 1
        gauss_control_rank_hist[transform['support_control_rank']] += 1
        if not transform['identically_zero']:
            gauss_exponent_hist[transform['log2_abs_nonzero_gauss']] += 1

        image_size_hist[census['image_size']] += 1
        state_bits_hist[census['state_bits']] += 1
        nonzero_count_hist[census['nonzero_value_count']] += 1
        if census['minimum_nonzero_valuation'] is not None:
            min_v2_hist[census['minimum_nonzero_valuation']] += 1
        normalized_alphabet_hist[tuple(census['normalized_alphabet'])] += 1
        by_local_dim_image[local_dim][census['image_size']] += 1
        by_projection_rank_image[projection_rank][census['image_size']] += 1

        records.append({
            'group_id': gid,
            'multiplicity': 1,
            'support_free_dimension': d,
            'shared_projection_rank': projection_rank,
            'local_fiber_dimension': local_dim,
            'gauss_support_control_rank': transform['support_control_rank'],
            'gauss_log2_abs_nonzero': transform['log2_abs_nonzero_gauss'],
            'gauss_normalized_sign_polar_rank': transform['normalized_sign_polar_rank'],
            **census,
        })

    assert len(records) == 103
    assert sum(image_size_hist.values()) == 103
    assert max(state_bits_hist) <= 2

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'synthetic_singleton_regression_cases': regression_cases,
        'raw_e0_sectors': raw,
        'support_groups': len(grouped),
        'support_multiplicity_histogram': {1: 103, 2: 57, 4: 90},
        'singleton_groups': len(records),
        'singleton_residual_identity': 'R=(sum_t(-1)^q-2^k)/2=-sum_t q',
        'singleton_projection_rank_histogram': dict(sorted(projection_rank_hist.items())),
        'singleton_local_fiber_dimension_histogram': dict(sorted(local_dim_hist.items())),
        'singleton_identically_zero_gauss_histogram': {
            str(k).lower(): v for k, v in sorted(gauss_zero_hist.items())
        },
        'singleton_gauss_support_control_rank_histogram': dict(sorted(gauss_control_rank_hist.items())),
        'singleton_nonzero_gauss_log2_abs_histogram': dict(sorted(gauss_exponent_hist.items())),
        'singleton_residual_image_size_histogram': dict(sorted(image_size_hist.items())),
        'singleton_residual_state_bits_histogram': dict(sorted(state_bits_hist.items())),
        'singleton_residual_nonzero_value_count_histogram': dict(sorted(nonzero_count_hist.items())),
        'singleton_residual_minimum_nonzero_valuation_histogram': dict(sorted(min_v2_hist.items())),
        'singleton_residual_normalized_alphabet_histogram': {
            str(list(k)): v for k, v in sorted(normalized_alphabet_hist.items())
        },
        'residual_image_size_by_local_fiber_dimension': {
            int(k): dict(sorted(h.items()))
            for k, h in sorted(by_local_dim_image.items())
        },
        'residual_image_size_by_projection_rank': {
            int(p): dict(sorted(h.items()))
            for p, h in sorted(by_projection_rank_image.items())
        },
        'groups': records,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_SINGLETON_VALUE_IMAGE_CENSUS')
    print('identity=for a singleton support group, (-1)^q=1-2q pointwise, hence after summing the k-bit local fiber the exact first-dyadic integer residual is R(s)=(G(s)-2^k)/2=-sum_t q(s,t)')
    print('scope=exact 149-bit shared-domain value->multiplicity census for all 103 singleton C e0 first-dyadic residual groups, using the existing exact local Gauss transform')
    print('important=this closes the singleton evaluation-state regime only; it is not an all-250 joint separator-state theorem')
    print('not_included=support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
