#!/usr/bin/env python3
import itertools,sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_mask_coeff124_tt as C
import verify_v26_qr_q138_physical_rank_envelope27 as P

MASK_NAMES=(
    'u1_3','u2_3','u1_4','u2_4','u1_5','u2_5',
    'u1_6','u2_6','u1_7','u2_7','u2_8','u2_31',
)
PRIME=1000000007


def flatG(G):return {i*64+j:x for i,row in enumerate(G) for j,x in row.items() if x}

def rank_rows(rows):
    B={}
    for r in rows:C.add_basis_q(B,r)
    return len(B)

def tt_profile(D,dim):
    out=[]
    for k in range(1,13):
        B={};ns=1<<(12-k)
        for pref in range(1<<k):
            row={}
            for suff in range(ns):
                base=suff*dim
                for q,x in D[(pref<<(12-k))|suff].items():row[base+q]=x
            C.add_basis_q(B,row)
        out.append(len(B));print('tt_cut',k,'rank',len(B),flush=True)
    return tuple(out)


def main():
    cert=sys.argv[1] if len(sys.argv)>1 else 'research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json'
    intA,prefix,closures,close_ref,L=C.build_objects(cert)
    ctrls=list(itertools.product((0,1),repeat=12));MB={};witness=[];cache=[]
    for n,ctrl in enumerate(ctrls,1):
        G=P.gram_rows(intA,close_ref,prefix[ctrl[:8]],closures[ctrl[8:]])
        g=flatG(G);cache.append(g)
        if C.add_basis_mod(MB,{j:C.modfrac(x) for j,x in g.items()}):witness.append(n-1)
        if n%512==0:print('mod_gram_span',n,len(MB),flush=True)
    r=len(MB);print('mod_gram_family_rank',r,flush=True)
    # A full mod-p rank of 4096 already proves exact Q-rank 4096.
    if r==4096:
        profile=(2,4,8,16,32,64,128,256,512,1024,2048,4096)
        print('PASS V26_QR_Q138_RIGHT_GRAM_FAMILY_TT')
        print('mask_order='+','.join(MASK_NAMES))
        print('exact_right_gram_matrix_family_rank=4096 via full mod-p witness')
        print('exact_tt_profile='+','.join(map(str,profile))+' max=4096')
        print('interpretation=all 4096 physical Gram matrices linearly independent')
        return
    # Otherwise reconstruct a rational witness basis and prove exact coverage.
    F={}
    for i in witness:assert C.add_basis_q(F,cache[i])
    assert len(F)==r
    pindex={p:i for i,p in enumerate(sorted(F))};D=[]
    for n,g in enumerate(cache,1):
        D.append(C.reduce_q(g,F,pindex))
        if n%512==0:print('exact_gram_cover',n,flush=True)
    assert rank_rows(D)==r
    profile=tt_profile(D,r)
    # Shared u2_8 = control index10; bit31 index11.
    sector={}
    for idx,name in ((10,'u2_8'),(11,'u2_31')):
        sector[name]=tuple(rank_rows([cache[i] for i,c in enumerate(ctrls) if c[idx]==b]) for b in (0,1))
    print('PASS V26_QR_Q138_RIGHT_GRAM_FAMILY_TT')
    print('mask_order='+','.join(MASK_NAMES))
    print('exact_right_gram_matrix_family_rank='+str(r))
    print('exact_tt_profile='+','.join(map(str,profile))+' max='+str(max(profile)))
    print('u2_8_conditioned_family_ranks='+','.join(map(str,sector['u2_8'])))
    print('u2_31_conditioned_family_ranks='+','.join(map(str,sector['u2_31'])))
if __name__=='__main__':main()
