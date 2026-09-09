#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_all_transform_maximal_template_cover as G

A = G.A
Q = G.Q
S = G.S
PHYS_N = G.PHYS_N
THRESHOLDS = (0, 2, 4)


def aid(t):
    return (t['group_id'], t['sector_index'])


def exact_pivot_dp(covers, full_mask):
    """Exact minimum set cover by memoized pivot recurrence.

    For any non-empty residual universe U, every cover must contain one of the
    candidates covering a chosen pivot element e in U. Branching over all such
    candidates and solving U\\C recursively is therefore exhaustive. Memoizing
    U merges all equivalent residual subproblems. Among minimum-cardinality
    solutions, the lexicographically smallest sorted candidate-index tuple is
    retained.
    """
    covers = tuple(int(m) for m in covers)
    union = 0
    for m in covers:
        union |= m

    stats = {
        'states_solved': 0,
        'memo_hits': 0,
        'branches_examined': 0,
        'max_depth': 0,
    }

    if union != full_mask:
        return {
            'feasible': False,
            'minimum_size': None,
            'chosen_candidate_indices': [],
            'union_mask': union,
            'uncovered_mask': full_mask & ~union,
            'solver_stats': stats,
        }

    bit_candidates = {}
    y = full_mask
    while y:
        b = y & -y
        opts = tuple(i for i, m in enumerate(covers) if m & b)
        assert opts
        bit_candidates[b] = opts
        y ^= b

    memo = {}

    def solve(uncovered, depth):
        if uncovered == 0:
            return ()
        got = memo.get(uncovered)
        if got is not None or uncovered in memo:
            stats['memo_hits'] += 1
            return got

        stats['states_solved'] += 1
        stats['max_depth'] = max(stats['max_depth'], depth)

        pivot = None
        pivot_opts = None
        y = uncovered
        while y:
            b = y & -y
            opts = bit_candidates[b]
            if pivot is None or (len(opts), b) < (len(pivot_opts), pivot):
                pivot = b
                pivot_opts = opts
            y ^= b
        assert pivot is not None and pivot_opts

        best = None
        for i in pivot_opts:
            new_uncovered = uncovered & ~covers[i]
            assert new_uncovered != uncovered
            stats['branches_examined'] += 1
            sub = solve(new_uncovered, depth + 1)
            if sub is None:
                continue
            cand = tuple(sorted((i,) + sub))
            if best is None or (len(cand), cand) < (len(best), best):
                best = cand

        memo[uncovered] = best
        return best

    chosen = solve(full_mask, 0)
    assert chosen is not None
    assert len(set(chosen)) == len(chosen)
    check = 0
    for i in chosen:
        check |= covers[i]
    assert check == full_mask

    return {
        'feasible': True,
        'minimum_size': len(chosen),
        'chosen_candidate_indices': list(chosen),
        'union_mask': union,
        'uncovered_mask': 0,
        'solver_stats': stats,
    }


def synthetic_solver_regression():
    cases = 0

    full = 0b1111
    rec = exact_pivot_dp((0b0011, 0b0110, 0b1100), full)
    assert rec['feasible'] and rec['minimum_size'] == 2
    assert rec['chosen_candidate_indices'] == [0, 2]
    cases += 1

    rec = exact_pivot_dp((0b0011, 0b0100), full)
    assert not rec['feasible']
    assert rec['uncovered_mask'] == 0b1000
    cases += 1

    rec = exact_pivot_dp((0b0011, 0b1100, 0b0101, 0b1010), full)
    assert rec['feasible'] and rec['minimum_size'] == 2
    assert rec['chosen_candidate_indices'] == [0, 1]
    cases += 1

    covers = tuple([1 << i for i in range(5)] + [1] * 20)
    rec = exact_pivot_dp(covers, (1 << 5) - 1)
    assert rec['feasible'] and rec['minimum_size'] == 5
    assert rec['chosen_candidate_indices'] == [0, 1, 2, 3, 4]
    cases += 1

    return cases


