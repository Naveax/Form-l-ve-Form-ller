#!/usr/bin/env python3
import io
import json
import sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_pair_value_image_census as V

P = V.P
L = V.L
POS = V.POS
PHYS_N = V.PHYS_N
assert PHYS_N == 149


def submasks(mask):
    s = mask
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & mask


def xor_character_form(transforms, char_mask, p):
    c = 0
    lin = 0
    rows = [0] * p
    for i, t in enumerate(transforms):
        if not ((char_mask >> i) & 1):
            continue
        c ^= t['shared_survivor_constant']
        lin ^= t['shared_survivor_linear']
        assert len(t['shared_survivor_rows']) == p
        for j, row in enumerate(t['shared_survivor_rows']):
            rows[j] ^= row
    return c, lin, tuple(rows)


def group_value_census(transforms, p, domain_dim):
    """Exact census of F=(sum_i G_i)/2 for n=2 or n=4 transforms.

    The active-support cells are isolated by inclusion-exclusion. On each exact
    membership cell, all joint sign populations are recovered by Walsh inversion
    from exact quadratic character moments. No physical-domain enumeration is
    performed.
    """
    n = len(transforms)
    assert n in (2, 4)
    assert domain_dim >= p
    full = (1 << n) - 1
    domain = 1 << domain_dim

    exponents = tuple(t['log2_abs_nonzero_gauss'] for t in transforms)
    assert all(e is not None and e >= 1 for e in exponents)

    intersection_cache = {}
    character_cache = {}

    def intersection(mask):
        assert mask
        if mask in intersection_cache:
            return intersection_cache[mask]
        constraints = []
        for i, t in enumerate(transforms):
            if (mask >> i) & 1:
                constraints.extend(P.transform_constraints(t))
        sol = P.C.P.U.T.rref(constraints, n=p)
        intersection_cache[mask] = sol
        return sol

    def moment(support_mask, char_mask):
        assert char_mask & ~support_mask == 0
        key = (support_mask, char_mask)
        if key in character_cache:
            return character_cache[key]
        if support_mask == 0:
            assert char_mask == 0
            out = domain
        else:
            sol = intersection(support_mask)
            if sol is None:
                out = 0
            else:
                _rank, x0, basis = sol
                if char_mask == 0:
                    out = 1 << len(basis)
                else:
                    c, lin, rows = xor_character_form(transforms, char_mask, p)
                    out = V.signed_quadratic_moment(c, lin, rows, x0, basis)
        character_cache[key] = out
        return out

    def exact_cell_character(active_mask, char_mask):
        assert char_mask & ~active_mask == 0
        inactive = full ^ active_mask
        total = 0
        for u in submasks(inactive):
            term = moment(active_mask | u, char_mask)
            total += -term if (u.bit_count() & 1) else term
        return total

    counts = Counter()
    exact_membership_sizes = {}

    for active in range(full + 1):
        k = active.bit_count()
        cell_size = exact_cell_character(active, 0)
        assert cell_size >= 0
        exact_membership_sizes[active] = cell_size
        if cell_size == 0:
            continue

        if active == 0:
            counts[0] += cell_size
            continue

        chars = {
            char: exact_cell_character(active, char)
            for char in submasks(active)
        }
        assert chars[0] == cell_size

        for negative in submasks(active):
            num = 0
            for char, walsh in chars.items():
                num += -walsh if ((negative & char).bit_count() & 1) else walsh
            divisor = 1 << k
            assert num % divisor == 0
            population = num // divisor
            assert population >= 0
            if not population:
                continue

            value_num = 0
            for i, e in enumerate(exponents):
                if not ((active >> i) & 1):
                    continue
                amp = 1 << e
                value_num += -amp if ((negative >> i) & 1) else amp
            assert value_num % 2 == 0
            counts[value_num // 2] += population

    counts = Counter({int(v): int(c) for v, c in counts.items() if c})
    assert sum(exact_membership_sizes.values()) == domain
    assert sum(counts.values()) == domain
    assert all(c > 0 for c in counts.values())

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
        'transform_count': n,
        'projection_rank': p,
        'image_size': image_size,
        'state_bits': state_bits,
        'nonzero_value_count': len(nonzero),
        'minimum_nonzero_valuation': min_v2,
        'normalized_alphabet': list(normalized),
        'alphabet_sign_symmetric': all(-v in counts for v in counts),
        'multiplicity_sign_symmetric': all(counts[v] == counts.get(-v, 0) for v in counts),
        'realized_exact_membership_cells': sum(c > 0 for c in exact_membership_sizes.values()),
        'exact_membership_size_by_mask': {
            str(mask): exact_membership_sizes[mask]
            for mask in sorted(exact_membership_sizes)
            if exact_membership_sizes[mask]
        },
        'value_multiplicity': [
            {'value': v, 'multiplicity': counts[v]}
            for v in values
        ],
        'cached_support_intersections': len(intersection_cache),
        'cached_character_moments': len(character_cache),
    }


