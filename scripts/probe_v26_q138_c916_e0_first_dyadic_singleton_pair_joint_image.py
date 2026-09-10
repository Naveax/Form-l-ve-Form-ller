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

import probe_v26_q138_c916_e0_first_dyadic_group_output_pair_dependency as D
import probe_v26_q138_c916_e0_first_dyadic_singleton_value_image_census as S

P = D.P
POS = D.POS
PHYS_N = D.PHYS_N
assert PHYS_N == 149


def zero_sign_anchor(anchor):
    out = dict(anchor)
    out['normalized_sign_constant'] = 0
    out['normalized_sign_linear'] = 0
    out['normalized_sign_rows'] = tuple(0 for _ in anchor['normalized_sign_rows'])
    return out


def feature_term(term_id, anchor, ambient):
    return {
        'term_id': int(term_id),
        'group_id': -1,
        'kind': 'joint_feature',
        'coefficient': 1,
        'anchor': anchor,
        'ambient_dimension': int(ambient),
    }


def make_constant_term(n, term_id=0):
    return feature_term(term_id, P.make_synthetic_anchor((), n, 'zero'), n)


def make_bundle(group, feature_base, one, ambient):
    assert group['multiplicity'] == 1
    gauss_terms = [t for t in group['terms'] if t['kind'] == 'gauss_sector']
    baseline_terms = [
        t for t in group['terms'] if t['kind'] == 'singleton_projection_baseline'
    ]
    assert len(gauss_terms) == len(baseline_terms) == 1
    gauss = gauss_terms[0]
    baseline = baseline_terms[0]

    projection_anchor = group['projection_anchor']
    gauss_anchor = gauss['anchor']
    relation, _inter = P.support_relation(gauss_anchor, projection_anchor, ambient)
    assert relation in ('left_subset_right', 'equal')

    b = int(baseline['coefficient'])
    a = int(gauss['coefficient'])
    assert b < 0 and a > 0

    pterm = feature_term(feature_base, projection_anchor, ambient)
    aterm = feature_term(feature_base + 1, zero_sign_anchor(gauss_anchor), ambient)
    qterm = feature_term(feature_base + 2, gauss_anchor, ambient)

    values = (0, b, b + a, b - a)
    assert len(set(values)) == 4

    return {
        'group_id': int(group['group_id']),
        'projection_anchor': projection_anchor,
        'gauss_anchor': gauss_anchor,
        'baseline': b,
        'gauss_half_amplitude': a,
        'features': (one, pterm, aterm, qterm),
        'values': values,
    }


def state_specs(bundle):
    half = Fraction(1, 2)
    b = bundle['baseline']
    a = bundle['gauss_half_amplitude']
    return (
        (0, (Fraction(1), Fraction(-1), Fraction(0), Fraction(0))),
        (b, (Fraction(0), Fraction(1), Fraction(-1), Fraction(0))),
        (b + a, (Fraction(0), Fraction(0), half, half)),
        (b - a, (Fraction(0), Fraction(0), half, -half)),
    )


def state_indicator_count(bundle, one, cache):
    features = bundle['features']
    out = Counter()
    for value, coeffs in state_specs(bundle):
        total = Fraction(0)
        for i, coeff in enumerate(coeffs):
            if coeff:
                total += coeff * D.term_inner(features[i], one, cache)
        assert total.denominator == 1
        count = int(total.numerator)
        assert count >= 0
        if count:
            out[int(value)] += count
    assert sum(out.values()) == (1 << int(one['ambient_dimension']))
    return dict(sorted(out.items()))