def build_geometry():
    transforms = A.build_all_transforms()
    n = len(transforms)
    assert n == 577
    ids = tuple(aid(t) for t in transforms)
    assert len(set(ids)) == n
    dims = tuple(len(t['physical_support_basis']) for t in transforms)

    anchors = A.F.build_term_anchors()
    anchor_role = {aid(t): t['role'] for t in anchors}
    assert len(anchor_role) == 340
    role = {tid: anchor_role.get(tid, 'pair_mate') for tid in ids}
    assert Counter(role.values()) == Counter({
        'pair_anchor': 237,
        'pair_mate': 237,
        'singleton_anchor': 103,
    })

    strict_super_count = [0] * n
    for i, child in enumerate(transforms):
        di = dims[i]
        for j, root in enumerate(transforms):
            if dims[j] <= di:
                continue
            if Q.affine_subset(child, root['physical_support_constraints']):
                strict_super_count[i] += 1
    maximal = tuple(i for i in range(n) if strict_super_count[i] == 0)
    assert len(maximal) == 62

    unseen = set(maximal)
    classes = []
    while unseen:
        seed = min(unseen, key=lambda i: ids[i])
        cls = tuple(sorted(
            (j for j in unseen if S.support_equal(transforms[seed], transforms[j])),
            key=lambda j: ids[j],
        ))
        assert cls
        unseen.difference_update(cls)
        classes.append(cls)
    classes.sort(key=lambda c: ids[c[0]])
    assert len(classes) == 18
    assert dict(sorted(Counter(len(c) for c in classes).items())) == {
        1: 16, 21: 1, 25: 1,
    }

    owner_class = {}
    children_by_class = defaultdict(list)
    owner_hist = Counter()
    for i, child in enumerate(transforms):
        owners = []
        for ci, cls in enumerate(classes):
            if Q.affine_subset(child, transforms[cls[0]]['physical_support_constraints']):
                owners.append(ci)
        owner_hist[len(owners)] += 1
        assert len(owners) == 1, (ids[i], owners)
        owner_class[i] = owners[0]
        children_by_class[owners[0]].append(i)
    assert dict(sorted(owner_hist.items())) == {1: 577}

    residual_rank = {}
    residual_rank_hist = Counter()
    min_rank_hist = Counter()
    min_rank_by_role = defaultdict(Counter)
    for ci, cls in enumerate(classes):
        for i in children_by_class[ci]:
            ranks = []
            for root in cls:
                if i == root:
                    rank = 0
                else:
                    rec = Q.compare_phases(transforms[i], transforms[root], PHYS_N)
                    assert rec['support_relation'] in ('equal', 'left_subset_right')
                    assert rec['intersection_dimension'] == dims[i]
                    rank = rec['sign_difference_polar_rank']
                    assert rank is not None and rank % 2 == 0
                residual_rank[(i, root)] = rank
                residual_rank_hist[rank] += 1
                ranks.append(rank)
            mr = min(ranks)
            min_rank_hist[mr] += 1
            min_rank_by_role[role[ids[i]]][mr] += 1

    assert dict(sorted(min_rank_hist.items())) == {0: 413, 2: 164}
    assert {
        k: dict(sorted(v.items()))
        for k, v in sorted(min_rank_by_role.items())
    } == {
        'pair_anchor': {0: 147, 2: 90},
        'pair_mate': {0: 188, 2: 49},
        'singleton_anchor': {0: 78, 2: 25},
    }

    return {
        'transforms': transforms,
        'ids': ids,
        'dims': dims,
        'role': role,
        'maximal': maximal,
        'classes': classes,
        'owner_class': owner_class,
        'children_by_class': children_by_class,
        'residual_rank': residual_rank,
        'residual_rank_hist': residual_rank_hist,
        'min_rank_hist': min_rank_hist,
        'min_rank_by_role': min_rank_by_role,
    }


