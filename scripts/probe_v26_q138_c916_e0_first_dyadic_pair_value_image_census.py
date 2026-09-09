#!/usr/bin/env python3
import io
import json
import sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_transformed_pair_compatibility as P
import probe_v26_q138_c916_e0_local_gauss_transform_quotient_geometry as L

POS = P.POS
PHYS_N = len(P.G.SHARED_EXT)
assert PHYS_N == 149

EXPECTED_RELATION_HIST = {
    'disjoint': 28,
    'equal': 6,
    'left_subset_right': 4,
    'overlap_incomparable': 112,
    'right_subset_left': 87,
}
EXPECTED_AMPLITUDE_DELTA_HIST = {0: 132, 1: 105}
EXPECTED_DIFFERENCE_TYPE_HIST = {
    'affine_nonconstant': 201,
    'constant': 2,
    'quadratic_nonconstant': 6,
}
EXPECTED_DIFFERENCE_RANK_HIST = {0: 203, 2: 6}


def signed_quadratic_moment(c, lin, rows, x0, basis):
    """Exact sum of (-1)^q over one affine parameterization."""
    rc, rlin, rrows = L.restrict_form(c, lin, rows, x0, basis)
    d = len(basis)
    got = L.partial_gauss_eliminate(rc, rlin, rrows, 0, d)
    if got['identically_zero']:
        return 0
    assert got['support_control_rank'] == 0
    assert got['support_free_dimension'] == 0
    assert got['normalized_sign_linear'] == 0
    assert tuple(got['normalized_sign_rows']) == ()
    sign = -1 if got['normalized_sign_constant'] else 1
    return sign * (1 << got['log2_abs_nonzero_gauss'])


def add_signed_cells(counts, n, moment, positive_value, negative_value):
    assert n >= 0
    assert -n <= moment <= n
    assert (n + moment) % 2 == 0
    pos = (n + moment) // 2
    neg = (n - moment) // 2
    assert pos >= 0 and neg >= 0 and pos + neg == n
    if pos:
        counts[positive_value] += pos
    if neg:
        counts[negative_value] += neg


