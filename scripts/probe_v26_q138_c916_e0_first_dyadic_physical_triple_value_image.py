#!/usr/bin/env python3
import hashlib
import itertools
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_group_output_pair_dependency as D
import probe_v26_q138_c916_e0_post_gauss_physical_phase_common as P

PHYS_N = 149
assert P.PHYS_N == PHYS_N
M4_PATH = Path(os.environ.get(
    'C916_M4_AUTHORITY',
    'authorities/m4/c916_e0_first_dyadic_four_separator_complete_authority.json',
))
TARGET_INDEX = int(os.environ.get('C916_PHYSICAL_TRIPLE_INDEX', '0'))
MAX_CELLS = int(os.environ.get('C916_PHYSICAL_TRIPLE_MAX_CELLS', '50000'))
MAX_PHASES = int(os.environ.get('C916_PHYSICAL_TRIPLE_MAX_PHASES', '14'))
MAX_WALSH_EVALS = int(os.environ.get('C916_PHYSICAL_TRIPLE_MAX_WALSH_EVALS', '2000000'))


class ResourceCap(RuntimeError):
    pass


def solve_cell(constraints):
    got = P.C.P.U.T.rref(list(constraints), n=PHYS_N)
    if got is None:
        return None
    rank, x0, basis = got
    return int(rank), int(x0), tuple(map(int, basis))


def subset_of_support(cell, support_constraints):
    _rank, x0, basis = cell
    for m, rhs in support_constraints:
        m = int(m)
        rhs = int(rhs)
        if P.parity(m & x0) != rhs:
            return False
        if any(P.parity(m & b) for b in basis):
            return False
    return True


def split_by_support(constraints, cell, support_constraints):
    support_constraints = tuple((int(m), int(rhs)) for m, rhs in support_constraints)
    if subset_of_support(cell, support_constraints):
        return ((True, tuple(constraints), cell),)

    inside = solve_cell(tuple(constraints) + support_constraints)
    if inside is None:
        return ((False, tuple(constraints), cell),)

    parts = []
    prefix = list(constraints)
    for m, rhs in support_constraints:
        outside_constraints = tuple(prefix) + ((m, rhs ^ 1),)
        outside = solve_cell(outside_constraints)
        if outside is not None:
            parts.append((False, outside_constraints, outside))
        prefix.append((m, rhs))
    final_constraints = tuple(prefix)
    final_inside = solve_cell(final_constraints)
    assert final_inside is not None
    parts.append((True, final_constraints, final_inside))

    total = sum(1 << (PHYS_N - rec[2][0]) for rec in parts)
    assert total == (1 << (PHYS_N - cell[0]))
    return tuple(parts)


def remap_mask(mask, old_to_new):
    out = 0
    y = int(mask)
    while y:
        b = y & -y
        old = b.bit_length() - 1
        out |= 1 << old_to_new[old]
        y ^= b
    return out


def leaf_value_distribution(groups, terms, active_mask, cell, stats):
    _rank, x0, basis = cell
    d = len(basis)
    base = [0, 0, 0]
    coeff_by_form = defaultdict(lambda: [0, 0, 0])

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
        clin = remap_mask(lin, old_to_new) if lin else 0
        crows = []
        for old in indices:
            crows.append(remap_mask(rows[old], old_to_new) if rows[old] else 0)
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
            for gi in range(3):
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
    assert 3 <= len(terms) <= 12

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
    root = solve_cell(())
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
        for is_active, child_constraints, child_cell in split_by_support(constraints, cell, support):
            dfs(
                ci + 1,
                child_constraints,
                child_cell,
                active_mask | term_mask if is_active else active_mask,
            )

    dfs(0, (), root, 0)
    assert sum(dist.values()) == (1 << PHYS_N)
    return dict(dist), stats


def build_ordered_groups():
    e0, _e1, _half = P.C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for zc in range(4):
        for zs, cls in e0[zc]:
            can = P.C.P.U.H.support_for('C', zs, cls)
            if can is None:
                continue
            raw += 1
            grouped[can].append((zs, cls))
    ordered = list(sorted(grouped.items(), key=lambda kv: kv[0]))
    assert raw == 577 and len(ordered) == 250
    return ordered


def candidate_triples(gids, ordered):
    anchors = {}
    codims = {}
    for gid in gids:
        can, _sectors = ordered[int(gid)]
        _prank, _local, anchor = D.projection_anchor(can)
        anchors[int(gid)] = anchor
        codims[int(gid)] = len(anchor['physical_support_constraints'])

    ranked = []
    for triple in itertools.combinations(sorted(map(int, gids)), 3):
        constraints = []
        for gid in triple:
            constraints.extend(anchors[gid]['physical_support_constraints'])
        got = P.C.P.U.T.rref(constraints, n=PHYS_N)
        if got is None:
            continue
        rank = int(got[0])
        redundancy = sum(codims[g] for g in triple) - rank
        pair_redundancy = 0
        for a, b in itertools.combinations(triple, 2):
            pair = P.C.P.U.T.rref(
                list(anchors[a]['physical_support_constraints'])
                + list(anchors[b]['physical_support_constraints']),
                n=PHYS_N,
            )
            assert pair is not None
            pair_redundancy += codims[a] + codims[b] - int(pair[0])
        ranked.append((redundancy, pair_redundancy, rank, triple))
    ranked.sort(key=lambda x: (-x[0], -x[1], -x[2], x[3]))

    diverse = []
    used = set()
    for rec in ranked:
        triple = rec[3]
        if not (set(triple) & used):
            diverse.append(rec)
            used.update(triple)
            if len(diverse) >= 16:
                break
    if len(diverse) < 16:
        seen = {rec[3] for rec in diverse}
        for rec in ranked:
            if rec[3] in seen:
                continue
            diverse.append(rec)
            seen.add(rec[3])
            if len(diverse) >= 16:
                break
    return diverse, anchors


