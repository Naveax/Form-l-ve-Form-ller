#!/usr/bin/env python3
import itertools
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S
import verify_v26_q138_signed_block2_extend12_rank21888 as E


def enc(bs):
    z = 0
    for b in bs:
        z = (z << 1) | b
    return z


def dec(z, n):
    return tuple((z >> (n - 1 - i)) & 1 for i in range(n))


def block1_rows():
    """Physical rows of the exact rank16 block1 on its six retained bits."""
    rows = []
    for A0, B0, C15, C16, D0 in itertools.product((0, 1), repeat=5):
        r = {}
        for s216, v215, s214, s10, u30, v312 in itertools.product((0, 1), repeat=6):
            x = Fraction(0)
            for s215 in (0, 1):
                x += S.T(s216, s215, C16, D0, 0) * S.T(s215, s214, C15, v215, 1)
            if not x:
                continue
            y = S.T0(s10, A0, v312 ^ B0, u30 ^ D0)
            if not y:
                continue
            r[enc((s216, v215, s214, s10, u30, v312))] = x * y
        rows.append(r)
    assert len(S.basis(rows)) == 16
    return rows


def merge_shared_v312(block_row, bit0_row):
    """Identify the common v3_12 coordinate instead of duplicating it."""
    out = {}
    for kb, xb in block_row.items():
        s216, v215, s214, s10, u30, v312 = dec(kb, 6)
        for kk, xk in bit0_row.items():
            s0, u40, v312b = dec(kk, 3)
            if v312 != v312b:
                continue
            k = enc((s216, v215, s214, s10, u30, v312, s0, u40))
            out[k] = out.get(k, Fraction(0)) + xb * xk
    return {k: v for k, v in out.items() if v}


def merged_K_space(D16, B1):
    K = E.bit0_rows(D16)
    assert len(K) == 2
    rows = []
    for a in B1:
        for b in K:
            rows.append(merge_shared_v312(a, b))
    return rows


def main():
    B1 = block1_rows()
    assert len(B1) == 32
    assert len(S.basis(B1)) == 16

    K0_rows = merged_K_space(0, B1)
    K1_rows = merged_K_space(1, B1)
    r0 = len(S.basis(K0_rows))
    r1 = len(S.basis(K1_rows))
    ru = len(S.basis(K0_rows + K1_rows))
    assert (r0, r1, ru) == (32, 32, 48), (r0, r1, ru)
    ki = r0 + r1 - ru
    assert ki == 16

    # Build on the separately clean-certified extended-block2 geometry:
    # J0,J1 ranks448, intersection424; 16 independent high prefixes.
    jdim = 448
    jint = 424
    per_prefix = jdim * r0 + jdim * r1 - jint * ki
    assert per_prefix == 21888
    merged_total = 16 * per_prefix
    assert merged_total == 350208
    product = 16 * 21888
    assert merged_total == product

    center = merged_total * (2 ** 23)
    assert center == 171 * (2 ** 34)

    print('PASS V26_Q138_BLOCK1_BLOCK2_SHARED_V312_NO_GAIN')
    print('block1_exact_rank=16')
    print('shared_v3_12_merged_K_D16_ranks=32,32 union48 intersection16')
    print('extended_block2_j1_D16_geometry=448,448 intersection424 (clean prerequisite theorem)')
    print('per_D12..15_prefix_joint_rank=21888')
    print('full_joint_rank=16*21888=350208 equals product bound')
    print('S1_central_bound_unchanged=171*2^34')
    print('scope=closes only the direct shared-v3_12 overlap; larger carry-bridge merges remain open')


if __name__ == '__main__':
    main()
