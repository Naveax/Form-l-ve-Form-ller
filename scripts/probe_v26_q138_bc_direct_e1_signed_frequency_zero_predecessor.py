#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H

NLEFT=1<<11


def span(B):
    out={0}
    for b in B:
        out |= {x^b for x in list(out)}
    return out


def fwht_support_of_sign(qbits):
    a=[-1 if ((qbits>>x)&1) else 1 for x in range(NLEFT)]
    h=1
    while h<NLEFT:
        for i in range(0,NLEFT,2*h):
            for j in range(i,i+h):
                u=a[j];v=a[j+h]
                a[j]=u+v;a[j+h]=u-v
        h*=2
    return {i for i,v in enumerate(a) if v}


def xor3(A0,B0,C0):
    return {a^b^c for a in A0 for b in B0 for c in C0}


def sector_frequency_envelope(pos,zs,cls):
    can=H.support_for(pos,zs,cls)
    if can is None:return None
    qbits,cols,rank,meta=S.corrected_phase_data(pos,D.carries(zs))

    # Fixed predecessor x=0. Only the 21 right-beta variables vary as matrix
    # columns; predecessor columns are fixed and therefore do not enlarge the
    # row space in this diagnostic.
    cross=[]
    for i in A.R1:
        e=128+i
        cross.append(cols[S.RIDX[e]])
    C=span(S.row_basis(cross))
    L=span(S.left_basis(can))
    Q=fwht_support_of_sign(qbits)
    E=xor3(Q,C,L)
    return E,(len(Q),len(C),len(L),len(E),rank,meta['pr'])


def main():
    e0,e1,half=H.classify_patterns()
    assert [len(e1[k]) for k in range(4)]==[0,102,2397,8196]

    for pos in 'BC':
        U=set();seen=0;unreachable=0;stats=Counter();first_sat=None
        for k in range(4):
            for zs,cls in e1[k]:
                r=sector_frequency_envelope(pos,zs,cls)
                if r is None:
                    unreachable+=1;continue
                E,meta=r;seen+=1;stats[meta]+=1
                U |= E
                if len(U)==NLEFT and first_sat is None:
                    first_sat=seen
                    break
            if first_sat is not None:break
        print('position',pos,'reachable_scanned',seen,'unreachable_before_stop',unreachable,
              'fixed_x0_signed_frequency_union',len(U),'first_saturation_at',first_sat,flush=True)
        print('position',pos,'sector_meta_distribution_prefix',dict(sorted(stats.items())),flush=True)
        if first_sat is None:
            # If the envelope did not saturate, complete the remaining sectors.
            U=set();seen=0;unreachable=0;stats=Counter()
            for k in range(4):
                for zs,cls in e1[k]:
                    r=sector_frequency_envelope(pos,zs,cls)
                    if r is None:
                        unreachable+=1;continue
                    E,meta=r;seen+=1;stats[meta]+=1;U|=E
            print('position',pos,'complete_reachable',seen,'complete_unreachable',unreachable,
                  'complete_fixed_x0_signed_frequency_union',len(U),flush=True)

    print('PASS PROBE V26_Q138_BC_DIRECT_E1_SIGNED_FREQUENCY_ZERO_PREDECESSOR')
    print('scope=fixed predecessor x=0 direct-e1 exact-signed left-Fourier envelope; saturation closes this global-frequency route, non-saturation requires predecessor-shift quotient analysis')

if __name__=='__main__':main()
