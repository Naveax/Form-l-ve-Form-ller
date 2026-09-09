#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_phase_overlap_forest as F
import probe_v26_q138_c916_e0_post_gauss_physical_phase_common as Q

PHYS_N = Q.PHYS_N


class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.sz = [1] * n

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.sz[a] < self.sz[b]:
            a, b = b, a
        self.p[b] = a
        self.sz[a] += self.sz[b]
        return True


def component_summary(n, ids, edges, threshold=None):
    dsu = DSU(n)
    for i, j, rank in edges:
        if threshold is None or rank <= threshold:
            dsu.union(i, j)

    groups = defaultdict(list)
    for i in range(n):
        groups[dsu.find(i)].append(i)

    comps = [
        tuple(sorted(v, key=lambda i: ids[i]))
        for v in groups.values()
    ]
    comps.sort(key=lambda c: ids[c[0]])
    sizes = sorted((len(c) for c in comps), reverse=True)
    roots = [list(ids[c[0]]) for c in comps]
    label = {}
    for ci, comp in enumerate(comps):
        for i in comp:
            label[i] = ci
    return {
        'component_count': len(comps),
        'component_size_histogram': dict(sorted(Counter(sizes).items())),
        'component_sizes_descending': sizes,
        'component_roots': roots,
        '_label': label,
    }


def synthetic_component_regression():
    ids = tuple((i, 0) for i in range(6))
    edges = [
        (0, 1, 0),
        (1, 2, 2),
        (2, 3, 6),
        (3, 4, 4),
        (4, 5, 8),
    ]
    s0 = component_summary(6, ids, edges, 0)
    s2 = component_summary(6, ids, edges, 2)
    s4 = component_summary(6, ids, edges, 4)
    s6 = component_summary(6, ids, edges, 6)
    sall = component_summary(6, ids, edges, None)
    assert s0['component_sizes_descending'] == [2, 1, 1, 1, 1]
    assert s2['component_sizes_descending'] == [3, 1, 1, 1]
    assert s4['component_sizes_descending'] == [3, 2, 1]
    assert s6['component_sizes_descending'] == [5, 1]
    assert sall['component_sizes_descending'] == [6]
    return 5


def public_summary(s):
    return {k: v for k, v in s.items() if not k.startswith('_')}


