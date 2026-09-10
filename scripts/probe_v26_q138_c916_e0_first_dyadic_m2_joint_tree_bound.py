#!/usr/bin/env python3
import hashlib
import io
import json
import math
import sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_m2_pair_joint_image as M

E = M.E
D = M.D
P = M.P
POS = M.POS
PHYS_N = M.PHYS_N
N = 57
assert PHYS_N == 149


def relation_matrix(relations, u, v):
    if u < v:
        return relations[(u, v)]
    raw = relations[(v, u)]
    return tuple(
        tuple(raw[j][i] for j in range(len(raw)))
        for i in range(len(raw[0]))
    )


def relation_size(matrix):
    return sum(int(x) for row in matrix for x in row)


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


def tree_count_and_marginals(nodes, edges, relations, state_counts):
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
        src_weight = [1] * state_counts[src]
        for w in incoming:
            msg = message(w, src)
            assert len(msg) == state_counts[src]
            for s in range(state_counts[src]):
                src_weight[s] *= msg[s]

        matrix = relation_matrix(relations, src, dst)
        assert len(matrix) == state_counts[src]
        assert len(matrix[0]) == state_counts[dst]
        out = []
        for t in range(state_counts[dst]):
            out.append(sum(
                src_weight[s]
                for s in range(state_counts[src])
                if matrix[s][t]
            ))
        memo[key] = tuple(out)
        return memo[key]

    marginals = {}
    for u in nodes:
        weights = [1] * state_counts[u]
        for w in adj[u]:
            msg = message(w, u)
            for s in range(state_counts[u]):
                weights[s] *= msg[s]
        marginals[u] = tuple(weights)

    totals = {sum(m) for m in marginals.values()}
    assert len(totals) == 1
    total = totals.pop()
    assert total > 0
    return total, marginals


def synthetic_tree_regression():
    state_counts = (3, 5, 4, 3)
    n = len(state_counts)
    relations = {}
    for u in range(n):
        for v in range(u + 1, n):
            matrix = tuple(
                tuple(
                    (
                        (s + 2 * t + u + v) % 3 != 0
                        or s == (t % state_counts[u])
                    )
                    for t in range(state_counts[v])
                )
                for s in range(state_counts[u])
            )
            assert all(any(row) for row in matrix)
            assert all(
                any(matrix[s][t] for s in range(state_counts[u]))
                for t in range(state_counts[v])
            )
            relations[(u, v)] = matrix

    edges = ((0, 1), (1, 2), (1, 3))
    got, marginals = tree_count_and_marginals(
        range(n), edges, relations, state_counts
    )

    brute = 0
    brute_marginals = {
        u: [0] * state_counts[u] for u in range(n)
    }
    import itertools
    for assignment in itertools.product(
        *(range(state_counts[u]) for u in range(n))
    ):
        if not all(
            relation_matrix(relations, u, v)[assignment[u]][assignment[v]]
            for u, v in edges
        ):
            continue
        brute += 1
        for u, s in enumerate(assignment):
            brute_marginals[u][s] += 1

    assert got == brute
    assert {
        u: tuple(v) for u, v in brute_marginals.items()
    } == marginals
    return {'nodes': n, 'tree_count': got}


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
        prod = len(matrix) * len(matrix[0])
        rsize = relation_size(matrix)
        candidates.append((Fraction(rsize, prod), rsize, u, v))
    candidates.sort()

    edges = []
    for _density, _size, u, v in candidates:
        if union(u, v):
            edges.append((u, v))
            if len(edges) == n - 1:
                break
    validate_tree(range(n), edges)
    return tuple(edges)


def greedy_growth_tree(root, n, relations, state_counts):
    selected = {int(root)}
    edges = []
    history = []

    while len(selected) < n:
        current_count, marginals = tree_count_and_marginals(
            selected, edges, relations, state_counts
        )
        best = None
        outside = [v for v in range(n) if v not in selected]
        for u in sorted(selected):
            mu = marginals[u]
            for v in outside:
                matrix = relation_matrix(relations, u, v)
                degrees = tuple(sum(row) for row in matrix)
                extension = sum(
                    mu[s] * degrees[s]
                    for s in range(state_counts[u])
                )
                assert extension >= current_count
                key = (
                    extension,
                    relation_size(matrix),
                    max(degrees),
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
            'relation_size': key[1],
            'max_parent_to_child_degree': key[2],
            'degree_vector': list(degrees),
        })

    final_count, _ = tree_count_and_marginals(
        range(n), edges, relations, state_counts
    )
    assert final_count == history[-1]['new_count']
    return tuple(edges), final_count, tuple(history)


