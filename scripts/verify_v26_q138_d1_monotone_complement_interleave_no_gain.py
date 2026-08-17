#!/usr/bin/env python3
import itertools
import math
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

WORDS='ABCD'
S1={0,1,2,3,4,5,12,13,14,15,16}
COMP=set(range(32))-S1
LOW=({('A',i) for i in range(6)} |
     {('B',i) for i in range(6)} |
     {('D',i) for i in range(6)} |
     {('C',i) for i in range(12,17)})
HIGH=({('A',i) for i in range(12,17)} |
      {('B',i) for i in range(12,17)} |
      {('D',i) for i in range(12,17)} |
      {('C',i) for i in range(6)})
assert len(LOW)==23 and len(HIGH)==21 and LOW.isdisjoint(HIGH)


def phi(k):
    return min(k,32-k)


def generic_leaf_min_at_44():
    best=10**9; witnesses=[]
    for aA in range(22):
        for aB in range(22):
            for aC in range(22):
                aD=44-aA-aB-aC
                if not (0<=aD<=21):
                    continue
                z=phi(5+aA)+phi(5+aB)+phi(6+aC)+phi(5+aD)
                if z<best:
                    best=z;witnesses=[(aA,aB,aC,aD)]
                elif z==best:
                    witnesses.append((aA,aB,aC,aD))
    return best,witnesses


def central_edges():
    E=[]
    for i in range(31):
        E.append((('s',i),('s',i+1),4))
    for r in (8,12,16):
        seen=set()
        for i in range(32):
            j=(i+r)%32;e=tuple(sorted((i,j)))
            if e in seen:
                continue
            seen.add(e);E.append((('s',e[0]),('s',e[1]),1))
    assert len(E)==111
    return E


def topology_leaf_milp():
    # Binary base variables: 32 central sites, four leaf hubs and the84
    # non-S1 physical terminals. HIGH/LOW physical terminals are constants1/0.
    nodes=[('s',i) for i in range(32)]
    nodes += [('l',w) for w in WORDS]
    nodes += [('p',w,i) for w in WORDS for i in sorted(COMP)]
    vid={v:i for i,v in enumerate(nodes)}
    nbase=len(nodes)
    assert nbase==120

    edges=list(central_edges())
    for w in WORDS:
        for i in range(32):
            p=('p',w,i)
            if (w,i) in HIGH:
                p=1
            elif (w,i) in LOW:
                p=0
            else:
                assert i in COMP
            edges.append((p,('s',i),1))
            edges.append((p,('l',w),1))
    assert len(edges)==367

    m=len(edges);nv=nbase+m
    obj=np.zeros(nv)
    for ei,(_,_,cap) in enumerate(edges):
        obj[nbase+ei]=cap

    rows=[];lo=[];hi=[]
    def abs_ineq(u,v,di,sign):
        # sign*(x_u-x_v)-d <=0, with fixed terminals represented by0/1.
        row=np.zeros(nv);const=0
        for node,coef in ((u,sign),(v,-sign)):
            if isinstance(node,int):
                const += coef*node
            else:
                row[vid[node]] += coef
        row[nbase+di] = -1
        rows.append(row);lo.append(-np.inf);hi.append(-const)

    for ei,(u,v,_) in enumerate(edges):
        abs_ineq(u,v,ei,1)
        abs_ineq(u,v,ei,-1)

    card=np.zeros(nv)
    for w in WORDS:
        for i in COMP:
            card[vid[('p',w,i)]]=1
    rows.append(card);lo.append(44);hi.append(44)

    integrality=np.zeros(nv,dtype=int);integrality[:nbase]=1
    ans=milp(obj,
             integrality=integrality,
             bounds=Bounds(np.zeros(nv),np.ones(nv)),
             constraints=LinearConstraint(np.vstack(rows),np.array(lo),np.array(hi)),
             options={'time_limit':120})
    assert ans.success,ans.message
    assert abs(ans.fun-86.0)<1e-9,ans.fun
    assert abs(ans.mip_dual_bound-86.0)<1e-9,ans.mip_dual_bound
    assert ans.mip_gap==0.0,ans.mip_gap
    return ans


def explicit_topology_witness_cost():
    # 44 additions: all B/C complement bits plus A11 and D11.
    E={('B',i) for i in COMP}|{('C',i) for i in COMP}|{('A',11),('D',11)}
    assert len(E)==44
    P=HIGH|E
    counts={w:sum((w,i) in P for i in range(32)) for w in WORDS}
    assert counts=={'A':6,'B':26,'C':27,'D':6}
    # Put all central sites on selected side: no internal cut, and exactly the
    # 63 unselected physical terminals cross central terminal legs.
    central=128-len(P)
    assert central==63
    # Put A,D leaf hubs on unselected side; B,C hubs on selected side.
    leaf=counts['A']+(32-counts['B'])+(32-counts['C'])+counts['D']
    assert leaf==23
    return central+leaf


def main():
    leaf_min,wit=generic_leaf_min_at_44()
    assert leaf_min==23
    assert (0,2,21,21) in wit

    high_center=490112
    assert high_center==3829*(2**7)
    coeff_center_exp=math.log2(high_center)+44
    coeff_total=coeff_center_exp+leaf_min
    target=73+math.log2(3829)
    assert abs(coeff_total-(target+1))<1e-12

    assert explicit_topology_witness_cost()==86
    ans=topology_leaf_milp()

    print('PASS V26_Q138_D1_MONOTONE_COMPLEMENT_INTERLEAVE_NO_GAIN')
    print('unavoidable_added_complement_layer=44')
    print('generic_leaf_Hilbert_min_at_layer44=23 witness_count=%d' % len(wit))
    print('coefficient_raw_extension_certificate=%.15f' % coeff_total)
    print('topology_plus_generic_leaf_MILP_optimum=%.0f dual=%.0f gap=%.1f nodes=%d' %
          (ans.fun,ans.mip_dual_bound,ans.mip_gap,ans.mip_node_count))
    print('current_rank3829_factor_exponent=%.15f' % target)
    print('method_barrier_gap_bits=1.000000000000000')
    print('consequence=generic-leaf monotone complement interleaving cannot certify an improvement')
    print('next=coefficient-specific leaf/central joint algebra or a different non-monotone identity')
    print('scope=exact finite method-scope NO-GAIN; not a true-rank or unrestricted-work lower bound')


if __name__=='__main__':
    main()
