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

import probe_v26_q138_c916_e0_first_dyadic_m2_joint_tree_bound as T
import probe_v26_q138_c916_e0_first_dyadic_singleton_joint_tree_bound as ST
import probe_v26_q138_c916_e0_first_dyadic_singleton_m2_cross_joint_image as X

E = X.E
S = X.S
D = X.D
P = X.P
POS = X.POS
PHYS_N = X.PHYS_N
N_SINGLETON = 103
N_M2 = 57
N = N_SINGLETON + N_M2
assert PHYS_N == 149

EXPECTED_SINGLETON_PAIR_HIST = {
    5: 160, 6: 688, 8: 386, 9: 1399, 10: 207,
    11: 687, 12: 646, 13: 567, 14: 11, 16: 502,
}
EXPECTED_M2_PAIR_HIST = {
    7: 138, 9: 638, 11: 20, 13: 21, 15: 142,
    17: 82, 21: 232, 23: 2, 25: 321,
}
EXPECTED_CROSS_PAIR_HIST = {
    6: 107, 7: 74, 8: 1538, 10: 200, 12: 2092,
    14: 67, 16: 678, 18: 186, 20: 929,
}
EXPECTED_SINGLETON_TREE_COUNT = 1238500713816799073288417443840
EXPECTED_M2_TREE_COUNT = 10734454152343751701


def relation_size(matrix):
    return sum(int(x) for row in matrix for x in row)


def census_map(record):
    return {
        int(item['value']): int(item['multiplicity'])
        for item in record['value_multiplicity']
    }


def component_sizes(n, relations, state_counts):
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
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    strict = 0
    for (u, v), matrix in relations.items():
        cart = state_counts[u] * state_counts[v]
        if relation_size(matrix) < cart:
            strict += 1
            union(u, v)
    hist = Counter(find(i) for i in range(n))
    return strict, sorted(hist.values(), reverse=True)


def remap_family(global_nodes, relations, state_counts):
    global_nodes = tuple(global_nodes)
    local_states = tuple(state_counts[g] for g in global_nodes)
    local_relations = {}
    for i, gu in enumerate(global_nodes):
        for j in range(i + 1, len(global_nodes)):
            gv = global_nodes[j]
            local_relations[(i, j)] = T.relation_matrix(relations, gu, gv)
    return local_states, local_relations


def map_edges(local_edges, global_nodes):
    return tuple((global_nodes[u], global_nodes[v]) for u, v in local_edges)


def greedy_extend_tree(initial_nodes, initial_edges, n, relations, state_counts):
    selected = set(int(x) for x in initial_nodes)
    edges = [tuple(e) for e in initial_edges]
    assert selected
    T.validate_tree(selected, edges)
    history = []

    while len(selected) < n:
        current_count, marginals = T.tree_count_and_marginals(
            selected, edges, relations, state_counts
        )
        best = None
        outside = [v for v in range(n) if v not in selected]
        for u in sorted(selected):
            mu = marginals[u]
            for v in outside:
                matrix = T.relation_matrix(relations, u, v)
                degrees = tuple(sum(row) for row in matrix)
                extension = sum(mu[s] * degrees[s] for s in range(state_counts[u]))
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
            'parent': u,
            'new_node': v,
            'old_count': current_count,
            'new_count': key[0],
            'relation_size': key[1],
            'max_parent_to_child_degree': key[2],
            'degree_vector': list(degrees),
        })

    final_count, marginals = T.tree_count_and_marginals(
        range(n), edges, relations, state_counts
    )
    if history:
        assert history[-1]['new_count'] == final_count
    return tuple(edges), final_count, marginals, tuple(history)


