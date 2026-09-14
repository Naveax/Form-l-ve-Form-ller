#!/usr/bin/env python3
import itertools
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_group_output_pair_dependency as D
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T
import probe_v26_q138_c916_e0_post_gauss_physical_phase_common as P

PHYS_N = 149
AFFINE_FIVE = (4, 5, 8, 9, 114)
TARGETS = tuple(itertools.combinations(AFFINE_FIVE, 4))
TARGET_INDEX = int(os.environ.get('C916_PHYSICAL_QUAD_INDEX', '0'))
MAX_CELLS = int(os.environ.get('C916_PHYSICAL_QUAD_MAX_CELLS', '150000'))
MAX_PHASES = int(os.environ.get('C916_PHYSICAL_QUAD_MAX_PHASES', '18'))
MAX_WALSH_EVALS = int(os.environ.get('C916_PHYSICAL_QUAD_MAX_WALSH_EVALS', '8000000'))


class ResourceCap(RuntimeError):
    pass


def leaf_value_distribution(groups, terms, active_mask, cell, stats):
    _rank, x0, basis = cell
    d = len(basis)
    arity = len(groups)
    base = [0] * arity
    coeff_by_form = defaultdict(lambda: [0] * arity)

    scan = int(active_mask)
    while scan:
        b = scan & -scan
        ti = b.bit_length() - 1
        scan ^= b
        term = terms[ti]
        c, lin, rows = P.restrict_anchor_sign(term['anchor'], x0, basis)
        coef = int(term['coefficient'])
        if int(c):
            coef = -coef
        form = (int(lin), tuple(map(int, rows)))
        coeff_by_form[form][int(term['_group_slot'])] += coef

    forms = []
    coeffs = []
    for form, vec in sorted(coeff_by_form.items()):
        if not any(vec):
            continue
        lin, rows = form
        if lin == 0 and not any(rows):
            for i, value in enumerate(vec):
                base[i] += int(value)
        else:
            forms.append((lin, rows))
            coeffs.append(tuple(map(int, vec)))

    if len(forms) > MAX_PHASES:
        raise ResourceCap(f'phase_forms>{MAX_PHASES}')

    used = 0
    for lin, rows in forms:
        used |= int(lin)
        for i, row in enumerate(rows):
            row = int(row)
            if row:
                used |= row | (1 << i)
    indices = [i for i in range(d) if (used >> i) & 1]
    old_to_new = {old: new for new, old in enumerate(indices)}
    kdim = len(indices)
    free = d - kdim

    compact_forms = []
    for lin, rows in forms:
        clin = T.remap_mask(lin, old_to_new) if lin else 0
        crows = []
        for old in indices:
            crows.append(T.remap_mask(rows[old], old_to_new) if rows[old] else 0)
        compact_forms.append((clin, tuple(crows)))

    t = len(compact_forms)
    n = 1 << t
    stats['walsh_evals'] += max(0, n - 1)
    if stats['walsh_evals'] > MAX_WALSH_EVALS:
        raise ResourceCap(f'walsh_evals>{MAX_WALSH_EVALS}')

    combo_lin = [0] * n
    zero_rows = tuple(0 for _ in range(kdim))
    combo_rows = [zero_rows] * n
    walsh = [0] * n
    walsh[0] = 1 << kdim
    for mask in range(1, n):
        bit = mask & -mask
        j = bit.bit_length() - 1
        prev = mask ^ bit
        flin, frows = compact_forms[j]
        lin = combo_lin[prev] ^ flin
        rows = tuple(a ^ b for a, b in zip(combo_rows[prev], frows))
        combo_lin[mask] = lin
        combo_rows[mask] = rows
        walsh[mask] = D.full_quadratic_moment(0, lin, rows)

    free_factor = 1 << free
    counts = [int(v) * free_factor for v in walsh]
    h = 1
    while h < n:
        for start in range(0, n, 2 * h):
            for j in range(h):
                a = counts[start + j]
                b = counts[start + j + h]
                counts[start + j] = a + b
                counts[start + j + h] = a - b
        h *= 2

    out = defaultdict(int)
    cell_points = 1 << d
    total = 0
    for bits, raw in enumerate(counts):
        assert raw % n == 0
        multiplicity = raw // n
        assert multiplicity >= 0
        if multiplicity == 0:
            continue
        values = list(base)
        for j, vec in enumerate(coeffs):
            sign = -1 if ((bits >> j) & 1) else 1
            for gi in range(arity):
                values[gi] += sign * vec[gi]
        out[tuple(values)] += multiplicity
        total += multiplicity
    assert total == cell_points
    stats['leaf_cells'] += 1
    stats['max_phase_forms'] = max(stats['max_phase_forms'], t)
    stats['max_relevant_phase_dimension'] = max(stats['max_relevant_phase_dimension'], kdim)
    return out


