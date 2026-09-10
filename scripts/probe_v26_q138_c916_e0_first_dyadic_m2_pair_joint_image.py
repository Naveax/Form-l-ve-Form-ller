#!/usr/bin/env python3
import io
import json
import math
import sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_even_group_value_image_census as E
import probe_v26_q138_c916_e0_first_dyadic_group_output_pair_dependency as D

P = D.P
POS = D.POS
PHYS_N = D.PHYS_N
assert PHYS_N == 149


def submasks(mask):
    s = int(mask)
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & mask


def census_map(record):
    return {
        int(item['value']): int(item['multiplicity'])
        for item in record['value_multiplicity']
    }


def eval_term(term, x):
    q = P.eval_anchor_sign(term['anchor'], x)
    if q is None:
        return 0
    c = int(term['coefficient'])
    return -c if q else c


def eval_group(group, x):
    return sum(eval_term(t, x) for t in group['terms'])


def physical_character_moment(terms, support_mask, char_mask, intersection_cache, moment_cache):
    n = len(terms)
    full = (1 << n) - 1
    assert 0 <= support_mask <= full
    assert char_mask & ~support_mask == 0

    if support_mask == 0:
        assert char_mask == 0
        return 1 << PHYS_N

    support_ids = tuple(
        int(terms[i]['term_id'])
        for i in range(n)
        if (support_mask >> i) & 1
    )
    char_ids = tuple(
        int(terms[i]['term_id'])
        for i in range(n)
        if (char_mask >> i) & 1
    )
    key = (support_ids, char_ids)
    if key in moment_cache:
        return moment_cache[key]

    if support_ids in intersection_cache:
        inter = intersection_cache[support_ids]
    else:
        constraints = []
        for i in range(n):
            if (support_mask >> i) & 1:
                constraints.extend(terms[i]['anchor']['physical_support_constraints'])
        inter = P.C.P.U.T.rref(constraints, n=PHYS_N)
        intersection_cache[support_ids] = inter

    if inter is None:
        out = 0
    else:
        _rank, ix0, ibasis = inter
        ibasis = tuple(ibasis)
        if char_mask == 0:
            out = 1 << len(ibasis)
        else:
            c = 0
            lin = 0
            rows = [0] * len(ibasis)
            for i in range(n):
                if not ((char_mask >> i) & 1):
                    continue
                rc, rlin, rrows = P.restrict_anchor_sign(
                    terms[i]['anchor'], ix0, ibasis
                )
                c ^= rc
                lin ^= rlin
                assert len(rrows) == len(rows)
                for j, row in enumerate(rrows):
                    rows[j] ^= row
            out = D.full_quadratic_moment(c, lin, tuple(rows))

    moment_cache[key] = int(out)
    return int(out)


def exact_signed_cells(terms, intersection_cache, moment_cache):
    n = len(terms)
    assert 1 <= n <= 4
    full = (1 << n) - 1

    def moment(support_mask, char_mask):
        return physical_character_moment(
            terms, support_mask, char_mask,
            intersection_cache, moment_cache
        )

    def exact_cell_character(active_mask, char_mask):
        assert char_mask & ~active_mask == 0
        inactive = full ^ active_mask
        total = 0
        for u in submasks(inactive):
            z = moment(active_mask | u, char_mask)
            total += -z if (u.bit_count() & 1) else z
        return total

    populations = Counter()
    for active in range(full + 1):
        cell_size = exact_cell_character(active, 0)
        assert cell_size >= 0
        if not cell_size:
            continue

        chars = {
            char: exact_cell_character(active, char)
            for char in submasks(active)
        }
        assert chars[0] == cell_size

        k = active.bit_count()
        divisor = 1 << k
        for negative in submasks(active):
            num = 0
            for char, walsh in chars.items():
                num += -walsh if ((negative & char).bit_count() & 1) else walsh
            assert num % divisor == 0, (active, negative, num, divisor)
            population = num // divisor
            assert population >= 0, (active, negative, population)
            if population:
                populations[(active, negative)] += population

    assert sum(populations.values()) == (1 << PHYS_N)
    return populations