def build_real_relations():
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
    assert len(sfrozen) == N_SINGLETON
    assert len(m2frozen) == N_M2
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
    assert dict(sorted(Counter(len(v) for _can, v in ordered).items())) == {
        1: 103, 2: 57, 4: 90,
    }

    by_gid = {}
    family = {}
    tid = 1
    for gid, (can, sectors) in enumerate(ordered):
        if len(sectors) not in (1, 2):
            continue
        group, tid = D.build_group_terms(gid, can, sectors, tid)
        assert len(group['terms']) == 2
        by_gid[gid] = group
        family[gid] = 's' if len(sectors) == 1 else 'm2'

    sgids = tuple(sorted(g for g in by_gid if family[g] == 's'))
    mgids = tuple(sorted(g for g in by_gid if family[g] == 'm2'))
    assert set(sgids) == set(sfrozen)
    assert set(mgids) == set(m2frozen)

    descriptors = tuple([('s', g) for g in sgids] + [('m2', g) for g in mgids])
    assert len(descriptors) == N
    local = {desc: i for i, desc in enumerate(descriptors)}
    values = {}
    frozen = {}
    groups = {}
    for i, (kind, gid) in enumerate(descriptors):
        fmap = sfrozen[gid] if kind == 's' else m2frozen[gid]
        values[i] = tuple(sorted(fmap))
        frozen[i] = fmap
        groups[i] = by_gid[gid]
    state_counts = tuple(len(values[i]) for i in range(N))
    assert Counter(state_counts) == Counter({4: 103, 3: 6, 5: 51})

    relations = {}
    family_hists = {
        'singleton_singleton': Counter(),
        'm2_m2': Counter(),
        'singleton_m2': Counter(),
    }
    strict_by_family = Counter()
    icache = {}
    mcache = {}
    marginal_checks = 0

    for u in range(N):
        ku, _gu = descriptors[u]
        for v in range(u + 1, N):
            kv, _gv = descriptors[v]
            rec = X.pair_joint_census(
                groups[u], groups[v], PHYS_N, icache, mcache
            )
            assert rec['left_marginal'] == frozen[u]
            assert rec['right_marginal'] == frozen[v]
            marginal_checks += 2
            counts = rec['joint_counts']
            matrix = tuple(
                tuple((a, b) in counts for b in values[v])
                for a in values[u]
            )
            assert all(any(row) for row in matrix)
            assert all(
                any(matrix[a][b] for a in range(len(matrix)))
                for b in range(len(matrix[0]))
            )
            relations[(u, v)] = matrix
            size = relation_size(matrix)
            if ku == 's' and kv == 's':
                fkey = 'singleton_singleton'
            elif ku == 'm2' and kv == 'm2':
                fkey = 'm2_m2'
            else:
                fkey = 'singleton_m2'
            family_hists[fkey][size] += 1
            if size < state_counts[u] * state_counts[v]:
                strict_by_family[fkey] += 1

    assert len(relations) == N * (N - 1) // 2 == 12720
    assert marginal_checks == 2 * len(relations) == 25440
    assert dict(sorted(family_hists['singleton_singleton'].items())) == EXPECTED_SINGLETON_PAIR_HIST
    assert dict(sorted(family_hists['m2_m2'].items())) == EXPECTED_M2_PAIR_HIST
    assert dict(sorted(family_hists['singleton_m2'].items())) == EXPECTED_CROSS_PAIR_HIST
    assert strict_by_family == Counter({
        'singleton_singleton': 4751,
        'm2_m2': 1119,
        'singleton_m2': 4781,
    })

    strict_total, comps = component_sizes(N, relations, state_counts)
    assert strict_total == 10651
    assert comps == [160]

    return {
        'descriptors': descriptors,
        'local': local,
        'state_counts': state_counts,
        'relations': relations,
        'family_hists': family_hists,
        'strict_by_family': strict_by_family,
        'strict_total': strict_total,
        'component_sizes': comps,
        'marginal_checks': marginal_checks,
        'support_intersections': len(icache),
        'character_moments': len(mcache),
    }