def synthetic_group_regression():
    p = 4
    z = (0, 0, 0, 0)
    q01 = (2, 1, 0, 0)
    q23 = (0, 0, 8, 4)
    q02 = (4, 0, 1, 0)
    synthetic = (
        P.make_synthetic_transform((), p, 2, 0, 0, z),
        P.make_synthetic_transform(((1, 0),), p, 2, 0, 2, z),
        P.make_synthetic_transform(((1, 1),), p, 3, 1, 4, q01),
        P.make_synthetic_transform(((2, 0),), p, 3, 0, 1, q23),
        P.make_synthetic_transform(((3, 0),), p, 2, 1, 8, q02),
    )

    tested = 0
    by_n = Counter()
    for n in (2, 4):
        for ids in product(range(len(synthetic)), repeat=n):
            ts = tuple(synthetic[i] for i in ids)
            got = group_value_census(ts, p, p)
            brute = Counter()
            for s in range(1 << p):
                numerator = sum(P.eval_transform(t, s) for t in ts)
                assert numerator % 2 == 0
                brute[numerator // 2] += 1
            exact = {
                rec['value']: rec['multiplicity']
                for rec in got['value_multiplicity']
            }
            assert exact == dict(sorted(brute.items()))
            tested += 1
            by_n[n] += 1

    assert dict(sorted(by_n.items())) == {2: 25, 4: 625}
    assert tested == 650
    return tested, dict(sorted(by_n.items()))


def analyze():
    regression_cases, regression_by_n = synthetic_group_regression()

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
    mult_hist = Counter(len(v) for v in grouped.values())
    assert dict(sorted(mult_hist.items())) == {1: 103, 2: 57, 4: 90}

    image_hist = Counter()
    state_hist = Counter()
    nonzero_hist = Counter()
    min_v2_hist = Counter()
    normalized_hist = Counter()
    alphabet_symmetry_hist = Counter()
    multiplicity_symmetry_hist = Counter()
    membership_cell_hist = Counter()
    support_moment_count_hist = Counter()

    by_mult_image = defaultdict(Counter)
    by_mult_state = defaultdict(Counter)
    by_mult_nonzero = defaultdict(Counter)
    by_mult_v2 = defaultdict(Counter)
    by_mult_membership = defaultdict(Counter)

    m2_pair_crosschecks = 0
    m4_pairing_partition_checks = 0
    group_records = []

    for gid, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        m = len(sectors)
        if m == 1:
            continue
        assert m in (2, 4)

        authority = pair_groups[gid]
        assert authority['multiplicity'] == m
        projection_rank, transforms = P.group_transforms(can, sectors)
        assert len(transforms) == m

        selected_pairs = [tuple(rec['pair']) for rec in authority['selected_pairs']]
        flat = sorted(i for pair in selected_pairs for i in pair)
        assert flat == list(range(m))
        if m == 4:
            assert len(selected_pairs) == 2
            m4_pairing_partition_checks += 1
        else:
            assert selected_pairs == [(0, 1)]

        rec = group_value_census(tuple(transforms), projection_rank, PHYS_N)
        rec.update({
            'group_id': gid,
            'multiplicity': m,
            'matching_index': authority['matching_index'],
            'selected_pairs': [list(pair) for pair in selected_pairs],
        })

        if m == 2:
            pair = V.pair_value_census(
                transforms[0], transforms[1], projection_rank, PHYS_N
            )
            group_map = {
                x['value']: x['multiplicity'] for x in rec['value_multiplicity']
            }
            pair_map = {
                x['value']: x['multiplicity'] for x in pair['value_multiplicity']
            }
            assert group_map == pair_map
            assert rec['image_size'] == pair['image_size']
            assert rec['state_bits'] == pair['state_bits']
            assert rec['minimum_nonzero_valuation'] == pair['minimum_nonzero_valuation']
            m2_pair_crosschecks += 1

        image_hist[rec['image_size']] += 1
        state_hist[rec['state_bits']] += 1
        nonzero_hist[rec['nonzero_value_count']] += 1
        if rec['minimum_nonzero_valuation'] is not None:
            min_v2_hist[rec['minimum_nonzero_valuation']] += 1
        normalized_hist[tuple(rec['normalized_alphabet'])] += 1
        alphabet_symmetry_hist[rec['alphabet_sign_symmetric']] += 1
        multiplicity_symmetry_hist[rec['multiplicity_sign_symmetric']] += 1
        membership_cell_hist[rec['realized_exact_membership_cells']] += 1
        support_moment_count_hist[rec['cached_character_moments']] += 1

        by_mult_image[m][rec['image_size']] += 1
        by_mult_state[m][rec['state_bits']] += 1
        by_mult_nonzero[m][rec['nonzero_value_count']] += 1
        by_mult_membership[m][rec['realized_exact_membership_cells']] += 1
        if rec['minimum_nonzero_valuation'] is not None:
            by_mult_v2[m][rec['minimum_nonzero_valuation']] += 1

        group_records.append(rec)

    assert len(group_records) == 147
    assert m2_pair_crosschecks == 57
    assert m4_pairing_partition_checks == 90
    assert sum(image_hist.values()) == 147
    assert sum(by_mult_image[2].values()) == 57
    assert sum(by_mult_image[4].values()) == 90

    # Each transform is 0 or one of two signed amplitudes. Four transforms have
    # at most 3^4 raw signed-membership states before equal output values merge.
    assert max(image_hist) <= 81
    assert max(state_hist) <= 7

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'synthetic_group_regression_cases': regression_cases,
        'synthetic_group_regression_by_transform_count': regression_by_n,
        'raw_e0_sectors': raw,
        'support_groups': len(grouped),
        'support_multiplicity_histogram': dict(sorted(mult_hist.items())),
        'singleton_groups_deferred': mult_hist[1],
        'even_multiplicity_groups': len(group_records),
        'multiplicity2_pair_census_crosschecks': m2_pair_crosschecks,
        'multiplicity4_pairing_partition_checks': m4_pairing_partition_checks,
        'even_group_value_image_size_histogram': dict(sorted(image_hist.items())),
        'even_group_value_state_bits_histogram': dict(sorted(state_hist.items())),
        'even_group_nonzero_value_count_histogram': dict(sorted(nonzero_hist.items())),
        'even_group_minimum_nonzero_valuation_histogram': dict(sorted(min_v2_hist.items())),
        'even_group_normalized_alphabet_histogram': {
            str(list(k)): v for k, v in sorted(normalized_hist.items())
        },
        'even_group_alphabet_sign_symmetry_histogram': {
            str(k).lower(): v for k, v in sorted(alphabet_symmetry_hist.items())
        },
        'even_group_multiplicity_sign_symmetry_histogram': {
            str(k).lower(): v for k, v in sorted(multiplicity_symmetry_hist.items())
        },
        'realized_exact_membership_cell_histogram': dict(sorted(membership_cell_hist.items())),
        'cached_character_moment_count_histogram': dict(sorted(support_moment_count_hist.items())),
        'image_size_by_group_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(by_mult_image.items())
        },
        'state_bits_by_group_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(by_mult_state.items())
        },
        'nonzero_value_count_by_group_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(by_mult_nonzero.items())
        },
        'minimum_nonzero_valuation_by_group_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(by_mult_v2.items())
        },
        'membership_cells_by_group_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(by_mult_membership.items())
        },
        'maximum_even_group_image_size': max(image_hist),
        'maximum_even_group_state_bits': max(state_hist),
        'groups': group_records,
        'decision': 'EVEN_MULTIPLICITY_GROUP_EXACT_NONLINEAR_VALUE_IMAGE_CENSUS_COMPLETE',
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_EVEN_GROUP_VALUE_IMAGE_CENSUS')
    print('identity=for each C e0 support group of multiplicity 2 or 4, evaluate F_g(s)=(sum_i G_i(s))/2 exactly; for multiplicity 4 this equals the sum of the two frozen pair residual functions and is independent of the chosen perfect matching')
    print('method=exact support-membership cells by inclusion-exclusion plus exact joint quadratic sign populations by Walsh inversion; no 2^149 physical-domain enumeration')
    print('crosscheck=all 57 multiplicity-2 group censuses reproduce the frozen pair-value census exactly; all 90 multiplicity-4 frozen matchings partition the four transforms exactly once')
    print('important=group-local image/state bits are not a joint separator width across the 147 groups')
    print('next=freeze this even-group image authority, then define and measure the 103 singleton signed-unit 2-adic lift before attempting any all-250-group joint state analysis')
    print('not_included=singleton signed-unit lift, joint state across groups, complete grouped-e0 separator, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
