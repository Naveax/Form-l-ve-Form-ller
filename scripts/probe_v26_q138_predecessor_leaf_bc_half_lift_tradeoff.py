#!/usr/bin/env python3
import itertools,sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as B

SECTORS=[((1,0),(2,0)),((1,0),(4,0)),((2,0),(3,0)),((3,0),(4,0))]


def parity(q):return sum(q)&1

def fbit(q):return 1 if sum(q) in (0,3,4) else 0

def walsh_support(vals):
    out=[]
    for mask in range(16):
        s=0
        for idx,q in enumerate(itertools.product((0,1),repeat=4)):
            ch=-1 if (sum(q[i] for i in range(4) if (mask>>i)&1)&1) else 1
            s += vals[idx]*ch
        if s:out.append(mask)
    return out


def subset_cross_ranks(pos):
    qrows=[B.sign_cross_rows(pos,D.carries(z)) for z in SECTORS]
    supports=[A.canonical_support(pos,D.carries(z),expect_internal=128) for z in SECTORS]
    assert all(s==supports[0] for s in supports)
    sd=A.cut_intersection(supports[0]);assert sd==2
    ranks={}
    for mask in range(16):
        rows=[0]*len(A.S1)
        for i in range(4):
            if (mask>>i)&1:rows=[a^b for a,b in zip(rows,qrows[i])]
        ranks[mask]=T.gf2_rank(rows,len(A.R1))
    return sd,ranks


def rank_bound(supp,sd,ranks):
    return min(2048,(1<<sd)*sum(1<<ranks[m] for m in supp))


def main():
    qs=list(itertools.product((0,1),repeat=4))
    for pos in 'BC':
        sd,ranks=subset_cross_ranks(pos)
        pairs={};best_by_first={}
        frontier=[]
        for htab in range(1<<16):
            kval=[];gval=[]
            for idx,q in enumerate(qs):
                h=(htab>>idx)&1
                kval.append(parity(q)+2*h)
                gval.append(fbit(q)^h)
            ks=walsh_support(kval);gs=walsh_support(gval)
            r0=rank_bound(ks,sd,ranks);r1=rank_bound(gs,sd,ranks)
            key=(r0,r1)
            if key not in pairs:pairs[key]=(htab,tuple(ks),tuple(gs))
        # Pareto-minimal pairs.
        for (r0,r1),data in sorted(pairs.items()):
            if any(a<=r0 and b<=r1 and (a<r0 or b<r1) for a,b in pairs):continue
            frontier.append((r0,r1,data[0],data[1],data[2]))
        print('position',pos,'subset_cross_ranks',ranks,'pareto_count',len(frontier),flush=True)
        for rec in frontier:
            print('pareto',pos,'first_rank_bound',rec[0],'second_rank_bound',rec[1],
                  'h_truth_hex',hex(rec[2]),'first_walsh_support',rec[3],
                  'second_walsh_support',rec[4],flush=True)
        for cap in (20,40,80,160,320,640,1280,2048):
            feasible=[(r1,r0,h) for (r0,r1),(h,ks,gs) in pairs.items() if r0<=cap]
            if feasible:
                r1,r0,h=min(feasible)
                print('cap',pos,'first_cap',cap,'best_second',r1,'actual_first',r0,'h',hex(h),flush=True)
    print('PASS PROBE V26_Q138_BC_HALF_LIFT_TRADEOFF')
    print('scope=exact local 16-state lift-choice Pareto bounds via common-support rectangles and subset cross-rank envelopes')

if __name__=='__main__':main()
