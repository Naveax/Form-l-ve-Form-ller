#!/usr/bin/env python3
"""Exact memory-bounded junction count for tail4-expanded physical + affine factors.

The merged topology authority gives a width-12 chordal completion with a largest raw
clique capacity of 67,108,864 assignments. Materializing those assignments as Python
tuples is wasteful. This verifier instead builds one dense boolean relation tensor per
clique and performs junction-tree sum-product modulo several 31-bit primes using NumPy
uint64 arrays. Every multiply is reduced modulo the current prime before the next
multiply, and every eliminated axis has size at most five, so uint64 arithmetic cannot
overflow. CRT reconstruction is unique because the product of moduli is required to
exceed the full quotient assignment universe.

This changes representation only. The factors are the same exact 38 frozen ternaries,
10 tail3 ternaries, 12 tail4 ternaries, five-quaternary conjunction, and 19 complete
affine all-nonzero obstructions.
"""
from __future__ import annotations

import itertools
import json
import math
import os
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from sympy import prevprime

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_compiler_exact as P
import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_forest_exact as J
import verify_v26_q138_c916_e0_first_dyadic_current_physical_plus_affine_junction_compiler_exact as C
import verify_v26_q138_c916_e0_first_dyadic_current_physical_plus_affine_treewidth_exact as W
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_all_known_physical_exact as H
import verify_v26_q138_c916_e0_first_dyadic_tail3_expanded_physical_junction_compiler_exact as E3
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_junction_compiler_exact as E4
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_plus_affine_topology as TOP

EXPECTED_TERNARY_COUNT = 60
EXPECTED_AFFINE_COUNT = 19
CURRENT_38_COMBINED_COUNT = 681_934_454_409_791_000_768_011_200
TAIL3_COMBINED_COUNT = 610_168_911_320_611_717_122_698_496
EXPECTED_WIDTH = 12
EXPECTED_LARGEST_CAPACITY = 67_108_864
EXPECTED_TOTAL_CAPACITY = 125_989_520


def assign_scope(scope, cliques):
    wanted = set(scope)
    candidates = [i for i, bag in enumerate(cliques) if wanted <= set(bag)]
    assert candidates, scope
    return min(candidates, key=lambda i: (len(cliques[i]), tuple(cliques[i]), i))


def build_model():
    frozen = P.load_ternary_factors()
    tail3 = E3.load_tail3_factors()
    tail4 = E4.load_tail4_factors()
    assert len(frozen) == 38 and len(tail3) == 10 and len(tail4) == 12
    ternary = frozen + tail3 + tail4
    scopes = [tuple(f["scope"]) for f in ternary]
    assert len(scopes) == EXPECTED_TERNARY_COUNT
    assert len(set(scopes)) == len(scopes)

    affine = C.affine_scopes()
    assert len(affine) == EXPECTED_AFFINE_COUNT

    base_scopes = tuple(W.all_scopes())
    tail3_scopes_all = base_scopes + tuple(f["scope"] for f in tail3)
    all_scopes = tail3_scopes_all + tuple(f["scope"] for f in tail4)
    assert len(all_scopes) == 84
    tail3_variables = {v for scope in tail3_scopes_all for v in scope}
    tail4_variables = {v for scope in all_scopes for v in scope}
    newly_introduced_variables_vs_tail3 = tuple(sorted(tail4_variables - tail3_variables))
    assert not newly_introduced_variables_vs_tail3, newly_introduced_variables_vs_tail3
    assert len(tail4_variables) == 48
    adj = W.build_primal_graph(all_scopes)
    rows, fills = W.deterministic_min_fill_certificate(adj)
    width = max(int(row["later_degree"]) for row in rows)
    assert width == EXPECTED_WIDTH
    simple_rows = tuple(
        (int(row["vertex"]), tuple(map(int, row["later_neighbors"])))
        for row in rows
    )
    cliques = J.maximal_cliques(simple_rows)
    forest = J.maximum_intersection_forest(cliques)
    J.verify_running_intersection(cliques, forest)
    assert len(cliques) == 25
    assert len(forest) == 20

    qsizes = J.quotient_sizes_from_m4()
    capacities = tuple(math.prod(qsizes[v] for v in bag) for bag in cliques)
    assert max(capacities) == EXPECTED_LARGEST_CAPACITY
    assert sum(capacities) == EXPECTED_TOTAL_CAPACITY

    attached = defaultdict(list)
    attachments = []

    for factor in ternary:
        ci = assign_scope(factor["scope"], cliques)
        attached[ci].append(("finite_forbidden", tuple(factor["scope"]), factor["forbidden"], str(factor["name"])))
        attachments.append((str(factor["name"]), ci))

    quad_scope = tuple(map(int, H.FIVE_GIDS))
    quad_allowed = frozenset(tuple(map(int, row)) for row in H.ALLOWED)
    assert len(quad_allowed) == 832
    qci = assign_scope(quad_scope, cliques)
    attached[qci].append(("allowed", quad_scope, quad_allowed, "physical_quads:compiled5"))
    attachments.append(("physical_quads:compiled5", qci))

    for ai, scope in enumerate(affine):
        scope = tuple(map(int, scope))
        ci = assign_scope(scope, cliques)
        attached[ci].append(("affine_all_nonzero_forbidden", scope, None, f"affine:{ai}"))
        attachments.append((f"affine:{ai}", ci))

    assert len(attachments) == EXPECTED_TERNARY_COUNT + 1 + EXPECTED_AFFINE_COUNT
    return (
        tuple(cliques),
        tuple(forest),
        qsizes,
        dict(attached),
        tuple(sorted(attachments)),
        tuple(fills),
        newly_introduced_variables_vs_tail3,
    )


