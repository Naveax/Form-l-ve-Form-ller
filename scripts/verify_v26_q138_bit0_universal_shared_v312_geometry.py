#!/usr/bin/env python3
import itertools
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S


def enc(bs):
    z = 0
    for b in bs:
        z = (z << 1) | b
    return z


def local_rows(D16, v312):
    rows = []
    labels = []
    for C0 in (0, 1):
        r = {}
        for s0, u40 in itertools.product((0, 1), repeat=2):
            q = S.T0(s0, C0, D16, u40 ^ v312)
            if q:
                r[enc((v312, s0, u40))] = q
        rows.append(r)
        labels.append((D16, C0, v312))
    return labels, rows


def main():
    full = {0: [], 1: []}
    common = 0
    for v in (0, 1):
        L0, K0 = local_rows(0, v)
        L1, K1 = local_rows(1, v)
        assert len(S.basis(K0)) == 2
        assert len(S.basis(K1)) == 2
        assert len(S.basis(K0 + K1)) == 3

        p0 = {lab: i for i, lab in enumerate(L0)}
        p1 = {lab: i for i, lab in enumerate(L1)}
        # The one-dimensional local intersection has an explicit common row,
        # independent of the retained v312 slice.
        assert K0[p0[(0, 1, v)]] == K1[p1[(1, 0, v)]]
        common += 1
        full[0].extend(K0)
        full[1].extend(K1)

    assert common == 2
    r0 = len(S.basis(full[0]))
    r1 = len(S.basis(full[1]))
    ru = len(S.basis(full[0] + full[1]))
    assert (r0, r1, ru) == (4, 4, 6)
    assert r0 + r1 - ru == 2

    print('PASS V26_Q138_BIT0_UNIVERSAL_SHARED_V312_GEOMETRY')
    print('per_v312_D16_spaces=rank2,rank2 union3 intersection1')
    print('explicit_common_row: D16=0,C0=1 == D16=1,C0=0 for both v312 slices')
    print('full_retained_v312_spaces=rank4,rank4 union6 intersection2')
    print('universal_consequence_for_any_incoming_W: dims=2*dimW,2*dimW intersection=dimW')
    print('scope=exact local theorem used to scale D16/bit0 geometry for enlarged block1 spaces')


if __name__ == '__main__':
    main()
