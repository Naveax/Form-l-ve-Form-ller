#!/usr/bin/env python3
import json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_u2_31_one_rank8_global_sub40 as S
import verify_v26_qr_q138_general_rank27_support216_global_sub39 as Old
import verify_v26_qr_q138_general_rank27_support218_global_sub39 as New


def edge_map(E):return {n:(d,set(W)) for n,d,W in E}
def bset(E,U):return {n for n,d,W in E if (set(W)&U) and (set(W)-U)}
def dimprod(names,M):
    q=1
    for n in names:q*=M[n][0]
    return q

def tree_work(E,T,nleaf):
    M=edge_map(E);ops=[];seen=[]
    def walk(t):
        if isinstance(t,int):seen.append(t);return {t}
        A=walk(t[0]);B=walk(t[1]);ba=bset(E,A);bb=bset(E,B);u=ba|bb
        cost=dimprod(u,M);U=A|B;ops.append((cost,len(U),u));return U
    root=walk(T);assert root==set(range(nleaf)) and len(seen)==nleaf==len(set(seen))
    return sum(x[0] for x in ops),max(x[0] for x in ops),ops

def source27(base,source):
    E=[]
    for n,d,W in S.build(base,source):
        if n=='RP8':n='RP27';d=27
        E.append((n,d,W))
    return E

def main():
    corr=Path('research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_GENERAL_RANK27_SUPPORT218_GLOBAL_SUB39_CERTIFICATE.json')
    C=json.loads(corr.read_text());base=json.loads(Path(C['dependencies']['base_width40_certificate']).read_text());source=json.loads(Path(C['dependencies']['source_tree_geometry']).read_text())
    sourceE=source27(base,source); sourceT=source['certificate']['tree']
    source_sum,source_max,_=tree_work(sourceE,sourceT,367)
    sourceRaw=S.build(base,source); targetT=Old.rewrite_tree(sourceRaw,source);targetE=New.build_target(base,source,C)
    target_sum,target_max,_=tree_work(targetE,targetT,368)
    ratio=target_sum/source_sum
    print('PASS V26_QR_Q138_SUPPORT218_WORK_ACCOUNTING')
    print('source_rank27_tree_dense_work='+str(source_sum))
    print('source_max_dense_operation='+str(source_max))
    print('support218_tree_dense_work='+str(target_sum))
    print('support218_max_dense_operation='+str(target_max))
    print('work_ratio_new_over_source='+repr(ratio))
    print('log2_work_penalty='+repr(math.log2(ratio)))
    print('message_max='+str(218*(2**31))+' message_log2='+repr(math.log2(218*(2**31))))
    print('scope=naive dense union-boundary operation proxy; rank/support factor generation excluded')
if __name__=='__main__':main()
