#!/usr/bin/env python3
"""Exact quotient-descent test for one sixth-tail physical ternary target."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image_tail6 as S
import verify_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_authority as Q
import verify_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_batch4 as G

TARGET = int(os.environ.get("C916_PHYSICAL_QUOTIENT_TAIL6_TARGET", "0"))


def analyze():
    m4 = json.loads(T.M4_PATH.read_text())
    gids = tuple(map(int, m4["m4_group_ids"]))
    ordered = T.build_ordered_groups()
    shortlist, _anchors = S.candidate_triples_tail6(gids, ordered)
    assert len(shortlist) == S.TAIL_LIMIT == 16
    assert 0 <= TARGET < len(shortlist)
    _r, _pr, _ar, triple = shortlist[TARGET]
    triple = tuple(map(int, triple))

    groups = Q.build_groups(triple)
    dist, stats = T.exact_joint_distribution(groups)
    image = set(dist)
    assert sum(int(v) for v in dist.values()) == (1 << T.PHYS_N)

    values = tuple(tuple(sorted({int(row[i]) for row in image})) for i in range(3))
    assert all(len(v) in (7, 9) for v in values)
    raw_closure = Q.pairwise_closure(image, values)
    raw_holes = tuple(sorted(raw_closure - image))

    maps, expected_qvalues = G.generalized_quotient_map(values)
    qimage = {Q.qtuple(row, maps) for row in image}
    qvalues = tuple(tuple(sorted({row[i] for row in qimage})) for i in range(3))
    assert qvalues == expected_qvalues
    qclosure = Q.pairwise_closure(qimage, qvalues)
    qholes = tuple(sorted(qclosure - qimage))

    details = []
    for qrow in qholes:
        lifts = tuple(sorted(row for row in raw_closure if Q.qtuple(row, maps) == qrow))
        assert lifts
        assert all(row not in image for row in lifts)
        details.append({
            "quotient_tuple": list(qrow),
            "raw_pairwise_closure_tuples_eliminated": len(lifts),
            "raw_tuples": [list(row) for row in lifts],
        })

    out = {
        "position": "C",
        "physical_shared_dimension": T.PHYS_N,
        "tail6_target": TARGET,
        "triple": list(triple),
        "raw_alphabet_sizes": [len(v) for v in values],
        "raw_exact_image_size": len(image),
        "raw_pairwise_closure_size": len(raw_closure),
        "raw_holes": len(raw_holes),
        "raw_hole_digest_sha256": T.digest_rows([list(row) for row in raw_holes]),
        "quotient_alphabet_sizes": [len(v) for v in qvalues],
        "quotient_exact_image_size": len(qimage),
        "quotient_pairwise_closure_size": len(qclosure),
        "quotient_holes": len(qholes),
        "quotient_hole_tuples": [list(row) for row in qholes],
        "quotient_hole_digest_sha256": Q.digest_rows(qholes),
        "quotient_hole_details": details,
        "support_classes": stats["support_classes"],
        "cells_visited": stats["cells_visited"],
        "leaf_cells": stats["leaf_cells"],
        "walsh_evals": stats["walsh_evals"],
        "promotable_to_current_quotient_factor_inventory": bool(qholes),
        "decision": (
            "EXACT_TAIL6_PHYSICAL_TERNARY_OBSTRUCTION_DESCENDS_TO_SIGN_REFLECTION_QUOTIENT"
            if qholes else (
                "EXACT_TAIL6_PHYSICAL_TERNARY_OBSTRUCTION_IS_SIGN_ONLY_AT_SIGN_REFLECTION_QUOTIENT"
                if raw_holes else "EXACT_TAIL6_PHYSICAL_TERNARY_PAIRWISE_COMPLETE_NEGATIVE_CONTROL"
            )
        ),
    }
    output_path = os.environ.get("C916_PHYSICAL_QUOTIENT_TAIL6_OUTPUT")
    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_QUOTIENT_TAIL6_EXACT")
    print("boundary=this target-level theorem does not alter the frozen weighted authority")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