def star_tree(root, n):
    return tuple((root, v) for v in range(n) if v != root)


def build_real():
    with redirect_stdout(io.StringIO()):
        upstream = M.analyze()
        frozen = E.analyze()

    assert upstream['multiplicity2_groups'] == N
    assert upstream['multiplicity2_pairs'] == N * (N - 1) // 2
    assert frozen['image_size_by_group_multiplicity'][2] == {3: 6, 5: 51}

    frozen_m2 = {
        int(rec['group_id']): M.census_map(rec)
        for rec in frozen['groups']
        if int(rec['multiplicity']) == 2
    }
    assert len(frozen_m2) == N

    e0, _e1, _half = P.C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    for zc in range(4):
        for zs, cls in e0[zc]:
            can = P.C.P.U.H.support_for(POS, zs, cls)
            if can is not None:
                grouped[can].append((zs, cls))
    ordered = list(sorted(grouped.items(), key=lambda kv: kv[0]))
    assert len(ordered) == 250

    groups = {}
    tid = 1
    for gid, (can, sectors) in enumerate(ordered):
        if len(sectors) != 2:
            continue
        group, tid = D.build_group_terms(gid, can, sectors, tid)
        groups[gid] = group
    assert len(groups) == N

    gids = tuple(sorted(groups))
    assert tuple(sorted(frozen_m2)) == gids
    local = {gid: i for i, gid in enumerate(gids)}

    values = {
        gid: tuple(sorted(frozen_m2[gid]))
        for gid in gids
    }
    state_counts = tuple(len(values[gid]) for gid in gids)
    assert Counter(state_counts) == Counter({3: 6, 5: 51})

    icache = {}
    mcache = {}
    relations = {}
    hist = Counter()
    marginals = 0

    for ai, gid in enumerate(gids):
        for hid in gids[ai + 1:]:
            rec = M.pair_joint_census(
                groups[gid], groups[hid], icache, mcache
            )
            assert rec['left_marginal'] == frozen_m2[gid]
            assert rec['right_marginal'] == frozen_m2[hid]
            marginals += 2

            lv = values[gid]
            rv = values[hid]
            counts = rec['joint_counts']
            matrix = tuple(
                tuple((a, b) in counts for b in rv)
                for a in lv
            )
            assert all(any(row) for row in matrix)
            assert all(
                any(matrix[s][t] for s in range(len(lv)))
                for t in range(len(rv))
            )
            u, v = local[gid], local[hid]
            relations[(u, v)] = matrix
            hist[relation_size(matrix)] += 1

    assert len(relations) == N * (N - 1) // 2
    assert marginals == 2 * len(relations)
    assert dict(sorted(hist.items())) == upstream['joint_image_size_histogram']
    return upstream, gids, state_counts, relations