def pair_joint_census(left, right, intersection_cache, moment_cache):
    assert left['multiplicity'] == right['multiplicity'] == 2
    assert len(left['terms']) == len(right['terms']) == 2

    terms = tuple(left['terms']) + tuple(right['terms'])
    assert len({int(t['term_id']) for t in terms}) == 4

    populations = exact_signed_cells(
        terms, intersection_cache, moment_cache
    )
    counts = Counter()

    for (active, negative), population in populations.items():
        lv = 0
        rv = 0
        for i, term in enumerate(terms):
            if not ((active >> i) & 1):
                continue
            z = int(term['coefficient'])
            if (negative >> i) & 1:
                z = -z
            if i < 2:
                lv += z
            else:
                rv += z
        counts[(lv, rv)] += population

    counts = Counter({k: int(v) for k, v in counts.items() if v})
    assert sum(counts.values()) == (1 << PHYS_N)
    assert all(v > 0 for v in counts.values())

    lm = Counter()
    rm = Counter()
    for (lv, rv), population in counts.items():
        lm[lv] += population
        rm[rv] += population

    return {
        'joint_counts': counts,
        'left_marginal': dict(sorted(lm.items())),
        'right_marginal': dict(sorted(rm.items())),
        'joint_image_size': len(counts),
        'joint_state_bits': (len(counts) - 1).bit_length(),
    }


def make_synthetic_term(term_id, anchor, coefficient, ambient):
    return {
        'term_id': int(term_id),
        'group_id': -1,
        'kind': 'synthetic_m2',
        'coefficient': int(coefficient),
        'anchor': anchor,
        'ambient_dimension': int(ambient),
    }


def synthetic_regression():
    n = 5
    anchors = (
        P.make_synthetic_anchor((), n, 'linear'),
        P.make_synthetic_anchor(((1, 0),), n, 'quadratic'),
        P.make_synthetic_anchor(((2, 1),), n, 'one'),
        P.make_synthetic_anchor(((4, 0),), n, 'linear'),
        P.make_synthetic_anchor(((1, 1), (8, 0)), n, 'quadratic'),
        P.make_synthetic_anchor(((3, 0),), n, 'zero'),
    )
    specs = (
        ((0, 1), (1, 2)),
        ((0, 2), (3, 1)),
        ((1, 1), (4, 2)),
        ((2, 2), (5, 4)),
        ((3, 1), (4, 4)),
        ((0, 4), (5, 2)),
    )

    groups = []
    tid = 1
    for gid, spec in enumerate(specs):
        terms = []
        for anchor_index, coefficient in spec:
            terms.append(make_synthetic_term(
                tid, anchors[anchor_index], coefficient, n
            ))
            tid += 1
        groups.append({
            'group_id': gid,
            'multiplicity': 2,
            'terms': tuple(terms),
        })

    def local_moment(terms, support_mask, char_mask, icache, mcache):
        m = len(terms)
        assert char_mask & ~support_mask == 0
        if support_mask == 0:
            assert char_mask == 0
            return 1 << n
        support_ids = tuple(
            int(terms[i]['term_id'])
            for i in range(m)
            if (support_mask >> i) & 1
        )
        char_ids = tuple(
            int(terms[i]['term_id'])
            for i in range(m)
            if (char_mask >> i) & 1
        )
        key = (support_ids, char_ids)
        if key in mcache:
            return mcache[key]
        if support_ids in icache:
            inter = icache[support_ids]
        else:
            constraints = []
            for i in range(m):
                if (support_mask >> i) & 1:
                    constraints.extend(
                        terms[i]['anchor']['physical_support_constraints']
                    )
            inter = P.C.P.U.T.rref(constraints, n=n)
            icache[support_ids] = inter
        if inter is None:
            out = 0
        else:
            _rank, ix0, ibasis = inter
            ibasis = tuple(ibasis)
            if char_mask == 0:
                out = 1 << len(ibasis)
            else:
                c = 0
                lin = 0
                rows = [0] * len(ibasis)
                for i in range(m):
                    if not ((char_mask >> i) & 1):
                        continue
                    rc, rlin, rrows = P.restrict_anchor_sign(
                        terms[i]['anchor'], ix0, ibasis
                    )
                    c ^= rc
                    lin ^= rlin
                    for j, row in enumerate(rrows):
                        rows[j] ^= row
                out = D.full_quadratic_moment(c, lin, tuple(rows))
        mcache[key] = int(out)
        return int(out)

    def local_cells(terms, icache, mcache):
        m = len(terms)
        full = (1 << m) - 1
        def exact_char(active, char):
            inactive = full ^ active
            total = 0
            for u in submasks(inactive):
                z = local_moment(terms, active | u, char, icache, mcache)
                total += -z if (u.bit_count() & 1) else z
            return total
        pops = Counter()
        for active in range(full + 1):
            size = exact_char(active, 0)
            assert size >= 0
            if not size:
                continue
            chars = {c: exact_char(active, c) for c in submasks(active)}
            divisor = 1 << active.bit_count()
            for negative in submasks(active):
                num = sum(
                    (-w if ((negative & c).bit_count() & 1) else w)
                    for c, w in chars.items()
                )
                assert num % divisor == 0
                pop = num // divisor
                assert pop >= 0
                if pop:
                    pops[(active, negative)] += pop
        assert sum(pops.values()) == (1 << n)
        return pops

    tested = 0
    icache = {}
    mcache = {}
    for left, right in combinations(groups, 2):
        terms = tuple(left['terms']) + tuple(right['terms'])
        pops = local_cells(terms, icache, mcache)
        got = Counter()
        for (active, negative), pop in pops.items():
            lv = rv = 0
            for i, term in enumerate(terms):
                if not ((active >> i) & 1):
                    continue
                z = int(term['coefficient'])
                if (negative >> i) & 1:
                    z = -z
                if i < 2:
                    lv += z
                else:
                    rv += z
            got[(lv, rv)] += pop

        brute = Counter(
            (eval_group(left, x), eval_group(right, x))
            for x in range(1 << n)
        )
        assert got == brute, (
            left['group_id'], right['group_id'], got, brute
        )
        tested += 1

    assert tested == 15
    return {
        'groups': len(groups),
        'pairs': tested,
        'domain_points_checked': tested * (1 << n),
    }


