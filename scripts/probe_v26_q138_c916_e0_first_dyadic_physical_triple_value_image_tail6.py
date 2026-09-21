#!/usr/bin/env python3
"""Exact scout selector for the sixth 16-target physical ternary tail.

The selector reconstructs the same global redundancy ranking used by the merged physical
triple scouts, verifies that unseen positions 64..79 exactly match the active tail5
selector, then admits only positions 80..95. This is preparation only; no factor is
promoted until an exact quotient-descent matrix and aggregate pass.
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image_extended as X
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image_tail5 as S5

TAIL_LIMIT = 16
TAIL6_START = 80
TAIL6_END = 96


def candidate_triples_tail6(gids, ordered):
    tested_records, anchors = X.candidate_triples_extended(gids, ordered)
    tested = {tuple(rec[3]) for rec in tested_records}
    assert len(tested) == 32

    codims = {
        int(gid): len(anchors[int(gid)]["physical_support_constraints"])
        for gid in gids
    }

    ranked = []
    for triple in itertools.combinations(sorted(map(int, gids)), 3):
        constraints = []
        for gid in triple:
            constraints.extend(anchors[gid]["physical_support_constraints"])
        got = T.P.C.P.U.T.rref(constraints, n=T.PHYS_N)
        if got is None:
            continue
        rank = int(got[0])
        redundancy = sum(codims[g] for g in triple) - rank
        pair_redundancy = 0
        for a, b in itertools.combinations(triple, 2):
            pair = T.P.C.P.U.T.rref(
                list(anchors[a]["physical_support_constraints"])
                + list(anchors[b]["physical_support_constraints"]),
                n=T.PHYS_N,
            )
            assert pair is not None
            pair_redundancy += codims[a] + codims[b] - int(pair[0])
        ranked.append((redundancy, pair_redundancy, rank, triple))

    ranked.sort(key=lambda x: (-x[0], -x[1], -x[2], x[3]))
    unseen = [rec for rec in ranked if tuple(rec[3]) not in tested]
    assert len(unseen) >= TAIL6_END

    tail5, _ = S5.candidate_triples_tail5(gids, ordered)
    assert tuple(tuple(rec[3]) for rec in unseen[64:80]) == tuple(
        tuple(rec[3]) for rec in tail5
    )

    tail6 = unseen[TAIL6_START:TAIL6_END]
    assert len(tail6) == TAIL_LIMIT
    already = tested | {tuple(rec[3]) for rec in unseen[:TAIL6_START]}
    assert len(already) == 112
    assert not ({tuple(rec[3]) for rec in tail6} & already)
    return tail6, anchors


T.candidate_triples = candidate_triples_tail6

if __name__ == "__main__":
    T.analyze()
