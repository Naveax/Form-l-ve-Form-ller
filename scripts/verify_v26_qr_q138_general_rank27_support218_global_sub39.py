#!/usr/bin/env python3
import argparse,json,math,sys
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_u2_31_one_rank8_global_sub40 as S
import verify_v26_qr_q138_general_rank27_support216_global_sub39 as Old


def build_target(base,source,C):
    E=S.build(base,source);I9=set(C['replacement']['I9_edges']);O7=set(C['replacement']['O7_edges'])
    assert I9|O7==set(source['replacement']['external_left_binary_edges']);out=[]
    for name,dim,W in E:
        W=list(W)
        if name=='RP8':name='RP27';dim=27
        if 365 in W:
            W.remove(365)
            if name in I9:W.append(365)
            elif name in O7 or name=='RP27':W.append(367)
            else:raise AssertionError(('unexpected X incidence',name,dim,W))
        if len(set(W))>1:out.append((name,dim,tuple(sorted(set(W)))))
    out.append(('RL218',218,(365,367)))
    dims=Counter(d for _,d,_ in out);Q=C['modified_network']
    assert Q['leaf_count']==368 and Q['internal_nodes']==367 and len(out)==468
    assert dims[2]==371 and dims[3]==94 and dims[528]==1 and dims[27]==1 and dims[218]==1
    return out


def verify(E,T,C):
    seen=[];internal=0;vals=[]
    def walk(t,root=False):
        nonlocal internal
        if isinstance(t,int):seen.append(t);U={t}
        else:
            internal+=1;A=walk(t[0]);B=walk(t[1]);assert A.isdisjoint(B);U=A|B
        if not root:
            d,fac=Old.boundary(E,U);vals.append((d,len(U),fac))
        return U
    assert walk(T,True)==set(range(368));assert len(seen)==368==len(set(seen)) and internal==367
    vals.sort(key=lambda x:x[0],reverse=True);d,n,fac=vals[0];Q=C['certificate']
    assert d==Q['max_boundary_dimension']==218*(2**31),(d,n,fac)
    assert abs(math.log2(d)-Q['max_log2_boundary_dimension'])<1e-12
    assert n==2 and Counter(q for _,q in fac)==Counter({2:31,218:1}),fac
    assert vals[1][0]==Q['second_largest_boundary_dimension']==528*(2**29)
    assert d<2**39
    return d,n,fac,vals[1]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('cert',nargs='?',default='research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_GENERAL_RANK27_SUPPORT218_GLOBAL_SUB39_CERTIFICATE.json');a=ap.parse_args()
    C=json.loads(Path(a.cert).read_text());base=json.loads(Path(C['dependencies']['base_width40_certificate']).read_text());source=json.loads(Path(C['dependencies']['source_tree_geometry']).read_text())
    assert C['milestone']=='V26_QR_Q138_GENERAL_RANK27_SUPPORT218_GLOBAL_SUB39_CERTIFICATE'
    assert C['replacement']['parent_schmidt_dimension_bound']==27 and C['replacement']['left_support_dimension_bound']==218
    sourceE=S.build(base,source);T=Old.rewrite_tree(sourceE,source);E=build_target(base,source,C);d,n,fac,second=verify(E,T,C)
    print('PASS V26_QR_Q138_GENERAL_RANK27_SUPPORT218_GLOBAL_SUB39_CERTIFICATE')
    print(f'leaves=368 internal_nodes=367 indices=468 max_boundary_dimension={d} log2={math.log2(d):.12f}')
    print('max_boundary_factors=31_binary + RL218; RP27 is internal')
    print(f'second_boundary_dimension={second[0]} log2={math.log2(second[0]):.12f}')
    print('DEPENDENCIES: physical_rank_envelope27 and exact left_i9_gram_support')
if __name__=='__main__':main()
