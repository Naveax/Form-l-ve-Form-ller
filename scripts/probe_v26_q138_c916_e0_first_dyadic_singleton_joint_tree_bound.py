#!/usr/bin/env python3
import hashlib
import io
import json
import math
import sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_singleton_pair_joint_image as J

D = J.D
S = J.S
P = J.P
POS = J.POS
PHYS_N = J.PHYS_N
N = 103
STATES = 4
assert PHYS_N == 149


def relation_matrix(relations, u, v):
    if u < v:
        return relations[(u, v)]
    raw = relations[(v, u)]
    return tuple(
        tuple(raw[j][i] for j in range(STATES))
        for i in range(STATES)
    )


def relation_size(matrix):
    return sum(int(x) for row in matrix for x in row)


def relation_mask(matrix):
    out = 0
    bit = 0
    for row in matrix:
        for x in row:
            if x:
                out |= 1 << bit
            bit += 1
    return out


def validate_tree(nodes, edges):
    nodes = set(nodes)
    if len(nodes) == 1:
        assert not edges
        return
    assert len(edges) == len(nodes) - 1
    adj = {u: [] for u in nodes}
    for u, v in edges:
        assert u in nodes and v in nodes and u != v
        adj[u].append(v)
        adj[v].append(u)
    seen = set()
    stack = [min(nodes)]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        stack.extend(v for v in adj[u] if v not in seen)
    assert seen == nodes


def tree_count_and_marginals(nodes, edges, relations):
    nodes = tuple(sorted(nodes))
    validate_tree(nodes, edges)
    adj = {u: [] for u in nodes}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    memo = {}

    def message(src, dst):
        key = (src, dst)
        if key in memo:
            return memo[key]
        incoming = [w for w in adj[src] if w != dst]
        src_weight = [1] * STATES
        for w in incoming:
            msg = message(w, src)
            for s in range(STATES):
                src_weight[s] *= msg[s]

        matrix = relation_matrix(relations, src, dst)
        out = []
        for t in range(STATES):
            out.append(sum(
                src_weight[s]
                for s in range(STATES)
                if matrix[s][t]
            ))
        memo[key] = tuple(out)
        return memo[key]

    marginals = {}
    for u in nodes:
        weights = [1] * STATES
        for w in adj[u]:
            msg = message(w, u)
            for s in range(STATES):
                weights[s] *= msg[s]
        marginals[u] = tuple(weights)

    totals = {sum(m) for m in marginals.values()}
    assert len(totals) == 1
    total = totals.pop()
    assert total > 0
    return total, marginals


def synthetic_tree_dp_regression():
    n = 5
    relations = {}
    for u in range(n):
        for v in range(u + 1, n):
            matrix = []
            for s in range(STATES):
                row = []
                for t in range(STATES):
                    allowed = (
                        s == t
                        or ((s + 2 * t + u + v) % 4) != 0
                    )
                    row.append(bool(allowed))
                matrix.append(tuple(row))
            matrix = tuple(matrix)
            assert all(any(row) for row in matrix)
            assert all(any(matrix[s][t] for s in range(STATES))
                       for t in range(STATES))
            relations[(u, v)] = matrix

    edges = ((0, 1), (1, 2), (1, 3), (3, 4))
    got_count, got_marginals = tree_count_and_marginals(
        range(n), edges, relations
    )

    brute_count = 0
    brute_marginals = {u: [0] * STATES for u in range(n)}
    for assignment in product(range(STATES), repeat=n):
        ok = True
        for u, v in edges:
            matrix = relation_matrix(relations, u, v)
            if not matrix[assignment[u]][assignment[v]]:
                ok = False
                break
        if not ok:
            continue
        brute_count += 1
        for u, state in enumerate(assignment):
            brute_marginals[u][state] += 1

    assert got_count == brute_count
    assert {
        u: tuple(v) for u, v in brute_marginals.items()
    } == got_marginals

    greedy_edges, greedy_count, _history = greedy_growth_tree(
        0, n, relations
    )
    brute_greedy = 0
    for assignment in product(range(STATES), repeat=n):
        if all(
            relation_matrix(relations, u, v)[assignment[u]][assignment[v]]
            for u, v in greedy_edges
        ):
            brute_greedy += 1
    assert greedy_count == brute_greedy
    return {
        'nodes': n,
        'fixed_tree_count': got_count,
        'greedy_tree_count': greedy_count,
    }


