#!/usr/bin/env python3
"""Compile all current C916 physical quotient factors into exact junction tables.

This verifier is deliberately independent of the weighted pairwise/affine counter.  Its
purpose is to turn the merged treewidth-5 / junction-forest theorem into executable exact
relation tables and to prove that the compiled tables are semantically identical to the
current physical higher-order factor inventory.

Input:
  * 38 exact ternary quotient-factor JSON files emitted by the all-current factor matrix;
  * the already-certified conjunction of the five physical quaternary quotient factors;
  * the merged current physical junction-forest topology.

Output:
  * exact allowed table for every maximal clique;
  * exact separator-message domains;
  * an exact junction-tree count of assignments satisfying the physical layer alone.

This is not yet the final weighted count.  It is the bounded-table compiler needed to
replace repeated forbidden-tuple scans by exact separator messages inside that counter.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as T
import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_forest_exact as J
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_all_known_physical_exact as H

FACTOR_DIR = Path(os.environ.get("C916_CURRENT_PHYSICAL_FACTOR_DIR", "authorities/current-physical-factors"))
EXPECTED_TERNARY_COUNT = 38
EXPECTED_QUAD_CONJUNCTION_ROWS = 832


def digest(obj) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def load_ternary_factors():
    rows = []
    for i, expected_scope in enumerate(T.TERNARY_FACTORS):
        path = FACTOR_DIR / f"factor_{i:02d}.json"
        row = json.loads(path.read_text())
        assert int(row["inventory_index"]) == i
        scope = tuple(map(int, row["triple"]))
        assert scope == tuple(map(int, expected_scope))
        qsizes = tuple(map(int, row["quotient_alphabet_sizes"]))
        forbidden = frozenset(tuple(map(int, x)) for x in row["quotient_hole_tuples"])
        assert len(qsizes) == 3
        assert forbidden and len(forbidden) == int(row["quotient_holes"])
        rows.append(
            {
                "name": f"ternary:{i}",
                "scope": scope,
                "qsizes": qsizes,
                "forbidden": forbidden,
                "digest": str(row["quotient_hole_digest_sha256"]),
            }
        )
    assert len(rows) == EXPECTED_TERNARY_COUNT
    return tuple(rows)


def build_cliques_and_forest():
    adj = J.build_primal_graph()
    rows = J.perfect_elimination_rows(adj)
    cliques = J.maximal_cliques(rows)
    forest = J.maximum_intersection_forest(cliques)
    J.verify_running_intersection(cliques, forest)
    assert len(cliques) == J.EXPECTED_CLIQUE_COUNT
    assert len(forest) == J.EXPECTED_FOREST_EDGES
    return cliques, forest


def assign_factor_to_clique(scope, cliques):
    s = set(scope)
    candidates = [i for i, bag in enumerate(cliques) if s <= set(bag)]
    assert candidates, scope
    return min(candidates, key=lambda i: (len(cliques[i]), cliques[i], i))


def compile_tables(cliques, ternary_factors, qsizes):
    attached = defaultdict(list)
    for factor in ternary_factors:
        ci = assign_factor_to_clique(factor["scope"], cliques)
        attached[ci].append(factor)

    # The five physical quaternary relations were already certified as one exact
    # five-variable allowed relation.  Their union of scopes is itself contained in one
    # maximal clique, so imposing the compiled relation there is exactly equivalent to
    # imposing the five original quaternary factors separately.
    quad_scope = tuple(map(int, H.FIVE_GIDS))
    qci = assign_factor_to_clique(quad_scope, cliques)
    allowed5 = frozenset(tuple(map(int, row)) for row in H.ALLOWED)
    assert len(allowed5) == EXPECTED_QUAD_CONJUNCTION_ROWS

    tables = []
    attachment_rows = []
    for ci, bag in enumerate(cliques):
        bag = tuple(map(int, bag))
        pos = {v: p for p, v in enumerate(bag)}
        domains = [range(qsizes[v]) for v in bag]
        allowed = []
        local_factors = tuple(attached.get(ci, ()))
        for assignment in itertools.product(*domains):
            ok = True
            for factor in local_factors:
                row = tuple(assignment[pos[v]] for v in factor["scope"])
                if row in factor["forbidden"]:
                    ok = False
                    break
            if ok and ci == qci:
                qrow = tuple(assignment[pos[v]] for v in quad_scope)
                if qrow not in allowed5:
                    ok = False
            if ok:
                allowed.append(tuple(map(int, assignment)))
        allowed = tuple(allowed)
        assert allowed, (ci, bag)
        tables.append(allowed)
        attachment_rows.append(
            {
                "clique": ci,
                "bag": list(bag),
                "capacity": math.prod(qsizes[v] for v in bag),
                "allowed_rows": len(allowed),
                "ternary_factors": [f["name"] for f in local_factors],
                "contains_compiled_five_quad_relation": ci == qci,
                "table_digest_sha256": digest([list(row) for row in allowed]),
            }
        )

    assigned_names = {name for row in attachment_rows for name in row["ternary_factors"]}
    assert len(assigned_names) == EXPECTED_TERNARY_COUNT
    assert assigned_names == {f"ternary:{i}" for i in range(EXPECTED_TERNARY_COUNT)}
    assert sum(bool(row["contains_compiled_five_quad_relation"]) for row in attachment_rows) == 1
    return tuple(tables), tuple(attachment_rows), qci


def forest_adjacency(ncliques, forest):
    adj = [[] for _ in range(ncliques)]
    for i, j, sep in forest:
        sep = tuple(map(int, sep))
        adj[i].append((j, sep))
        adj[j].append((i, sep))
    return adj


def exact_junction_count(cliques, tables, forest):
    cadj = forest_adjacency(len(cliques), forest)
    seen = set()
    component_counts = []
    message_sizes = []

    for root in range(len(cliques)):
        if root in seen:
            continue
        parent = {root: None}
        parent_sep = {}
        order = []
        q = deque([root])
        seen.add(root)
        while q:
            i = q.popleft()
            order.append(i)
            for j, sep in cadj[i]:
                if j in parent:
                    continue
                parent[j] = i
                parent_sep[j] = sep
                seen.add(j)
                q.append(j)

        messages = {}
        for i in reversed(order):
            bag = tuple(cliques[i])
            pos = {v: p for p, v in enumerate(bag)}
            p = parent[i]
            sep_to_parent = tuple(parent_sep[i]) if p is not None else ()
            accum = defaultdict(int)
            for assignment in tables[i]:
                weight = 1
                for child, sep in cadj[i]:
                    if parent.get(child) != i:
                        continue
                    child_msg = messages[child]
                    key = tuple(assignment[pos[v]] for v in sep)
                    weight *= int(child_msg.get(key, 0))
                    if weight == 0:
                        break
                if weight == 0:
                    continue
                if p is None:
                    accum[()] += weight
                else:
                    key = tuple(assignment[pos[v]] for v in sep_to_parent)
                    accum[key] += weight
            if p is None:
                assert set(accum) <= {()}
                component_counts.append(int(accum.get((), 0)))
            else:
                messages[i] = dict(accum)
                message_sizes.append(
                    {
                        "child": i,
                        "parent": p,
                        "separator": list(sep_to_parent),
                        "positive_message_rows": len(accum),
                        "message_weight_sum": sum(accum.values()),
                    }
                )

    assert len(component_counts) == 6
    total = math.prod(component_counts)
    return total, tuple(component_counts), tuple(message_sizes)


def analyze():
    ternary = load_ternary_factors()
    cliques, forest = build_cliques_and_forest()
    qsizes = J.quotient_sizes_from_m4()

    # Every current physical variable must have its authoritative quotient alphabet.
    vars_in_layer = {v for bag in cliques for v in bag}
    assert vars_in_layer == set(qsizes) & vars_in_layer

    tables, attachments, quad_clique = compile_tables(cliques, ternary, qsizes)
    total, component_counts, messages = exact_junction_count(cliques, tables, forest)
    assert total > 0

    capacities = [math.prod(qsizes[v] for v in bag) for bag in cliques]
    allowed_sizes = [len(tab) for tab in tables]
    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "physical_factor_scope_digest_sha256": T.EXPECTED_SCOPE_DIGEST,
        "exact_treewidth": T.EXPECTED_TREEWIDTH,
        "ternary_factors": len(ternary),
        "physical_quaternary_factors": len(T.QUATERNARY_FACTORS),
        "compiled_five_quad_relation_rows": len(H.ALLOWED),
        "maximal_cliques": len(cliques),
        "junction_forest_edges": len(forest),
        "compiled_quad_clique": quad_clique,
        "clique_table_capacity_sum": sum(capacities),
        "clique_table_allowed_rows_sum": sum(allowed_sizes),
        "largest_clique_capacity": max(capacities),
        "largest_compiled_allowed_table": max(allowed_sizes),
        "component_physical_assignment_counts": list(component_counts),
        "exact_physical_layer_assignment_count": int(total),
        "exact_physical_layer_assignment_log2": math.log2(total),
        "message_rows": list(messages),
        "max_positive_separator_message_rows": max((row["positive_message_rows"] for row in messages), default=1),
        "attachments": list(attachments),
        "decision": "C916_ALL_CURRENT_PHYSICAL_FACTORS_COMPILE_EXACTLY_INTO_WIDTH5_JUNCTION_TABLES",
        "next_exact_step": "replace repeated higher-order forbidden-tuple scans in the all-current weighted counter by these exact clique tables and separator messages, preserving pairwise and affine coupling",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_CURRENT_PHYSICAL_JUNCTION_COMPILER_EXACT")
    print("theorem=all 38 current ternary physical quotient factors plus the exact conjunction of the five current quaternary physical factors compile into the certified treewidth-5 junction forest, and exact sum-product over that forest counts the physical layer without expanding one event bit per forbidden tuple")
    print("boundary=this is an exact compiler/count for the physical higher-order layer alone; the 4005 pairwise quotient relations and complete affine-support constraints are not yet folded into these messages")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
