#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D

N=2048


def fwht_pm(bits):
    a=[-1 if ((bits>>x)&1) else 1 for x in range(N)]
    h=1
    while h<N:
        for i in range(0,N,2*h):
            for j in range(i,i+h):
                u=a[j];v=a[j+h]
                a[j]=u+v;a[j+h]=u-v
        h*=2
    return {i for i,v in enumerate(a) if v}


def span_set(basis):
    out={0}
    for v in basis:out |= {x^v for x in list(out)}
    return out


def sector_frequency_envelope(pos,zs,cls):
    can=H.support_for(pos,zs,cls)
    if can is None:return None
    qbits,cols,rank,meta=S.corrected_phase_data(pos,D.carries(zs))
    cb=S.row_basis(cols)
    lb=S.left_basis(can)
    fq=fwht_pm(qbits)
    shifts=span_set(cb)
    support=span_set(lb)
    # sign spectrum shifted by every cross-linear character, then convolved
    # with the affine-support indicator spectrum. Affine offsets only change
    # Fourier signs, never the support set.
    out=set()
    for f in fq:
        for t in shifts:
            z=f^t
            for u in support:out.add(z^u)
    return out


def main():
    e0,e1,half=H.classify_patterns()
    assert sum(len(e0[k]) for k in range(4))==581
    assert len(half)==4
    for pos in 'BC':
        U0=set(); raw0=0; imp0=0; max_sector=0
        for k in range(4):
            for zs,cls in e0[k]:
                E=sector_frequency_envelope(pos,zs,cls)
                if E is None:
                    imp0+=1;continue
                raw0+=1;max_sector=max(max_sector,len(E));U0 |= E
        expected_raw=581 if pos=='B' else 577
        assert raw0==expected_raw,(pos,raw0)

        UH=set(); rawh=0; imph=0; half_sizes=[]
        for zs,cls in half:
            E=sector_frequency_envelope(pos,zs,cls)
            if E is None:
                imph+=1;continue
            rawh+=1;half_sizes.append(len(E));UH |= E
        assert rawh==4 and imph==0
        UK0=U0|UH
        print('position',pos,
              'reachable_raw_e0',raw0,'impossible_e0',imp0,
              'raw_e0_exact_signed_left_frequency_union',len(U0),
              'max_individual_e0_frequency_envelope',max_sector,
              'half_sector_frequency_sizes',half_sizes,
              'half_exact_sum_frequency_union',len(UH),
              'complete_exact_signed_K0_frequency_envelope',len(UK0),flush=True)
        print('position',pos,
              'interpretation=complete exact signed valuation-e0 plus four half-sector aggregate lies in this fixed left Walsh character space; rank is at most envelope size',flush=True)

    print('PASS PROBE V26_Q138_BC_EXACT_SIGNED_K0_FREQUENCY_ENVELOPE')
    print('scope=safe uniform left-frequency envelope for exact signed K0 candidate; no cancellation between sectors assumed')

if __name__=='__main__':main()
