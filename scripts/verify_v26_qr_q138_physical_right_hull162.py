#!/usr/bin/env python3
import itertools, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_right_map_reachable_hull197 as H

PHYS=list(itertools.product((0,1),repeat=2))

def project(v,sign):
    s=H.swap(v); keys=set(v)|set(s)
    return {j:v.get(j,0)+sign*s.get(j,0) for j in keys}

def sector_basis(B,sign):
    out={}
    for v in B.values(): H.add_basis(out,project(v,sign))
    return out

def rank_images(B,K):
    return H.rank_vectors(H.image(v,K) for v in B.values())

def main():
    cert=sys.argv[1] if len(sys.argv)>1 else 'research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json'
    ctx=H.setup(cert)
    Ks={(u1,u2):H.transfer(ctx,4,(u1,u2,0)) for u1,u2 in PHYS}
    for uv in PHYS:
        assert Ks[uv]==H.transfer(ctx,5,(uv[0],uv[1],0))==H.transfer(ctx,6,(uv[0],uv[1],0))
    ambient=[H.rank_vectors(K.values()) for K in Ks.values()]
    assert ambient==[1016,384,454,431],ambient

    U={}
    for u1,u2 in PHYS:
        B=H.boundary(ctx,(u1,u2,0))
        assert H.rank_vectors(B.values())==4
        for v in B.values(): H.add_basis(U,v)
    dims=[len(U)]
    sectors=[(len(sector_basis(U,+1)),len(sector_basis(U,-1)))]
    for _ in range(5):
        old=list(U.values()); added=0
        for K in Ks.values():
            for v in old: added += H.add_basis(U,H.image(v,K))
        dims.append(len(U)); sectors.append((len(sector_basis(U,+1)),len(sector_basis(U,-1))))
        if not added: break
    assert dims==[15,70,153,162,162],dims
    assert sectors==[(11,4),(50,20),(106,47),(114,48),(114,48)],sectors

    P=sector_basis(U,+1); M=sector_basis(U,-1)
    assert (len(P),len(M))==(114,48)
    full=[rank_images(U,K) for K in Ks.values()]
    sym=[rank_images(P,K) for K in Ks.values()]
    anti=[rank_images(M,K) for K in Ks.values()]
    assert full==[159,79,99,97],full
    assert sym==[112,56,71,66],sym
    assert anti==[47,23,28,31],anti
    assert [a+b for a,b in zip(sym,anti)]==full

    print('PASS V26_QR_Q138_PHYSICAL_RIGHT_HULL162')
    print('physical_controls=(u1,u2), p=0')
    print('cumulative_hull_dims=15,70,153,162,162 invariant_hull=162')
    print('copy_swap_sectors=symmetric:114 antisymmetric:48')
    print('restricted_ranks=159,79,99,97')

if __name__=='__main__': main()
