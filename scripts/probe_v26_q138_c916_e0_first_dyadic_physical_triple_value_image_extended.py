#!/usr/bin/env python3
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T

SHORTLIST_LIMIT = 32


def candidate_triples_extended(gids, ordered):
    anchors = {}
    codims = {}
    for gid in gids:
        can, _sectors = ordered[int(gid)]
        _prank, _local, anchor = T.D.projection_anchor(can)
        anchors[int(gid)] = anchor
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

    diverse = []
    used = set()
    for rec in ranked:
        triple = rec[3]
        if not (set(triple) & used):
            diverse.append(rec)
            used.update(triple)
            if len(diverse) >= SHORTLIST_LIMIT:
                break
    if len(diverse) < SHORTLIST_LIMIT:
        seen = {rec[3] for rec in diverse}
        for rec in ranked:
            if rec[3] in seen:
                continue
            diverse.append(rec)
            seen.add(rec[3])
            if len(diverse) >= SHORTLIST_LIMIT:
                break
    assert len(diverse) >= 20
    return diverse, anchors


T.candidate_triples = candidate_triples_extended

if __name__ == '__main__':
    T.analyze()