def pair_value_census(left, right, p, domain_dim):
    """Exact value->multiplicity census for H=(G_left+G_right)/2."""
    assert domain_dim >= p
    e1 = left['log2_abs_nonzero_gauss']
    e2 = right['log2_abs_nonzero_gauss']
    assert e1 is not None and e2 is not None
    assert e1 >= 1 and e2 >= 1

    relation, inter = P.support_relation(left, right, p)
    nl = 1 << len(left['support_basis'])
    nr = 1 << len(right['support_basis'])

    lm = signed_quadratic_moment(
        left['shared_survivor_constant'],
        left['shared_survivor_linear'],
        left['shared_survivor_rows'],
        left['support_x0'],
        left['support_basis'],
    )
    rm = signed_quadratic_moment(
        right['shared_survivor_constant'],
        right['shared_survivor_linear'],
        right['shared_survivor_rows'],
        right['support_x0'],
        right['support_basis'],
    )

    if inter is None:
        ni = 0
        la = rb = dc = 0
        ibasis = ()
    else:
        _irank, ix0, ibasis = inter
        ni = 1 << len(ibasis)
        la = signed_quadratic_moment(
            left['shared_survivor_constant'],
            left['shared_survivor_linear'],
            left['shared_survivor_rows'],
            ix0,
            ibasis,
        )
        rb = signed_quadratic_moment(
            right['shared_survivor_constant'],
            right['shared_survivor_linear'],
            right['shared_survivor_rows'],
            ix0,
            ibasis,
        )
        dc = signed_quadratic_moment(
            left['shared_survivor_constant'] ^ right['shared_survivor_constant'],
            left['shared_survivor_linear'] ^ right['shared_survivor_linear'],
            tuple(a ^ b for a, b in zip(
                left['shared_survivor_rows'],
                right['shared_survivor_rows'],
            )),
            ix0,
            ibasis,
        )

    domain = 1 << domain_dim
    outside = domain - nl - nr + ni
    left_only = nl - ni
    right_only = nr - ni
    assert min(outside, left_only, right_only) >= 0

    counts = Counter()
    if outside:
        counts[0] += outside

    a1 = 1 << e1
    a2 = 1 << e2
    h1 = a1 >> 1
    h2 = a2 >> 1

    add_signed_cells(counts, left_only, lm - la, h1, -h1)
    add_signed_cells(counts, right_only, rm - rb, h2, -h2)

    if ni:
        numerators = {
            (+1, +1): ni + la + rb + dc,
            (+1, -1): ni + la - rb - dc,
            (-1, +1): ni - la + rb - dc,
            (-1, -1): ni - la - rb + dc,
        }
        for (sl, sr), num in numerators.items():
            assert num % 4 == 0
            cell = num // 4
            assert cell >= 0
            if not cell:
                continue
            value_num = sl * a1 + sr * a2
            assert value_num % 2 == 0
            counts[value_num // 2] += cell

    counts = Counter({int(v): int(n) for v, n in counts.items() if n})
    assert sum(counts.values()) == domain
    assert all(n > 0 for n in counts.values())

    values = tuple(sorted(counts))
    nonzero = tuple(v for v in values if v)
    image_size = len(values)
    state_bits = (image_size - 1).bit_length()

    if nonzero:
        min_v2 = min(P.v2_nonzero(v) for v in nonzero)
        normalized = tuple(sorted(v >> min_v2 for v in values))
    else:
        min_v2 = None
        normalized = (0,)

    return {
        'support_relation': relation,
        'left_support_size': nl,
        'right_support_size': nr,
        'intersection_size': ni,
        'outside_union_size': outside,
        'left_total_sign_moment': lm,
        'right_total_sign_moment': rm,
        'intersection_left_sign_moment': la,
        'intersection_right_sign_moment': rb,
        'intersection_difference_sign_moment': dc,
        'image_size': image_size,
        'state_bits': state_bits,
        'nonzero_value_count': len(nonzero),
        'minimum_nonzero_valuation': min_v2,
        'normalized_alphabet': list(normalized),
        'alphabet_sign_symmetric': all(-v in counts for v in counts),
        'multiplicity_sign_symmetric': all(counts[v] == counts.get(-v, 0) for v in counts),
        'value_multiplicity': [
            {'value': v, 'multiplicity': counts[v]}
            for v in values
        ],
    }


def synthetic_census_regression():
    p = 4
    systems = (
        (),
        ((1, 0),),
        ((1, 1),),
        ((2, 0),),
        ((1, 0), (2, 1)),
        ((3, 0),),
    )
    zero = (0, 0, 0, 0)
    quad01 = (2, 1, 0, 0)
    forms = (
        (0, 0, zero),
        (1, 0, zero),
        (0, 1, zero),
        (0, 0, quad01),
    )

    tested = 0
    for lc in systems:
        for rc in systems:
            for e1 in (2, 3):
                for e2 in (2, 3):
                    for f1 in forms:
                        for f2 in forms:
                            left = P.make_synthetic_transform(lc, p, e1, *f1)
                            right = P.make_synthetic_transform(rc, p, e2, *f2)
                            got = pair_value_census(left, right, p, p)

                            brute = Counter()
                            for s in range(1 << p):
                                num = P.eval_transform(left, s) + P.eval_transform(right, s)
                                assert num % 2 == 0
                                brute[num // 2] += 1
                            exact = {
                                rec['value']: rec['multiplicity']
                                for rec in got['value_multiplicity']
                            }
                            assert exact == dict(sorted(brute.items()))
                            tested += 1

    assert tested == 2304
    return tested


def analyze():
    regression_cases = synthetic_census_regression()

    with redirect_stdout(io.StringIO()):
        pair_authority = P.R.analyze()
    assert pair_authority['first_dyadic_pair_residual_terms'] == 237
    pair_groups = {g['group_id']: g for g in pair_authority['groups']}
    assert len(pair_groups) == 147

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

    relation_hist = Counter()
    amplitude_delta_hist = Counter()
    difference_type_hist = Counter()
    difference_rank_hist = Counter()

    image_size_hist = Counter()
    state_bits_hist = Counter()
    nonzero_count_hist = Counter()
    min_v2_hist = Counter()
    normalized_alphabet_hist = Counter()
    alphabet_symmetry_hist = Counter()
    multiplicity_symmetry_hist = Counter()

    by_mult_image = defaultdict(Counter)
    by_mult_state = defaultdict(Counter)
    by_relation_image = defaultdict(Counter)
    by_delta_image = defaultdict(Counter)

    group_records = []
    total_pairs = 0

    for gid, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        m = len(sectors)
        if m == 1:
            continue

        authority = pair_groups[gid]
        assert authority['multiplicity'] == m
        projection_rank, transforms = P.group_transforms(can, sectors)
        assert len(transforms) == m

        records = []
        for pair_slot, selected in enumerate(authority['selected_pairs']):
            i, j = selected['pair']
            left, right = transforms[i], transforms[j]

            cls = P.classify_pair(left, right, projection_rank)
            census = pair_value_census(left, right, projection_rank, PHYS_N)
            assert census['support_relation'] == cls['support_relation']
            assert census['minimum_nonzero_valuation'] == cls['first_dyadic_min_nonzero_valuation']

            rec = {
                'pair_slot': pair_slot,
                'pair': [i, j],
                'projection_rank': projection_rank,
                'amplitude_delta': cls['amplitude_delta'],
                'sign_difference_type': cls['sign_difference_type'],
                'sign_difference_polar_rank': cls['sign_difference_polar_rank'],
                'global_pair_class': cls['global_pair_class'],
                **census,
            }
            records.append(rec)
            total_pairs += 1

            relation_hist[cls['support_relation']] += 1
            amplitude_delta_hist[cls['amplitude_delta']] += 1
            if cls['sign_difference_type'] is not None:
                difference_type_hist[cls['sign_difference_type']] += 1
                difference_rank_hist[cls['sign_difference_polar_rank']] += 1

            image_size_hist[census['image_size']] += 1
            state_bits_hist[census['state_bits']] += 1
            nonzero_count_hist[census['nonzero_value_count']] += 1
            if census['minimum_nonzero_valuation'] is not None:
                min_v2_hist[census['minimum_nonzero_valuation']] += 1
            normalized_alphabet_hist[tuple(census['normalized_alphabet'])] += 1
            alphabet_symmetry_hist[census['alphabet_sign_symmetric']] += 1
            multiplicity_symmetry_hist[census['multiplicity_sign_symmetric']] += 1

            by_mult_image[m][census['image_size']] += 1
            by_mult_state[m][census['state_bits']] += 1
            by_relation_image[cls['support_relation']][census['image_size']] += 1
            by_delta_image[cls['amplitude_delta']][census['image_size']] += 1

        group_records.append({
            'group_id': gid,
            'multiplicity': m,
            'shared_projection_rank': projection_rank,
            'matching_index': authority['matching_index'],
            'pairs': records,
        })

    assert total_pairs == 237
    assert len(group_records) == 147
    assert dict(sorted(relation_hist.items())) == EXPECTED_RELATION_HIST
    assert dict(sorted(amplitude_delta_hist.items())) == EXPECTED_AMPLITUDE_DELTA_HIST
    assert dict(sorted(difference_type_hist.items())) == EXPECTED_DIFFERENCE_TYPE_HIST
    assert dict(sorted(difference_rank_hist.items())) == EXPECTED_DIFFERENCE_RANK_HIST

    # A frozen pair combines two signed powers of two. With the authority's
    # amplitude delta in {0,1}, its full-domain value alphabet can never exceed
    # seven values; the exact census below determines which of them are realized.
    assert max(image_size_hist) <= 7
    assert max(state_bits_hist) <= 3

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'synthetic_census_regression_cases': regression_cases,
        'raw_e0_sectors': raw,
        'support_groups': len(grouped),
        'group_multiplicity_histogram': {1: 103, 2: 57, 4: 90},
        'even_multiplicity_support_groups': len(group_records),
        'frozen_transformed_pairs': total_pairs,
        'reproduced_support_relation_histogram': dict(sorted(relation_hist.items())),
        'reproduced_amplitude_delta_histogram': dict(sorted(amplitude_delta_hist.items())),
        'reproduced_sign_difference_type_histogram': dict(sorted(difference_type_hist.items())),
        'reproduced_sign_difference_polar_rank_histogram': dict(sorted(difference_rank_hist.items())),
        'pair_value_image_size_histogram': dict(sorted(image_size_hist.items())),
        'pair_value_state_bits_histogram': dict(sorted(state_bits_hist.items())),
        'pair_nonzero_value_count_histogram': dict(sorted(nonzero_count_hist.items())),
        'pair_minimum_nonzero_valuation_histogram': dict(sorted(min_v2_hist.items())),
        'pair_normalized_alphabet_histogram': {
            str(list(k)): v for k, v in sorted(normalized_alphabet_hist.items())
        },
        'pair_alphabet_sign_symmetry_histogram': {
            str(k).lower(): v for k, v in sorted(alphabet_symmetry_hist.items())
        },
        'pair_multiplicity_sign_symmetry_histogram': {
            str(k).lower(): v for k, v in sorted(multiplicity_symmetry_hist.items())
        },
        'image_size_by_group_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(by_mult_image.items())
        },
        'state_bits_by_group_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(by_mult_state.items())
        },
        'image_size_by_support_relation': {
            relation: dict(sorted(h.items()))
            for relation, h in sorted(by_relation_image.items())
        },
        'image_size_by_amplitude_delta': {
            int(delta): dict(sorted(h.items()))
            for delta, h in sorted(by_delta_image.items())
        },
        'maximum_pair_image_size': max(image_size_hist),
        'maximum_pair_state_bits': max(state_bits_hist),
        'groups': group_records,
        'decision': 'FROZEN_PAIR_EXACT_NONLINEAR_VALUE_IMAGE_CENSUS_COMPLETE',
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PAIR_VALUE_IMAGE_CENSUS')
    print('identity=for every one of the 237 frozen transformed pairs, compute the exact H=(G_i+G_j)/2 value multiplicities over the full 149-bit physical shared domain from affine support sizes and four quadratic Walsh moments')
    print('method=no 2^149 enumeration: support-only sign counts come from exact quadratic Gauss moments, and overlap joint signs come from the Walsh inverse of N,A,B,C')
    print('important=pair-local image/state bits are not a global separator width; they measure only each frozen pair function independently')
    print('next=freeze this census, then compute exact grouped arithmetic images: 103 singleton functions, 57 multiplicity-2 groups, and the joint H1+H2 image for 90 multiplicity-4 groups')
    print('not_included=joint state across all groups, complete grouped-e0 separator, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