def kruskal_tree(n, relations):
    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return True

    candidates = []
    for (u, v), matrix in relations.items():
        deg_u = tuple(sum(row) for row in matrix)
        deg_v = tuple(
            sum(matrix[s][t] for s in range(STATES))
            for t in range(STATES)
        )
        candidates.append((
            relation_size(matrix),
            max(deg_u),
            max(deg_v),
            u,
            v,
        ))
    candidates.sort()

    edges = []
    for _rsize, _du, _dv, u, v in candidates:
        if union(u, v):
            edges.append((u, v))
            if len(edges) == n - 1:
                break
    validate_tree(range(n), edges)
    return tuple(edges)


def greedy_growth_tree(root, n, relations):
    selected = {int(root)}
    edges = []
    history = []

    while len(selected) < n:
        current_count, marginals = tree_count_and_marginals(
            selected, edges, relations
        )
        best = None
        outside = [v for v in range(n) if v not in selected]
        for u in sorted(selected):
            mu = marginals[u]
            for v in outside:
                matrix = relation_matrix(relations, u, v)
                degrees = tuple(sum(row) for row in matrix)
                extension_count = sum(
                    mu[s] * degrees[s] for s in range(STATES)
                )
                assert extension_count >= current_count
                key = (
                    extension_count,
                    max(degrees),
                    relation_size(matrix),
                    u,
                    v,
                )
                if best is None or key < best[0]:
                    best = (key, u, v, degrees)
        assert best is not None
        key, u, v, degrees = best
        selected.add(v)
        edges.append((u, v))
        history.append({
            'new_node': v,
            'parent': u,
            'old_count': current_count,
            'new_count': key[0],
            'directional_degree_vector': list(degrees),
            'relation_size': key[2],
        })

    final_count, _ = tree_count_and_marginals(
        range(n), edges, relations
    )
    assert history[-1]['new_count'] == final_count
    return tuple(edges), final_count, tuple(history)


def star_tree(root, n):
    return tuple((root, v) for v in range(n) if v != root)


def build_real_bundles():
    with redirect_stdout(io.StringIO()):
        frozen = S.analyze()
    assert frozen['physical_shared_dimension'] == PHYS_N
    assert frozen['singleton_groups'] == N
    frozen_by_gid = {
        int(rec['group_id']): D.census_map(rec)
        for rec in frozen['groups']
    }

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

    one = J.make_constant_term(PHYS_N, 0)
    bundles = {}
    next_term_id = 1
    feature_index = 0
    for gid, (can, sectors) in enumerate(ordered):
        if len(sectors) != 1:
            continue
        group, next_term_id = D.build_group_terms(
            gid, can, sectors, next_term_id
        )
        bundle = J.make_bundle(
            group, 1 + 3 * feature_index, one, PHYS_N
        )
        feature_index += 1
        assert gid in frozen_by_gid
        assert set(bundle['values']) == set(frozen_by_gid[gid])
        bundles[gid] = bundle

    assert len(bundles) == N
    gids = tuple(sorted(bundles))
    assert tuple(sorted(frozen_by_gid)) == gids
    return one, bundles, frozen_by_gid, gids


