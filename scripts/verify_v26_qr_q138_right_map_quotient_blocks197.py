#!/usr/bin/env python3
import itertools,sys
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_right_map_reachable_hull197 as H

TAUS=list(itertools.product((0,1),repeat=3))

def project(v,sign):
    s=H.swap(v);keys=set(v)|set(s)
    return {j:v.get(j,0)+sign*s.get(j,0) for j in keys}

def sector_basis(B,sign):
    out={}
    for v in B.values():H.add_basis(out,project(v,sign))
    return out

def rank_images(B,K):
    out={}
    for v in B.values():H.add_basis(out,H.image(v,K))
    return len(out)

def main():
    cert=sys.argv[1] if len(sys.argv)>1 else 'research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json'
    ctx=H.setup(cert);Ks={tau:H.transfer(ctx,4,tau) for tau in TAUS}
    U={}
    for tau in TAUS:
        for v in H.boundary(ctx,tau).values():H.add_basis(U,v)
    growth=[(len(sector_basis(U,+1)),len(sector_basis(U,-1)))]
    for _ in range(4):
        old=list(U.values());added=0
        for K in Ks.values():
            for v in old:added+=H.add_basis(U,H.image(v,K))
        growth.append((len(sector_basis(U,+1)),len(sector_basis(U,-1))))
        if not added:break
    assert growth==[(20,8),(107,43),(135,58),(138,59),(138,59)],growth
    assert len(U)==197
    P=sector_basis(U,+1);M=sector_basis(U,-1);assert (len(P),len(M))==(138,59)
    # exact copy-swap commutation for all ambient transfers
    for tau,K in Ks.items():
        for r,row in K.items():
            sr=((r&31)<<5)|(r>>5);srow=K.get(sr,{})
            for c,v in row.items():
                sc=((c&31)<<5)|(c>>5);assert srow.get(sc,0)==v
    rp=[rank_images(P,K) for K in Ks.values()];rm=[rank_images(M,K) for K in Ks.values()]
    assert rp==[136,89,63,66,80,87,68,56],rp
    assert rm==[58,37,26,28,32,35,32,24],rm
    assert [a+b for a,b in zip(rp,rm)]==[194,126,89,94,112,122,100,80]
    print('PASS V26_QR_Q138_RIGHT_MAP_QUOTIENT_BLOCKS197')
    print('sector_growth=(20,8)->(107,43)->(135,58)->(138,59)->(138,59)')
    print('symmetric_block_dim=138 ranks='+','.join(map(str,rp)))
    print('antisymmetric_block_dim=59 ranks='+','.join(map(str,rm)))
if __name__=='__main__':main()
