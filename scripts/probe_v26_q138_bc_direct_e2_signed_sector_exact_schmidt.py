#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as V
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import verify_v26_q138_bc_third_weight119_frequency_envelope1796_2048 as E2

LEFT=sorted(A.S1)
RIGHT=list(A.R1)


def null_basis(rows,n):
    sol=T.rref([(r,0) for r in rows if r],n=n)
    assert sol is not None
    return sol[2]


def support_kernels(can):
    HL=[];HR=[]
    for row in can:
        l=r=0
        for q,i in enumerate(LEFT):
            if (row>>(128+i))&1:l|=1<<q
        for q,i in enumerate(RIGHT):
            if (row>>(128+i))&1:r|=1<<q
        if l:HL.append(l)
        if r:HR.append(r)
    return null_basis(HL,len(LEFT)),null_basis(HR,len(RIGHT))


def restricted_cross_rank(cols,KX,KY):
    vec=[]
    for ky in KY:
        leftmask=0
        for q,i in enumerate(RIGHT):
            if (ky>>q)&1:leftmask ^= cols[S.RIDX[128+i]]
        v=0
        for a,kx in enumerate(KX):
            if (leftmask&kx).bit_count()&1:v|=1<<a
        vec.append(v)
    return T.gf2_rank(vec,len(KX))


def exact_sector_exponent(pos,zs,cls):
    can=H.support_for(pos,zs,cls)
    if can is None:return None
    qbits,cols,rank,meta=S.corrected_phase_data(pos,D.carries(zs))
    KX,KY=support_kernels(can)
    d=A.cut_intersection(can)
    r=restricted_cross_rank(cols,KX,KY)
    assert d+r<=11
    return d,r,d+r,len(KX),len(KY),rank,meta['pr']


def setup_classes():
    sites=[(j,i) for j in range(1,5) for i in range(31)]
    F0=T.forms('B',(0,0,0,0,0))
    base=A.internal_null('B',D.carries([]))
    assert base[0]==124 and len(base[2])==4
    sig={z:V.quotient_signature(F0,base[2],*z) for z in sites}
    inert=[z for z in sites if sig[z]==(0,0)]
    active=[z for z in sites if sig[z]!=(0,0)]
    P=V.polar_rows('B',base[2])
    assert len(inert)==95 and len(active)==29 and T.gf2_rank(P,4)==2
    return active,inert,sig,P


def sectors(active,inert,sig,P):
    for k in (2,3,4):
        for zs,cls in E2.e2_candidates(k,active,inert,sig,P):
            yield k,zs,cls
    for zs in E2.fullrank5_candidates(active,inert,sig):
        yield 5,zs,(128,0,0)


def main():
    active,inert,sig,P=setup_classes()
    for pos in 'BC':
        seen=unreachable=0;dist=Counter();first=None;meta=None
        for k,zs,cls in sectors(active,inert,sig,P):
            ex=exact_sector_exponent(pos,zs,cls)
            if ex is None:
                unreachable+=1;continue
            seen+=1;dist[(k,)+ex]+=1
            if ex[2]==11:
                first=(k,zs,cls);meta=ex;break
        print('position',pos,'reachable_scanned',seen,'unreachable_before_stop',unreachable,
              'first_full_rank_direct_e2_sector',first,'first_full_meta',meta,
              'rank_exponent_distribution_prefix',dict(sorted(dist.items())),flush=True)
        if first is not None:
            print('position',pos,'exact_sector_rank',1<<11,
                  'consequence=sectorwise exact-signed direct-e2 rank subadditivity cannot provide a subgeneric K2 bound; aggregate cancellation or a different mod4 lift is required',flush=True)
        else:
            print('position',pos,'no_full_sector_found_in_complete_scan',True,flush=True)
    print('PASS PROBE V26_Q138_BC_DIRECT_E2_SIGNED_SECTOR_EXACT_SCHMIDT')
    print('theorem=on each affine support rectangle the signed quadratic sector has exact rank 2^(d+r), with support coupling d and restricted cross rank r')
    print('scope=individual direct-e2 signed sectors only; no claim about cancellation in their exact aggregate or about the optimal mod4 K1 lift')

if __name__=='__main__':main()
