#!/usr/bin/env python3
import io
import json
import math
import sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_even_group_value_image_census as E
import probe_v26_q138_c916_e0_first_dyadic_singleton_value_image_census as S
import probe_v26_q138_c916_e0_post_gauss_physical_phase_common as P

POS = 'C'
PHYS_N = P.PHYS_N
assert PHYS_N == 149


def census_map(record):
    return {
        int(item['value']): int(item['multiplicity'])
        for item in record['value_multiplicity']
    }


def scale_signature(counts):
    nonzero = [abs(v) for v in counts if v]
    assert nonzero
    g = 0
    for v in nonzero:
        g = math.gcd(g, v)
    assert g > 0
    direct = tuple(sorted((v // g, int(n)) for v, n in counts.items()))
    negated = tuple(sorted((-v // g, int(n)) for v, n in counts.items()))
    return min(direct, negated)


def census_norm2(counts):
    return sum(int(v) * int(v) * int(n) for v, n in counts.items())


def projection_anchor(can):
    _srank, full_x0, support_basis = P.C.X.support_param(can)
    support_basis = tuple(support_basis)
    d = len(support_basis)
    projection_rank, kernel = P.G.local_fiber_coeff_basis(support_basis)
    quotient = P.L.complement_to_kernel(kernel, d)
    assert len(quotient) == projection_rank

    shared_origin = P.compress_shared(full_x0)
    shared_qbasis = tuple(
        P.compress_shared(P.xor_combine(coeff, support_basis))
        for coeff in quotient
    )
    assert P.R.gf2_rank(shared_qbasis) == projection_rank
    constraints = P.affine_constraints_from_param(
        shared_origin, shared_qbasis, PHYS_N
    )
    assert len(constraints) == PHYS_N - projection_rank

    anchor = {
        'physical_support_x0': shared_origin,
        'physical_support_basis': shared_qbasis,
        'physical_support_constraints': constraints,
        'normalized_sign_constant': 0,
        'normalized_sign_linear': 0,
        'normalized_sign_rows': tuple(0 for _ in range(projection_rank)),
        '_coordinate_solver': P.coordinate_solver(shared_qbasis),
    }
    return projection_rank, len(kernel), anchor


def build_group_terms(gid, can, sectors, next_term_id):
    projection_rank, local_dim, proj_anchor = projection_anchor(can)
    p2, transforms = P.physical_group_transforms(can, sectors)
    assert p2 == projection_rank
    assert len(transforms) == len(sectors)

    terms = []
    tid = next_term_id
    for transform in transforms:
        exponent = transform['log2_abs_nonzero_gauss']
        assert exponent is not None and exponent >= 1
        terms.append({
            'term_id': tid,
            'group_id': gid,
            'kind': 'gauss_sector',
            'coefficient': 1 << (exponent - 1),
            'anchor': transform,
        })
        tid += 1

    if len(sectors) == 1:
        assert local_dim >= 1
        terms.append({
            'term_id': tid,
            'group_id': gid,
            'kind': 'singleton_projection_baseline',
            'coefficient': -(1 << (local_dim - 1)),
            'anchor': proj_anchor,
        })
        tid += 1

    return {
        'group_id': gid,
        'multiplicity': len(sectors),
        'projection_rank': projection_rank,
        'local_fiber_dimension': local_dim,
        'projection_anchor': proj_anchor,
        'terms': tuple(terms),
    }, tid


def full_quadratic_moment(c, lin, rows):
    rows = tuple(int(x) for x in rows)
    d = len(rows)
    got = P.L.partial_gauss_eliminate(
        int(c), int(lin), rows, 0, d
    )
    if got['identically_zero']:
        return 0
    assert got['support_control_rank'] == 0
    assert got['support_free_dimension'] == 0
    assert got['normalized_sign_linear'] == 0
    assert tuple(got['normalized_sign_rows']) == ()
    exponent = got['log2_abs_nonzero_gauss']
    assert exponent is not None
    sign = -1 if got['normalized_sign_constant'] else 1
    return sign * (1 << exponent)


def term_inner(left, right, cache):
    a = int(left['term_id'])
    b = int(right['term_id'])
    key = (a, b) if a <= b else (b, a)
    if key in cache:
        return cache[key]

    la = left['anchor']
    ra = right['anchor']
    _relation, inter = P.support_relation(la, ra, PHYS_N)
    if inter is None:
        value = 0
    else:
        _rank, ix0, ibasis = inter
        lc, llin, lrows = P.restrict_anchor_sign(la, ix0, ibasis)
        rc, rlin, rrows = P.restrict_anchor_sign(ra, ix0, ibasis)
        moment = full_quadratic_moment(
            lc ^ rc,
            llin ^ rlin,
            tuple(x ^ y for x, y in zip(lrows, rrows)),
        )
        value = int(left['coefficient']) * int(right['coefficient']) * moment

    cache[key] = value
    return value


def group_inner(left, right, cache):
    return sum(
        term_inner(a, b, cache)
        for a in left['terms']
        for b in right['terms']
    )


def eval_term(term, x):
    q = P.eval_anchor_sign(term['anchor'], x)
    if q is None:
        return 0
    return int(term['coefficient']) * (-1 if q else 1)


def eval_group(group, x):
    return sum(eval_term(term, x) for term in group['terms'])


def synthetic_regression():
    n = 5
    anchors = [
        P.make_synthetic_anchor((), n, 'linear'),
        P.make_synthetic_anchor(((1, 0),), n, 'quadratic'),
        P.make_synthetic_anchor(((2, 1),), n, 'one'),
        P.make_synthetic_anchor(((1, 1), (4, 0)), n, 'linear'),
    ]

    specs = (
        ((1, 0),),
        ((1, 0),),
        ((-1, 0),),
        ((2, 0),),
        ((1, 1),),
        ((1, 0), (1, 1)),
        ((2, 1), (-1, 2)),
        ((1, 3), (1, 0)),
    )
    groups = []
    tid = 0
    for gid, spec in enumerate(specs):
        terms = []
        for coefficient, anchor_index in spec:
            terms.append({
                'term_id': tid,
                'group_id': gid,
                'kind': 'synthetic',
                'coefficient': coefficient,
                'anchor': anchors[anchor_index],
            })
            tid += 1
        groups.append({'group_id': gid, 'terms': tuple(terms)})

    cache = {}
    tested = 0
    for i, left in enumerate(groups):
        for j in range(i, len(groups)):
            right = groups[j]
            got = group_inner(left, right, cache)
            brute = sum(
                eval_group(left, x) * eval_group(right, x)
                for x in range(1 << n)
            )
            assert got == brute, (i, j, got, brute)
            tested += 1

    assert tested == 36

    norms = [
        sum(eval_group(g, x) ** 2 for x in range(1 << n))
        for g in groups
    ]
    assert group_inner(groups[0], groups[1], cache) ** 2 == norms[0] * norms[1]
    assert Fraction(group_inner(groups[0], groups[1], cache), norms[0]) == 1
    assert Fraction(group_inner(groups[0], groups[2], cache), norms[0]) == -1
    assert Fraction(group_inner(groups[0], groups[3], cache), norms[0]) == 2
    return tested


def dependency_components(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for a, b in edges:
        union(a, b)

    sizes = Counter(find(i) for i in range(n))
    return sorted(sizes.values(), reverse=True)


def analyze():
    regression_cases = synthetic_regression()

    with redirect_stdout(io.StringIO()):
        even = E.analyze()
        singleton = S.analyze()

    assert even['support_groups'] == singleton['support_groups'] == 250
    assert even['raw_e0_sectors'] == singleton['raw_e0_sectors'] == 577
    assert even['even_multiplicity_groups'] == 147
    assert singleton['singleton_groups'] == 103

    census_by_gid = {}
    for record in even['groups']:
        gid = int(record['group_id'])
        assert gid not in census_by_gid
        census_by_gid[gid] = {
            'group_id': gid,
            'multiplicity': int(record['multiplicity']),
            'counts': census_map(record),
        }
    for record in singleton['groups']:
        gid = int(record['group_id'])
        assert gid not in census_by_gid
        census_by_gid[gid] = {
            'group_id': gid,
            'multiplicity': 1,
            'counts': census_map(record),
        }
    assert sorted(census_by_gid) == list(range(250))

    for rec in census_by_gid.values():
        rec['norm2'] = census_norm2(rec['counts'])
        assert rec['norm2'] > 0
        rec['scale_signature'] = scale_signature(rec['counts'])

    signature_classes = defaultdict(list)
    for gid, rec in census_by_gid.items():
        signature_classes[rec['scale_signature']].append(gid)

    scale_class_size_hist = Counter(len(v) for v in signature_classes.values())
    candidate_pairs = sum(len(v) * (len(v) - 1) // 2 for v in signature_classes.values())
    all_pairs = 250 * 249 // 2
    assert candidate_pairs <= all_pairs

    e0, _e1, _half = P.C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for k in range(4):
        for zs, cls in e0[k]:
            can = P.C.P.U.H.support_for(POS, zs, cls)
            if can is None:
                continue
            raw += 1
            grouped[can].append((zs, cls))
    ordered = list(sorted(grouped.items(), key=lambda kv: kv[0]))
    assert raw == 577 and len(ordered) == 250

    physical_groups = {}
    next_term_id = 0
    for gid, (can, sectors) in enumerate(ordered):
        group, next_term_id = build_group_terms(
            gid, can, sectors, next_term_id
        )
        assert group['multiplicity'] == census_by_gid[gid]['multiplicity']
        physical_groups[gid] = group
    assert next_term_id == 680

    term_cache = {}
    norm_crosscheck_failures = []
    for gid in range(250):
        got = group_inner(physical_groups[gid], physical_groups[gid], term_cache)
        expected = census_by_gid[gid]['norm2']
        if got != expected:
            norm_crosscheck_failures.append({
                'group_id': gid,
                'term_norm2': got,
                'census_norm2': expected,
            })
    assert not norm_crosscheck_failures, norm_crosscheck_failures[:5]

    exact_distribution_equal_candidates = 0
    exact_distribution_negated_candidates = 0
    zero_inner_candidates = 0
    proportional_pairs = []
    proportional_ratio_hist = Counter()
    proportional_by_multiplicity = Counter()
    proportional_projection_relation_hist = Counter()
    nonproportional_candidates = 0

    for gids in signature_classes.values():
        gids = sorted(gids)
        for ai, gid in enumerate(gids):
            gc = census_by_gid[gid]['counts']
            for hid in gids[ai + 1:]:
                hc = census_by_gid[hid]['counts']

                if gc == hc:
                    exact_distribution_equal_candidates += 1
                neg_gc = {-v: n for v, n in gc.items()}
                if neg_gc == hc:
                    exact_distribution_negated_candidates += 1

                inner = group_inner(
                    physical_groups[gid],
                    physical_groups[hid],
                    term_cache,
                )
                if inner == 0:
                    zero_inner_candidates += 1

                ng = census_by_gid[gid]['norm2']
                nh = census_by_gid[hid]['norm2']
                if inner * inner != ng * nh:
                    nonproportional_candidates += 1
                    continue

                ratio = Fraction(inner, ng)
                assert ratio != 0
                residual_norm_num = (
                    ratio.denominator * ratio.denominator * nh
                    + ratio.numerator * ratio.numerator * ng
                    - 2 * ratio.numerator * ratio.denominator * inner
                )
                assert residual_norm_num == 0

                relation, _inter = P.support_relation(
                    physical_groups[gid]['projection_anchor'],
                    physical_groups[hid]['projection_anchor'],
                    PHYS_N,
                )
                rstr = str(ratio)
                proportional_ratio_hist[rstr] += 1
                proportional_by_multiplicity[
                    (
                        physical_groups[gid]['multiplicity'],
                        physical_groups[hid]['multiplicity'],
                    )
                ] += 1
                proportional_projection_relation_hist[relation] += 1
                proportional_pairs.append({
                    'left_group_id': gid,
                    'right_group_id': hid,
                    'left_multiplicity': physical_groups[gid]['multiplicity'],
                    'right_multiplicity': physical_groups[hid]['multiplicity'],
                    'ratio_right_over_left': rstr,
                    'projection_support_relation': relation,
                })

    assert nonproportional_candidates + len(proportional_pairs) == candidate_pairs

    exact_equal_pairs = sum(
        rec['ratio_right_over_left'] == '1'
        for rec in proportional_pairs
    )
    exact_negated_pairs = sum(
        rec['ratio_right_over_left'] == '-1'
        for rec in proportional_pairs
    )
    exact_scaled_pairs = len(proportional_pairs) - exact_equal_pairs - exact_negated_pairs

    components = dependency_components(
        250,
        [
            (rec['left_group_id'], rec['right_group_id'])
            for rec in proportional_pairs
        ],
    )
    component_size_hist = dict(sorted(Counter(components).items()))

    if proportional_pairs:
        decision = (
            'PAIRWISE_EXACT_SCALAR_DEPENDENCIES_FOUND_'
            f'{len(proportional_pairs)}'
        )
    else:
        decision = 'NO_PAIRWISE_EXACT_SCALAR_DEPENDENCY_ACROSS_250_GROUP_OUTPUTS'

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'synthetic_inner_product_regression_cases': regression_cases,
        'raw_e0_sectors': raw,
        'support_groups': 250,
        'support_multiplicity_histogram': {1: 103, 2: 57, 4: 90},
        'physical_term_count': next_term_id,
        'singleton_baseline_term_count': 103,
        'all_unordered_group_pairs': all_pairs,
        'scale_signature_class_count': len(signature_classes),
        'scale_signature_class_size_histogram': dict(sorted(scale_class_size_hist.items())),
        'scale_compatible_candidate_pairs': candidate_pairs,
        'distribution_filter_rejected_pairs': all_pairs - candidate_pairs,
        'exact_distribution_equal_candidate_pairs': exact_distribution_equal_candidates,
        'exact_distribution_negated_candidate_pairs': exact_distribution_negated_candidates,
        'zero_inner_scale_compatible_candidate_pairs': zero_inner_candidates,
        'nonproportional_scale_compatible_candidate_pairs': nonproportional_candidates,
        'exact_scalar_proportional_pairs': len(proportional_pairs),
        'exact_equal_function_pairs': exact_equal_pairs,
        'exact_negated_function_pairs': exact_negated_pairs,
        'exact_other_scaled_function_pairs': exact_scaled_pairs,
        'proportional_ratio_histogram': dict(sorted(proportional_ratio_hist.items())),
        'proportional_pair_multiplicity_histogram': {
            str(k): v for k, v in sorted(proportional_by_multiplicity.items())
        },
        'proportional_projection_support_relation_histogram': dict(
            sorted(proportional_projection_relation_hist.items())
        ),
        'proportional_dependency_component_sizes_descending': components,
        'proportional_dependency_component_size_histogram': component_size_hist,
        'term_inner_product_cache_entries': len(term_cache),
        'norm_crosscheck_failures': norm_crosscheck_failures,
        'proportional_pairs': proportional_pairs,
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_GROUP_OUTPUT_PAIR_DEPENDENCY')
    print('scope=exact pairwise scalar-dependency census across all 250 C916 e0 first-dyadic residual output functions')
    print('filter=global exact value-multiplicity distributions reject scale-incompatible pairs before any physical quadratic inner-product work')
    print('proof=for scale-compatible pairs, exact physical affine-quadratic inner products are used; Cauchy equality is necessary and sufficient for scalar proportionality')
    print('crosscheck=every physical term decomposition reproduces the independently frozen exact per-group L2 norm from the singleton/even value censuses')
    print('important=pairwise scalar independence does not exclude higher-order linear relations, nonlinear dependencies, or a compressed non-linear joint state')
    print('not_included=complete all-250 joint image, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
