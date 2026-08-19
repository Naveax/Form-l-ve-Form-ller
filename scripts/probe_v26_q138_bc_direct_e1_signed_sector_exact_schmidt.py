#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H

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
    KX=null_basis(HL,len(LEFT))
    KY=null_basis(HR,len(RIGHT))
    return KX,KY


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
    # Homogeneous support splits into 2^d disjoint row/column rectangles.
    # On each rectangle, row-only and column-only quadratic/linear phases are
    # invertible diagonal scalings; the restricted cross-bilinear character
    # matrix has exact rational rank 2^r. Hence total exact rank is 2^(d+r).
    assert d+r<=11
    assert d+len(KX)<=11
    return d,r,d+r,len(KX),len(KY),rank,meta['pr']


def main():
    e0,e1,half=H.classify_patterns()
    assert [len(e1[k]) for k in range(4)]==[0,102,2397,8196]
    for pos in 'BC':
        dist=Counter();seen=0;unreachable=0;first_full=None;first_full_meta=None
        for k in range(4):
            for zs,cls in e1[k]:
                ex=exact_sector_exponent(pos,zs,cls)
                if ex is None:
                    unreachable+=1;continue
                seen+=1;dist[ex]+=1
                if ex[2]==11:
                    first_full=(zs,cls);first_full_meta=ex
                    break
            if first_full is not None:break
        print('position',pos,'reachable_scanned',seen,'unreachable_before_stop',unreachable,
              'first_full_rank_sector',first_full,'first_full_meta',first_full_meta,
              'rank_exponent_distribution_prefix',dict(sorted(dist.items())),flush=True)
        if first_full is not None:
            print('position',pos,'exact_sector_rank',1<<11,
                  'consequence=at least one direct-e1 signed sector is individually full row rank; sectorwise rank-subadditivity cannot yield a subgeneric universal K1 bound',flush=True)
        else:
            print('position',pos,'no_full_sector_found_in_complete_scan',True,flush=True)

    print('PASS PROBE V26_Q138_BC_DIRECT_E1_SIGNED_SECTOR_EXACT_SCHMIDT')
    print('theorem=for signed affine-quadratic sector support coupling d and restricted cross rank r, exact rational Schmidt rank is 2^(d+r)')
    print('scope=individual direct-e1 sector ranks; cross-sector cancellation in the signed aggregate remains open')

if __name__=='__main__':main()
