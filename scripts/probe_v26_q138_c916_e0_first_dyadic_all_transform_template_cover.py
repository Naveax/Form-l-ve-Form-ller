#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_minimum_template_set_cover as S
import verify_v26_q138_c916_e0_first_dyadic_minimum_template_set_cover_result as V

F = S.F
Q = S.Q
PHYS_N = S.PHYS_N


def build_all_transforms():
    e0, _e1, _half = Q.C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    for zc in range(4):
        for zs, cls in e0[zc]:
            can = Q.C.P.U.H.support_for(Q.POS, zs, cls)
            if can is not None:
                grouped[can].append((zs, cls))
    assert len(grouped) == 250

    out = []
    for gid, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        _projection_rank, transforms = Q.physical_group_transforms(can, sectors)
        assert len(transforms) == len(sectors)
        for t in transforms:
            t['group_id'] = gid
            t['multiplicity'] = len(sectors)
            out.append(t)
    out.sort(key=lambda t: (t['group_id'], t['sector_index']))
    assert len(out) == 577
    assert len({(t['group_id'], t['sector_index']) for t in out}) == 577
    return out


def aid(t):
    return (t['group_id'], t['sector_index'])


def support_equal(a, b):
    return S.support_equal(a, b)


def analyze():
    anchors = F.build_term_anchors()
    assert len(anchors) == 340
    anchor_map = {aid(t): t for t in anchors}
    assert len(anchor_map) == 340

    mate_ids = set()
    for t in anchors:
        if t['role'] == 'pair_anchor':
            mate_ids.add((t['group_id'], t['mate_sector_index']))
    assert len(mate_ids) == 237
    assert not (mate_ids & set(anchor_map))

    transforms = build_all_transforms()
    transform_map = {aid(t): t for t in transforms}
    assert set(transform_map) == set(anchor_map) | mate_ids

    role = {}
    for key in transform_map:
        if key in anchor_map:
            role[key] = anchor_map[key]['role']
        else:
            role[key] = 'pair_mate'
    assert Counter(role.values()) == Counter({
        'pair_anchor': 237,
        'pair_mate': 237,
        'singleton_anchor': 103,
    })

    anchor_list = sorted(anchor_map.values(), key=aid)
    dims = {aid(t): len(t['physical_support_basis']) for t in anchor_list}
    maximal = []
    for child in anchor_list:
        cid = aid(child)
        dc = dims[cid]
        has_strict_super = False
        for root in anchor_list:
            if dims[aid(root)] <= dc:
                continue
            if Q.affine_subset(child, root['physical_support_constraints']):
                has_strict_super = True
                break
        if not has_strict_super:
            maximal.append(child)
    maximal.sort(key=aid)
    assert len(maximal) == 52

    unseen = set(aid(t) for t in maximal)
    maximal_by_id = {aid(t): t for t in maximal}
    classes = []
    while unseen:
        seed_id = min(unseen)
        seed = maximal_by_id[seed_id]
        cls_ids = tuple(sorted(
            rid for rid in unseen
            if support_equal(seed, maximal_by_id[rid])
        ))
        assert cls_ids
        unseen.difference_update(cls_ids)
        classes.append(cls_ids)
    classes.sort(key=lambda c: c[0])
    assert len(classes) == 15
    assert dict(sorted(Counter(len(c) for c in classes).items())) == {
        1: 13, 18: 1, 21: 1,
    }

    owner_class = {}
    children_by_class = defaultdict(list)
    owner_count_hist = Counter()
    uncovered_by_anchor_template_support = []
    multiple_owner = []
    for t in transforms:
        tid = aid(t)
        owners = []
        for ci, cls in enumerate(classes):
            rep = maximal_by_id[cls[0]]
            if Q.affine_subset(t, rep['physical_support_constraints']):
                owners.append(ci)
        owner_count_hist[len(owners)] += 1
        if len(owners) == 1:
            owner_class[tid] = owners[0]
            children_by_class[owners[0]].append(tid)
        elif len(owners) == 0:
            uncovered_by_anchor_template_support.append(tid)
        else:
            multiple_owner.append((tid, owners))

    residual_rank = {}
    min_rank_hist = Counter()
    min_rank_by_role = defaultdict(Counter)
    if not uncovered_by_anchor_template_support and not multiple_owner:
        for ci, cls in enumerate(classes):
            for tid in children_by_class[ci]:
                child = transform_map[tid]
                ranks = []
                for rid in cls:
                    root = maximal_by_id[rid]
                    if tid == rid:
                        rank = 0
                    else:
                        rec = Q.compare_phases(child, root, PHYS_N)
                        assert rec['support_relation'] in ('equal', 'left_subset_right')
                        assert rec['intersection_dimension'] == len(child['physical_support_basis'])
                        rank = rec['sign_difference_polar_rank']
                    residual_rank[(tid, rid)] = rank
                    ranks.append(rank)
                mr = min(ranks)
                min_rank_hist[mr] += 1
                min_rank_by_role[role[tid]][mr] += 1

    def evaluate_selected(selected_ids, nominal_threshold):
        selected = [tuple(x) for x in selected_ids]
        rank_hist = Counter()
        rank_by_role = defaultdict(Counter)
        no_container = []
        no_container_by_role = Counter()
        over_nominal = []
        over_nominal_by_role = Counter()
        assignment = []
        for t in transforms:
            tid = aid(t)
            opts = []
            for rid in selected:
                root = anchor_map[rid]
                if not Q.affine_subset(t, root['physical_support_constraints']):
                    continue
                rank = residual_rank.get((tid, rid))
                if rank is None:
                    if tid == rid:
                        rank = 0
                    else:
                        rec = Q.compare_phases(t, root, PHYS_N)
                        assert rec['support_relation'] in ('equal', 'left_subset_right')
                        rank = rec['sign_difference_polar_rank']
                opts.append((rank, rid))
            if not opts:
                no_container.append(tid)
                no_container_by_role[role[tid]] += 1
                continue
            rank, rid = min(opts)
            rank_hist[rank] += 1
            rank_by_role[role[tid]][rank] += 1
            if rank > nominal_threshold:
                over_nominal.append((tid, rank, rid))
                over_nominal_by_role[role[tid]] += 1
            assignment.append((tid, rank, rid))
        return {
            'selected_templates': len(selected),
            'nominal_threshold': nominal_threshold,
            'full_support_covered': len(assignment),
            'no_containing_template': len(no_container),
            'over_nominal_threshold': len(over_nominal),
            'no_containing_template_by_role': dict(sorted(no_container_by_role.items())),
            'over_nominal_threshold_by_role': dict(sorted(over_nominal_by_role.items())),
            'max_minimum_residual_rank': max((r for _t, r, _root in assignment), default=None),
            'minimum_residual_rank_histogram': dict(sorted(rank_hist.items())),
            'minimum_residual_rank_by_role': {
                k: dict(sorted(v.items())) for k, v in sorted(rank_by_role.items())
            },
            'first_no_container_ids': [list(x) for x in no_container[:30]],
            'first_over_nominal': [
                {'transform': list(t), 'rank': r, 'template': list(root)}
                for t, r, root in over_nominal[:30]
            ],
        }

    selected_results = {
        2: evaluate_selected(V.EXPECTED_R2, 2),
        4: evaluate_selected(V.EXPECTED_R4, 4),
    }

    optimized = {}
    if not uncovered_by_anchor_template_support and not multiple_owner:
        for threshold in (0, 2, 4, 6, 8):
            all_feasible = True
            chosen_global = []
            class_results = []
            for ci, cls in enumerate(classes):
                children = tuple(sorted(children_by_class[ci]))
                pos = {tid: p for p, tid in enumerate(children)}
                full = (1 << len(children)) - 1
                covers = []
                for rid in cls:
                    mask = 0
                    for tid in children:
                        if residual_rank[(tid, rid)] <= threshold:
                            mask |= 1 << pos[tid]
                    covers.append(mask)
                solved = S.exact_cover(tuple(covers), full)
                if solved['feasible']:
                    roots = [cls[j] for j in solved['chosen_candidate_indices']]
                    chosen_global.extend(roots)
                else:
                    roots = []
                    all_feasible = False
                class_results.append({
                    'class_index': ci,
                    'candidate_roots': len(cls),
                    'children': len(children),
                    'feasible': solved['feasible'],
                    'minimum_templates': solved['minimum_size'],
                    'chosen_template_anchor_ids': [list(x) for x in roots],
                    'exhausted_subsets_below_optimum': solved['exhausted_subsets_below_optimum'],
                })
            optimized[threshold] = {
                'feasible': all_feasible,
                'minimum_templates': len(chosen_global) if all_feasible else None,
                'chosen_template_anchor_ids': [list(x) for x in sorted(chosen_global)] if all_feasible else [],
                'class_minimum_template_histogram': dict(sorted(Counter(
                    rec['minimum_templates'] for rec in class_results
                    if rec['minimum_templates'] is not None
                ).items())),
                'classes': class_results,
            }

    if uncovered_by_anchor_template_support:
        decision = 'ANCHOR_MAXIMAL_TEMPLATE_SUPPORT_DOES_NOT_COVER_ALL_577_TRANSFORMS'
    elif multiple_owner:
        decision = 'ALL_SECTOR_TEMPLATE_OWNER_CLASS_NOT_UNIQUE'
    else:
        decision = (
            f'ALL_577_TRANSFORM_MINIMUM_TEMPLATE_COVER_R2_{optimized[2]["minimum_templates"]}'
            f'_R4_{optimized[4]["minimum_templates"]}'
        )

    out = {
        'position': Q.POS,
        'physical_shared_dimension': PHYS_N,
        'all_transforms': len(transforms),
        'anchor_transforms': len(anchor_map),
        'pair_mates': len(mate_ids),
        'role_histogram': dict(sorted(Counter(role.values()).items())),
        'maximal_anchor_templates': len(maximal),
        'maximal_anchor_support_classes': len(classes),
        'maximal_anchor_support_class_size_histogram': dict(sorted(Counter(len(c) for c in classes).items())),
        'owner_class_count_histogram': dict(sorted(owner_count_hist.items())),
        'transforms_without_containing_anchor_template_support': len(uncovered_by_anchor_template_support),
        'transforms_with_multiple_maximal_support_classes': len(multiple_owner),
        'first_uncovered_support_ids': [list(x) for x in uncovered_by_anchor_template_support[:30]],
        'minimum_residual_rank_histogram_all_maximal_anchor_templates': dict(sorted(min_rank_hist.items())),
        'minimum_residual_rank_by_role_all_maximal_anchor_templates': {
            k: dict(sorted(v.items())) for k, v in sorted(min_rank_by_role.items())
        },
        'selected_anchor_optimum_template_results': selected_results,
        'optimized_all_transform_template_cover': optimized,
        'decision': decision,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_TRANSFORM_TEMPLATE_COVER')
    print('scope=full-physical-support coverage of all 577 transformed sectors, including all 237 pair mates, using only the 52 support-maximal anchor templates frozen by the anchor geometry')
    print('important=selected 33/R2 and 19/R4 anchor-optimal sets are tested directly on pair-mate full supports; if the 52-template universe covers all transforms, exact all-transform minima are also computed by support class')
    print('next=only after full-sector coverage is established should residual evaluation signatures be lifted into the 149-bit radical-support separator')
    print('not_included=template common high-rank sign cost, complete grouped-e0 separator, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
