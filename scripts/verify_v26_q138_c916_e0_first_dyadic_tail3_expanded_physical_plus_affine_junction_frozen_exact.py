#!/usr/bin/env python3
"""Freeze the exact tail3-expanded physical+affine C916 junction authority."""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_tail3_expanded_physical_plus_affine_junction_exact as C

EXPECTED_COUNT = 610168911320611717122698496
EXPECTED_COMPONENTS = (33258087916833958528, 63, 61, 77, 62)
EXPECTED_LOWER = 9
EXPECTED_UPPER = 11
EXPECTED_CLIQUES = 25
EXPECTED_FOREST_EDGES = 20
EXPECTED_LARGEST_CAPACITY = 16777216
EXPECTED_TOTAL_CAPACITY = 30825488
EXPECTED_LARGEST_ALLOWED = 16777216
EXPECTED_TOTAL_ALLOWED = 27829295
EXPECTED_MAX_SEPARATOR = 842752
EXPECTED_REMOVED = 71765543089179283645312704
EXPECTED_GAIN_BITS = 0.16042440306917172
EXPECTED_FILL_EDGES = (
    (4, 7), (12, 113), (4, 104), (3, 6), (3, 10), (4, 112),
    (24, 113), (112, 165), (8, 11), (8, 24), (11, 113), (4, 182),
    (5, 24), (165, 182), (113, 181), (113, 182), (5, 11), (8, 182),
)


def analyze():
    out = C.analyze()
    assert out["decision"] == "C916_TAIL3_EXPANDED_PHYSICAL_PLUS_COMPLETE_AFFINE_EXACT_JUNCTION_TABLES_WITH_TREEWIDTH_BOUNDS"
    assert out["affine_constraint_semantics"] == "all-nonzero forbidden; maximal local quotient-state index is zero"
    assert int(out["frozen_ternary_factors"]) == 38
    assert int(out["tail3_promoted_ternary_factors"]) == 10
    assert int(out["expanded_ternary_factors"]) == 48
    assert int(out["physical_quaternary_factors"]) == 5
    assert int(out["affine_constraints"]) == 19

    assert int(out["treewidth_lower_bound_from_maximum_clique"]) == EXPECTED_LOWER
    assert int(out["deterministic_min_fill_upper_bound"]) == EXPECTED_UPPER
    assert int(out["selected_elimination_upper_bound"]) == EXPECTED_UPPER
    assert out["selected_elimination_source"] == "deterministic_min_fill"
    assert out["exact_treewidth_if_bounds_match"] is None
    assert tuple(tuple(map(int, row)) for row in out["fill_edges"]) == EXPECTED_FILL_EDGES

    assert int(out["maximal_cliques"]) == EXPECTED_CLIQUES
    assert int(out["junction_forest_edges"]) == EXPECTED_FOREST_EDGES
    assert int(out["largest_clique_capacity"]) == EXPECTED_LARGEST_CAPACITY
    assert int(out["total_clique_capacity"]) == EXPECTED_TOTAL_CAPACITY
    assert int(out["largest_compiled_allowed_table"]) == EXPECTED_LARGEST_ALLOWED
    assert int(out["total_compiled_allowed_rows"]) == EXPECTED_TOTAL_ALLOWED
    assert tuple(map(int, out["component_assignment_counts"])) == EXPECTED_COMPONENTS
    assert int(out["exact_expanded_physical_plus_affine_assignment_count"]) == EXPECTED_COUNT
    assert int(out["removed_assignments_vs_frozen_38"]) == EXPECTED_REMOVED
    assert int(out["max_positive_separator_rows"]) == EXPECTED_MAX_SEPARATOR

    exact_log2 = math.log2(EXPECTED_COUNT)
    assert abs(float(out["exact_expanded_physical_plus_affine_assignment_log2"]) - exact_log2) < 1e-12
    assert abs(float(out["gain_vs_frozen_38_log2_bits"]) - EXPECTED_GAIN_BITS) < 1e-12

    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL3_EXPANDED_PHYSICAL_PLUS_AFFINE_JUNCTION_FROZEN_EXACT")
    print(f"exact_count={EXPECTED_COUNT}")
    print(f"exact_log2={exact_log2}")
    print("boundary=treewidth remains bounded by 9 <= tw <= 11; the junction count itself is exact on the explicit width-11 chordal completion")
    print("boundary=this excludes the dense 4005 pairwise quotient relations and multiplicity weights")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
