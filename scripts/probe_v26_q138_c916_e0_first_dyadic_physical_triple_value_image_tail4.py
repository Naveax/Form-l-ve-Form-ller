#!/usr/bin/env python3
"""Exact scout for the fourth 16-target tail of physical ternary value images.

The merged deterministic inventory covers the original 32-target shortlist and three
successive 16-target high-redundancy tails.  This module reconstructs the same ranking
from current exact support constraints, checks that the preceding third-tail slice still
matches the merged selector, and evaluates the next 16 previously untested triples with
the existing exact 149-bit physical joint-image engine.
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image_extended as X
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image_tail3 as S

TAIL_LIMIT = 16
PREVIOUS_TAILS = 48


def candidate_triples_tail4(gids, ordered):
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
    assert len(unseen) >= PREVIOUS_TAILS + TAIL_LIMIT

    # The immediately preceding slice is independently reconstructed by the merged
    # tail3 selector.  Requiring equality here makes ranking drift a hard failure before
    # the fourth tail can certify anything new.
    tail3, _tail3_anchors = S.candidate_triples_tail3(gids, ordered)
    assert tuple(tuple(rec[3]) for rec in unseen[32:48]) == tuple(
        tuple(rec[3]) for rec in tail3
    )

    tail4 = unseen[48:64]
    assert len(tail4) == TAIL_LIMIT
    known = tested | {tuple(rec[3]) for rec in unseen[:48]}
    assert len(known) == 80
    assert not ({tuple(rec[3]) for rec in tail4} & known)
    return tail4, anchors


T.candidate_triples = candidate_triples_tail4

if __name__ == "__main__":
    T.analyze()