def digest_rows(rows):
    payload = json.dumps(rows, separators=(',', ':'), sort_keys=False)
    return hashlib.sha256(payload.encode()).hexdigest()


def analyze():
    m4 = json.loads(M4_PATH.read_text())
    gids = tuple(map(int, m4['m4_group_ids']))
    assert len(gids) == len(set(gids)) == 90
    image_sizes = {
        int(row['m4_group_id']): int(row['cols'])
        for row in m4['four_parent_relations']
    }
    assert set(image_sizes) == set(gids)

    ordered = build_ordered_groups()
    shortlist, anchors = candidate_triples(gids, ordered)
    assert 0 <= TARGET_INDEX < len(shortlist)
    redundancy, pair_redundancy, anchor_rank, triple = shortlist[TARGET_INDEX]

    groups = []
    next_tid = 0
    for gid in triple:
        can, sectors = ordered[gid]
        group, next_tid = D.build_group_terms(gid, can, sectors, next_tid)
        groups.append(group)

    try:
        dist, stats = exact_joint_distribution(groups)
    except ResourceCap as exc:
        out = {
            'position': 'C',
            'physical_shared_dimension': PHYS_N,
            'target_index': TARGET_INDEX,
            'triple': list(triple),
            'projection_anchor_rank': anchor_rank,
            'projection_anchor_redundancy': redundancy,
            'pair_projection_redundancy_sum': pair_redundancy,
            'complete': False,
            'resource_cap': str(exc),
            'decision': 'PHYSICAL_TRIPLE_VALUE_IMAGE_INCOMPLETE_RESOURCE_CAP',
        }
        print('result', json.dumps(out, sort_keys=True), flush=True)
        print('INCOMPLETE V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_VALUE_IMAGE')
        print('ALPHA_PASS=0')
        return out

    image = set(dist)
    values = [sorted({row[i] for row in image}) for i in range(3)]
    for i, gid in enumerate(triple):
        assert len(values[i]) == image_sizes[gid], (gid, len(values[i]), image_sizes[gid])

    pair01 = {(a, b) for a, b, _c in image}
    pair02 = {(a, c) for a, _b, c in image}
    pair12 = {(b, c) for _a, b, c in image}
    closure = []
    for a in values[0]:
        for b in values[1]:
            if (a, b) not in pair01:
                continue
            for c in values[2]:
                if (a, c) in pair02 and (b, c) in pair12:
                    closure.append((a, b, c))
    holes = sorted(set(closure) - image)

    # The selected triples are required to have a nonempty intersection of all
    # three projection anchors. Hence every subset of their nonzero activities
    # is affine-consistent. Any pairwise-allowed missing value tuple is therefore
    # a true physical value obstruction beyond all-order affine support.
    all_anchor_constraints = []
    for gid in triple:
        all_anchor_constraints.extend(anchors[gid]['physical_support_constraints'])
    assert P.C.P.U.T.rref(all_anchor_constraints, n=PHYS_N) is not None

    image_rows = [
        [list(key), int(dist[key])]
        for key in sorted(dist)
    ]
    hole_rows = [list(row) for row in holes]
    out = {
        'position': 'C',
        'physical_shared_dimension': PHYS_N,
        'target_index': TARGET_INDEX,
        'triple': list(triple),
        'projection_anchor_rank': anchor_rank,
        'projection_anchor_redundancy': redundancy,
        'pair_projection_redundancy_sum': pair_redundancy,
        'group_image_sizes': [len(v) for v in values],
        'exact_joint_image_size': len(image),
        'pairwise_closure_size': len(closure),
        'pairwise_closure_holes': len(holes),
        'higher_order_physical_value_obstruction_found': bool(holes),
        'first_holes': hole_rows[:16],
        'hole_digest_sha256': digest_rows(hole_rows),
        'joint_distribution_digest_sha256': digest_rows(image_rows),
        'support_classes': stats['support_classes'],
        'terms': stats['terms'],
        'cells_visited': stats['cells_visited'],
        'leaf_cells': stats['leaf_cells'],
        'walsh_evals': stats['walsh_evals'],
        'max_phase_forms': stats['max_phase_forms'],
        'max_relevant_phase_dimension': stats['max_relevant_phase_dimension'],
        'complete': True,
        'decision': (
            'EXACT_PHYSICAL_TRIPLE_VALUE_OBSTRUCTION_BEYOND_PAIRWISE_AND_AFFINE'
            if holes
            else 'NO_TRIPLE_VALUE_OBSTRUCTION_FOR_THIS_EXACT_TARGET'
        ),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    if holes:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_VALUE_OBSTRUCTION')
        print('theorem=for the emitted affine-consistent m4 triple, the exact physical joint value image is strictly smaller than the join of its three exact pair projections; every emitted hole is therefore forbidden by a genuine ternary physical-value constraint not implied by pairwise value factors or all-order affine support')
    else:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_VALUE_IMAGE_TARGET')
        print('theorem=for this emitted affine-consistent m4 triple, the exact physical joint value image equals the join of its three exact pair projections')
    print('boundary=this is an exact target-level theorem only; untested m4 triples and higher arities remain open')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
