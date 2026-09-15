#!/usr/bin/env python3
"""Freeze the authority-correct C916 physical+affine width-9 junction result.

This is a regression authority layered on the merged exact compiler.  It does not change
relations or topology.  It reruns the exact compiler from clean inputs and requires the
previously observed authority-correct integer, component counts, and table/message
statistics to remain byte-for-byte stable at the semantic level.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_current_physical_plus_affine_junction_compiler_exact as C

EXPECTED_EXACT_ASSIGNMENT_COUNT = 681_934_454_409_791_000_768_011_200
EXPECTED_COMPONENT_COUNTS = (
    37_169_766_629_362_021_600,
    63,
    61,
    77,
    62,
)
EXPECTED_TOTAL_COMPILED_ALLOWED_ROWS = 3_905_754
EXPECTED_MAX_POSITIVE_SEPARATOR_ROWS = 262_144
EXPECTED_LARGEST_COMPILED_ALLOWED_TABLE = 1_048_576
EXPECTED_MAXIMAL_CLIQUES = 26
EXPECTED_JUNCTION_FOREST_EDGES = 21
EXPECTED_FILL_EDGES = 13
EXPECTED_TREEWIDTH = 9


def analyze():
    out = C.analyze()

    assert out["decision"] == "C916_CURRENT_PHYSICAL_PLUS_COMPLETE_AFFINE_ACTIVITY_CORRECT_WIDTH9_JUNCTION_TABLES"
    assert out["affine_constraint_semantics"] == "all-nonzero forbidden; maximal local quotient-state index is zero"
    assert int(out["exact_treewidth"]) == EXPECTED_TREEWIDTH
    assert int(out["maximal_cliques"]) == EXPECTED_MAXIMAL_CLIQUES
    assert int(out["junction_forest_edges"]) == EXPECTED_JUNCTION_FOREST_EDGES
    assert int(out["fill_edges"]) == EXPECTED_FILL_EDGES
    assert int(out["largest_clique_capacity"]) == 1_048_576
    assert int(out["total_clique_capacity"]) == 5_023_824
    assert int(out["largest_compiled_allowed_table"]) == EXPECTED_LARGEST_COMPILED_ALLOWED_TABLE
    assert int(out["total_compiled_allowed_rows"]) == EXPECTED_TOTAL_COMPILED_ALLOWED_ROWS
    assert tuple(map(int, out["component_assignment_counts"])) == EXPECTED_COMPONENT_COUNTS
    assert int(out["exact_physical_plus_affine_assignment_count"]) == EXPECTED_EXACT_ASSIGNMENT_COUNT
    assert int(out["max_positive_separator_rows"]) == EXPECTED_MAX_POSITIVE_SEPARATOR_ROWS

    exact_log2 = math.log2(EXPECTED_EXACT_ASSIGNMENT_COUNT)
    assert abs(float(out["exact_physical_plus_affine_assignment_log2"]) - exact_log2) < 1e-12

    frozen = {
        "position": "C",
        "physical_shared_dimension": 149,
        "exact_treewidth": EXPECTED_TREEWIDTH,
        "maximal_cliques": EXPECTED_MAXIMAL_CLIQUES,
        "junction_forest_edges": EXPECTED_JUNCTION_FOREST_EDGES,
        "fill_edges": EXPECTED_FILL_EDGES,
        "total_compiled_allowed_rows": EXPECTED_TOTAL_COMPILED_ALLOWED_ROWS,
        "max_positive_separator_rows": EXPECTED_MAX_POSITIVE_SEPARATOR_ROWS,
        "component_assignment_counts": list(EXPECTED_COMPONENT_COUNTS),
        "exact_physical_plus_affine_assignment_count": EXPECTED_EXACT_ASSIGNMENT_COUNT,
        "exact_physical_plus_affine_assignment_log2": exact_log2,
        "affine_constraint_semantics": "all-nonzero forbidden; maximal local quotient-state index is zero",
        "decision": "C916_CURRENT_PHYSICAL_PLUS_COMPLETE_AFFINE_WIDTH9_JUNCTION_RESULT_FROZEN_EXACT",
    }
    print("frozen_result", json.dumps(frozen, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_CURRENT_PHYSICAL_PLUS_AFFINE_JUNCTION_FROZEN_EXACT")
    print("theorem=clean recomputation of the authority-correct current physical plus complete affine higher-order layer exactly reproduces the frozen width-9 junction integer and structural statistics")
    print("boundary=this remains a higher-order quotient-layer authority only; the dense 4005 pairwise value relations and multiplicity weights are not included")
    print("ALPHA_PASS=0")
    return frozen


if __name__ == "__main__":
    analyze()