def build_current_38_regression_model():
    frozen = P.load_ternary_factors()
    assert len(frozen) == 38
    affine = C.affine_scopes()
    assert len(affine) == EXPECTED_AFFINE_COUNT

    cliques, forest, fills = C.build_cliques_and_forest()
    qsizes = J.quotient_sizes_from_m4()
    attached = defaultdict(list)

    for factor in frozen:
        ci = assign_scope(factor["scope"], cliques)
        attached[ci].append(("finite_forbidden", tuple(factor["scope"]), factor["forbidden"], str(factor["name"])))

    quad_scope = tuple(map(int, H.FIVE_GIDS))
    quad_allowed = frozenset(tuple(map(int, row)) for row in H.ALLOWED)
    assert len(quad_allowed) == 832
    qci = assign_scope(quad_scope, cliques)
    attached[qci].append(("allowed", quad_scope, quad_allowed, "physical_quads:compiled5"))

    for ai, scope in enumerate(affine):
        scope = tuple(map(int, scope))
        ci = assign_scope(scope, cliques)
        attached[ci].append(("affine_all_nonzero_forbidden", scope, None, f"affine:{ai}"))

    return tuple(cliques), tuple(forest), qsizes, dict(attached), tuple(fills)


def local_relation(kind, scope, relation, bag, qsizes):
    pos = {v: i for i, v in enumerate(bag)}
    ordered_scope = tuple(sorted(scope, key=lambda v: pos[v]))
    shape = tuple(qsizes[v] for v in ordered_scope)
    rel = np.ones(shape, dtype=np.bool_)

    if kind == "finite_forbidden":
        original_pos = {v: i for i, v in enumerate(scope)}
        for row in relation:
            key = tuple(int(row[original_pos[v]]) for v in ordered_scope)
            rel[key] = False
    elif kind == "allowed":
        rel.fill(False)
        original_pos = {v: i for i, v in enumerate(scope)}
        for row in relation:
            key = tuple(int(row[original_pos[v]]) for v in ordered_scope)
            rel[key] = True
    else:
        assert kind == "affine_all_nonzero_forbidden"
        # In this quotient encoding the maximal local state index is zero activity.
        # Therefore nonzero activity is exactly states 0..q-2.
        forbidden_box = tuple(slice(0, qsizes[v] - 1) for v in ordered_scope)
        rel[forbidden_box] = False

    full_shape = [1] * len(bag)
    for v in ordered_scope:
        full_shape[pos[v]] = qsizes[v]
    return rel.reshape(tuple(full_shape))


def build_allowed_masks(cliques, qsizes, attached):
    masks = []
    meta = []
    for ci, bag0 in enumerate(cliques):
        bag = tuple(map(int, bag0))
        shape = tuple(qsizes[v] for v in bag)
        mask = np.ones(shape, dtype=np.bool_)
        names = []
        for kind, scope, relation, name in attached.get(ci, ()):
            mask &= local_relation(kind, scope, relation, bag, qsizes)
            names.append(name)
        allowed = int(np.count_nonzero(mask))
        assert allowed > 0, (ci, bag)
        masks.append(mask)
        meta.append({
            "clique": ci,
            "bag": list(bag),
            "capacity": int(mask.size),
            "allowed_rows": allowed,
            "constraints": names,
        })
    return tuple(masks), tuple(meta)


