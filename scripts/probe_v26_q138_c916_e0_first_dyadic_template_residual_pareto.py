#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_all_577_exact_template_cover as E
import probe_v26_q138_c916_e0_first_dyadic_residual_signature_separator as R

THRESHOLDS = (6, 8)


def solve_assignment(geo, threshold):
    ids = geo['ids']
    classes = geo['classes']
    children_by_class = geo['children_by_class']
    residual_rank = geo['residual_rank']

    chosen_by_class = {}
    chosen_global = []
    class_minima = []
    stats_total = Counter()

    for ci, cls in enumerate(classes):
        children = tuple(sorted(children_by_class[ci], key=lambda i: ids[i]))
        pos = {i: p for p, i in enumerate(children)}
        full = (1 << len(children)) - 1
        covers = []
        for root in cls:
            mask = 0
            for i in children:
                if residual_rank[(i, root)] <= threshold:
                    mask |= 1 << pos[i]
            covers.append(mask)
        solved = E.exact_pivot_dp(tuple(covers), full)
        assert solved['feasible']
        roots = tuple(cls[j] for j in solved['chosen_candidate_indices'])
        chosen_by_class[ci] = roots
        chosen_global.extend(roots)
        class_minima.append(len(roots))
        stats_total.update(solved['solver_stats'])

    assignment = {}
    hist = Counter()
    for ci, children in children_by_class.items():
        roots = chosen_by_class[ci]
        for i in children:
            opts = sorted(
                (residual_rank[(i, root)], ids[root], root)
                for root in roots
                if residual_rank[(i, root)] <= threshold
            )
            assert opts
            rank, _rid, root = opts[0]
            assignment[i] = root
            hist[rank] += 1

    return {
        'chosen_global': tuple(sorted(chosen_global, key=lambda i: ids[i])),
        'chosen_by_class': chosen_by_class,
        'assignment': assignment,
        'assignment_rank_hist': hist,
        'class_minimum_histogram': dict(sorted(Counter(class_minima).items())),
        'solver_stats_total': dict(sorted(stats_total.items())),
    }


def analyze_threshold(geo, base_groups, threshold):
    transforms = geo['transforms']
    ids = geo['ids']
    residual_rank = geo['residual_rank']
    solved = solve_assignment(geo, threshold)

    rows_by_group = defaultdict(list)
    gauge_failures = []
    signature_rank_hist = Counter()
    signature_by_polar = defaultdict(Counter)
    scalar_cut_hist = Counter()
    raw_rows = 0

    for i, child in enumerate(transforms):
        root_i = solved['assignment'][i]
        root = transforms[root_i]
        dc, dlin, drows, _ix0, ibasis = R.residual_form(child, root)
        rec = R.minimal_quadratic_signature(dc, dlin, drows)
        expected = residual_rank[(i, root_i)]
        assert rec['polar_rank'] == expected <= threshold
        signature_rank_hist[rec['signature_rank']] += 1
        signature_by_polar[expected][rec['signature_rank']] += 1
        scalar_cut_hist[rec['scalar_cut']] += 1
        raw_rows += rec['signature_rank']

        gid = child['group_id']
        base = base_groups[gid]
        for coeff in rec['signature_basis']:
            rep, gauge = R.lift_signature_row(coeff, ibasis)
            delta = (
                R.gf2_rank(list(base['combined_basis']) + list(gauge))
                - base['combined_rank']
            )
            if delta:
                gauge_failures.append((ids[i], ids[root_i], gid, delta))
            rows_by_group[gid].append(rep)

    augmented = []
    extra_hist = Counter()
    residual_union_hist = Counter()
    for gid, base in enumerate(base_groups):
        rbasis = R.gf2_basis(rows_by_group.get(gid, ()))
        residual_union_hist[len(rbasis)] += 1
        cbasis = R.gf2_basis(list(base['combined_basis']) + list(rbasis))
        extra = len(cbasis) - base['combined_rank']
        extra_hist[extra] += 1
        augmented.append({
            'group_id': gid,
            'multiplicity': base['multiplicity'],
            'base_rank': base['combined_rank'],
            'residual_signature_union_rank': len(rbasis),
            'combined_rank': len(cbasis),
            'extra_rank': extra,
            'combined_basis': cbasis,
        })

    profiles = None
    if not gauge_failures:
        profiles = R.recursive_profiles(augmented)

    return {
        'threshold': threshold,
        'minimum_templates': len(solved['chosen_global']),
        'chosen_template_ids': [list(ids[i]) for i in solved['chosen_global']],
        'class_minimum_template_histogram': solved['class_minimum_histogram'],
        'solver_stats_total': solved['solver_stats_total'],
        'assignment_residual_polar_rank_histogram': dict(sorted(solved['assignment_rank_hist'].items())),
        'minimal_signature_rank_histogram': dict(sorted(signature_rank_hist.items())),
        'minimal_signature_rank_by_polar_rank': {
            k: dict(sorted(v.items())) for k, v in sorted(signature_by_polar.items())
        },
        'scalar_cut_histogram': dict(sorted(scalar_cut_hist.items())),
        'total_signature_rows_before_group_union': raw_rows,
        'gauge_failure_count': len(gauge_failures),
        'all_lift_gauges_contained': not gauge_failures,
        'first_gauge_failures': [
            {'transform': list(a), 'template': list(b), 'group_id': gid, 'gauge_delta': d}
            for a, b, gid, d in gauge_failures[:30]
        ],
        'residual_signature_union_rank_histogram': dict(sorted(residual_union_hist.items())),
        'extra_rank_histogram': dict(sorted(extra_hist.items())),
        'groups_with_zero_extra_rank': extra_hist.get(0, 0),
        'max_extra_rank': max(extra_hist) if extra_hist else 0,
        'global_augmented_linear_rank': R.B.A.L.union_rank(augmented, 'combined_basis'),
        **(profiles or {}),
    }


def analyze():
    geo = E.build_geometry()
    base_groups, baseline = R.build_radical_support_groups()
    assert baseline == 61
    results = {
        t: analyze_threshold(geo, base_groups, t)
        for t in THRESHOLDS
    }
    out = {
        'position': 'C',
        'physical_shared_dimension': 149,
        'baseline_width': 61,
        'results': results,
        'decision': (
            f'ALL_577_TEMPLATE_RESIDUAL_PARETO_'
            f'R6_T{results[6]["minimum_templates"]}_W{results[6].get("best_recursive_width","NA")}_'
            f'R8_T{results[8]["minimum_templates"]}_W{results[8].get("best_recursive_width","NA")}'
        ),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_TEMPLATE_RESIDUAL_PARETO')
    print('scope=exact R6/R8 template minima and gauge-aware residual-signature separator measurements completing the R2/R4 trade-off table')
    print('important=selected-template common high-rank signs remain excluded from all widths')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
