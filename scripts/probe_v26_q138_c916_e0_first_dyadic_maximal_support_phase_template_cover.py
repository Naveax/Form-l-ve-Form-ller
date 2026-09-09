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
            return
        if self.sz[a] < self.sz[b]:
            a, b = b, a
        self.p[b] = a
        self.sz[a] += self.sz[b]


def synthetic_cover_regression():
    candidates = {
        0: [(0, 0)],
        1: [(1, 0)],
        2: [(0, 4), (1, 2)],
        3: [(1, 4)],
    }
    chosen = {}
    for child, opts in candidates.items():
        root, rank = min(opts, key=lambda x: (x[1], x[0]))
        chosen[child] = (root, rank)
    assert chosen == {0: (0, 0), 1: (1, 0), 2: (1, 2), 3: (1, 4)}
    assert max(rank for _root, rank in chosen.values()) == 4
    return 4


def analyze():
    regression_cases = synthetic_cover_regression()
    anchors = F.build_term_anchors()
    n = len(anchors)
    assert n == 340
    ids = tuple(F.anchor_id(t) for t in anchors)
    dims = tuple(len(t['physical_support_basis']) for t in anchors)

    strict_supersets = [set() for _ in range(n)]
    equal_support = [set([i]) for i in range(n)]
    containment_rank = {}
    containment_type = {}
    dsu = DSU(n)

    relation_hist = Counter()
    containment_rank_hist = Counter()
    equal_rank_hist = Counter()
    strict_rank_hist = Counter()

    for i in range(n):
        for j in range(i + 1, n):
            relation, inter = Q.support_relation(anchors[i], anchors[j], PHYS_N)
            relation_hist[relation] += 1
            if inter is not None:
                dsu.union(i, j)

            if relation in ('disjoint', 'overlap_incomparable'):
                continue

            rec = Q.compare_phases(anchors[i], anchors[j], PHYS_N)
            rank = rec['sign_difference_polar_rank']
            assert rank is not None
            containment_rank_hist[rank] += 1

            if relation == 'equal':
                equal_support[i].add(j)
                equal_support[j].add(i)
                containment_rank[(i, j)] = containment_rank[(j, i)] = rank
                containment_type[(i, j)] = containment_type[(j, i)] = rec['sign_difference_type']
                equal_rank_hist[rank] += 1
            elif relation == 'left_subset_right':
                assert dims[i] < dims[j]
                strict_supersets[i].add(j)
                containment_rank[(i, j)] = rank
                containment_type[(i, j)] = rec['sign_difference_type']
                strict_rank_hist[rank] += 1
            elif relation == 'right_subset_left':
                assert dims[j] < dims[i]
                strict_supersets[j].add(i)
                containment_rank[(j, i)] = rank
                containment_type[(j, i)] = rec['sign_difference_type']
                strict_rank_hist[rank] += 1
            else:
                raise AssertionError(relation)

    maximal = tuple(i for i in range(n) if not strict_supersets[i])
    maximal_set = set(maximal)
    assert maximal

    unseen = set(maximal)
    maximal_classes = []
    while unseen:
        seed = min(unseen, key=lambda i: ids[i])
        cls_set = unseen & equal_support[seed]
        cls = tuple(sorted(cls_set, key=lambda i: ids[i]))
        for i in cls:
            assert (equal_support[i] & maximal_set) == cls_set
        unseen -= cls_set
        maximal_classes.append(cls)
    maximal_classes.sort(key=lambda c: ids[c[0]])

    assignment = []
    chosen_roots = Counter()
    min_rank_hist = Counter()
    min_type_hist = Counter()
    candidate_count_hist = Counter()
    min_rank_by_role = defaultdict(Counter)
    worst = []

    for i, anchor in enumerate(anchors):
        candidates = []
        for root in maximal:
            if i == root:
                candidates.append((0, ids[root], root, 'constant'))
                continue
            rank = containment_rank.get((i, root))
            if rank is not None:
                candidates.append((rank, ids[root], root, containment_type[(i, root)]))

        assert candidates, (i, ids[i], dims[i])
        candidate_count_hist[len(candidates)] += 1
        rank, _root_id, root, dtype = min(candidates)
        chosen_roots[root] += 1
        min_rank_hist[rank] += 1
        min_type_hist[dtype] += 1
        min_rank_by_role[anchor['role']][rank] += 1
        assignment.append((i, root, rank, dtype))
        worst.append((rank, ids[i], ids[root], dims[i], dims[root], anchor['role']))

    worst.sort(key=lambda x: (-x[0], x[1], x[2]))
    max_min_rank = max(rank for _i, _root, rank, _dtype in assignment)

    comp_map = defaultdict(list)
    for i in range(n):
        comp_map[dsu.find(i)].append(i)
    comps = [tuple(sorted(v, key=lambda i: ids[i])) for v in comp_map.values()]
    comps.sort(key=lambda c: ids[c[0]])
    assert sorted((len(c) for c in comps), reverse=True) == [332, 2, 2, 2, 2]
    comp_label = {}
    for ci, comp in enumerate(comps):
        for i in comp:
            comp_label[i] = ci

    maximal_by_component = Counter(comp_label[i] for i in maximal)
    chosen_by_component = Counter(comp_label[i] for i in chosen_roots)

    thresholds = {}
    for threshold in (0, 2, 4, 6, 8):
        uncovered = [
            list(ids[i])
            for i, _root, rank, _dtype in assignment
            if rank > threshold
        ]
        thresholds[threshold] = {
            'covered_anchors': n - len(uncovered),
            'uncovered_anchors': len(uncovered),
            'all_covered': not uncovered,
            'first_uncovered_examples': uncovered[:20],
        }

    if max_min_rank <= 4:
        decision = 'MAXIMAL_SUPPORT_ANCHOR_TEMPLATE_COVER_RESIDUAL_POLAR_RANK_LE_4'
    else:
        decision = f'MAXIMAL_SUPPORT_ANCHOR_TEMPLATE_COVER_REQUIRES_POLAR_RANK_{max_min_rank}'

    out = {
        'position': Q.POS,
        'physical_shared_dimension': PHYS_N,
        'synthetic_cover_regression_cases': regression_cases,
        'first_dyadic_term_anchors': n,
        'physical_support_components': len(comps),
        'physical_support_component_sizes_descending': sorted((len(c) for c in comps), reverse=True),
        'support_relation_histogram': dict(sorted(relation_hist.items())),
        'containment_pair_polar_rank_histogram': dict(sorted(containment_rank_hist.items())),
        'equal_support_pair_polar_rank_histogram': dict(sorted(equal_rank_hist.items())),
        'strict_containment_pair_polar_rank_histogram': dict(sorted(strict_rank_hist.items())),
        'maximal_support_anchors': len(maximal),
        'maximal_support_anchor_ids': [list(ids[i]) for i in maximal],
        'maximal_support_dimension_histogram': dict(sorted(Counter(dims[i] for i in maximal).items())),
        'maximal_support_equal_classes': len(maximal_classes),
        'maximal_support_equal_class_size_histogram': dict(sorted(Counter(len(c) for c in maximal_classes).items())),
        'maximal_support_anchors_by_component': dict(sorted(maximal_by_component.items())),
        'containing_maximal_candidate_count_histogram': dict(sorted(candidate_count_hist.items())),
        'minimum_direct_residual_polar_rank_histogram': dict(sorted(min_rank_hist.items())),
        'minimum_direct_residual_type_histogram': dict(sorted(min_type_hist.items())),
        'minimum_direct_residual_polar_rank_by_role': {
            role: dict(sorted(h.items())) for role, h in sorted(min_rank_by_role.items())
        },
        'max_minimum_direct_residual_polar_rank': max_min_rank,
        'threshold_coverage': thresholds,
        'deterministically_chosen_template_anchors': len(chosen_roots),
        'chosen_template_anchor_ids': [list(ids[i]) for i in sorted(chosen_roots, key=lambda i: ids[i])],
        'chosen_template_assignment_size_histogram': dict(sorted(Counter(chosen_roots.values()).items())),
        'chosen_template_anchors_by_component': dict(sorted(chosen_by_component.items())),
        'worst_assignment_examples': [
            {
                'rank': rank,
                'anchor': list(anchor_id),
                'template': list(root_id),
                'anchor_support_dimension': anchor_dim,
                'template_support_dimension': root_dim,
                'role': role,
            }
            for rank, anchor_id, root_id, anchor_dim, root_dim, role in worst[:40]
        ],
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_MAXIMAL_SUPPORT_PHASE_TEMPLATE_COVER')
    print('scope=gauge-free constructive phase-template cover using only actual anchors whose physical supports contain the covered anchor support; residual rank is measured on the entire child support')
    print('important=this is a direct-support containment construction, not an arbitrary ambient quadratic extension and not merely an overlap-graph path argument')
    print('next=if residual rank <=4 succeeds, optimize the number of containing templates and attach the resulting exact correction family to the radical-support separator; otherwise escalate the chart-local template class')
    print('not_included=complete grouped-e0 separator, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
