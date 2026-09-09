#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_maximal_support_phase_template_cover as M

F = M.F
Q = M.Q
PHYS_N = M.PHYS_N
THRESHOLDS = (0, 2, 4)


def exact_cover(covers, full_mask):
    """Exact minimum set cover over <=21 candidate masks, lexicographic tie-break."""
    union = 0
    for mask in covers:
        union |= mask
    if union != full_mask:
        return {
            'feasible': False,
            'minimum_size': None,
            'chosen_candidate_indices': [],
            'union_mask': union,
            'exhausted_subsets_below_optimum': 0,
            'examined_at_optimum_size': 0,
        }

    exhausted = 0
    for k in range(1, len(covers) + 1):
        examined = 0
        for combo in combinations(range(len(covers)), k):
            examined += 1
            mask = 0
            for j in combo:
                mask |= covers[j]
            if mask == full_mask:
                return {
                    'feasible': True,
                    'minimum_size': k,
                    'chosen_candidate_indices': list(combo),
                    'union_mask': union,
                    'exhausted_subsets_below_optimum': exhausted,
                    'examined_at_optimum_size': examined,
                }
        exhausted += examined
    raise AssertionError('union covers the universe but no subset was found')


def synthetic_solver_regression():
    full = (1 << 4) - 1
    rec = exact_cover((0b0011, 0b0110, 0b1100), full)
    assert rec['feasible']
    assert rec['minimum_size'] == 2
    assert rec['chosen_candidate_indices'] == [0, 2]
    rec2 = exact_cover((0b0011, 0b0100), full)
    assert not rec2['feasible']
    return 2


def support_equal(a, b):
    if len(a['physical_support_basis']) != len(b['physical_support_basis']):
        return False
    return (
        Q.affine_subset(a, b['physical_support_constraints'])
        and Q.affine_subset(b, a['physical_support_constraints'])
    )