def analyze():
    synthetic = synthetic_tree_regression()
    upstream, gids, state_counts, relations = build_real()

    isolated_count = 1
    for nstates in state_counts:
        isolated_count *= nstates
    isolated_bits = (isolated_count - 1).bit_length()
    isolated_log2 = math.log2(isolated_count)
    assert isolated_count == (3 ** 6) * (5 ** 51)
    assert isolated_bits == 128

    k_edges = kruskal_tree(N, relations)
    k_count, _ = tree_count_and_marginals(
        range(N), k_edges, relations, state_counts
    )

    best_star = None
    for root in range(N):
        edges = star_tree(root, N)
        count, _ = tree_count_and_marginals(
            range(N), edges, relations, state_counts
        )
        key = (count, root)
        if best_star is None or key < best_star[0]:
            best_star = (key, edges)
    assert best_star is not None
    star_count, star_root = best_star[0]
    star_edges = best_star[1]

    greedy = []
    best_greedy = None
    for root in range(N):
        edges, count, history = greedy_growth_tree(
            root, N, relations, state_counts
        )
        greedy.append((count, root))
        key = (count, root)
        if best_greedy is None or key < best_greedy[0]:
            best_greedy = (key, edges, history)
    assert best_greedy is not None
    greedy.sort()

    greedy_count, greedy_root = best_greedy[0]
    greedy_edges = best_greedy[1]
    greedy_history = best_greedy[2]

    candidates = {
        'kruskal_min_relation_density': k_count,
        'best_star': star_count,
        'best_exact_incremental_greedy': greedy_count,
    }
    method, bound = min(candidates.items(), key=lambda kv: (kv[1], kv[0]))
    if method == 'best_exact_incremental_greedy':
        selected_edges = greedy_edges
    elif method == 'best_star':
        selected_edges = star_edges
    else:
        selected_edges = k_edges

    assert bound <= isolated_count
    bound_bits = (bound - 1).bit_length()
    bound_log2 = math.log2(bound)

    edge_hist = Counter()
    edge_density_hist = Counter()
    digest_rows = []
    for u, v in selected_edges:
        matrix = relation_matrix(relations, u, v)
        size = relation_size(matrix)
        edge_hist[size] += 1
        prod = len(matrix) * len(matrix[0])
        edge_density_hist[f'{size}/{prod}'] += 1
        mask = 0
        bit = 0
        for row in matrix:
            for x in row:
                if x:
                    mask |= 1 << bit
                bit += 1
        digest_rows.append(
            f'{gids[u]}:{gids[v]}:{len(matrix)}x{len(matrix[0])}:{mask:x}'
        )
    digest = hashlib.sha256(
        ('\n'.join(digest_rows) + '\n').encode()
    ).hexdigest()

    if bound < isolated_count:
        decision = 'M2_57WAY_TREE_BOUND_STRICTLY_BELOW_ISOLATED_CARTESIAN'
    else:
        decision = 'M2_57WAY_TREE_BOUND_NO_STRICT_GAIN'

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'multiplicity2_groups': N,
        'synthetic_tree_dp_regression': synthetic,
        'upstream_pair_decision': upstream['decision'],
        'upstream_subcartesian_pairs': upstream['subcartesian_pair_count'],
        'upstream_component_sizes': upstream['subcartesian_dependency_component_sizes'],
        'isolated_cartesian_state_count': isolated_count,
        'isolated_cartesian_log2': isolated_log2,
        'isolated_cartesian_state_bits': isolated_bits,
        'candidate_tree_counts': candidates,
        'best_star_root_group_id': gids[star_root],
        'best_greedy_root_group_id': gids[greedy_root],
        'best_greedy_root_counts_top10': [
            {'root_group_id': gids[root], 'tree_count': count}
            for count, root in greedy[:10]
        ],
        'selected_tree_method': method,
        'selected_tree_consistent_assignment_count': bound,
        'selected_tree_consistent_log2': bound_log2,
        'selected_tree_state_bits': bound_bits,
        'tree_gain_vs_isolated_log2_bits': isolated_log2 - bound_log2,
        'tree_gain_vs_physical_log2_bits': PHYS_N - bound_log2,
        'selected_tree': {
            'edge_count': len(selected_edges),
            'edge_joint_image_size_histogram': dict(sorted(edge_hist.items())),
            'edge_density_histogram': dict(sorted(edge_density_hist.items())),
            'edge_relation_digest_sha256': digest,
            'edges': [
                {
                    'left_group_id': gids[u],
                    'right_group_id': gids[v],
                    'left_states': state_counts[u],
                    'right_states': state_counts[v],
                    'joint_image_size': relation_size(
                        relation_matrix(relations, u, v)
                    ),
                }
                for u, v in selected_edges
            ],
        },
        'greedy_history_final_count': greedy_history[-1]['new_count'],
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M2_JOINT_TREE_BOUND')
    print('scope=rigorous upper bound on the 57-way multiplicity-2 output joint image from exact pairwise allowed-state relations and exact variable-alphabet tree DP')
    print('theorem=the true 57-way output image is a subset of assignments satisfying any selected spanning tree of exact pair relations')
    print('important=this bounds only the 57 multiplicity-2 outputs and does not combine them with singleton or multiplicity-4 families')
    print('not_included=singleton/m2 cross relations, m4 outputs, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
