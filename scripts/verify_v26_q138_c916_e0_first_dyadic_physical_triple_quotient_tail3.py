#!/usr/bin/env python3
"""Test each third-tail physical value image for exact quotient-level ternary holes.

The merged tail3 scout evaluates raw physical value-image obstructions target by target;
some targets have raw holes and some may already equal their raw pairwise closure.  This
verifier applies exactly the sign-reflection quotient construction used by the frozen
current physical factor pipeline.  A target is promotable to that quotient factor
inventory only when an entire quotient tuple is absent from the exact image while all
three quotient pair projections allow it, with the same raw-lift admission invariant used
by the 38-factor generator.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image_tail3 as S
import verify_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_authority as Q
import verify_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_batch4 as G

TARGET = int(os.environ.get("C916_PHYSICAL_QUOTIENT_TAIL3_TARGET", "0"))


def analyze():
    m4 = json.loads(T.M4_PATH.read_text())
    gids = tuple(map(int, m4["m4_group_ids"]))
    assert len(gids) == len(set(gids)) == 90

    ordered = T.build_ordered_groups()
    shortlist, _anchors = S.candidate_triples_tail3(gids, ordered)
    assert len(shortlist) == S.TAIL_LIMIT == 16
    assert 0 <= TARGET < len(shortlist)
    _redundancy, _pair_redundancy, _anchor_rank, triple = shortlist[TARGET]
    triple = tuple(map(int, triple))

    groups = Q.build_groups(triple)
    dist, stats = T.exact_joint_distribution(groups)
    image = set(dist)
    assert sum(int(v) for v in dist.values()) == (1 << T.PHYS_N)

    values = tuple(tuple(sorted({int(row[i]) for row in image})) for i in range(3))
    assert all(len(v) in (7, 9) for v in values), (triple, tuple(map(len, values)))
    raw_closure = Q.pairwise_closure(image, values)
    raw_holes = tuple(sorted(raw_closure - image))

    maps, expected_qvalues = G.generalized_quotient_map(values)
    qimage = {Q.qtuple(row, maps) for row in image}
    qvalues = tuple(tuple(sorted({row[i] for row in qimage})) for i in range(3))
    assert qvalues == expected_qvalues
    qclosure = Q.pairwise_closure(qimage, qvalues)
    qholes = tuple(sorted(qclosure - qimage))

    qhole_rows = []
    for qrow in qholes:
        raw_candidates = tuple(sorted(row for row in raw_closure if Q.qtuple(row, maps) == qrow))
        # Match the exact admission invariant of the 38-factor generator from PR #284.
        # This prevents a quotient-projection artifact from being silently admitted as
        # a new current physical factor.
        assert raw_candidates, ("quotient hole has no raw pairwise-closure lift", triple, qrow)
        assert all(row not in image for row in raw_candidates)
        qhole_rows.append({
            "quotient_tuple": list(qrow),
            "raw_pairwise_closure_tuples_eliminated": len(raw_candidates),
            "raw_tuples": [list(row) for row in raw_candidates],
        })

    if qholes:
        decision = "EXACT_TAIL3_PHYSICAL_TERNARY_OBSTRUCTION_DESCENDS_TO_SIGN_REFLECTION_QUOTIENT"
    elif raw_holes:
        decision = "EXACT_TAIL3_PHYSICAL_TERNARY_OBSTRUCTION_IS_SIGN_ONLY_AT_SIGN_REFLECTION_QUOTIENT"
    else:
        decision = "NO_TAIL3_TERNARY_OBSTRUCTION_BEYOND_PAIRWISE_AT_RAW_OR_QUOTIENT_LEVEL"

    out = {
        "position": "C",
        "physical_shared_dimension": T.PHYS_N,
        "tail3_target": TARGET,
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
        "quotient_hole_details": qhole_rows,
        "support_classes": stats["support_classes"],
        "cells_visited": stats["cells_visited"],
        "leaf_cells": stats["leaf_cells"],
        "walsh_evals": stats["walsh_evals"],
        "promotable_to_current_quotient_factor_inventory": bool(qholes),
        "decision": decision,
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    if qholes:
        print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_QUOTIENT_TAIL3_OBSTRUCTION")
        print("theorem=the emitted third-tail exact physical relation contains complete sign-reflection-orbit holes and is admissible as an exact forbidden ternary relation on the existing quotient states")
    elif raw_holes:
        print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_QUOTIENT_TAIL3_SIGN_ONLY")
        print("theorem=the emitted third-tail exact physical value obstruction has no complete sign-reflection quotient hole and is not admissible as a new factor on the current quotient state space")
    else:
        print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_QUOTIENT_TAIL3_NONE")
        print("theorem=the emitted third-tail exact physical value image equals its raw pairwise closure and contributes no new ternary obstruction at the current quotient level")
    print("boundary=this decides quotient descent only for the emitted tail3 target; it does not modify the frozen 38-factor weighted authority")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