def build_pair_relations(one, bundles, frozen_by_gid, gids):
    cache = {}
    for gid in gids:
        got = J.state_indicator_count(bundles[gid], one, cache)
        assert got == frozen_by_gid[gid]

    relations = {}
    size_hist = Counter()
    pair_marginal_crosschecks = 0
    local = {gid: i for i, gid in enumerate(gids)}

    for ai, gid in enumerate(gids):
        left = bundles[gid]
        lvalues = tuple(v for v, _coeff in J.state_specs(left))
        assert len(set(lvalues)) == STATES
        for hid in gids[ai + 1:]:
            right = bundles[hid]
            rvalues = tuple(v for v, _coeff in J.state_specs(right))
            assert len(set(rvalues)) == STATES
            rec = J.joint_census(left, right, cache)
            assert rec['left_marginal'] == frozen_by_gid[gid]
            assert rec['right_marginal'] == frozen_by_gid[hid]
            pair_marginal_crosschecks += 2

            counts = rec['joint_counts']
            matrix = tuple(
                tuple((lv, rv) in counts for rv in rvalues)
                for lv in lvalues
            )
            assert all(any(row) for row in matrix)
            assert all(
                any(matrix[s][t] for s in range(STATES))
                for t in range(STATES)
            )
            u, v = local[gid], local[hid]
            assert u < v
            relations[(u, v)] = matrix
            size = relation_size(matrix)
            assert size == rec['joint_image_size']
            size_hist[size] += 1

    expected_pairs = N * (N - 1) // 2
    assert len(relations) == expected_pairs == 5253
    assert pair_marginal_crosschecks == 2 * expected_pairs
    expected_hist = {
        5: 160,
        6: 688,
        8: 386,
        9: 1399,
        10: 207,
        11: 687,
        12: 646,
        13: 567,
        14: 11,
        16: 502,
    }
    assert dict(sorted(size_hist.items())) == expected_hist
    return relations, cache, pair_marginal_crosschecks


def describe_tree(edges, relations, gids):
    hist = Counter()
    directional_max_hist = Counter()
    records = []
    payload = []
    for u, v in edges:
        matrix = relation_matrix(relations, u, v)
        rsize = relation_size(matrix)
        max_uv = max(sum(row) for row in matrix)
        max_vu = max(
            sum(matrix[s][t] for s in range(STATES))
            for t in range(STATES)
        )
        hist[rsize] += 1
        directional_max_hist[(max_uv, max_vu)] += 1
        mask = relation_mask(matrix)
        gu, gv = int(gids[u]), int(gids[v])
        records.append({
            'left_group_id': gu,
            'right_group_id': gv,
            'joint_image_size': rsize,
            'relation_mask_hex': f'{mask:04x}',
            'max_left_to_right_degree': max_uv,
            'max_right_to_left_degree': max_vu,
        })
        payload.append(f'{gu}:{gv}:{mask:04x}')
    digest = hashlib.sha256('|'.join(payload).encode()).hexdigest()
    return {
        'edge_count': len(edges),
        'edge_joint_image_size_histogram': dict(sorted(hist.items())),
        'directional_max_degree_histogram': {
            str(k): v for k, v in sorted(directional_max_hist.items())
        },
        'edge_relation_digest_sha256': digest,
        'edges': records,
    }