def analyze():
    regression_cases = synthetic_solver_regression()
    geo = build_geometry()

    transforms = geo['transforms']
    ids = geo['ids']
    role = geo['role']
    classes = geo['classes']
    children_by_class = geo['children_by_class']
    residual_rank = geo['residual_rank']
    n = len(transforms)

    threshold_results = {}

    for threshold in THRESHOLDS:
        global_chosen = []
        class_results = []
        all_feasible = True
        covered_by_all = 0
        uncovered_ids = []
        total_stats = Counter()

        for ci, cls in enumerate(classes):
            children = tuple(sorted(children_by_class[ci], key=lambda i: ids[i]))
            pos = {i: p for p, i in enumerate(children)}
            full = (1 << len(children)) - 1

            covers = []
            union = 0
            for root in cls:
                mask = 0
                for i in children:
                    if residual_rank[(i, root)] <= threshold:
                        mask |= 1 << pos[i]
                covers.append(mask)
                union |= mask

            covered_by_all += union.bit_count()
            missing = full & ~union
            if missing:
                for i in children:
                    if missing & (1 << pos[i]):
                        uncovered_ids.append(ids[i])

            solved = exact_pivot_dp(tuple(covers), full)
            for k, v in solved['solver_stats'].items():
                total_stats[k] += v

            if solved['feasible']:
                roots = [cls[j] for j in solved['chosen_candidate_indices']]
                global_chosen.extend(roots)
            else:
                roots = []
                all_feasible = False

            class_results.append({
                'class_index': ci,
                'representative': list(ids[cls[0]]),
                'candidate_roots': len(cls),
                'children': len(children),
                'covered_by_all_candidates': union.bit_count(),
                'feasible': solved['feasible'],
                'minimum_templates': solved['minimum_size'],
                'chosen_template_ids': [list(ids[r]) for r in roots],
                'solver_stats': solved['solver_stats'],
            })

        assignment_rank_hist = Counter()
        assignment_rank_by_role = defaultdict(Counter)
        chosen_role_hist = Counter()
        assignment_examples = []

        if all_feasible:
            chosen_by_class = defaultdict(list)
            class_of_root = {}
            for ci, cls in enumerate(classes):
                for root in cls:
                    class_of_root[root] = ci
            for root in global_chosen:
                chosen_by_class[class_of_root[root]].append(root)
                chosen_role_hist[role[ids[root]]] += 1

            for ci, children in children_by_class.items():
                roots = tuple(chosen_by_class[ci])
                assert roots
                for i in children:
                    opts = sorted(
                        (residual_rank[(i, root)], ids[root], root)
                        for root in roots
                        if residual_rank[(i, root)] <= threshold
                    )
                    assert opts, (threshold, ids[i], [ids[r] for r in roots])
                    rank, rid, root = opts[0]
                    assignment_rank_hist[rank] += 1
                    assignment_rank_by_role[role[ids[i]]][rank] += 1
                    if rank:
                        assignment_examples.append({
                            'transform': list(ids[i]),
                            'template': list(rid),
                            'rank': rank,
                            'role': role[ids[i]],
                        })

        threshold_results[threshold] = {
            'feasible': all_feasible,
            'covered_by_all_candidates': covered_by_all,
            'uncovered_by_all_candidates': n - covered_by_all,
            'first_uncovered_ids': [list(x) for x in sorted(uncovered_ids)[:40]],
            'minimum_templates': len(global_chosen) if all_feasible else None,
            'chosen_template_ids': [
                list(ids[r]) for r in sorted(global_chosen, key=lambda i: ids[i])
            ] if all_feasible else [],
            'chosen_template_role_histogram': dict(sorted(chosen_role_hist.items())) if all_feasible else {},
            'class_minimum_template_histogram': dict(sorted(Counter(
                rec['minimum_templates']
                for rec in class_results
                if rec['minimum_templates'] is not None
            ).items())),
            'assignment_residual_rank_histogram': dict(sorted(assignment_rank_hist.items())) if all_feasible else {},
            'assignment_residual_rank_by_role': {
                k: dict(sorted(v.items()))
                for k, v in sorted(assignment_rank_by_role.items())
            } if all_feasible else {},
            'first_nonzero_assignment_examples': assignment_examples[:40],
            'solver_stats_total': dict(sorted(total_stats.items())),
            'classes': class_results,
        }

    r0 = threshold_results[0]
    r2 = threshold_results[2]
    r4 = threshold_results[4]
    r0_tag = f'R0_{r0["minimum_templates"]}' if r0['feasible'] else 'R0_INFEASIBLE'
    r2_tag = f'R2_{r2["minimum_templates"]}' if r2['feasible'] else 'R2_INFEASIBLE'
    r4_tag = f'R4_{r4["minimum_templates"]}' if r4['feasible'] else 'R4_INFEASIBLE'
    decision = f'ALL_577_EXACT_MAXIMAL_TEMPLATE_COVER_{r0_tag}_{r2_tag}_{r4_tag}'

    out = {
        'position': Q.POS,
        'physical_shared_dimension': PHYS_N,
        'synthetic_solver_regression_cases': regression_cases,
        'all_transforms': 577,
        'support_maximal_templates': len(geo['maximal']),
        'support_maximal_equal_classes': len(classes),
        'support_maximal_equal_class_size_histogram': dict(sorted(Counter(len(c) for c in classes).items())),
        'owner_class_count_histogram': {1: 577},
        'direct_containing_template_residual_rank_histogram': dict(sorted(geo['residual_rank_hist'].items())),
        'minimum_direct_residual_rank_histogram': dict(sorted(geo['min_rank_hist'].items())),
        'minimum_direct_residual_rank_by_role': {
            k: dict(sorted(v.items()))
            for k, v in sorted(geo['min_rank_by_role'].items())
        },
        'threshold_results': threshold_results,
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_577_EXACT_TEMPLATE_COVER')
    print('scope=exact minimum set cover over the complete 62-template / 18-support-class all-transform phase-template universe, using a cap-free memoized pivot recurrence')
    print('optimality=for each residual universe U the recurrence branches over every template covering a deterministic uncovered pivot, so every valid cover is represented; memoization only merges identical residual universes')
    print('important=R0/R2/R4 minima are exact and the chosen roots are deterministic lexicographic minima under the exact recurrence')
    print('next=freeze the exact complete-template minima, then measure minimal residual evaluation-signature union rank and cut width over the 149-bit radical-support separator; template common-sign cost remains separate')
    print('not_included=template common high-rank sign cost, complete grouped-e0 separator theorem, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
