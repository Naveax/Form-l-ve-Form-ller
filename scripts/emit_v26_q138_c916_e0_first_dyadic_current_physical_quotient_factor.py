#!/usr/bin/env python3
"""Recompute one currently certified physical ternary quotient factor exactly.

The factor inventory is imported from the merged width-5 topology certificate so the
weighted-count pipeline cannot silently drift to a stale seven-factor inventory.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T
import verify_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_authority as Q
import verify_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_batch4 as G
import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as H


TARGET = int(os.environ.get("C916_CURRENT_PHYSICAL_FACTOR_TARGET", "0"))
OUTPUT = Path(os.environ.get("C916_CURRENT_PHYSICAL_FACTOR_OUTPUT", f"factor_{TARGET:02d}.json"))


def digest_rows(rows):
    payload = json.dumps([list(map(int, row)) for row in rows], separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def analyze():
    assert 0 <= TARGET < len(H.TERNARY_FACTORS)
    triple = tuple(map(int, H.TERNARY_FACTORS[TARGET]))
    groups = Q.build_groups(triple)
    dist, stats = T.exact_joint_distribution(groups)
    image = set(dist)
    assert sum(int(v) for v in dist.values()) == (1 << T.PHYS_N)

    values = tuple(tuple(sorted({int(row[i]) for row in image})) for i in range(3))
    assert all(len(v) in (7, 9) for v in values), (triple, tuple(map(len, values)))
    raw_closure = Q.pairwise_closure(image, values)
    raw_holes = tuple(sorted(raw_closure - image))
    assert raw_holes, ("inventory contains a non-obstructed triple", triple)

    maps, expected_qvalues = G.generalized_quotient_map(values)
    qimage = {Q.qtuple(row, maps) for row in image}
    qvalues = tuple(tuple(sorted({row[i] for row in qimage})) for i in range(3))
    assert qvalues == expected_qvalues
    qclosure = Q.pairwise_closure(qimage, qvalues)
    qholes = tuple(sorted(qclosure - qimage))
    assert qholes, ("certified physical obstruction became sign-only", triple)

    # Every quotient hole must eliminate only raw tuples that are genuinely absent.
    eliminated = 0
    for qrow in qholes:
        raw_candidates = tuple(row for row in raw_closure if Q.qtuple(row, maps) == qrow)
        assert raw_candidates
        assert all(row not in image for row in raw_candidates)
        eliminated += len(raw_candidates)

    out = {
        "position": "C",
        "physical_shared_dimension": T.PHYS_N,
        "inventory_index": TARGET,
        "triple": list(triple),
        "raw_alphabet_sizes": [len(v) for v in values],
        "raw_exact_image_size": len(image),
        "raw_pairwise_closure_size": len(raw_closure),
        "raw_holes": len(raw_holes),
        "raw_hole_digest_sha256": T.digest_rows([list(row) for row in raw_holes]),
        "raw_joint_distribution_digest_sha256": T.digest_rows(
            [[list(key), int(dist[key])] for key in sorted(dist)]
        ),
        "quotient_alphabet_sizes": [len(v) for v in qvalues],
        "quotient_exact_image_size": len(qimage),
        "quotient_pairwise_closure_size": len(qclosure),
        "quotient_holes": len(qholes),
        "quotient_hole_tuples": [list(row) for row in qholes],
        "quotient_hole_digest_sha256": digest_rows(qholes),
        "raw_pairwise_closure_tuples_eliminated_by_quotient_holes": eliminated,
        "support_classes": stats["support_classes"],
        "cells_visited": stats["cells_visited"],
        "leaf_cells": stats["leaf_cells"],
        "walsh_evals": stats["walsh_evals"],
        "decision": "EXACT_CURRENT_PHYSICAL_TERNARY_QUOTIENT_FACTOR_RECOMPUTED",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(out, sort_keys=True, indent=2) + "\n")
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_CURRENT_PHYSICAL_QUOTIENT_FACTOR")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
