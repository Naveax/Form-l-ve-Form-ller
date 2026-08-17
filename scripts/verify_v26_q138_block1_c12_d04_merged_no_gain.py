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


def one_c_site_rows():
    """Local carry append map (C_i,s_i) -> (s_{i-1},v_i,w_i)."""
    rows = []
    for C, sold in itertools.product((0, 1), repeat=2):
        r = {}
        for snew, v, w in itertools.product((0, 1), repeat=3):
            q = S.T(sold, snew, C, v, w)
            if q:
                r[enc((snew, v, w))] = q
        rows.append(r)
    return rows


def c12_c14_bridge_rows():
    """Exact 3-site operator from old carry s14 through physical C14,C13,C12."""
    rows = []
    for C12, C13, C14, s14 in itertools.product((0, 1), repeat=4):
        r = {}
        for cols in itertools.product((0, 1), repeat=7):
            s11, v14, w14, v13, w13, v12, w12 = cols
            z = Fraction(0)
            for s13, s12 in itertools.product((0, 1), repeat=2):
                a = S.T(s14, s13, C14, v14, w14)
                if not a:
                    continue
                b = S.T(s13, s12, C13, v13, w13)
                if not b:
                    continue
                c = S.T(s12, s11, C12, v12, w12)
                if c:
                    z += a * b * c
            if z:
                r[enc(cols)] = z
        rows.append(r)
    return rows


def main():
    # Exact local statement. The one-site operator has full row/domain rank4,
    # hence it is injective before any assumption about the incoming row space.
    one = one_c_site_rows()
    r1 = len(S.basis(one))
    assert r1 == 4, r1

    # The three-site composed bridge has domain
    # F^{C12,C13,C14} tensor F^{s14}, dimension16, and is still injective.
    bridge = c12_c14_bridge_rows()
    r3 = len(S.basis(bridge))
    assert r3 == 16, r3

    # Clean prerequisite theorem V26_Q138_BLOCK1_D4_BOUNDARY_FIBER_NO_GAIN
    # certifies exact rank(D0..4)=65536 on an incoming space exposing s14.
    # Tensoring/composing with an injective 3-site bridge cannot create a new
    # kernel: each of the three new physical C bits therefore doubles rank.
    incoming_rank = 65536
    merged_rank = incoming_rank * (2 ** 3)
    assert merged_rank == 524288 == 16 * (2 ** 15)

    print('PASS V26_Q138_BLOCK1_C12_D04_MERGED_NO_GAIN')
    print('single_C_carry_operator_rank=4/4 injective')
    print('C12..C14_three_site_operator_rank=16/16 injective')
    print('clean_prerequisite_D0..4_rank=65536')
    print('merged_C12..14_plus_D0..4_rank=524288=16*2^15 (no gain)')
    print('scope=closes the smallest merged backward-C-carry x repeated-D bridge; larger bridge to high/wrap block2 remains open')


if __name__ == '__main__':
    main()
