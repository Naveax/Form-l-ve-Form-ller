#!/usr/bin/env python3
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image_extended as X
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image_tail as Y

TAIL2_LIMIT = 16


def candidate_triples_tail2(gids, ordered):
    tested_records, anchors = X.candidate_triples_extended(gids, ordered)
    tested = {tuple(rec[3]) for rec in tested_records}
    assert len(tested) == 32

    first_tail, anchors2 = Y.candidate_triples_tail(gids, ordered)
    assert set(anchors) == set(anchors2)
    first = {tuple(rec[3]) for rec in first_tail}
    assert len(first) == 16 and not (tested & first)
    excluded = tested | first
    assert len(excluded) == 48

    codims = {}
    for gid in gids:
        anchor = anchors[int(gid)]
        codims[int(gid)] = len(anchor['physical_support_constraints'])

    ranked = []
    for triple in itertools.combinations(sorted(map(int, gids)), 3):
        constraints = []
        for gid in triple:
            constraints.extend(anchors[gid]['physical_support_constraints'])
        got = T.P.C.P.U.T.rref(constraints, n=T.PHYS_N)
        if got is None:
            continue
        rank = int(got[0])
        redundancy = sum(codims[g] for g in triple) - rank
        pair_redundancy = 0
        for a, b in itertools.combinations(triple, 2):
            pair = T.P.C.P.U.T.rref(
                list(anchors[a]['physical_support_constraints'])
                + list(anchors[b]['physical_support_constraints']),
                n=T.PHYS_N,
            )
            assert pair is not None
            pair_redundancy += codims[a] + codims[b] - int(pair[0])
        ranked.append((redundancy, pair_redundancy, rank, triple))
    ranked.sort(key=lambda x: (-x[0], -x[1], -x[2], x[3]))

    tail2 = [rec for rec in ranked if tuple(rec[3]) not in excluded][:TAIL2_LIMIT]
    assert len(tail2) == TAIL2_LIMIT
    assert not ({tuple(rec[3]) for rec in tail2} & excluded)
    return tail2, anchors


T.candidate_triples = candidate_triples_tail2

if __name__ == '__main__':
    T.analyze()
