#!/usr/bin/env python3
"""Freeze the exact tail4-expanded physical-only C916 junction authority."""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_junction_compiler_exact as C
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_treewidth8_exact as T

EXPECTED_COUNT = 75309497737888679701161264
EXPECTED_COMPONENTS = (67292570321074232, 63, 61, 77, 62, 61)
EXPECTED_TREEWIDTH = 8
EXPECTED_TERNARY = 60
EXPECTED_QUADS = 5
EXPECTED_CLIQUES = 23
EXPECTED_FOREST_EDGES = 17
EXPECTED_LARGEST_CAPACITY = 262144
EXPECTED_TOTAL_CAPACITY = 350736
EXPECTED_LARGEST_ALLOWED = 191392
EXPECTED_TOTAL_ALLOWED = 253953
EXPECTED_MAX_SEPARATOR = 3206
EXPECTED_NEW_VARIABLES = (10,)
EXPECTED_LIFT_FACTOR = 4
EXPECTED_LIFTED_TAIL3 = 97344772584057061635914496
EXPECTED_REMOVED = 22035274846168381934753232
EXPECTED_GAIN_BITS = 0.3702716848772525


def analyze():
    topo = T.analyze()
    assert int(topo["exact_treewidth"]) == EXPECTED_TREEWIDTH
    assert int(topo["width7_exhaustive_states_visited"]) == 655360
    assert tuple(tuple(map(int, x)) for x in topo["deterministic_fill_edges"]) == ((4, 7), (165, 182))

    out = C.analyze()
    assert out["decision"] == "C916_TAIL4_EXPANDED_PHYSICAL_FACTORS_EXACT_JUNCTION_COUNT"
    assert int(out["frozen_ternary_factors"]) == 38
    assert int(out["tail3_promoted_ternary_factors"]) == 10
    assert int(out["tail4_promoted_ternary_factors"]) == 12
    assert int(out["expanded_ternary_factors"]) == EXPECTED_TERNARY
    assert int(out["physical_quaternary_factors"]) == EXPECTED_QUADS
    assert int(out["deterministic_min_fill_upper_bound"]) == EXPECTED_TREEWIDTH
    assert tuple(map(int, out["newly_introduced_variables_vs_tail3"])) == EXPECTED_NEW_VARIABLES
    assert int(out["tail3_lift_factor_into_tail4_variable_universe"]) == EXPECTED_LIFT_FACTOR
    assert int(out["tail3_lifted_assignment_count_in_tail4_variable_universe"]) == EXPECTED_LIFTED_TAIL3
    assert int(out["maximal_cliques"]) == EXPECTED_CLIQUES
    assert int(out["junction_forest_edges"]) == EXPECTED_FOREST_EDGES
    assert int(out["largest_clique_capacity"]) == EXPECTED_LARGEST_CAPACITY
    assert int(out["total_clique_capacity"]) == EXPECTED_TOTAL_CAPACITY
    assert int(out["largest_compiled_allowed_table"]) == EXPECTED_LARGEST_ALLOWED
    assert int(out["total_compiled_allowed_rows"]) == EXPECTED_TOTAL_ALLOWED
    assert tuple(map(int, out["component_physical_assignment_counts"])) == EXPECTED_COMPONENTS
    assert int(out["exact_tail4_expanded_physical_layer_assignment_count"]) == EXPECTED_COUNT
    assert int(out["removed_assignments_vs_lifted_tail3_inventory"]) == EXPECTED_REMOVED
    assert int(out["max_positive_separator_message_rows"]) == EXPECTED_MAX_SEPARATOR
    assert abs(float(out["gain_vs_lifted_tail3_inventory_log2_bits"]) - EXPECTED_GAIN_BITS) < 1e-12

    exact_log2 = math.log2(EXPECTED_COUNT)
    assert abs(float(out["exact_tail4_expanded_physical_layer_assignment_log2"]) - exact_log2) < 1e-12

    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL4_EXPANDED_PHYSICAL_JUNCTION_FROZEN_EXACT")
    print(f"exact_count={EXPECTED_COUNT}")
    print(f"exact_log2={exact_log2}")
    print("boundary=physical higher-order quotient layer only; pairwise, affine, multiplicity weights, and end-to-end work remain outside")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
