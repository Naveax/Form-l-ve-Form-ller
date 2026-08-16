#!/usr/bin/env python3
import argparse, json
from collections import Counter, defaultdict
from pathlib import Path

LOCAL_ORDERS={4:("t","s","v","u"),3:("u","t","s","v","w"),2:("t","w","v","s"),1:("w","v","s","t")}

class N:
    def __init__(self):
        self.k=0; self.e={}; self.d={}; self.ops=[]; self.names=[]
    def edge(self,n,d):
        if n in self.e:
            assert self.d[self.e[n]]==d
            return self.e[n]
        x=self.k; self.k+=1; self.e[n]=x; self.d[x]=d; return x
    def add(self,n,I):
        self.names.append(n); self.ops.append(tuple(I))

def sig(j,k): return f"sig{j}_{k}"

def ph(j,i,x):
    if x=="s": return None if i==31 else sig(j,i)
    if x=="t": return None if i==0 else sig(j,i-1)
    if j==4: return {"u":f"u4_{i}","v":f"v4_{i}"}[x]
    if j==3: return {"u":f"u3_{i}","v":f"v3_{i}","w":f"v4_{(i+8)%32}"}[x]
    if j==2: return {"v":f"v4_{(i+8)%32}","w":f"w2_{i}"}[x]
    if j==1: return {"v":f"v3_{(i+12)%32}","w":f"u3_{i}"}[x]
    raise KeyError((j,i,x))

def rs(j,i):
    if j==3:
        return [2,3,2] if i==0 else ([2,2,2] if i==31 else [2,3,3,2])
    return [2,2] if i==0 else ([1,1] if i==31 else [2,3,2])

def build_original():
    B=N()
    for j in (4,3,2,1):
        O=LOCAL_ORDERS[j]
        for i in range(32):
            V=[x for x in O if not(x=="t" and i==0) and not(x=="s" and i==31)]
            R=rs(j,i); left=None
            for k,x in enumerate(V):
                I=[] if left is None else [left]
                p=ph(j,i,x)
                if p is not None: I.append(B.edge(p,2))
                if k<len(V)-1:
                    right=B.edge(f"aux_j{j}_i{i}_k{k}",R[k]); I.append(right); left=right
                else:
                    left=None
                B.add(f"J{j}_i{i}_c{k}_{x}",I)
    for i in range(32):
        B.add(f"P_i{i}",[B.edge(f"u4_{i}",2),B.edge(f"v3_{(i+12)%32}",2),B.edge(f"w2_{i}",2)])
    assert len(B.ops)==568
    return B

def build_modified(C):
    B=build_original()
    inc=defaultdict(list)
    for v,I in enumerate(B.ops):
        for e in I:
            if B.d[e]>1: inc[e].append(v)

    rc=C["rank_compression"]
    removed=set(rc["removed_original_leaf_ids"])
    assert len(removed)==34
    keep=[v for v in range(568) if v not in removed]
    assert len(keep)==534
    old2new={v:i for i,v in enumerate(keep)}
    X=rc["replacement_vertices"]["X"]; Z=rc["replacement_vertices"]["Z"]
    assert (X,Z)==(534,535)
    xnames=set(rc["X_external_edges"]); znames=set(rc["Z_interface_edges"])
    assert len(xnames)==12 and len(znames)==11 and xnames.isdisjoint(znames)

    medges=[]
    seen_special=set()
    for name,e in B.e.items():
        d=B.d[e]
        if d<=1: continue
        V=inc[e]
        outside=[old2new[v] for v in V if v not in removed]
        had_removed=any(v in removed for v in V)
        new=list(outside)
        if name in xnames:
            assert had_removed and outside, (name,V)
            new.append(X); seen_special.add(name)
        elif name in znames:
            assert had_removed and outside, (name,V)
            new.append(Z); seen_special.add(name)
        elif had_removed and outside:
            raise AssertionError(f"unexpected removed/outside crossing edge {name}: {V}")
        if len(set(new))>1:
            medges.append((name,d,tuple(sorted(set(new)))))
    assert seen_special==xnames|znames
    medges.append(("R528",528,(X,Z)))

    dims=Counter(d for _,d,_ in medges)
    Q=C["modified_network"]
    assert Q["leaf_count"]==536 and Q["original_surviving_leaf_count"]==534
    assert len(medges)==Q["nontrivial_indices"]==656, (len(medges),Q)
    assert dims[2]==Q["binary_indices"]==513, dims
    assert dims[3]==Q["ternary_indices"]==142, dims
    assert dims[528]==Q["rank528_indices"]==1, dims
    return medges

def verify_tree(C,medges):
    seen=[]; internal=0; maxd=1; maxn=0; maxdims=None
    universe=set(range(C["modified_network"]["leaf_count"]))
    def boundary(S):
        nonlocal maxd,maxn,maxdims
        d=1; dc=Counter()
        for _,dim,V in medges:
            inside=any(v in S for v in V)
            if inside and any(v not in S for v in V):
                d*=dim; dc[dim]+=1
        if d>maxd:
            maxd=d; maxn=len(S); maxdims=dc.copy()
        return d,dc
    def walk(x,root=False):
        nonlocal internal
        if isinstance(x,int):
            assert x in universe
            seen.append(x); boundary({x}); return {x}
        assert isinstance(x,list) and len(x)==2
        internal+=1
        A=walk(x[0]); B=walk(x[1]); assert A.isdisjoint(B)
        S=A|B
        if not root: boundary(S)
        return S
    root=walk(C["certificate"]["tree"],True)
    assert root==universe
    assert len(seen)==536==len(set(seen))
    assert internal==535==C["certificate"]["internal_nodes"]
    assert maxd==2**40==C["certificate"]["max_boundary_dimension"], (maxd,maxn,maxdims)
    assert maxn==171==C["certificate"]["max_node_leaf_count"], (maxn,maxdims)
    assert maxdims==Counter({2:40}), maxdims
    return maxd,maxn,maxdims

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("cert",nargs="?",default="research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json")
    a=ap.parse_args()
    C=json.loads(Path(a.cert).read_text())
    assert C["milestone"]=="V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE"
    assert C["rank_compression"]["exact_rank"]==528
    assert C["rank_compression"]["replacement_bond_dimension"]==528
    assert C["q138_output"]["t4_mask"]=="0x00000008"
    assert C["q138_output"]["t4_bits_23_28"]==[0,0,0,0,0,0]
    medges=build_modified(C)
    maxd,maxn,maxdims=verify_tree(C,medges)
    print("PASS V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE")
    print(f"leaves=536 internal_nodes=535 indices=656 max_boundary_dimension={maxd}=2^40 max_cluster_leaves={maxn} max_dims={dict(maxdims)}")
    print("DEPENDENCY exact rank-528 replacement must be verified separately by scripts/verify_v26_qr_width41_left_rank528.py")

if __name__=="__main__": main()
