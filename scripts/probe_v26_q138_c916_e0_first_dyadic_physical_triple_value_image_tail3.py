#!/usr/bin/env python3
"""Exact scout for the third 16-target tail of physical ternary value images.

The previously merged deterministic inventory covers the original 32-target shortlist,
the first 16-target high-redundancy tail, and the second 16-target tail.  This module
reconstructs the same ranking from current exact support constraints and selects the next
16 disjoint triples.  Each selected target is then evaluated by the existing exact
149-bit physical joint-image engine.
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image_extended as X

TAIL_LIMIT = 16
PREVIOUS_TAILS = 32


def candidate_triples_tail3(gids, ordered):
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

    first_tail = unseen[:16]
    second_tail = unseen[16:32]
    tail3 = unseen[32:48]
    assert len(first_tail) == len(second_tail) == len(tail3) == TAIL_LIMIT

    # Frozen merged tail inventories: these assertions make accidental ranking drift a
    # hard failure before any new target is admitted.
    assert tuple(tuple(rec[3]) for rec in first_tail) == (
        (3, 7, 10), (3, 7, 11), (3, 7, 12), (3, 7, 24),
        (3, 7, 62), (3, 7, 67), (3, 7, 104), (3, 7, 111),
        (3, 7, 112), (3, 7, 113), (3, 7, 114), (3, 7, 135),
        (3, 7, 136), (3, 7, 138), (3, 7, 144), (3, 7, 154),
    )
    assert tuple(tuple(rec[3]) for rec in second_tail) == (
        (3, 7, 165), (3, 7, 181), (3, 7, 182), (3, 7, 183),
        (3, 7, 185), (3, 7, 186), (3, 7, 239), (3, 7, 244),
        (3, 7, 245), (3, 7, 249), (3, 181, 182), (4, 5, 165),
        (4, 7, 165), (4, 8, 165), (4, 9, 165), (4, 10, 165),
    )

    known = tested | {tuple(rec[3]) for rec in first_tail + second_tail}
    assert len(known) == 64
    assert not ({tuple(rec[3]) for rec in tail3} & known)
    return tail3, anchors


T.candidate_triples = candidate_triples_tail3

if __name__ == "__main__":
    T.analyze()
