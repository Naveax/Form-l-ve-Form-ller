#!/usr/bin/env python3
import itertools,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_predecessor_leaf_bc_half_lift_tradeoff as P

qs=list(itertools.product((0,1),repeat=4))
for pos in 'BC':
    sd,ranks=P.subset_cross_ranks(pos)
    pairs={}
    for htab in range(1<<16):
        kval=[];gval=[]
        for idx,q in enumerate(qs):
            h=(htab>>idx)&1
            kval.append(P.parity(q)+2*h)
            gval.append(P.fbit(q)^h)
        r0=P.rank_bound(P.walsh_support(kval),sd,ranks)
        r1=P.rank_bound(P.walsh_support(gval),sd,ranks)
        pairs[(r0,r1)]=True
    frontier=[]
    for r0,r1 in pairs:
        if not any(a<=r0 and b<=r1 and (a<r0 or b<r1) for a,b in pairs):
            frontier.append((r0,r1))
    frontier=sorted(frontier)
    assert frontier==[(20,2048),(2048,0)],(pos,frontier)
    print('position',pos,'pareto_frontier',frontier)
print('PASS V26_Q138_BC_HALF_LIFT_PARETO_NO_GAIN')
print('scope=local four-sign Walsh/cross-rank certificate only')
