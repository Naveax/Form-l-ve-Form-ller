#!/usr/bin/env python3
import json
import sys
from collections import Counter, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_all_577_exact_template_cover as E
import probe_v26_q138_c916_e0_first_dyadic_residual_signature_separator as R
import probe_v26_q138_c916_e0_first_dyadic_template_residual_pareto as P

Q = E.Q
PHYS_N = E.PHYS_N
THRESHOLDS = (2, 4, 6, 8)


def selected_roots(geo, threshold):
    if threshold in (2, 4):
        solved = R.solve_threshold_assignment(geo, threshold)
    else:
        solved = P.solve_assignment(geo, threshold)
    return tuple(solved['chosen_global'])


def component_sizes(n, edges):
    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a, b = find(a), find(b)
        if a == b:
            return
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]

    for a, b in edges:
        union(a, b)
    hist = Counter(find(i) for i in range(n))
    return sorted(hist.values(), reverse=True)


def constant_edge_cocycle(n, edges):
    adj = [[] for _ in range(n)]
    for a, b, bit in edges:
        adj[a].append((b, bit))
        adj[b].append((a, bit))

    offset = [None] * n
    components = []
    contradictions = []
    for root in range(n):
        if offset[root] is not None:
            continue
        offset[root] = 0
        q = deque([root])
        comp = []
        while q:
            u = q.popleft()
            comp.append(u)
            for v, bit in adj[u]:
                want = offset[u] ^ bit
                if offset[v] is None:
                    offset[v] = want
                    q.append(v)
                elif offset[v] != want:
                    contradictions.append((u, v, bit, offset[u], offset[v]))
        components.append(tuple(sorted(comp)))

    return {
        'consistent': not contradictions,
        'component_sizes': sorted((len(c) for c in components), reverse=True),
        'offset_histogram': dict(sorted(Counter(offset).items())),
        'first_contradictions': [
            {
                'left_index': a,
                'right_index': b,
                'edge_difference_bit': bit,
                'left_offset': oa,
                'right_offset': ob,
            }
            for a, b, bit, oa, ob in contradictions[:20]
        ],
    }


def analyze_threshold(geo, threshold):
    ids = geo['ids']
    transforms = geo['transforms']
    classes = geo['classes']
    selected = selected_roots(geo, threshold)

    class_of = {}
    for ci, cls in enumerate(classes):
        for i in cls:
            class_of[i] = ci

    relation_hist = Counter()
    rank_hist = Counter()
    type_hist = Counter()
    same_class_rank_hist = Counter()
    cross_class_rank_hist = Counter()
    physical_edges = []
    constant_edges = []
    incompatible = []

    for ai in range(len(selected)):
        i = selected[ai]
        for aj in range(ai + 1, len(selected)):
            j = selected[aj]
            rec = Q.compare_phases(transforms[i], transforms[j], PHYS_N)
            relation = rec['support_relation']
            relation_hist[relation] += 1
            if relation == 'disjoint':
                continue

            physical_edges.append((ai, aj))
            rank = rec['sign_difference_polar_rank']
            dtype = rec['sign_difference_type']
            rank_hist[rank] += 1
            type_hist[dtype] += 1
            if class_of[i] == class_of[j]:
                same_class_rank_hist[rank] += 1
            else:
                cross_class_rank_hist[rank] += 1

            if dtype == 'constant':
                bit = rec['sign_difference_constant_bit']
                assert bit in (0, 1)
                constant_edges.append((ai, aj, bit))
            else:
                incompatible.append({
                    'left': list(ids[i]),
                    'right': list(ids[j]),
                    'left_class': class_of[i],
                    'right_class': class_of[j],
                    'support_relation': relation,
                    'difference_type': dtype,
                    'polar_rank': rank,
                    'linear_weight': rec['sign_difference_linear_weight'],
                })

    cocycle = constant_edge_cocycle(len(selected), constant_edges)
    physical_components = component_sizes(len(selected), physical_edges)
    constant_components = component_sizes(
        len(selected), [(a, b) for a, b, _bit in constant_edges]
    )

    # A single phase defined on the union, modulo one constant per template,
    # exists exactly when every physical overlap difference is constant and
    # those constant differences are cycle-consistent. This says nothing yet
    # about whether the glued union function extends to one ambient quadratic.
    union_glue = (not incompatible) and cocycle['consistent']

    return {
        'threshold': threshold,
        'selected_templates': len(selected),
        'selected_template_ids': [list(ids[i]) for i in selected],
        'template_pair_count': len(selected) * (len(selected) - 1) // 2,
        'support_relation_histogram': dict(sorted(relation_hist.items())),
        'physical_overlap_edges': len(physical_edges),
        'physical_overlap_component_sizes': physical_components,
        'overlap_sign_difference_polar_rank_histogram': dict(sorted(rank_hist.items())),
        'overlap_sign_difference_type_histogram': dict(sorted(type_hist.items())),
        'same_support_class_overlap_rank_histogram': dict(sorted(same_class_rank_hist.items())),
        'cross_support_class_overlap_rank_histogram': dict(sorted(cross_class_rank_hist.items())),
        'constant_overlap_edges': len(constant_edges),
        'constant_overlap_component_sizes': constant_components,
        'constant_difference_cocycle': cocycle,
        'nonconstant_overlap_edges': len(incompatible),
        'first_nonconstant_overlap_examples': incompatible[:40],
        'common_phase_on_union_mod_template_constants_exists': union_glue,
        'ambient_quadratic_extension_not_tested': True,
    }


def analyze():
    geo = E.build_geometry()
    results = {t: analyze_threshold(geo, t) for t in THRESHOLDS}
    compatible = [
        t for t, rec in results.items()
        if rec['common_phase_on_union_mod_template_constants_exists']
    ]
    out = {
        'position': 'C',
        'physical_shared_dimension': PHYS_N,
        'thresholds': list(THRESHOLDS),
        'results': results,
        'compatible_thresholds': compatible,
        'decision': (
            'SELECTED_TEMPLATE_COMMON_PHASE_ON_UNION_EXISTS_FOR_' + '_'.join(map(str, compatible))
            if compatible
            else 'SELECTED_TEMPLATE_COMMON_PHASE_ON_UNION_REFUTED_FOR_R2_R4_R6_R8'
        ),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_SELECTED_TEMPLATE_COMMON_PHASE_OVERLAP')
    print('scope=exact physical-overlap compatibility of the deterministic R2/R4/R6/R8 selected templates, including constant-difference cycle consistency')
    print('gluing=common phase on the union modulo one constant per template exists iff every physical-overlap difference is constant and the constant-edge GF(2) cocycle is consistent')
    print('important=ambient 149-bit quadratic extension is not tested here; a nonconstant overlap refutes it immediately, while union gluing would only open the extension gate')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