def joint_census(left, right, cache):
    lf = left['features']
    rf = right['features']
    moments = tuple(
        tuple(D.term_inner(a, b, cache) for b in rf)
        for a in lf
    )

    counts = Counter()
    for lv, lc in state_specs(left):
        for rv, rc in state_specs(right):
            total = Fraction(0)
            for i, ci in enumerate(lc):
                if not ci:
                    continue
                for j, cj in enumerate(rc):
                    if cj:
                        total += ci * cj * moments[i][j]
            assert total.denominator == 1, (
                left['group_id'], right['group_id'], lv, rv, total
            )
            count = int(total.numerator)
            assert count >= 0, (
                left['group_id'], right['group_id'], lv, rv, count
            )
            if count:
                counts[(int(lv), int(rv))] += count

    domain = 1 << int(lf[0]['ambient_dimension'])
    assert sum(counts.values()) == domain

    lm = Counter()
    rm = Counter()
    for (lv, rv), count in counts.items():
        lm[lv] += count
        rm[rv] += count

    return {
        'joint_counts': counts,
        'left_marginal': dict(sorted(lm.items())),
        'right_marginal': dict(sorted(rm.items())),
        'joint_image_size': len(counts),
        'joint_state_bits': (len(counts) - 1).bit_length(),
    }


def eval_bundle(bundle, x):
    if P.eval_anchor_sign(bundle['projection_anchor'], x) is None:
        return 0
    value = bundle['baseline']
    q = P.eval_anchor_sign(bundle['gauss_anchor'], x)
    if q is not None:
        amp = bundle['gauss_half_amplitude']
        value += -amp if q else amp
    return int(value)


def synthetic_regression():
    n = 5
    one = make_constant_term(n, 0)
    specs = (
        ((), ((1, 0),), 'linear', -4, 1),
        (((2, 0),), ((2, 0), (4, 1)), 'quadratic', -5, 2),
        (((1, 1),), ((1, 1), (8, 0)), 'one', -6, 1),
        (((3, 0),), ((3, 0),), 'linear', -7, 2),
        (((4, 1),), ((4, 1), (1, 0)), 'quadratic', -8, 1),
    )

    bundles = []
    for gid, (pc, ac, kind, baseline, amp) in enumerate(specs):
        projection = P.make_synthetic_anchor(pc, n, 'zero')
        gauss = P.make_synthetic_anchor(ac, n, kind)
        relation, _ = P.support_relation(gauss, projection, n)
        assert relation in ('left_subset_right', 'equal')
        group = {
            'group_id': gid,
            'multiplicity': 1,
            'projection_anchor': projection,
            'terms': (
                {
                    'term_id': 100 + 2 * gid,
                    'group_id': gid,
                    'kind': 'gauss_sector',
                    'coefficient': amp,
                    'anchor': gauss,
                    'ambient_dimension': n,
                },
                {
                    'term_id': 101 + 2 * gid,
                    'group_id': gid,
                    'kind': 'singleton_projection_baseline',
                    'coefficient': baseline,
                    'anchor': projection,
                    'ambient_dimension': n,
                },
            ),
        }
        bundles.append(make_bundle(group, 1 + 3 * gid, one, n))

    cache = {}
    single_cases = 0
    for bundle in bundles:
        got = state_indicator_count(bundle, one, cache)
        brute = Counter(eval_bundle(bundle, x) for x in range(1 << n))
        assert got == dict(sorted(brute.items())), (
            bundle['group_id'], got, brute
        )
        single_cases += 1

    pair_cases = 0
    for i, left in enumerate(bundles):
        for right in bundles[i + 1:]:
            got = joint_census(left, right, cache)
            brute = Counter(
                (eval_bundle(left, x), eval_bundle(right, x))
                for x in range(1 << n)
            )
            assert got['joint_counts'] == brute, (
                left['group_id'], right['group_id'], got['joint_counts'], brute
            )
            pair_cases += 1

    assert single_cases == 5 and pair_cases == 10
    return {
        'singletons': single_cases,
        'pairs': pair_cases,
        'domain_points_checked': (single_cases + pair_cases) * (1 << n),
    }