def analyze():
    synthetic = synthetic_tree_dp_regression()
    with redirect_stdout(io.StringIO()):
        pair_regression = J.synthetic_regression()

    one, bundles, frozen_by_gid, gids = build_real_bundles()
    relations, cache, pair_marginal_crosschecks = build_pair_relations(
        one, bundles, frozen_by_gid, gids
    )

    kruskal_edges = kruskal_tree(N, relations)
    kruskal_count, _ = tree_count_and_marginals(
        range(N), kruskal_edges, relations
    )

    best_star = None
    for root in range(N):
        edges = star_tree(root, N)
        count, _ = tree_count_and_marginals(
            range(N), edges, relations
        )
        key = (count, int(gids[root]))
        if best_star is None or key < best_star[0]:
            best_star = (key, root, edges)
    assert best_star is not None

    greedy_results = []
    best_greedy = None
    for root in range(N):
        edges, count, history = greedy_growth_tree(
            root, N, relations
        )
        key = (count, int(gids[root]))
        greedy_results.append((int(gids[root]), count))
        if best_greedy is None or key < best_greedy[0]:
            best_greedy = (key, root, edges, history)
    assert best_greedy is not None

    candidates = [
        ('kruskal_min_joint_image', kruskal_count, kruskal_edges),
        ('best_star', best_star[0][0], best_star[2]),
        ('best_exact_incremental_greedy', best_greedy[0][0], best_greedy[2]),
    ]
    candidates.sort(key=lambda x: (x[1], x[0]))
    method, best_count, best_edges = candidates[0]

    check_count, _ = tree_count_and_marginals(
        range(N), best_edges, relations
    )
    assert check_count == best_count
    assert best_count < (1 << (2 * N))
    tree_bits = (best_count - 1).bit_length()
    tree_log2 = math.log2(best_count)
    physical_cap = 1 << PHYS_N
    certified_count = min(best_count, physical_cap)
    certified_bits = (certified_count - 1).bit_length()
    certified_log2 = math.log2(certified_count)

    tree_desc = describe_tree(best_edges, relations, gids)
    greedy_counts = sorted(greedy_results, key=lambda x: (x[1], x[0]))

    if best_count < physical_cap:
        decision = (
            'SINGLETON_103WAY_JOINT_IMAGE_TREE_UPPER_BOUND_BELOW_PHYSICAL_149'
        )
    else:
        decision = (
            'SINGLETON_TREE_BOUND_BEATS_ISOLATED_206_BUT_NOT_PHYSICAL_149'
        )

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'singleton_groups': N,
        'isolated_state_bits': 2 * N,
        'isolated_state_count': 1 << (2 * N),
        'physical_input_state_bits': PHYS_N,
        'physical_input_state_count': physical_cap,
        'synthetic_tree_dp_regression': synthetic,
        'upstream_pair_joint_regression': pair_regression,
        'pair_relation_count': len(relations),
        'pair_marginal_crosschecks': pair_marginal_crosschecks,
        'pair_joint_image_size_histogram': {
            5: 160,
            6: 688,
            8: 386,
            9: 1399,
            10: 207,
            11: 687,
            12: 646,
            13: 567,
            14: 11,
            16: 502,
        },
        'candidate_tree_counts': {
            'kruskal_min_joint_image': kruskal_count,
            'best_star': best_star[0][0],
            'best_exact_incremental_greedy': best_greedy[0][0],
        },
        'best_star_root_group_id': int(gids[best_star[1]]),
        'best_greedy_root_group_id': int(gids[best_greedy[1]]),
        'best_greedy_root_counts_top10': [
            {'root_group_id': gid, 'tree_count': count}
            for gid, count in greedy_counts[:10]
        ],
        'selected_tree_method': method,
        'selected_tree_consistent_assignment_count': best_count,
        'selected_tree_consistent_log2': tree_log2,
        'selected_tree_state_bits': tree_bits,
        'tree_gain_vs_isolated_log2_bits': (2 * N) - tree_log2,
        'tree_gain_vs_physical_log2_bits': PHYS_N - tree_log2,
        'certified_joint_image_upper_bound_count': certified_count,
        'certified_joint_image_upper_bound_log2': certified_log2,
        'certified_joint_image_state_bits': certified_bits,
        'selected_tree': tree_desc,
        'term_moment_cache_entries': len(cache),
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_SINGLETON_JOINT_TREE_BOUND')
    print('scope=rigorous upper bound on the 103-way singleton-output joint image using exact pairwise allowed-state relations and exact tree-consistency dynamic programming')
    print('theorem=the true 103-way output image is a subset of assignments satisfying every selected pair relation; restricting to any spanning tree preserves a valid superset, whose cardinality is counted exactly by sum-product DP')
    print('important=this bounds the joint image of the 103 singleton outputs only; it does not include the remaining 147 even-multiplicity outputs or establish complete C2/W_repr/arithmetic-work compression')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
