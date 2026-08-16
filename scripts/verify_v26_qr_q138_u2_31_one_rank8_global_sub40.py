#!/usr/bin/env python3
import argparse,json,math,sys
from collections import Counter,defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_algebraic_width40 as V

def build(base,C):
    E=V.build_modified(base)
    rc=C['replacement']; removed=set(rc['removed_width40_vertex_ids'])
    assert len(removed)==171
    keep=sorted(set(range(base['modified_network']['leaf_count']))-removed)
    assert len(keep)==365
    old2new={v:i for i,v in enumerate(keep)}
    X=rc['replacement_vertices']['X8']; Z=rc['replacement_vertices']['Z8']
    assert (X,Z)==(365,366)
    lx=set(rc['external_left_binary_edges']); rz=set(rc['external_right_binary_edges'])
    assert len(lx)==16 and len(rz)==24 and lx.isdisjoint(rz)
    out=[]; seen=set()
    for name,dim,W in E:
        outside=[old2new[v] for v in W if v not in removed]
        had=any(v in removed for v in W)
        new=list(outside)
        if name in lx:
            assert had and outside and dim==2,(name,dim,W); new.append(X); seen.add(name)
        elif name in rz:
            assert had and outside and dim==2,(name,dim,W); new.append(Z); seen.add(name)
        elif had and outside:
            raise AssertionError(('unexpected removed/outside edge',name,dim,W))
        if len(set(new))>1: out.append((name,dim,tuple(sorted(set(new)))))
    assert seen==lx|rz
    out.append((rc['schmidt_bond_name'],rc['schmidt_bond_dimension'],(X,Z)))
    Q=C['modified_network']; dims=Counter(d for _,d,_ in out)
    assert Q['leaf_count']==367 and Q['original_surviving_leaf_count']==365
    assert len(out)==Q['nontrivial_indices']==467
    assert dims[2]==Q['binary_indices']==371
    assert dims[3]==Q['ternary_indices']==94
    assert dims[528]==Q['rank528_indices']==1
    assert dims[8]==Q['rank8_indices']==1
    return out

def verify_tree(E,C):
    universe=set(range(C['modified_network']['leaf_count']))
    seen=[]; internal=0; mx=(1,0,None)
    def boundary(S):
        d=1; fac=[]
        for n,q,W in E:
            if any(v in S for v in W) and any(v not in S for v in W): d*=q;fac.append((n,q))
        return d,fac
    def walk(t,root=False):
        nonlocal internal,mx
        if isinstance(t,int):
            assert t in universe; seen.append(t); S={t}
        else:
            assert isinstance(t,list) and len(t)==2
            internal+=1; A=walk(t[0]); B=walk(t[1]); assert A.isdisjoint(B); S=A|B
        if not root:
            d,fac=boundary(S)
            if d>mx[0]: mx=(d,len(S),fac)
        return S
    root=walk(C['certificate']['tree'],True)
    assert root==universe
    assert len(seen)==367==len(set(seen))
    assert internal==366==C['certificate']['internal_nodes']
    d,n,fac=mx
    assert d==C['certificate']['max_boundary_dimension']==528*(2**30),(d,n)
    assert n==C['certificate']['max_node_leaf_count']==230
    assert sum(1 for _,q in fac if q==2)==27
    assert Counter(q for _,q in fac)==Counter({2:27,528:1,8:1})
    assert d<2**40
    return d,n,fac

def main():
    ap=argparse.ArgumentParser();
    ap.add_argument('cert',nargs='?',default='research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_U2_31_ONE_RANK8_GLOBAL_SUB40_CERTIFICATE.json')
    ap.add_argument('--base',default='research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json')
    a=ap.parse_args(); C=json.loads(Path(a.cert).read_text()); base=json.loads(Path(a.base).read_text())
    assert C['milestone']=='V26_QR_Q138_U2_31_ONE_RANK8_GLOBAL_SUB40_CERTIFICATE'
    assert C['scope']['condition']=='u2_31=1 physical fixed-input-mask subclass'
    assert C['replacement']['schmidt_bond_dimension']==8
    E=build(base,C);d,n,fac=verify_tree(E,C)
    print('PASS V26_QR_Q138_U2_31_ONE_RANK8_GLOBAL_SUB40_CERTIFICATE')
    print(f'leaves=367 internal_nodes=366 indices=467 max_boundary_dimension={d} log2={math.log2(d):.12f} max_cluster_leaves={n}')
    print('max_boundary_factors=27_binary + rank528 + rank8')
    print('DEPENDENCY rank<=8 for u2_31=1 must be verified separately by scripts/verify_v26_qr_q138_physical_rank_envelope27.py')
if __name__=='__main__':main()
