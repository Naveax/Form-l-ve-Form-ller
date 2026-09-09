#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_all_transform_template_cover as A

Q = A.Q
S = A.S
PHYS_N = A.PHYS_N
THRESHOLDS = (0, 2, 4)
MAX_EXHAUSTIVE_CLASS_ROOTS = 24


def aid(t):
    return (t['group_id'], t['sector_index'])


def analyze():
    transforms = A.build_all_transforms()
    n = len(transforms)
    assert n == 577
    ids = tuple(aid(t) for t in transforms)
    by_id = {aid(t): t for t in transforms}
    assert len(by_id) == n
    dims = tuple(len(t['physical_support_basis']) for t in transforms)

    anchors = A.F.build_term_anchors()
    anchor_ids = {aid(t) for t in anchors}
    mate_ids = set(ids) - anchor_ids
    assert len(anchor_ids) == 340 and len(mate_ids) == 237
    role = {
        tid: ('pair_mate' if tid in mate_ids else by_id[tid].get('role', 'anchor'))
        for tid in ids
    }
    for t in anchors:
        role[aid(t)] = t['role']
    assert Counter(role.values()) == Counter({
        'pair_anchor': 237,
        'pair_mate': 237,
        'singleton_anchor': 103,
    })

    # A transform is support-maximal iff no strictly higher-dimensional
    # transformed support contains it. Equal supports stay as separate template
    # candidates because their phases may differ.
    strict_super_count = [0] * n
    for i, child in enumerate(transforms):
        di = dims[i]
        for j, root in enumerate(transforms):
            if dims[j] <= di:
                continue
            if Q.affine_subset(child, root['physical_support_constraints']):
                strict_super_count[i] += 1
    maximal = tuple(i for i in range(n) if strict_super_count[i] == 0)
    maximal_set = set(maximal)

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

    maximal_role_hist = Counter(role[ids[i]] for i in maximal)
    maximal_dim_hist = Counter(dims[i] for i in maximal)
    class_size_hist = Counter(len(c) for c in classes)
    class_role_profiles = []
    for ci, cls in enumerate(classes):
        class_role_profiles.append({
            'class_index': ci,
            'representative': list(ids[cls[0]]),
            'support_dimension': dims[cls[0]],
            'candidate_roots': len(cls),
            'role_histogram': dict(sorted(Counter(role[ids[i]] for i in cls).items())),
            'root_ids': [list(ids[i]) for i in cls],
        })

    owner_classes = {}
    children_by_class = defaultdict(list)
    owner_count_hist = Counter()
    multiple_owner_examples = []
    no_owner = []
    for i, t in enumerate(transforms):
        owners = []
        for ci, cls in enumerate(classes):
            rep = transforms[cls[0]]
            if Q.affine_subset(t, rep['physical_support_constraints']):
                owners.append(ci)
        owner_count_hist[len(owners)] += 1
        if len(owners) == 1:
            owner_classes[i] = owners[0]
            children_by_class[owners[0]].append(i)
        elif not owners:
            no_owner.append(i)
        else:
            multiple_owner_examples.append((i, tuple(owners)))

    # By construction every transform must be contained in at least one
    # support-maximal transform; failure here means a bug in the maximality pass.
    assert not no_owner

    residual_rank = {}
    min_rank_hist = Counter()
    min_rank_by_role = defaultdict(Counter)
    max_class_roots = max((len(c) for c in classes), default=0)

    if not multiple_owner_examples:
        for ci, cls in enumerate(classes):
            for i in children_by_class[ci]:
                ranks = []
                child = transforms[i]
                for root in cls:
                    if i == root:
                        rank = 0
                    else:
                        rec = Q.compare_phases(child, transforms[root], PHYS_N)
                        assert rec['support_relation'] in ('equal', 'left_subset_right')
                        assert rec['intersection_dimension'] == dims[i]
                        rank = rec['sign_difference_polar_rank']
                        assert rank is not None and rank % 2 == 0
                    residual_rank[(i, root)] = rank
                    ranks.append(rank)
                mr = min(ranks)
                min_rank_hist[mr] += 1
                min_rank_by_role[role[ids[i]]][mr] += 1

    threshold_results = {}
    exact_classwise_allowed = (
        not multiple_owner_examples and max_class_roots <= MAX_EXHAUSTIVE_CLASS_ROOTS
    )
    if exact_classwise_allowed:
        for threshold in THRESHOLDS:
            feasible = True
            chosen_global = []
            class_results = []
            total_exhausted = 0
            total_examined_at_optimum = 0
            all_candidate_union_count = 0

            for ci, cls in enumerate(classes):
                children = tuple(sorted(children_by_class[ci], key=lambda i: ids[i]))
                pos = {i: p for p, i in enumerate(children)}
                full = (1 << len(children)) - 1
                covers = []
                union_mask = 0
                for root in cls:
                    mask = 0
                    for i in children:
                        if residual_rank[(i, root)] <= threshold:
                            mask |= 1 << pos[i]
                    covers.append(mask)
                    union_mask |= mask
                all_candidate_union_count += union_mask.bit_count()
                solved = S.exact_cover(tuple(covers), full)
                total_exhausted += solved['exhausted_subsets_below_optimum']
                total_examined_at_optimum += solved['examined_at_optimum_size']
                if solved['feasible']:
                    roots = [cls[j] for j in solved['chosen_candidate_indices']]
                    chosen_global.extend(roots)
                else:
                    roots = []
                    feasible = False
                class_results.append({
                    'class_index': ci,
                    'representative': list(ids[cls[0]]),
                    'candidate_roots': len(cls),
                    'children': len(children),
                    'covered_by_all_candidates': union_mask.bit_count(),
                    'feasible': solved['feasible'],
                    'minimum_templates': solved['minimum_size'],
                    'chosen_template_ids': [list(ids[r]) for r in roots],
                    'exhausted_subsets_below_optimum': solved['exhausted_subsets_below_optimum'],
                    'examined_at_optimum_size': solved['examined_at_optimum_size'],
                })

            threshold_results[threshold] = {
                'feasible': feasible,
                'covered_by_all_candidates': all_candidate_union_count,
                'uncovered_by_all_candidates': n - all_candidate_union_count,
                'minimum_templates': len(chosen_global) if feasible else None,
                'chosen_template_ids': [list(ids[r]) for r in sorted(chosen_global, key=lambda i: ids[i])] if feasible else [],
                'class_minimum_template_histogram': dict(sorted(Counter(
                    rec['minimum_templates'] for rec in class_results
                    if rec['minimum_templates'] is not None
                ).items())),
                'exhausted_subsets_below_optimum': total_exhausted,
                'examined_at_optimum_size': total_examined_at_optimum,
                'classes': class_results,
            }

    previous_uncovered = {(61, 1), (61, 3), (227, 1)}
    previous_uncovered_status = {
        str(tid): {
            'is_support_maximal_all_transform': ids.index(tid) in maximal_set,
            'support_dimension': dims[ids.index(tid)],
            'owner_class': owner_classes.get(ids.index(tid)),
        }
        for tid in sorted(previous_uncovered)
    }

    if multiple_owner_examples:
        decision = 'ALL_TRANSFORM_MAXIMAL_SUPPORT_CLASSES_OVERLAP_FOR_CHILDREN'
    elif not exact_classwise_allowed:
        decision = f'ALL_TRANSFORM_MAXIMAL_CLASS_TOO_LARGE_FOR_ENUMERATION_{max_class_roots}'
    else:
        r0 = threshold_results[0]
        r2 = threshold_results[2]
        r4 = threshold_results[4]
        r0_tag = f'R0_{r0["minimum_templates"]}' if r0['feasible'] else 'R0_INFEASIBLE'
        r2_tag = f'R2_{r2["minimum_templates"]}' if r2['feasible'] else 'R2_INFEASIBLE'
        r4_tag = f'R4_{r4["minimum_templates"]}' if r4['feasible'] else 'R4_INFEASIBLE'
        decision = f'ALL_577_MAXIMAL_TRANSFORM_TEMPLATE_COVER_{r0_tag}_{r2_tag}_{r4_tag}'

    out = {
        'position': Q.POS,
        'physical_shared_dimension': PHYS_N,
        'all_transforms': n,
        'role_histogram': dict(sorted(Counter(role.values()).items())),
        'support_maximal_all_transform_templates': len(maximal),
        'support_maximal_role_histogram': dict(sorted(maximal_role_hist.items())),
        'support_maximal_dimension_histogram': dict(sorted(maximal_dim_hist.items())),
        'support_maximal_equal_classes': len(classes),
        'support_maximal_equal_class_size_histogram': dict(sorted(class_size_hist.items())),
        'support_maximal_class_profiles': class_role_profiles,
        'max_support_class_candidate_roots': max_class_roots,
        'owner_class_count_histogram': dict(sorted(owner_count_hist.items())),
        'multiple_owner_transform_count': len(multiple_owner_examples),
        'first_multiple_owner_examples': [
            {'transform': list(ids[i]), 'owner_classes': list(owners)}
            for i, owners in multiple_owner_examples[:30]
        ],
        'previous_anchor_uncovered_transform_status': previous_uncovered_status,
        'minimum_direct_residual_rank_histogram': dict(sorted(min_rank_hist.items())),
        'minimum_direct_residual_rank_by_role': {
            k: dict(sorted(v.items())) for k, v in sorted(min_rank_by_role.items())
        },
        'exact_classwise_set_cover_allowed': exact_classwise_allowed,
        'threshold_results': threshold_results,
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_TRANSFORM_MAXIMAL_TEMPLATE_COVER')
    print('scope=support-maximal phase-template universe rebuilt from all 577 transformed C e0 sectors, followed by full-support residual-rank and exact classwise template-cover measurements when support ownership is unique')
    print('important=the three pair mates missed by the 340-anchor template universe are explicitly tracked; no separator attachment is made until the complete 577-transform universe is covered')
    print('next=freeze this complete template geometry, then lift the selected residual evaluation signatures into the existing 149-bit radical-support separator if an acceptable R2/R4 cover exists')
    print('not_included=template common high-rank sign cost, complete grouped-e0 separator, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
