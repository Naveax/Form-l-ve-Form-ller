#!/usr/bin/env python3
import io
import json
import math
import sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_even_group_value_image_census as E
import probe_v26_q138_c916_e0_first_dyadic_group_output_pair_dependency as D
import probe_v26_q138_c916_e0_first_dyadic_singleton_value_image_census as S

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
    z = int(term['coefficient'])
    return -z if q else z


def eval_group(group, x):
    return sum(eval_term(t, x) for t in group['terms'])


def character_moment(terms, support_mask, char_mask, ambient, intersection_cache, moment_cache):
    n = len(terms)
    assert char_mask & ~support_mask == 0
    if support_mask == 0:
        assert char_mask == 0
        return 1 << ambient

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
    key = (ambient, support_ids, char_ids)
    if key in moment_cache:
        return moment_cache[key]

    ikey = (ambient, support_ids)
    if ikey in intersection_cache:
        inter = intersection_cache[ikey]
    else:
        constraints = []
        for i in range(n):
            if (support_mask >> i) & 1:
                constraints.extend(
                    terms[i]['anchor']['physical_support_constraints']
                )
        inter = P.C.P.U.T.rref(constraints, n=ambient)
        intersection_cache[ikey] = inter

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


def exact_signed_cells(terms, ambient, intersection_cache, moment_cache):
    n = len(terms)
    assert 1 <= n <= 4
    full = (1 << n) - 1

    def exact_character(active, char):
        inactive = full ^ active
        total = 0
        for u in submasks(inactive):
            z = character_moment(
                terms, active | u, char, ambient,
                intersection_cache, moment_cache
            )
            total += -z if (u.bit_count() & 1) else z
        return total

    populations = Counter()
    for active in range(full + 1):
        cell_size = exact_character(active, 0)
        assert cell_size >= 0
        if not cell_size:
            continue
        chars = {
            c: exact_character(active, c)
            for c in submasks(active)
        }
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
                populations[(active, negative)] += pop

    assert sum(populations.values()) == (1 << ambient)
    return populations


def pair_joint_census(left, right, ambient, intersection_cache, moment_cache):
    lterms = tuple(left['terms'])
    rterms = tuple(right['terms'])
    assert len(lterms) == len(rterms) == 2
    terms = lterms + rterms
    assert len({int(t['term_id']) for t in terms}) == 4

    pops = exact_signed_cells(
        terms, ambient, intersection_cache, moment_cache
    )
    counts = Counter()
    for (active, negative), pop in pops.items():
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
        counts[(lv, rv)] += pop

    lm = Counter()
    rm = Counter()
    for (lv, rv), pop in counts.items():
        lm[lv] += pop
        rm[rv] += pop
    assert sum(counts.values()) == (1 << ambient)
    return {
        'joint_counts': Counter({k: int(v) for k, v in counts.items() if v}),
        'left_marginal': dict(sorted(lm.items())),
        'right_marginal': dict(sorted(rm.items())),
        'joint_image_size': len(counts),
        'joint_state_bits': (len(counts) - 1).bit_length(),
    }


def make_term(term_id, anchor, coefficient, ambient):
    return {
        'term_id': int(term_id),
        'group_id': -1,
        'kind': 'synthetic',
        'coefficient': int(coefficient),
        'anchor': anchor,
        'ambient_dimension': int(ambient),
    }


def synthetic_regression():
    n = 5
    zero = P.make_synthetic_anchor((), n, 'zero')
    projection_a = P.make_synthetic_anchor(((1, 0),), n, 'zero')
    gauss_a = P.make_synthetic_anchor(((1, 0), (2, 1)), n, 'quadratic')
    projection_b = P.make_synthetic_anchor(((4, 1),), n, 'zero')
    gauss_b = P.make_synthetic_anchor(((4, 1), (8, 0)), n, 'linear')
    m2_anchors = (
        P.make_synthetic_anchor((), n, 'linear'),
        P.make_synthetic_anchor(((2, 0),), n, 'quadratic'),
        P.make_synthetic_anchor(((3, 1),), n, 'one'),
        P.make_synthetic_anchor(((8, 0),), n, 'linear'),
    )

    singletons = (
        {
            'group_id': 0, 'multiplicity': 1,
            'terms': (
                make_term(1, gauss_a, 2, n),
                make_term(2, projection_a, -4, n),
            ),
        },
        {
            'group_id': 1, 'multiplicity': 1,
            'terms': (
                make_term(3, gauss_b, 1, n),
                make_term(4, projection_b, -2, n),
            ),
        },
        {
            'group_id': 2, 'multiplicity': 1,
            'terms': (
                make_term(5, P.make_synthetic_anchor((), n, 'quadratic'), 2, n),
                make_term(6, zero, -4, n),
            ),
        },
    )
    m2 = (
        {
            'group_id': 10, 'multiplicity': 2,
            'terms': (
                make_term(20, m2_anchors[0], 1, n),
                make_term(21, m2_anchors[1], 2, n),
            ),
        },
        {
            'group_id': 11, 'multiplicity': 2,
            'terms': (
                make_term(22, m2_anchors[2], 2, n),
                make_term(23, m2_anchors[3], 1, n),
            ),
        },
        {
            'group_id': 12, 'multiplicity': 2,
            'terms': (
                make_term(24, m2_anchors[1], 4, n),
                make_term(25, m2_anchors[3], 2, n),
            ),
        },
    )

    icache = {}
    mcache = {}
    tested = 0
    for left, right in product(singletons, m2):
        got = pair_joint_census(
            left, right, n, icache, mcache
        )
        brute = Counter(
            (eval_group(left, x), eval_group(right, x))
            for x in range(1 << n)
        )
        assert got['joint_counts'] == brute, (
            left['group_id'], right['group_id'],
            got['joint_counts'], brute
        )
        tested += 1
    assert tested == 9
    return {
        'singleton_groups': len(singletons),
        'm2_groups': len(m2),
        'cross_pairs': tested,
        'domain_points_checked': tested * (1 << n),
    }