def analyze():
    regression = synthetic_regression()

    with redirect_stdout(io.StringIO()):
        frozen = S.analyze()
    assert frozen['physical_shared_dimension'] == PHYS_N
    assert frozen['singleton_groups'] == 103
    frozen_by_gid = {
        int(rec['group_id']): {
            'counts': D.census_map(rec),
            'normalized_alphabet': tuple(
                int(v) for v in rec['normalized_alphabet']
            ),
        }
        for rec in frozen['groups']
    }
    assert len(frozen_by_gid) == 103

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
    ordered = list(sorted(grouped.items(), key=lambda kv: kv[0]))
    assert raw == 577 and len(ordered) == 250
    assert dict(sorted(Counter(len(v) for _can, v in ordered).items())) == {
        1: 103, 2: 57, 4: 90,
    }

    one = make_constant_term(PHYS_N, 0)
    bundles = {}
    next_term_id = 1
    feature_index = 0
    for gid, (can, sectors) in enumerate(ordered):
        if len(sectors) != 1:
            continue
        group, next_term_id = D.build_group_terms(
            gid, can, sectors, next_term_id
        )
        bundle = make_bundle(
            group, 1 + 3 * feature_index, one, PHYS_N
        )
        feature_index += 1
        assert gid in frozen_by_gid
        assert set(bundle['values']) == set(frozen_by_gid[gid]['counts'])
        bundles[gid] = bundle

    assert len(bundles) == feature_index == 103
    gids = sorted(bundles)
    assert sorted(frozen_by_gid) == gids

    term_cache = {}
    isolated_crosschecks = 0
    for gid in gids:
        got = state_indicator_count(bundles[gid], one, term_cache)
        assert got == frozen_by_gid[gid]['counts'], (
            gid, got, frozen_by_gid[gid]['counts']
        )
        isolated_crosschecks += 1
    assert isolated_crosschecks == 103

    pair_count = 0
    joint_size_hist = Counter()
    joint_bits_hist = Counter()
    deficit_hist = Counter()
    projection_relation_hist = Counter()
    gauss_relation_hist = Counter()
    joint_size_by_projection_relation = defaultdict(Counter)
    joint_size_by_gauss_relation = defaultdict(Counter)
    alphabet_pair_hist = Counter()
    subcartesian_edges = []
    integer_bit_saving_pairs = 0
    marginal_crosschecks = 0
    minimum_joint_size = 17
    strongest_examples = []

    local_index = {gid: i for i, gid in enumerate(gids)}

    for ai, gid in enumerate(gids):
        left = bundles[gid]
        for hid in gids[ai + 1:]:
            right = bundles[hid]
            rec = joint_census(left, right, term_cache)
            pair_count += 1

            assert rec['left_marginal'] == frozen_by_gid[gid]['counts']
            assert rec['right_marginal'] == frozen_by_gid[hid]['counts']
            marginal_crosschecks += 2

            size = int(rec['joint_image_size'])
            bits = int(rec['joint_state_bits'])
            assert 1 <= size <= 16
            assert bits <= 4
            deficit = 16 - size

            projection_relation, _ = P.support_relation(
                left['projection_anchor'], right['projection_anchor'], PHYS_N
            )
            gauss_relation, _ = P.support_relation(
                left['gauss_anchor'], right['gauss_anchor'], PHYS_N
            )

            joint_size_hist[size] += 1
            joint_bits_hist[bits] += 1
            deficit_hist[deficit] += 1
            projection_relation_hist[projection_relation] += 1
            gauss_relation_hist[gauss_relation] += 1
            joint_size_by_projection_relation[projection_relation][size] += 1
            joint_size_by_gauss_relation[gauss_relation][size] += 1

            alph = tuple(sorted((
                frozen_by_gid[gid]['normalized_alphabet'],
                frozen_by_gid[hid]['normalized_alphabet'],
            )))
            alphabet_pair_hist[str([list(alph[0]), list(alph[1])])] += 1

            if size < 16:
                subcartesian_edges.append(
                    (local_index[gid], local_index[hid])
                )
            if bits < 4:
                integer_bit_saving_pairs += 1

            example = {
                'left_group_id': gid,
                'right_group_id': hid,
                'joint_image_size': size,
                'joint_state_bits': bits,
                'missing_cartesian_pairs': deficit,
                'projection_support_relation': projection_relation,
                'gauss_support_relation': gauss_relation,
            }
            if size < minimum_joint_size:
                minimum_joint_size = size
                strongest_examples = [example]
            elif size == minimum_joint_size and len(strongest_examples) < 16:
                strongest_examples.append(example)

    expected_pairs = 103 * 102 // 2
    assert pair_count == expected_pairs == 5253
    assert marginal_crosschecks == 2 * expected_pairs
    assert sum(joint_size_hist.values()) == expected_pairs
    assert minimum_joint_size == min(joint_size_hist)

    subcartesian_pairs = len(subcartesian_edges)
    full_cartesian_pairs = expected_pairs - subcartesian_pairs
    components = D.dependency_components(103, subcartesian_edges)
    component_size_hist = dict(sorted(Counter(components).items()))

    if subcartesian_pairs:
        decision = 'SINGLETON_PAIR_SUBCARTESIAN_NONLINEAR_JOINT_IMAGES_FOUND'
    else:
        decision = 'ALL_SINGLETON_PAIRS_HAVE_FULL_CARTESIAN_NONLINEAR_JOINT_IMAGE'

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'synthetic_joint_image_regression': regression,
        'raw_e0_sectors': raw,
        'support_groups': 250,
        'support_multiplicity_histogram': {1: 103, 2: 57, 4: 90},
        'singleton_groups': 103,
        'singleton_pairs': expected_pairs,
        'isolated_singleton_census_crosschecks': isolated_crosschecks,
        'pair_marginal_crosschecks': marginal_crosschecks,
        'isolated_cartesian_image_size': 16,
        'isolated_cartesian_state_bits': 4,
        'joint_image_size_histogram': dict(sorted(joint_size_hist.items())),
        'joint_state_bits_histogram': dict(sorted(joint_bits_hist.items())),
        'missing_cartesian_pair_count_histogram': dict(sorted(deficit_hist.items())),
        'minimum_joint_image_size': minimum_joint_size,
        'maximum_missing_cartesian_pairs': 16 - minimum_joint_size,
        'maximum_exact_log2_cardinality_gain_bits': (
            4.0 - math.log2(minimum_joint_size)
        ),
        'pairs_with_integer_bit_saving': integer_bit_saving_pairs,
        'subcartesian_pair_count': subcartesian_pairs,
        'full_cartesian_pair_count': full_cartesian_pairs,
        'subcartesian_dependency_component_sizes': components,
        'subcartesian_dependency_component_size_histogram': component_size_hist,
        'projection_support_relation_histogram': dict(
            sorted(projection_relation_hist.items())
        ),
        'gauss_support_relation_histogram': dict(
            sorted(gauss_relation_hist.items())
        ),
        'joint_image_size_by_projection_support_relation': {
            relation: dict(sorted(hist.items()))
            for relation, hist in sorted(joint_size_by_projection_relation.items())
        },
        'joint_image_size_by_gauss_support_relation': {
            relation: dict(sorted(hist.items()))
            for relation, hist in sorted(joint_size_by_gauss_relation.items())
        },
        'normalized_alphabet_pair_histogram': dict(
            sorted(alphabet_pair_hist.items())
        ),
        'strongest_joint_image_examples': strongest_examples,
        'term_moment_cache_entries': len(term_cache),
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_SINGLETON_PAIR_JOINT_IMAGE')
    print('scope=exact joint value-image census for all 5253 unordered pairs among the 103 exact singleton first-dyadic residual functions on the common 149-bit physical domain')
    print('method=each four-valued singleton state indicator is expanded exactly in the basis {1, projection-indicator, Gauss-support-indicator, signed-Gauss-support}; pair state counts are recovered from exact affine/quadratic inner products')
    print('important=subcartesian joint images prove pairwise nonlinear output dependence but do not by themselves give an all-250 separator or complete C2 compression theorem')
    print('not_included=even/singleton cross pairs, even/even pairs, higher-order joint images, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
