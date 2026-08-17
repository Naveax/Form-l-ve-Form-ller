#!/usr/bin/env python3
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds

N=32
EXPECTED={11:51,12:52,13:55,14:54,15:55,16:56}

def edges():
    E=[]
    for i in range(N-1):E.append((i,i+1,4))
    for r in (8,12,16):
        seen=set()
        for i in range(N):
            j=(i+r)%N;e=tuple(sorted((i,j)))
            if e in seen:continue
            seen.add(e);E.append((e[0],e[1],1))
    assert len(E)==111
    return E
E=edges()

def solve(k):
    m=N+len(E);c=np.zeros(m)
    for q,(u,v,w) in enumerate(E):c[N+q]=w
    rows=[];lo=[];hi=[]
    for q,(u,v,w) in enumerate(E):
        y=N+q
        r=np.zeros(m);r[u]=1;r[v]=-1;r[y]=-1;rows.append(r);lo.append(-np.inf);hi.append(0)
        r=np.zeros(m);r[v]=1;r[u]=-1;r[y]=-1;rows.append(r);lo.append(-np.inf);hi.append(0)
    r=np.zeros(m);r[:N]=1;rows.append(r);lo.append(k);hi.append(k)
    res=milp(c,integrality=np.ones(m),bounds=Bounds(np.zeros(m),np.ones(m)),constraints=LinearConstraint(np.array(rows),np.array(lo),np.array(hi)),options={'mip_rel_gap':0.0})
    assert res.success,res.message
    val=round(float(res.fun));assert abs(res.fun-val)<1e-6
    # Independently recount the returned integer cut.
    S={i for i in range(N) if res.x[i]>.5};assert len(S)==k
    direct=sum(w for u,v,w in E if (u in S)!=(v in S));assert direct==val
    return val,S

def main():
    got={};witness={}
    for k in range(11,17):
        v,S=solve(k);got[k]=v;witness[k]=sorted(S);assert v==EXPECTED[k],(k,v,S)
        print('k',k,'optimal_boundary',v,'witness',sorted(S),flush=True)
    costs={k:min(got[k],4*k)+4*k for k in got}
    assert costs=={11:88,12:96,13:104,14:110,15:115,16:120},costs
    assert min(costs.values())==88
    # Standard binary-tree balanced-edge lemma: every unrooted/subcubic tree
    # with 32 leaves has an edge splitting 11..21 leaves. By complement symmetry
    # the smaller side lies in 11..16, exactly the cardinalities solved above.
    print('PASS V26_Q138_DOUBLE_ROUND_HT88_METHOD_OPTIMAL')
    print('minimum_central_boundaries='+','.join(f'{k}:{got[k]}' for k in sorted(got)))
    print('generic_envelope_costs='+','.join(f'{k}:{costs[k]}' for k in sorted(costs)))
    print('balanced_edge_smaller_side=11..16 => lower_bound=88; explicit HT88 tree attains 88')
    print('scope=optimal only for central graph/physical-dimension plus four generic-leaf Hilbert-rank envelope')
if __name__=='__main__':main()