def dependency_component_sizes(gids, edges):
    parent = {int(g): int(g) for g in gids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(int(a)), find(int(b))
        if ra != rb:
            parent[rb] = ra

    for a, b in edges:
        union(a, b)

    sizes = Counter(find(g) for g in gids)
    return sorted(sizes.values(), reverse=True)


def analyze():
    regression = synthetic_regression()

    with redirect_stdout(io.StringIO()):
        frozen = E.analyze()

    assert frozen['position'] == POS
    assert frozen['physical_shared_dimension'] == PHYS_N
    assert frozen['support_groups'] == 250
    assert frozen['support_multiplicity_histogram'] == {1: 103, 2: 57, 4: 90}
    assert frozen['image_size_by_group_multiplicity'][2] == {3: 6, 5: 51}

    frozen_m2 = {
        int(rec['group_id']): {
            'counts': census_map(rec),
            'image_size': int(rec['image_size']),
            'state_bits': int(rec['state_bits']),
        }
        for rec in frozen['groups']
        if int(rec['multiplicity']) == 2
    }
    assert len(frozen_m2) == 57

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

    groups = {}
    next_term_id = 1
    for gid, (can, sectors) in enumerate(ordered):
        if len(sectors) != 2:
            continue
        group, next_term_id = D.build_group_terms(
            gid, can, sectors, next_term_id
        )
        assert group['multiplicity'] == 2
        assert len(group['terms']) == 2
        assert gid in frozen_m2
        groups[gid] = group
    assert len(groups) == 57
    gids = sorted(groups)
    assert gids == sorted(frozen_m2)

    pair_count = 0
    cartesian_hist = Counter()
    joint_size_hist = Counter()
    joint_bits_hist = Counter()
    missing_hist = Counter()
    integer_bit_saving_hist = Counter()
    projection_relation_hist = Counter()
    subcartesian_edges = []
    strongest = []
    marginal_crosschecks = 0
    minimum_joint_size = None
    maximum_cardinality_gain = 0.0

    intersection_cache = {}
    moment_cache = {}

    for ai, gid in enumerate(gids):
        left = groups[gid]
        for hid in gids[ai + 1:]:
            right = groups[hid]
            rec = pair_joint_census(
                left, right, intersection_cache, moment_cache
            )
            pair_count += 1

            lc = frozen_m2[gid]
            rc = frozen_m2[hid]
            assert rec['left_marginal'] == lc['counts'], (
                gid, hid, 'left marginal'
            )
            assert rec['right_marginal'] == rc['counts'], (
                gid, hid, 'right marginal'
            )
            marginal_crosschecks += 2

            cart = lc['image_size'] * rc['image_size']
            size = int(rec['joint_image_size'])
            bits = int(rec['joint_state_bits'])
            assert 1 <= size <= cart

            separate_bits = lc['state_bits'] + rc['state_bits']
            integer_saving = separate_bits - bits
            assert integer_saving >= 0

            missing = cart - size
            gain = math.log2(cart) - math.log2(size)
            maximum_cardinality_gain = max(maximum_cardinality_gain, gain)

            relation, _ = P.support_relation(
                left['projection_anchor'],
                right['projection_anchor'],
                PHYS_N,
            )

            cartesian_hist[cart] += 1
            joint_size_hist[size] += 1
            joint_bits_hist[bits] += 1
            missing_hist[missing] += 1
            integer_bit_saving_hist[integer_saving] += 1
            projection_relation_hist[relation] += 1

            if size < cart:
                subcartesian_edges.append((gid, hid))
                strongest.append({
                    'left_group_id': gid,
                    'right_group_id': hid,
                    'left_image_size': lc['image_size'],
                    'right_image_size': rc['image_size'],
                    'cartesian_image_size': cart,
                    'joint_image_size': size,
                    'joint_state_bits': bits,
                    'separate_state_bits': separate_bits,
                    'integer_bit_saving': integer_saving,
                    'missing_cartesian_pairs': missing,
                    'exact_cardinality_gain_log2': gain,
                    'projection_support_relation': relation,
                })

            if minimum_joint_size is None or size < minimum_joint_size:
                minimum_joint_size = size

    assert pair_count == 57 * 56 // 2 == 1596
    assert marginal_crosschecks == 2 * pair_count
    assert dict(sorted(cartesian_hist.items())) == {
        9: 15,
        15: 306,
        25: 1275,
    }

    components = dependency_component_sizes(gids, subcartesian_edges)
    component_hist = dict(sorted(Counter(components).items()))

    strongest.sort(
        key=lambda r: (
            -r['exact_cardinality_gain_log2'],
            r['joint_image_size'],
            r['left_group_id'],
            r['right_group_id'],
        )
    )
    strongest = strongest[:20]

    subcartesian = len(subcartesian_edges)
    full_cartesian = pair_count - subcartesian
    if subcartesian:
        decision = 'M2_PAIR_SUBCARTESIAN_NONLINEAR_JOINT_IMAGES_FOUND'
    else:
        decision = 'M2_PAIR_ALL_FULL_CARTESIAN'

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'synthetic_m2_joint_regression': regression,
        'raw_e0_sectors': raw,
        'support_groups': 250,
        'support_multiplicity_histogram': {1: 103, 2: 57, 4: 90},
        'multiplicity2_groups': 57,
        'multiplicity2_pairs': pair_count,
        'isolated_m2_image_size_histogram': {3: 6, 5: 51},
        'cartesian_pair_image_size_histogram': dict(sorted(cartesian_hist.items())),
        'joint_image_size_histogram': dict(sorted(joint_size_hist.items())),
        'joint_state_bits_histogram': dict(sorted(joint_bits_hist.items())),
        'missing_cartesian_state_histogram': dict(sorted(missing_hist.items())),
        'integer_bit_saving_histogram': dict(sorted(integer_bit_saving_hist.items())),
        'projection_support_relation_histogram': dict(sorted(projection_relation_hist.items())),
        'subcartesian_pair_count': subcartesian,
        'full_cartesian_pair_count': full_cartesian,
        'subcartesian_dependency_component_sizes': components,
        'subcartesian_dependency_component_size_histogram': component_hist,
        'minimum_joint_image_size': int(minimum_joint_size),
        'maximum_exact_log2_cardinality_gain_bits': maximum_cardinality_gain,
        'pair_marginal_crosschecks': marginal_crosschecks,
        'cached_support_intersections': len(intersection_cache),
        'cached_character_moments': len(moment_cache),
        'strongest_joint_image_examples': strongest,
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M2_PAIR_JOINT_IMAGE')
    print('scope=exact joint value-image census for all 1596 unordered pairs among the 57 multiplicity-2 C916 e0 first-dyadic residual group outputs on the common 149-bit physical domain')
    print('method=for each pair, enumerate exact signed-support cells of the four post-Gauss sector terms using affine inclusion-exclusion plus exact quadratic-character Walsh inversion; no 2^149 physical-domain enumeration')
    print('important=subcartesian pair images prove nonlinear output dependence only for the 57 multiplicity-2 family; they do not by themselves establish a 57-way or all-250 joint-state bound')
    print('not_included=singleton/m2 cross pairs, multiplicity-4 pairs, higher-order constraints, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