def exact_joint_distribution(groups):
    terms = []
    for gi, group in enumerate(groups):
        for term in group['terms']:
            rec = dict(term)
            rec['_group_slot'] = gi
            terms.append(rec)

    class_map = defaultdict(list)
    for ti, term in enumerate(terms):
        key = tuple((int(m), int(rhs)) for m, rhs in term['anchor']['physical_support_constraints'])
        class_map[key].append(ti)
    classes = []
    for support, tis in class_map.items():
        mask = 0
        for ti in tis:
            mask |= 1 << ti
        classes.append((support, mask))
    classes.sort(key=lambda item: (len(item[0]), item[0]))

    stats = {
        'cells_visited': 0,
        'leaf_cells': 0,
        'walsh_evals': 0,
        'max_phase_forms': 0,
        'max_relevant_phase_dimension': 0,
        'support_classes': len(classes),
        'terms': len(terms),
    }
    dist = defaultdict(int)
    root = T.solve_cell(())
    assert root == (0, 0, tuple(1 << i for i in range(PHYS_N)))

    def dfs(ci, constraints, cell, active_mask):
        stats['cells_visited'] += 1
        if stats['cells_visited'] > MAX_CELLS:
            raise ResourceCap(f'cells>{MAX_CELLS}')
        if ci == len(classes):
            local = leaf_value_distribution(groups, terms, active_mask, cell, stats)
            for values, count in local.items():
                dist[values] += count
            return
        support, term_mask = classes[ci]
        for is_active, child_constraints, child_cell in T.split_by_support(constraints, cell, support):
            dfs(
                ci + 1,
                child_constraints,
                child_cell,
                active_mask | term_mask if is_active else active_mask,
            )

    dfs(0, (), root, 0)
    assert sum(dist.values()) == (1 << PHYS_N)
    return dict(dist), stats


def pairwise_closure(image, values):
    arity = len(values)
    pairsets = {}
    for i in range(arity):
        for j in range(i + 1, arity):
            pairsets[(i, j)] = {(row[i], row[j]) for row in image}
    closure = []
    for row in itertools.product(*values):
        if all((row[i], row[j]) in pairsets[(i, j)] for i in range(arity) for j in range(i + 1, arity)):
            closure.append(tuple(row))
    return tuple(closure)


def analyze():
    assert 0 <= TARGET_INDEX < len(TARGETS)
    target = tuple(map(int, TARGETS[TARGET_INDEX]))
    ordered = T.build_ordered_groups()

    groups = []
    next_tid = 0
    all_anchor_constraints = []
    for gid in target:
        can, sectors = ordered[gid]
        group, next_tid = D.build_group_terms(gid, can, sectors, next_tid)
        groups.append(group)
        all_anchor_constraints.extend(group['projection_anchor']['physical_support_constraints'])

    # The seed 5-set is an inclusion-minimal affine conflict, hence every
    # selected 4-subset must have nonempty simultaneous exact affine support.
    assert P.C.P.U.T.rref(all_anchor_constraints, n=PHYS_N) is not None

    try:
        dist, stats = exact_joint_distribution(groups)
    except ResourceCap as exc:
        out = {
            'position': 'C',
            'physical_shared_dimension': PHYS_N,
            'target_index': TARGET_INDEX,
            'quadruple': list(target),
            'complete': False,
            'resource_cap': str(exc),
            'decision': 'PHYSICAL_QUAD_VALUE_IMAGE_INCOMPLETE_RESOURCE_CAP',
        }
        print('result', json.dumps(out, sort_keys=True), flush=True)
        print('INCOMPLETE V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_QUAD_VALUE_IMAGE')
        print('ALPHA_PASS=0')
        return out

    image = set(dist)
    values = tuple(tuple(sorted({row[i] for row in image})) for i in range(4))
    assert tuple(map(len, values)) == (7, 7, 7, 7)
    closure = pairwise_closure(image, values)
    holes = tuple(sorted(set(closure) - image))
    image_rows = [[list(key), int(dist[key])] for key in sorted(dist)]

    out = {
        'position': 'C',
        'physical_shared_dimension': PHYS_N,
        'target_index': TARGET_INDEX,
        'quadruple': list(target),
        'group_image_sizes': [len(v) for v in values],
        'exact_joint_image_size': len(image),
        'pairwise_closure_size': len(closure),
        'pairwise_closure_holes': len(holes),
        'higher_order_physical_value_obstruction_found': bool(holes),
        'first_holes': [list(row) for row in holes[:16]],
        'hole_digest_sha256': T.digest_rows([list(row) for row in holes]),
        'joint_distribution_digest_sha256': T.digest_rows(image_rows),
        'support_classes': stats['support_classes'],
        'terms': stats['terms'],
        'cells_visited': stats['cells_visited'],
        'leaf_cells': stats['leaf_cells'],
        'walsh_evals': stats['walsh_evals'],
        'max_phase_forms': stats['max_phase_forms'],
        'max_relevant_phase_dimension': stats['max_relevant_phase_dimension'],
        'complete': True,
        'decision': (
            'EXACT_PHYSICAL_QUAD_VALUE_OBSTRUCTION_BEYOND_PAIRWISE_AND_AFFINE'
            if holes
            else 'NO_QUAD_VALUE_OBSTRUCTION_FOR_THIS_EXACT_TARGET'
        ),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    if holes:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_QUAD_VALUE_OBSTRUCTION')
        print('theorem=for the emitted affine-consistent four-output set, the exact physical joint value image is strictly smaller than the join of all six exact pair projections; every emitted hole is a genuine physical-value constraint not implied by pairwise value factors or all-order affine support')
    else:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_QUAD_VALUE_IMAGE_TARGET')
        print('theorem=for this emitted affine-consistent four-output set, the exact physical joint value image equals the join of all six exact pair projections')
    print('boundary=this is an exact target-level theorem only; other quadruples and higher arities remain open')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
