#!/usr/bin/env python3
"""Exact scout for the seventh 16-target tail of physical ternary value images."""
from __future__ import annotations
import itertools,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image_extended as X
import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image_tail6 as S6

TAIL_LIMIT=16
PREVIOUS_UNSEEN=96

def candidate_triples_tail7(gids,ordered):
    tested_records,anchors=X.candidate_triples_extended(gids,ordered)
    tested={tuple(rec[3]) for rec in tested_records}
    assert len(tested)==32
    codims={int(g):len(anchors[int(g)]["physical_support_constraints"]) for g in gids}
    ranked=[]
    for triple in itertools.combinations(sorted(map(int,gids)),3):
        constraints=[]
        for gid in triple: constraints.extend(anchors[gid]["physical_support_constraints"])
        got=T.P.C.P.U.T.rref(constraints,n=T.PHYS_N)
        if got is None: continue
        rank=int(got[0]); redundancy=sum(codims[g] for g in triple)-rank
        pair_redundancy=0
        for a,b in itertools.combinations(triple,2):
            pair=T.P.C.P.U.T.rref(
                list(anchors[a]["physical_support_constraints"])+list(anchors[b]["physical_support_constraints"]),
                n=T.PHYS_N)
            assert pair is not None
            pair_redundancy+=codims[a]+codims[b]-int(pair[0])
        ranked.append((redundancy,pair_redundancy,rank,triple))
    ranked.sort(key=lambda x:(-x[0],-x[1],-x[2],x[3]))
    unseen=[rec for rec in ranked if tuple(rec[3]) not in tested]
    assert len(unseen)>=PREVIOUS_UNSEEN+TAIL_LIMIT
    tail6,_=S6.candidate_triples_tail6(gids,ordered)
    assert tuple(tuple(rec[3]) for rec in unseen[80:96])==tuple(tuple(rec[3]) for rec in tail6)
    tail7=unseen[96:112]
    assert len(tail7)==TAIL_LIMIT
    known=tested|{tuple(rec[3]) for rec in unseen[:96]}
    assert len(known)==128
    assert not({tuple(rec[3]) for rec in tail7}&known)
    return tail7,anchors

T.candidate_triples=candidate_triples_tail7
if __name__=="__main__": T.analyze()