def tree_digest(edges, relations, descriptors):
    rows = []
    hist = Counter()
    densities = Counter()
    for u, v in edges:
        matrix = T.relation_matrix(relations, u, v)
        size = relation_size(matrix)
        prod = len(matrix) * len(matrix[0])
        hist[size] += 1
        densities[f'{size}/{prod}'] += 1
        mask = 0
        bit = 0
        for row in matrix:
            for x in row:
                if x:
                    mask |= 1 << bit
                bit += 1
        rows.append(
            f'{descriptors[u][0]}:{descriptors[u][1]}|'
            f'{descriptors[v][0]}:{descriptors[v][1]}|'
            f'{len(matrix)}x{len(matrix[0])}|{mask:x}'
        )
    digest = hashlib.sha256(('\n'.join(rows) + '\n').encode()).hexdigest()
    return dict(sorted(hist.items())), dict(sorted(densities.items())), digest


def analyze():
    synthetic_tree = T.synthetic_tree_regression()
    synthetic_cross = X.synthetic_regression()
    real = build_real_relations()
    descriptors = real['descriptors']
    local = real['local']
    state_counts = real['state_counts']
    relations = real['relations']

    isolated_count = 1
    for s in state_counts:
        isolated_count *= s
    isolated_log2 = math.log2(isolated_count)
    assert isolated_count == (4 ** 103) * (3 ** 6) * (5 ** 51)

    s_nodes = tuple(i for i, (kind, _gid) in enumerate(descriptors) if kind == 's')
    m_nodes = tuple(i for i, (kind, _gid) in enumerate(descriptors) if kind == 'm2')
    assert len(s_nodes) == 103 and len(m_nodes) == 57

    s_states, s_rel = remap_family(s_nodes, relations, state_counts)
    m_states, m_rel = remap_family(m_nodes, relations, state_counts)
    s_root = next(i for i, g in enumerate(s_nodes) if descriptors[g] == ('s', 207))
    m_root = next(i for i, g in enumerate(m_nodes) if descriptors[g] == ('m2', 15))

    assert all(x == 4 for x in s_states)
    s_edges_local, s_count, _s_history = ST.greedy_growth_tree(
        s_root, len(s_nodes), s_rel
    )
    m_edges_local, m_count, _m_history = T.greedy_growth_tree(
        m_root, len(m_nodes), m_rel, m_states
    )
    assert s_count == EXPECTED_SINGLETON_TREE_COUNT
    assert m_count == EXPECTED_M2_TREE_COUNT
    s_edges = map_edges(s_edges_local, s_nodes)
    m_edges = map_edges(m_edges_local, m_nodes)

    s_check, s_marg = T.tree_count_and_marginals(
        s_nodes, s_edges, relations, state_counts
    )
    m_check, m_marg = T.tree_count_and_marginals(
        m_nodes, m_edges, relations, state_counts
    )
    assert s_check == s_count and m_check == m_count

    best_bridge = None
    for u in s_nodes:
        for v in m_nodes:
            matrix = T.relation_matrix(relations, u, v)
            count = 0
            for a in range(state_counts[u]):
                for b in range(state_counts[v]):
                    if matrix[a][b]:
                        count += s_marg[u][a] * m_marg[v][b]
            key = (count, relation_size(matrix), u, v)
            if best_bridge is None or key < best_bridge[0]:
                best_bridge = (key, (u, v))
    assert best_bridge is not None
    bridge_count = best_bridge[0][0]
    bridge_edge = best_bridge[1]
    bridge_edges = tuple(s_edges) + tuple(m_edges) + (bridge_edge,)
    bridge_check, _ = T.tree_count_and_marginals(
        range(N), bridge_edges, relations, state_counts
    )
    assert bridge_check == bridge_count

    k_edges = T.kruskal_tree(N, relations)
    k_count, _ = T.tree_count_and_marginals(
        range(N), k_edges, relations, state_counts
    )

    s_ext_edges, s_ext_count, _s_ext_marg, _s_ext_history = greedy_extend_tree(
        s_nodes, s_edges, N, relations, state_counts
    )
    m_ext_edges, m_ext_count, _m_ext_marg, _m_ext_history = greedy_extend_tree(
        m_nodes, m_edges, N, relations, state_counts
    )

    seed_descriptors = [
        ('s', 207), ('s', 216), ('s', 224), ('s', 162), ('s', 166),
        ('s', 176), ('s', 94), ('s', 209), ('s', 193), ('s', 213),
        ('s', 2), ('s', 13), ('s', 16), ('s', 25), ('s', 26), ('s', 28),
        ('m2', 15), ('m2', 17), ('m2', 46), ('m2', 226), ('m2', 21),
        ('m2', 38), ('m2', 64), ('m2', 68), ('m2', 72), ('m2', 76),
    ]
    seed_nodes = []
    for desc in seed_descriptors:
        if desc in local:
            idx = local[desc]
            if idx not in seed_nodes:
                seed_nodes.append(idx)
    assert len(seed_nodes) >= 20

    root_results = []
    best_root = None
    for root in seed_nodes:
        edges, count, history = T.greedy_growth_tree(
            root, N, relations, state_counts
        )
        rec = (count, root, edges, history)
        root_results.append(rec)
        if best_root is None or (count, root) < (best_root[0], best_root[1]):
            best_root = rec
    assert best_root is not None

    pair_candidates = []
    for (u, v), matrix in relations.items():
        size = relation_size(matrix)
        prod = state_counts[u] * state_counts[v]
        pair_candidates.append((Fraction(size, prod), size, u, v))
    pair_candidates.sort()
    pair_seeds = []
    seen_pairs = set()
    for _density, _size, u, v in pair_candidates:
        key = (u, v)
        if key in seen_pairs:
            continue
        seen_pairs.add(key)
        pair_seeds.append(key)
        if len(pair_seeds) == 12:
            break

    pair_results = []
    best_pair = None
    for u, v in pair_seeds:
        edges, count, _marg, history = greedy_extend_tree(
            (u, v), ((u, v),), N, relations, state_counts
        )
        rec = (count, u, v, edges, history)
        pair_results.append(rec)
        if best_pair is None or (count, u, v) < (best_pair[0], best_pair[1], best_pair[2]):
            best_pair = rec
    assert best_pair is not None

    candidates = {
        'family_trees_best_cross_bridge': bridge_count,
        'kruskal_min_relation_density': k_count,
        'singleton_tree_then_global_greedy_extension': s_ext_count,
        'm2_tree_then_global_greedy_extension': m_ext_count,
        'best_selected_root_global_greedy': best_root[0],
        'best_density_pair_seed_global_greedy': best_pair[0],
    }
    method, bound = min(candidates.items(), key=lambda kv: (kv[1], kv[0]))
    edge_lookup = {
        'family_trees_best_cross_bridge': bridge_edges,
        'kruskal_min_relation_density': k_edges,
        'singleton_tree_then_global_greedy_extension': s_ext_edges,
        'm2_tree_then_global_greedy_extension': m_ext_edges,
        'best_selected_root_global_greedy': best_root[2],
        'best_density_pair_seed_global_greedy': best_pair[3],
    }
    selected_edges = edge_lookup[method]
    selected_count, selected_marginals = T.tree_count_and_marginals(
        range(N), selected_edges, relations, state_counts
    )
    assert selected_count == bound
    assert len(selected_edges) == N - 1

    bound_log2 = math.log2(bound)
    bound_bits = (bound - 1).bit_length()
    hist, density_hist, digest = tree_digest(
        selected_edges, relations, descriptors
    )
    family_edge_hist = Counter()
    for u, v in selected_edges:
        ku = descriptors[u][0]
        kv = descriptors[v][0]
        if ku == kv == 's':
            family_edge_hist['singleton_singleton'] += 1
        elif ku == kv == 'm2':
            family_edge_hist['m2_m2'] += 1
        else:
            family_edge_hist['singleton_m2'] += 1

    marginal_support_hist = Counter()
    for u, weights in selected_marginals.items():
        marginal_support_hist[sum(int(x > 0) for x in weights)] += 1

    if bound < (1 << PHYS_N):
        decision = 'SINGLETON_M2_160WAY_TREE_BOUND_BELOW_PHYSICAL_149'
    elif bound < isolated_count:
        decision = 'SINGLETON_M2_160WAY_TREE_BOUND_STRICTLY_BELOW_ISOLATED_ONLY'
    else:
        decision = 'SINGLETON_M2_160WAY_TREE_BOUND_NO_STRICT_GAIN'

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'singleton_groups': N_SINGLETON,
        'multiplicity2_groups': N_M2,
        'combined_outputs': N,
        'synthetic_tree_dp_regression': synthetic_tree,
        'synthetic_cross_regression': synthetic_cross,
        'pair_relation_count': len(relations),
        'pair_marginal_crosschecks': real['marginal_checks'],
        'pair_joint_image_histograms': {
            k: dict(sorted(v.items())) for k, v in real['family_hists'].items()
        },
        'strict_subcartesian_pair_counts': dict(sorted(real['strict_by_family'].items())),
        'strict_subcartesian_pair_total': real['strict_total'],
        'strict_subcartesian_component_sizes': real['component_sizes'],
        'cached_support_intersections': real['support_intersections'],
        'cached_character_moments': real['character_moments'],
        'isolated_cartesian_state_count': isolated_count,
        'isolated_cartesian_log2': isolated_log2,
        'isolated_cartesian_state_bits': (isolated_count - 1).bit_length(),
        'frozen_singleton_tree_count': s_count,
        'frozen_m2_tree_count': m_count,
        'candidate_tree_counts': candidates,
        'best_bridge': {
            'singleton_group_id': descriptors[bridge_edge[0]][1],
            'm2_group_id': descriptors[bridge_edge[1]][1],
            'joint_image_size': relation_size(T.relation_matrix(relations, *bridge_edge)),
            'tree_count': bridge_count,
        },
        'selected_root_global_greedy_top10': [
            {
                'kind': descriptors[root][0],
                'group_id': descriptors[root][1],
                'tree_count': count,
            }
            for count, root, _edges, _history in sorted(root_results)[:10]
        ],
        'density_pair_seed_global_greedy_top10': [
            {
                'left_kind': descriptors[u][0],
                'left_group_id': descriptors[u][1],
                'right_kind': descriptors[v][0],
                'right_group_id': descriptors[v][1],
                'initial_joint_image_size': relation_size(T.relation_matrix(relations, u, v)),
                'tree_count': count,
            }
            for count, u, v, _edges, _history in sorted(pair_results)[:10]
        ],
        'selected_tree_method': method,
        'selected_tree_consistent_assignment_count': bound,
        'selected_tree_consistent_log2': bound_log2,
        'selected_tree_state_bits': bound_bits,
        'tree_gain_vs_isolated_log2_bits': isolated_log2 - bound_log2,
        'tree_gain_vs_physical_log2_bits': PHYS_N - bound_log2,
        'selected_tree': {
            'edge_count': len(selected_edges),
            'family_edge_histogram': dict(sorted(family_edge_hist.items())),
            'edge_joint_image_size_histogram': hist,
            'edge_density_histogram': density_hist,
            'edge_relation_digest_sha256': digest,
            'node_marginal_positive_state_count_histogram': dict(sorted(marginal_support_hist.items())),
            'edges': [
                {
                    'left_kind': descriptors[u][0],
                    'left_group_id': descriptors[u][1],
                    'right_kind': descriptors[v][0],
                    'right_group_id': descriptors[v][1],
                    'joint_image_size': relation_size(T.relation_matrix(relations, u, v)),
                }
                for u, v in selected_edges
            ],
        },
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_SINGLETON_M2_160WAY_JOINT_TREE_BOUND')
    print('scope=rigorous joint-image upper bound for all 160 singleton plus multiplicity-2 C916 e0 first-dyadic outputs using all exact pair-relation families and exact variable-alphabet tree DP')
    print('theorem=the true 160-way output image is a subset of assignments satisfying every selected exact pair relation; any spanning tree therefore yields a valid superset counted exactly by sum-product DP')
    print('validation=all 12720 pair relations are recomputed from the common physical two-term group model; all three frozen family histograms and all 25440 marginals are asserted before tree selection')
    print('important=multiplicity-4 outputs and the rest of complete C2/W_repr/arithmetic-work remain outside this bound')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