def component_sizes(nodes, edges):
    parent = {n: n for n in nodes}

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
    c = Counter(find(n) for n in nodes)
    return sorted(c.values(), reverse=True)


def analyze():
    regression = synthetic_regression()

    with redirect_stdout(io.StringIO()):
        singleton = S.analyze()
        even = E.analyze()

    sfrozen = {
        int(rec['group_id']): census_map(rec)
        for rec in singleton['groups']
    }
    m2frozen = {
        int(rec['group_id']): census_map(rec)
        for rec in even['groups']
        if int(rec['multiplicity']) == 2
    }
    assert len(sfrozen) == 103
    assert len(m2frozen) == 57
    assert all(len(v) == 4 for v in sfrozen.values())
    assert Counter(len(v) for v in m2frozen.values()) == Counter({3: 6, 5: 51})

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

    sgroups = {}
    m2groups = {}
    tid = 1
    for gid, (can, sectors) in enumerate(ordered):
        if len(sectors) not in (1, 2):
            continue
        group, tid = D.build_group_terms(gid, can, sectors, tid)
        assert len(group['terms']) == 2
        if len(sectors) == 1:
            sgroups[gid] = group
        else:
            m2groups[gid] = group
    assert len(sgroups) == 103 and len(m2groups) == 57
    assert set(sgroups) == set(sfrozen)
    assert set(m2groups) == set(m2frozen)

    cart_hist = Counter()
    joint_hist = Counter()
    missing_hist = Counter()
    bit_saving_hist = Counter()
    sub_edges = []
    strongest = []
    marginal_checks = 0
    icache = {}
    mcache = {}

    for sgid in sorted(sgroups):
        left = sgroups[sgid]
        for mgid in sorted(m2groups):
            right = m2groups[mgid]
            rec = pair_joint_census(
                left, right, PHYS_N, icache, mcache
            )
            assert rec['left_marginal'] == sfrozen[sgid]
            assert rec['right_marginal'] == m2frozen[mgid]
            marginal_checks += 2

            cart = len(sfrozen[sgid]) * len(m2frozen[mgid])
            size = rec['joint_image_size']
            assert size <= cart
            separate_bits = 2 + (len(m2frozen[mgid]) - 1).bit_length()
            saving = separate_bits - rec['joint_state_bits']
            assert saving >= 0

            cart_hist[cart] += 1
            joint_hist[size] += 1
            missing_hist[cart - size] += 1
            bit_saving_hist[saving] += 1
            if size < cart:
                sub_edges.append((sgid, mgid))
                strongest.append({
                    'singleton_group_id': sgid,
                    'm2_group_id': mgid,
                    'm2_image_size': len(m2frozen[mgid]),
                    'cartesian_image_size': cart,
                    'joint_image_size': size,
                    'joint_state_bits': rec['joint_state_bits'],
                    'separate_state_bits': separate_bits,
                    'integer_bit_saving': saving,
                    'missing_cartesian_states': cart - size,
                    'exact_cardinality_gain_log2':
                        math.log2(cart) - math.log2(size),
                })

    pairs = 103 * 57
    assert sum(cart_hist.values()) == pairs == 5871
    assert dict(sorted(cart_hist.items())) == {
        12: 618,
        20: 5253,
    }
    assert marginal_checks == 2 * pairs

    nodes = (
        tuple(('s', g) for g in sorted(sgroups))
        + tuple(('m2', g) for g in sorted(m2groups))
    )
    tagged_edges = [
        (('s', a), ('m2', b)) for a, b in sub_edges
    ]
    comps = component_sizes(nodes, tagged_edges)

    strongest.sort(key=lambda r: (
        -r['exact_cardinality_gain_log2'],
        r['joint_image_size'],
        r['singleton_group_id'],
        r['m2_group_id'],
    ))
    strongest = strongest[:20]

    sub = len(sub_edges)
    if sub:
        decision = 'SINGLETON_M2_SUBCARTESIAN_CROSS_JOINT_IMAGES_FOUND'
    else:
        decision = 'SINGLETON_M2_ALL_FULL_CARTESIAN'

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'synthetic_cross_regression': regression,
        'singleton_groups': 103,
        'multiplicity2_groups': 57,
        'cross_pairs': pairs,
        'cartesian_pair_image_size_histogram': dict(sorted(cart_hist.items())),
        'joint_image_size_histogram': dict(sorted(joint_hist.items())),
        'missing_cartesian_state_histogram': dict(sorted(missing_hist.items())),
        'integer_bit_saving_histogram': dict(sorted(bit_saving_hist.items())),
        'subcartesian_cross_pair_count': sub,
        'full_cartesian_cross_pair_count': pairs - sub,
        'subcartesian_cross_component_sizes': comps,
        'subcartesian_cross_component_size_histogram':
            dict(sorted(Counter(comps).items())),
        'pair_marginal_crosschecks': marginal_checks,
        'cached_support_intersections': len(icache),
        'cached_character_moments': len(mcache),
        'strongest_joint_image_examples': strongest,
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_SINGLETON_M2_CROSS_JOINT_IMAGE')
    print('scope=exact nonlinear joint value images for all 5871 singleton-by-multiplicity2 output pairs on the common 149-bit physical domain')
    print('method=exact four-term signed-support cell decomposition with affine inclusion-exclusion and quadratic-character Walsh inversion; singleton projection baselines are included as exact constant-sign support terms')
    print('important=this is the cross-family relation layer needed before a combined 160-output singleton+m2 tree bound')
    print('not_included=m4 outputs, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
