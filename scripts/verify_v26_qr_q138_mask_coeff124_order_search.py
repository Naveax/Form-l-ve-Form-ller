#!/usr/bin/env python3
import itertools,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_mask_coeff124_tt as C
import verify_v26_qr_q138_physical_rank_envelope27 as P

NAMES=list(C.MASK_NAMES)

def build_D(cert):
    intA,prefix,closures,close_ref,L=C.build_objects(cert);ctrls=list(itertools.product((0,1),repeat=12))
    MB={};w=[];buf=[];F=None;findex=None;D=[]
    for n,ctrl in enumerate(ctrls,1):
        q=C.parent_flat(ctrl,intA,prefix,closures,close_ref,L)
        if F is None:
            buf.append(q)
            if C.add_basis_mod(MB,{j:C.modfrac(x) for j,x in q.items()}):w.append(q)
            if len(MB)==C.TARGET:
                F={}
                for z in w:assert C.add_basis_q(F,z)
                findex={p:i for i,p in enumerate(sorted(F))}
                D.extend(C.reduce_q(z,F,findex) for z in buf);buf=None
        else:D.append(C.reduce_q(q,F,findex))
    assert len(D)==4096 and len(F)==124
    return D

def prefix_rank(D,order):
    S=tuple(order);k=len(S);rest=tuple(i for i in range(12) if i not in S);B={}
    for leftbits in itertools.product((0,1),repeat=k):
        row={}
        for rb in itertools.product((0,1),repeat=len(rest)):
            bits=[0]*12
            for i,b in zip(S,leftbits):bits[i]=b
            for i,b in zip(rest,rb):bits[i]=b
            idx=0
            for b in bits:idx=(idx<<1)|b
            ridx=0
            for b in rb:ridx=(ridx<<1)|b
            base=ridx*124
            for q,x in D[idx].items():row[base+q]=x
        C.add_basis_q(B,row)
    return len(B)

def profile(D,order):return tuple(prefix_rank(D,order[:k]) for k in range(1,13))
def score(p):return (max(p[:-1]),sum(p[:-1]),p)

def greedy(D):
    order=[];rem=set(range(12));prof=[]
    while rem:
        cand=[]
        for b in sorted(rem):cand.append((prefix_rank(D,order+[b]),b))
        r,b=min(cand);order.append(b);rem.remove(b);prof.append(r);print('greedy_step',len(order),NAMES[b],r,flush=True)
    return order,tuple(prof)

def hill(D,order):
    best=list(order);bp=profile(D,best);changed=True
    while changed:
        changed=False
        for i in range(11):
            q=best.copy();q[i],q[i+1]=q[i+1],q[i];p=profile(D,q)
            if score(p)<score(bp):best,bp=q,p;changed=True;print('swap_improve',i,score(bp),[NAMES[x] for x in best],flush=True);break
    return best,bp

def main():
    cert=sys.argv[1] if len(sys.argv)>1 else 'research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json'
    D=build_D(cert)
    natural=list(range(12));np=profile(D,natural);assert np==(2,4,8,16,32,64,128,119,196,136,143,124),np
    candidates=[
        list(range(8,12))+list(range(8)),
        [11,10,8,9,6,7,4,5,2,3,0,1],
        [10,11,8,9,0,1,2,3,4,5,6,7],
    ]
    g,gp=greedy(D);candidates.append(g)
    tested=[]
    for o in candidates:
        p=profile(D,o);tested.append((score(p),o,p));print('candidate',score(p),[NAMES[x] for x in o],p,flush=True)
    _,bo,bp=min(tested);bo,bp=hill(D,bo)
    # Independent exact recomputation of final profile.
    final=profile(D,bo);assert final==bp
    print('PASS V26_QR_Q138_MASK_COEFF124_ORDER_SEARCH')
    print('natural_max=196 natural_profile='+','.join(map(str,np)))
    print('best_found_order='+','.join(NAMES[x] for x in bo))
    print('best_found_profile='+','.join(map(str,final)))
    print('best_found_internal_max='+str(max(final[:-1])))
    print('scope=exact ranks for tested order; heuristic search, no global ordering optimality claim')
if __name__=='__main__':main()
