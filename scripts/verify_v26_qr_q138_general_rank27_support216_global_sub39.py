#!/usr/bin/env python3
import argparse,json,math,sys
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_u2_31_one_rank8_global_sub40 as S


def build_target(base,source,C):
    E=S.build(base,source)
    I9=set(C['replacement']['I9_edges']);O7=set(C['replacement']['O7_edges'])
    assert I9|O7==set(source['replacement']['external_left_binary_edges'])
    out=[]
    for name,dim,W in E:
        W=list(W)
        if name=='RP8':
            name='RP27';dim=27
        if 365 in W:
            W.remove(365)
            if name in I9:W.append(365)       # XA
            elif name in O7 or name=='RP27':W.append(367)  # XB
            else:raise AssertionError(('unexpected X incidence',name,dim,W))
        if len(set(W))>1:out.append((name,dim,tuple(sorted(set(W)))))
    out.append(('RL216',216,(365,367)))
    Q=C['modified_network'];dims=Counter(d for _,d,_ in out)
    assert Q['leaf_count']==368 and Q['internal_nodes']==367
    assert len(out)==Q['nontrivial_indices']==468
    assert dims[2]==Q['binary_indices']==371
    assert dims[3]==Q['ternary_indices']==94
    assert dims[528]==Q['rank528_indices']==1
    assert dims[27]==Q['rank27_indices']==1
    assert dims[216]==Q['rank216_indices']==1
    return out


def boundary(E,U):
    d=1;fac=[]
    for n,q,W in E:
        if any(v in U for v in W) and any(v not in U for v in W):
            d*=q;fac.append((n,q))
    return d,fac


def source_max(sourceE,source):
    nodes=[]
    def walk(t):
        if isinstance(t,int):return {t}
        A=walk(t[0]);B=walk(t[1]);U=A|B
        d,_=boundary(sourceE,U);nodes.append((U,A,B,d,t));return U
    root=walk(source['certificate']['tree']);assert root==set(range(367))
    hits=[x for x in nodes if x[3]==source['certificate']['max_boundary_dimension']]
    assert len(hits)==1
    U,A,B,d,t=hits[0];assert len(U)==230
    assert {len(A),len(B)}=={1,229}
    single=A if len(A)==1 else B
    assert single=={365}
    A229=B if single is A else A
    return U,A229


def rewrite_tree(sourceE,source):
    max230,A229=source_max(sourceE,source)
    def ls(t):
        if isinstance(t,int):return {t}
        return ls(t[0])|ls(t[1])
    def rw(t):
        if isinstance(t,int):return t
        L,R=t;sL=ls(L);sR=ls(R)
        if (sL==max230 and sR=={366}) or (sR==max230 and sL=={366}):
            M=L if sL==max230 else R
            m0,m1=M;sm0=ls(m0);sm1=ls(m1)
            if sm0=={365}:Atree=m1
            elif sm1=={365}:Atree=m0
            else:raise AssertionError('source max does not contain singleton X8 child')
            assert ls(Atree)==A229
            return [[rw(Atree),365],[367,366]]
        return [rw(L),rw(R)]
    T=rw(source['certificate']['tree']);assert ls(T)==set(range(368))
    return T


def verify_target(E,T,C):
    seen=[];internal=0;vals=[]
    def walk(t,root=False):
        nonlocal internal
        if isinstance(t,int):
            assert 0<=t<368;seen.append(t);U={t}
        else:
            assert isinstance(t,list) and len(t)==2
            internal+=1;A=walk(t[0]);B=walk(t[1]);assert A.isdisjoint(B);U=A|B
        if not root:
            d,fac=boundary(E,U);vals.append((d,len(U),fac))
        return U
    root=walk(T,True);assert root==set(range(368))
    assert len(seen)==368==len(set(seen));assert internal==367
    vals.sort(key=lambda x:x[0],reverse=True)
    d,n,fac=vals[0];Q=C['certificate']
    assert d==Q['max_boundary_dimension']==216*(2**31),(d,n,fac)
    assert abs(math.log2(d)-Q['max_log2_boundary_dimension'])<1e-12
    assert n==Q['max_node_leaf_count']==2
    assert Counter(q for _,q in fac)==Counter({2:31,216:1}),fac
    assert vals[1][0]==Q['second_largest_boundary_dimension']==528*(2**29)
    assert d<2**39
    return d,n,fac,vals[1]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('cert',nargs='?',default='research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_GENERAL_RANK27_SUPPORT216_GLOBAL_SUB39_CERTIFICATE.json')
    a=ap.parse_args();C=json.loads(Path(a.cert).read_text())
    base=json.loads(Path(C['dependencies']['base_width40_certificate']).read_text())
    source=json.loads(Path(C['dependencies']['source_tree_geometry']).read_text())
    assert C['milestone']=='V26_QR_Q138_GENERAL_RANK27_SUPPORT216_GLOBAL_SUB39_CERTIFICATE'
    assert C['scope']['condition']=='all 4096 physical fixed-input-mask cases in the certified family'
    assert C['replacement']['parent_schmidt_dimension_bound']==27
    assert C['replacement']['left_support_dimension_bound']==216
    sourceE=S.build(base,source)
    E=build_target(base,source,C);T=rewrite_tree(sourceE,source)
    d,n,fac,second=verify_target(E,T,C)
    print('PASS V26_QR_Q138_GENERAL_RANK27_SUPPORT216_GLOBAL_SUB39_CERTIFICATE')
    print(f'leaves=368 internal_nodes=367 indices=468 max_boundary_dimension={d} log2={math.log2(d):.12f} max_cluster_leaves={n}')
    print('max_boundary_factors=31_binary + RL216; RP27 is internal to the maximizing XB-Z27 pair')
    print(f'second_boundary_dimension={second[0]} log2={math.log2(second[0]):.12f}')
    print('DEPENDENCIES: run physical_rank_envelope27 and left_i9_support216 verifiers separately')

if __name__=='__main__':main()