def analyze():
    regression_cases = synthetic_solver_regression()
    anchors = F.build_term_anchors()
    n = len(anchors)
    assert n == 340

    ids = tuple(F.anchor_id(t) for t in anchors)
    dims = tuple(len(t['physical_support_basis']) for t in anchors)

    strict_super_count = [0] * n
    for i, child in enumerate(anchors):
        di = dims[i]
        for j, root in enumerate(anchors):
            if dims[j] <= di:
                continue
            if Q.affine_subset(child, root['physical_support_constraints']):
                strict_super_count[i] += 1
    maximal = tuple(i for i in range(n) if strict_super_count[i] == 0)
    assert len(maximal) == 52

    unseen = set(maximal)
    maximal_classes = []
    while unseen:
        seed = min(unseen, key=lambda i: ids[i])
        cls = tuple(
            sorted(
                (j for j in unseen if support_equal(anchors[seed], anchors[j])),
                key=lambda j: ids[j],
            )
        )
        assert cls
        unseen.difference_update(cls)
        maximal_classes.append(cls)
    maximal_classes.sort(key=lambda c: ids[c[0]])
    assert len(maximal_classes) == 15
    assert dict(sorted(Counter(len(c) for c in maximal_classes).items())) == {
        1: 13,
        18: 1,
        21: 1,
    }

    owner_class = {}
    children_by_class = defaultdict(list)
    candidate_count_hist = Counter()
    for i, child in enumerate(anchors):
        owners = []
        for ci, cls in enumerate(maximal_classes):
            rep = cls[0]
            if Q.affine_subset(child, anchors[rep]['physical_support_constraints']):
                owners.append(ci)
        assert len(owners) == 1, (ids[i], owners)
        ci = owners[0]
        owner_class[i] = ci
        children_by_class[ci].append(i)
        candidate_count_hist[len(maximal_classes[ci])] += 1

    assert dict(sorted(candidate_count_hist.items())) == {1: 24, 18: 201, 21: 115}
    assert sum(len(v) for v in children_by_class.values()) == n

    residual_rank = {}
    residual_rank_hist = Counter()
    for ci, cls in enumerate(maximal_classes):
        for i in children_by_class[ci]:
            for root in cls:
                if i == root:
                    rank = 0
                else:
                    rec = Q.compare_phases(anchors[i], anchors[root], PHYS_N)
                    assert rec['support_relation'] in (
                        'equal',
                        'left_subset_right',
                    ), (ids[i], ids[root], rec['support_relation'])
                    assert rec['intersection_dimension'] == dims[i]
                    rank = rec['sign_difference_polar_rank']
                    assert rank is not None and rank % 2 == 0
                residual_rank[(i, root)] = rank
                residual_rank_hist[rank] += 1

    minimum_rank_hist = Counter()
    for i in range(n):
        cls = maximal_classes[owner_class[i]]
        minimum_rank_hist[min(residual_rank[(i, root)] for root in cls)] += 1
    assert dict(sorted(minimum_rank_hist.items())) == {0: 222, 2: 118}

    threshold_results = {}
    for threshold in THRESHOLDS:
        global_templates = []
        class_results = []
        covered_union = set()
        total_exhausted = 0
        total_examined_at_optimum = 0
        all_feasible = True

        for ci, cls in enumerate(maximal_classes):
            children = tuple(sorted(children_by_class[ci], key=lambda i: ids[i]))
            child_pos = {i: p for p, i in enumerate(children)}
            full_mask = (1 << len(children)) - 1

            covers = []
            for root in cls:
                mask = 0
                for i in children:
                    if residual_rank[(i, root)] <= threshold:
                        mask |= 1 << child_pos[i]
                covers.append(mask)

            solved = exact_cover(tuple(covers), full_mask)
            total_exhausted += solved['exhausted_subsets_below_optimum']
            total_examined_at_optimum += solved['examined_at_optimum_size']

            class_union = solved['union_mask']
            class_covered = [
                children[p]
                for p in range(len(children))
                if (class_union >> p) & 1
            ]
            covered_union.update(class_covered)

            chosen_roots = [cls[j] for j in solved['chosen_candidate_indices']]
            if solved['feasible']:
                global_templates.extend(chosen_roots)
            else:
                all_feasible = False

            class_results.append({
                'class_index': ci,
                'representative': list(ids[cls[0]]),
                'candidate_roots': len(cls),
                'children': len(children),
                'covered_by_all_candidates': len(class_covered),
                'feasible': solved['feasible'],
                'minimum_templates': solved['minimum_size'],
                'chosen_template_anchor_ids': [list(ids[j]) for j in chosen_roots],
                'exhausted_subsets_below_optimum': solved['exhausted_subsets_below_optimum'],
                'examined_at_optimum_size': solved['examined_at_optimum_size'],
            })

        uncovered = sorted((i for i in range(n) if i not in covered_union), key=lambda i: ids[i])
        if all_feasible:
            minimum_templates = len(global_templates)
            chosen_ids = [list(ids[i]) for i in sorted(global_templates, key=lambda i: ids[i])]
        else:
            minimum_templates = None
            chosen_ids = []

        threshold_results[threshold] = {
            'feasible': all_feasible,
            'covered_by_all_candidates': len(covered_union),
            'uncovered_anchors': len(uncovered),
            'first_uncovered_anchor_ids': [list(ids[i]) for i in uncovered[:30]],
            'minimum_templates': minimum_templates,
            'chosen_template_anchor_ids': chosen_ids,
            'class_minimum_template_histogram': dict(sorted(Counter(
                rec['minimum_templates']
                for rec in class_results
                if rec['minimum_templates'] is not None
            ).items())),
            'exhausted_subsets_below_optimum': total_exhausted,
            'examined_at_optimum_size': total_examined_at_optimum,
            'classes': class_results,
        }

    assert not threshold_results[0]['feasible']
    assert threshold_results[0]['covered_by_all_candidates'] == 222
    assert threshold_results[0]['uncovered_anchors'] == 118
    assert threshold_results[2]['feasible']
    assert threshold_results[2]['covered_by_all_candidates'] == 340
    assert threshold_results[4]['feasible']
    assert threshold_results[4]['covered_by_all_candidates'] == 340

    r2 = threshold_results[2]['minimum_templates']
    r4 = threshold_results[4]['minimum_templates']
    decision = f'MINIMUM_MAXIMAL_SUPPORT_TEMPLATE_COVER_R2_{r2}_R4_{r4}_R0_INFEASIBLE'

    out = {
        'position': Q.POS,
        'physical_shared_dimension': PHYS_N,
        'synthetic_solver_regression_cases': regression_cases,
        'first_dyadic_term_anchors': n,
        'maximal_support_anchors': len(maximal),
        'maximal_support_equal_classes': len(maximal_classes),
        'maximal_support_equal_class_size_histogram': dict(sorted(Counter(len(c) for c in maximal_classes).items())),
        'containing_maximal_candidate_count_histogram': dict(sorted(candidate_count_hist.items())),
        'children_per_maximal_support_class': [
            {
                'class_index': ci,
                'representative': list(ids[cls[0]]),
                'candidate_roots': len(cls),
                'children': len(children_by_class[ci]),
            }
            for ci, cls in enumerate(maximal_classes)
        ],
        'direct_containing_template_residual_rank_histogram': dict(sorted(residual_rank_hist.items())),
        'minimum_direct_residual_polar_rank_histogram': dict(sorted(minimum_rank_hist.items())),
        'threshold_results': threshold_results,
        'minimum_templates_r2': r2,
        'minimum_templates_r4': r4,
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_MINIMUM_TEMPLATE_SET_COVER')
    print('scope=exact minimum set cover over actual support-maximal anchor templates, decomposed by the uniquely containing maximal-support equality class; every candidate correction is defined on the entire child support')
    print('optimality=each class has at most 21 candidate roots, so all smaller candidate subsets are exhaustively rejected before the first lexicographic optimum is accepted')
    print('important=R0 infeasibility is certified by the union of all rank-0 candidate covers missing anchors; R2/R4 minima are exact, not heuristic')
    print('next=freeze the minimum-template authority, then lift the selected rank-0/2 residual signatures into the existing 149-bit radical-support separator and measure exact added cut state')
    print('not_included=template common high-rank sign cost, complete grouped-e0 separator, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
