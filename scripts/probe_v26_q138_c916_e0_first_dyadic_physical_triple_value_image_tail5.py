#!/usr/bin/env python3
"""Exact scout for the fifth 16-target tail of physical ternary value images.

The merged inventory covers the original 32-target shortlist and four successive
16-target high-redundancy tails. This module reconstructs the same global ranking,
hard-checks the merged tail4 slice, and selects the next sixteen previously untested
triples without overlap.
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image_extended as X
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image_tail4 as S4

TAIL_LIMIT = 16
PREVIOUS_UNSEEN = 64


def candidate_triples_tail5(gids, ordered):
    tested_records, anchors = X.candidate_triples_extended(gids, ordered)
    tested = {tuple(rec[3]) for rec in tested_records}
    assert len(tested) == 32

    codims = {}
    for gid in gids:
        anchor = anchors[int(gid)]
        codims[int(gid)] = len(anchor["physical_support_constraints"])

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
    assert len(unseen) >= PREVIOUS_UNSEEN + TAIL_LIMIT

    tail4, _tail4_anchors = S4.candidate_triples_tail4(gids, ordered)
    assert tuple(tuple(rec[3]) for rec in unseen[48:64]) == tuple(
        tuple(rec[3]) for rec in tail4
    )

    tail5 = unseen[64:80]
    assert len(tail5) == TAIL_LIMIT
    known = tested | {tuple(rec[3]) for rec in unseen[:64]}
    assert len(known) == 96
    assert not ({tuple(rec[3]) for rec in tail5} & known)
    return tail5, anchors


T.candidate_triples = candidate_triples_tail5

if __name__ == "__main__":
    T.analyze()
