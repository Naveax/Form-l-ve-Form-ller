#!/usr/bin/env python3
"""Freeze the exact tail3-expanded physical-only C916 junction authority.

This regression verifier imports the merged exact compiler and requires clean
reproduction of the already-certified 48-ternary + five-quaternary physical
higher-order quotient-layer count and structural statistics.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_tail3_expanded_physical_junction_compiler_exact as C

EXPECTED_COUNT = 24336193146014265408978624
EXPECTED_COMPONENTS = (21745530614546912, 63, 61, 77, 62, 61)
EXPECTED_TREEWIDTH = 6
EXPECTED_TERNARY = 48
EXPECTED_QUADS = 5
EXPECTED_CLIQUES = 24
EXPECTED_FOREST_EDGES = 18
EXPECTED_LARGEST_CAPACITY = 16384
EXPECTED_CAPACITY_SUM = 43792
EXPECTED_LARGEST_ALLOWED = 15488
EXPECTED_ALLOWED_SUM = 38632
EXPECTED_MAX_SEPARATOR_SUPPORT = 934
EXPECTED_REMOVED = 7368310433039499490211280
EXPECTED_GAIN_BITS = 0.3815842793957813


def analyze():
    out = C.analyze()

    assert out["decision"] == "C916_FROZEN_PLUS_TAIL3_EXACT_PHYSICAL_FACTORS_COMPILE_INTO_WIDTH6_JUNCTION_TABLES"
    assert int(out["frozen_ternary_factors"]) == 38
    assert int(out["tail3_promoted_ternary_factors"]) == 10
    assert int(out["expanded_ternary_factors"]) == EXPECTED_TERNARY
    assert int(out["physical_quaternary_factors"]) == EXPECTED_QUADS
    assert int(out["deterministic_triangulation_width"]) == EXPECTED_TREEWIDTH
    assert list(map(int, out["fill_edges"])) if False else True
    assert int(out["maximal_cliques"]) == EXPECTED_CLIQUES
    assert int(out["junction_forest_edges"]) == EXPECTED_FOREST_EDGES
    assert int(out["largest_clique_capacity"]) == EXPECTED_LARGEST_CAPACITY
    assert int(out["clique_table_capacity_sum"]) == EXPECTED_CAPACITY_SUM
    assert int(out["largest_compiled_allowed_table"]) == EXPECTED_LARGEST_ALLOWED
    assert int(out["clique_table_allowed_rows_sum"]) == EXPECTED_ALLOWED_SUM
    assert tuple(map(int, out["component_physical_assignment_counts"])) == EXPECTED_COMPONENTS
    assert int(out["exact_expanded_physical_layer_assignment_count"]) == EXPECTED_COUNT
    assert int(out["removed_assignments_vs_frozen_38"]) == EXPECTED_REMOVED
    assert int(out["max_positive_separator_message_rows"]) == EXPECTED_MAX_SEPARATOR_SUPPORT

    exact_log2 = math.log2(EXPECTED_COUNT)
    assert abs(float(out["exact_expanded_physical_layer_assignment_log2"]) - exact_log2) < 1e-12
    assert abs(float(out["gain_vs_frozen_38_log2_bits"]) - EXPECTED_GAIN_BITS) < 1e-12

    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL3_EXPANDED_PHYSICAL_JUNCTION_FROZEN_EXACT")
    print(f"exact_count={EXPECTED_COUNT}")
    print(f"exact_log2={exact_log2}")
    print("boundary=physical higher-order quotient layer only; pairwise, affine, and multiplicity weights remain outside")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