def analyze():
    regression_cases = synthetic_component_regression()
    anchors = F.build_term_anchors()
    n = len(anchors)
    assert n == 340
    ids = tuple(F.anchor_id(t) for t in anchors)

    total_pairs = n * (n - 1) // 2
    assert total_pairs == 57630

    relation_hist = Counter()
    rank_hist = Counter()
    type_hist = Counter()
    codim_hist = Counter()
    constant_bit_hist = Counter()
    linear_weight_hist = Counter()
    edges = []
    disjoint = 0

    for i in range(n):
        for j in range(i + 1, n):
            rec = Q.compare_phases(anchors[i], anchors[j], n=PHYS_N)
            relation_hist[rec['support_relation']] += 1
            rank = rec['sign_difference_polar_rank']
            if rank is None:
                disjoint += 1
                continue
            edges.append((i, j, rank))
            rank_hist[rank] += 1
            type_hist[rec['sign_difference_type']] += 1
            codim_hist[PHYS_N - rec['intersection_dimension']] += 1
            linear_weight_hist[rec['sign_difference_linear_weight']] += 1
            if rec['sign_difference_constant_bit'] is not None:
                constant_bit_hist[rec['sign_difference_constant_bit']] += 1

        if i % 25 == 0 or i == n - 1:
            print(
                f'progress left_index={i} overlap_edges={len(edges)} '
                f'disjoint_pairs={disjoint}',
                flush=True,
            )

    assert len(edges) + disjoint == total_pairs

    thresholds = sorted(rank_hist)
    summaries = {
        threshold: component_summary(n, ids, edges, threshold)
        for threshold in thresholds
    }
    support_summary = component_summary(n, ids, edges, None)

    # Reproduce the frozen forest authority from the complete edge census.
    assert 0 in summaries and 2 in summaries and 4 in summaries
    assert summaries[0]['component_count'] == 9
    assert summaries[0]['component_sizes_descending'] == [325, 2, 2, 2, 2, 2, 2, 2, 1]
    assert summaries[2]['component_count'] == 5
    assert summaries[2]['component_sizes_descending'] == [332, 2, 2, 2, 2]
    assert summaries[4]['component_count'] == 5
    assert summaries[4]['component_sizes_descending'] == [332, 2, 2, 2, 2]
    assert summaries[4]['component_roots'] == [
        [0, 0], [158, 0], [180, 0], [236, 0], [238, 0],
    ]

    rank4_label = summaries[4]['_label']
    cross_rank_hist = Counter()
    cross_pair_hist = Counter()
    internal_rank_hist = defaultdict(Counter)
    for i, j, rank in edges:
        ci = rank4_label[i]
        cj = rank4_label[j]
        if ci == cj:
            internal_rank_hist[ci][rank] += 1
        else:
            cross_rank_hist[rank] += 1
            a, b = sorted((ci, cj))
            cross_pair_hist[(a, b, rank)] += 1

    minimal_threshold_to_support_connectivity = None
    support_count = support_summary['component_count']
    for threshold in thresholds:
        if summaries[threshold]['component_count'] == support_count:
            minimal_threshold_to_support_connectivity = threshold
            break

    if support_count == 1:
        if minimal_threshold_to_support_connectivity is None:
            decision = 'FIRST_DYADIC_ALL_OVERLAP_SUPPORT_CONNECTED_THRESHOLD_UNRESOLVED'
        else:
            decision = (
                'FIRST_DYADIC_ALL_OVERLAP_SUPPORT_CONNECTED_AT_POLAR_RANK_'
                f'{minimal_threshold_to_support_connectivity}'
            )
    else:
        decision = 'FIRST_DYADIC_ALL_OVERLAP_SUPPORT_GRAPH_MULTIPLE_COMPONENTS'

    out = {
        'position': Q.POS,
        'physical_shared_dimension': PHYS_N,
        'synthetic_component_regression_cases': regression_cases,
        'first_dyadic_term_anchors': n,
        'all_unordered_anchor_pairs': total_pairs,
        'physical_overlap_pairs': len(edges),
        'physical_disjoint_pairs': disjoint,
        'support_relation_histogram': dict(sorted(relation_hist.items())),
        'all_overlap_sign_difference_polar_rank_histogram': dict(sorted(rank_hist.items())),
        'all_overlap_sign_difference_type_histogram': dict(sorted(type_hist.items())),
        'all_overlap_intersection_codimension_histogram': dict(sorted(codim_hist.items())),
        'all_overlap_constant_difference_bit_histogram': dict(sorted(constant_bit_hist.items())),
        'all_overlap_linear_weight_histogram': dict(sorted(linear_weight_hist.items())),
        'component_summary_by_polar_rank_threshold': {
            int(t): public_summary(summaries[t]) for t in thresholds
        },
        'physical_support_overlap_graph': public_summary(support_summary),
        'rank_le_4_cross_component_overlap_pairs': sum(cross_rank_hist.values()),
        'rank_le_4_cross_component_polar_rank_histogram': dict(sorted(cross_rank_hist.items())),
        'rank_le_4_cross_component_pair_rank_histogram': {
            f'{a}-{b}-r{r}': count
            for (a, b, r), count in sorted(cross_pair_hist.items())
        },
        'rank_le_4_internal_polar_rank_histogram_by_component': {
            int(ci): dict(sorted(h.items()))
            for ci, h in sorted(internal_rank_hist.items())
        },
        'minimal_polar_rank_threshold_reaching_support_connectivity': minimal_threshold_to_support_connectivity,
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_OVERLAP_PHASE_CENSUS')
    print('scope=complete physical-support overlap and intrinsic sign-difference census over all 57630 unordered pairs of the 340 frozen first-dyadic term anchors')
    print('important=unlike the forest pass, every physical-overlap pair is phase-evaluated, so cross-chart rank-6/rank-8 bridges and the true support-overlap connectivity are measured exactly')
    print('next=use the complete overlap-rank census to choose the smallest exact phase-chart/correction representation before quotient-aware first-dyadic message-state assembly')
    print('not_included=complete grouped-e0 separator, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