def forest_adjacency(n, forest):
    adj = [[] for _ in range(n)]
    for i, j, sep in forest:
        sep = tuple(map(int, sep))
        adj[i].append((j, sep))
        adj[j].append((i, sep))
    return adj


def component_roots(cadj, capacities):
    unseen = set(range(len(cadj)))
    roots = []
    while unseen:
        start = min(unseen)
        stack = [start]
        comp = []
        while stack:
            i = stack.pop()
            if i not in unseen:
                continue
            unseen.remove(i)
            comp.append(i)
            for j, _sep in cadj[i]:
                if j in unseen:
                    stack.append(j)
        # Root the component at its largest clique so the largest tensor never has to
        # be exported as a separator message.
        root = max(comp, key=lambda i: (capacities[i], len(cadj[i]), -i))
        roots.append((root, tuple(sorted(comp))))
    return tuple(roots)


def reduce_to_separator(work, bag, separator, prime):
    keep = set(separator)
    current_bag = list(bag)
    for axis in range(len(current_bag) - 1, -1, -1):
        if current_bag[axis] in keep:
            continue
        work = work.sum(axis=axis, dtype=np.uint64)
        if isinstance(work, np.ndarray):
            np.remainder(work, prime, out=work)
        else:
            work = np.uint64(int(work) % prime)
        current_bag.pop(axis)
    assert tuple(current_bag) == tuple(v for v in bag if v in keep)
    return work, tuple(current_bag)


def count_mod_prime(prime, cliques, masks, forest, qsizes):
    cadj = forest_adjacency(len(cliques), forest)
    capacities = tuple(mask.size for mask in masks)
    roots = component_roots(cadj, capacities)

    sys.setrecursionlimit(max(1000, len(cliques) * 10))

    def message(i, parent):
        bag = tuple(map(int, cliques[i]))
        work = masks[i].astype(np.uint64, copy=True)
        sep_to_parent = ()
        for j, sep in cadj[i]:
            if j == parent:
                sep_to_parent = tuple(sep)
                continue
            child_msg, child_vars = message(j, i)
            assert tuple(child_vars) == tuple(sep)
            shape = [1] * len(bag)
            pos = {v: p for p, v in enumerate(bag)}
            for axis, v in enumerate(child_vars):
                shape[pos[v]] = child_msg.shape[axis]
            view = child_msg.reshape(tuple(shape))
            np.multiply(work, view, out=work)
            np.remainder(work, prime, out=work)
            del child_msg, view

        if parent is None:
            reduced, variables = reduce_to_separator(work, bag, (), prime)
            assert variables == ()
            return int(reduced), ()
        reduced, variables = reduce_to_separator(work, bag, sep_to_parent, prime)
        return reduced, variables

    total = 1
    component_residues = []
    for root, _comp in roots:
        residue, variables = message(root, None)
        assert variables == ()
        component_residues.append(int(residue))
        total = (total * int(residue)) % prime
    return int(total), tuple(component_residues)


def exact_crt(residues, primes):
    x = 0
    modulus = 1
    for residue, prime in zip(residues, primes):
        t = ((int(residue) - x) % prime) * pow(modulus, -1, prime) % prime
        x += modulus * t
        modulus *= prime
    return int(x), int(modulus)


def choose_primes(universe_bound):
    primes = []
    product = 1
    cursor = 2**31
    while product <= universe_bound:
        p = int(prevprime(cursor))
        assert p < 2**31
        primes.append(p)
        product *= p
        cursor = p
    assert len(primes) >= 4
    return tuple(primes), int(product)


def modular_exact_count(label, cliques, masks, forest, qsizes):
    variables = tuple(sorted({v for bag in cliques for v in bag}))
    universe_bound = math.prod(qsizes[v] for v in variables)
    primes, modulus_product = choose_primes(universe_bound)
    assert modulus_product > universe_bound

    residues = []
    residue_rows = []
    for prime in primes:
        residue, components = count_mod_prime(prime, cliques, masks, forest, qsizes)
        residues.append(residue)
        row = {
            "label": label,
            "prime": prime,
            "total_residue": residue,
            "component_residues": list(components),
        }
        residue_rows.append(row)
        print("modular_residue", json.dumps(row, sort_keys=True), flush=True)

    total, crt_modulus = exact_crt(residues, primes)
    assert crt_modulus == modulus_product
    assert 0 < total <= universe_bound
    return total, universe_bound, primes, modulus_product, residue_rows


def analyze():
    # Mandatory representation regression: the new dense-mask + modular message engine
    # must exactly reproduce the already-frozen 38-ternary physical+affine authority.
    r_cliques, r_forest, r_qsizes, r_attached, _r_fills = build_current_38_regression_model()
    r_masks, _r_metadata = build_allowed_masks(r_cliques, r_qsizes, r_attached)
    regression_total, _r_universe, _r_primes, _r_modulus, _r_rows = modular_exact_count(
        "current_38_regression", r_cliques, r_masks, r_forest, r_qsizes
    )
    assert regression_total == CURRENT_38_COMBINED_COUNT, regression_total
    print(f"modular_regression_exact_count={regression_total}", flush=True)

    (
        cliques,
        forest,
        qsizes,
        attached,
        attachments,
        fills,
        newly_introduced_variables_vs_tail3,
    ) = build_model()
    masks, metadata = build_allowed_masks(cliques, qsizes, attached)

    total, universe_bound, primes, modulus_product, residue_rows = modular_exact_count(
        "tail4_expanded", cliques, masks, forest, qsizes
    )
    assert total <= TAIL3_COMBINED_COUNT
    variables = tuple(sorted({v for bag in cliques for v in bag}))

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "affine_constraint_semantics": "all-nonzero forbidden; maximal local quotient-state index is zero",
        "frozen_ternary_factors": 38,
        "tail3_promoted_ternary_factors": 10,
        "tail4_promoted_ternary_factors": 12,
        "expanded_ternary_factors": EXPECTED_TERNARY_COUNT,
        "physical_quaternary_factors": 5,
        "affine_constraints": EXPECTED_AFFINE_COUNT,
        "certified_chordal_completion_width": EXPECTED_WIDTH,
        "treewidth_lower_bound": 9,
        "treewidth_upper_bound": EXPECTED_WIDTH,
        "fill_edges": [list(map(int, row)) for row in fills],
        "maximal_cliques": len(cliques),
        "junction_forest_edges": len(forest),
        "largest_clique_capacity": max(int(mask.size) for mask in masks),
        "total_clique_capacity": sum(int(mask.size) for mask in masks),
        "largest_compiled_allowed_table": max(int(row["allowed_rows"]) for row in metadata),
        "total_compiled_allowed_rows": sum(int(row["allowed_rows"]) for row in metadata),
        "constraint_attachments": [list(x) for x in attachments],
        "quotient_variables_in_model": len(variables),
        "modular_regression_current_38_exact_count": regression_total,
        "full_assignment_universe_bound": universe_bound,
        "crt_primes": list(primes),
        "crt_modulus_product": modulus_product,
        "modular_residues": residue_rows,
        "exact_tail4_expanded_physical_plus_affine_assignment_count": total,
        "exact_tail4_expanded_physical_plus_affine_assignment_log2": math.log2(total),
        "tail3_physical_plus_affine_assignment_count": TAIL3_COMBINED_COUNT,
        "newly_introduced_variables_vs_tail3_combined": list(newly_introduced_variables_vs_tail3),
        "removed_assignments_vs_tail3_inventory": TAIL3_COMBINED_COUNT - total,
        "gain_vs_tail3_inventory_log2_bits": math.log2(TAIL3_COMBINED_COUNT) - math.log2(total),
        "clique_tables": list(metadata),
        "decision": "C916_TAIL4_EXPANDED_PHYSICAL_PLUS_COMPLETE_AFFINE_EXACT_MODULAR_JUNCTION_COUNT",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL4_EXPANDED_PHYSICAL_PLUS_AFFINE_JUNCTION_EXACT")
    print("theorem=the same dense-mask modular junction engine first reproduces the frozen 38-ternary physical+affine authority exactly, then CRT counts the 60 ternary physical factors, five-quaternary conjunction, and all 19 authority-correct affine obstructions without materializing Python tuple tables")
    print("boundary=treewidth remains bounded by 9 <= tw <= 12; the count is exact on the explicit width-12 chordal completion")
    print("boundary=this excludes the dense 4005 pairwise quotient relation layer and multiplicity weights, so it is not a weighted work exponent")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
