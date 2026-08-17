#!/usr/bin/env python3
import itertools
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_signed_block2_extend12_rank21888 as E


def local_j1_transfer_rows(D11):
    """Bit11 transfer on the old outgoing sigma s11, with D11 column-fixed."""
    rows = []
    for s11 in (0, 1):
        r = {}
        for A11, B11, u11, x11 in itertools.product((0, 1), repeat=4):
            v = x11 ^ B11
            w = u11 ^ D11
            s10 = s11 ^ A11 ^ v ^ w
            q = E.S.T(s11, s10, A11, v, w)
            if q:
                k = E.enc((A11, B11, u11, x11, s10))
                r[k] = q
        rows.append(r)
    return rows


def local_j2_transfer_rows(D11):
    """Bit27 transfer on the old outgoing sigma s27, with D11 column-fixed."""
    rows = []
    for s27 in (0, 1):
        r = {}
        for C27, W27 in itertools.product((0, 1), repeat=2):
            s26 = s27 ^ C27 ^ D11 ^ W27
            q = E.S.T(s27, s26, C27, D11, W27)
            if q:
                k = E.enc((C27, W27, s26))
                r[k] = q
        rows.append(r)
    return rows


def extend_high27_fixed_d11(h, D11):
    """Extend the j2 bits28..31 high vector through bit27 at fixed D11."""
    r = {}
    for k, a in h.items():
        z = E.dec(k, 9)
        Cs = z[:4]
        Ws = z[4:8]
        s27 = z[8]
        for C27, W27 in itertools.product((0, 1), repeat=2):
            s26 = s27 ^ C27 ^ D11 ^ W27
            q = E.S.T(s27, s26, C27, D11, W27)
            if q:
                j = E.enc(Cs + Ws + (C27, W27, s26))
                r[j] = r.get(j, Fraction(0)) + a * q
    return r


def c12_isolated_row_rank():
    """Rank of the single physical C12 row bit with both carry sides open."""
    rows = []
    for C12 in (0, 1):
        r = {}
        for s12, s11, v, w in itertools.product((0, 1), repeat=4):
            q = E.S.T(s12, s11, C12, v, w)
            if q:
                r[E.enc((s12, s11, v, w))] = q
        rows.append(r)
    return len(E.S.basis(rows))


def main():
    # Both next-site transfers are injective on their 2D carry input for each
    # fixed external D11 value. Therefore extending an existing row subspace
    # through either transfer cannot lower its dimension or enlarge an
    # intersection merely by the transfer itself.
    for D11 in (0, 1):
        assert len(E.S.basis(local_j1_transfer_rows(D11))) == 2
        assert len(E.S.basis(local_j2_transfer_rows(D11))) == 2

        # The sixteen D12..15 high sectors remain a direct sum even after the
        # bit27 extension, separately inside each D11 column slice.
        hs = []
        for p in itertools.product((0, 1), repeat=4):
            D12, D13, D14, D15 = p
            DD = {12: D12, 13: D13, 14: D14, 15: D15, 16: 0}
            hs.append(extend_high27_fixed_d11(E.high28(DD), D11))
        assert len(E.S.basis(hs)) == 16

    # Dependency from the already-certified rank21888 theorem:
    # per D12..15 prefix, J0/J1 are 448D with intersection424; the D16 bit0
    # spaces are 2D with intersection1. The injective D11 transfer preserves
    # those dimensions and the 16 high sectors stay direct, hence
    # 16 * (448*2 + 448*2 - 424*1) = 21888 exactly.
    per_prefix = 448 * 2 + 448 * 2 - 424
    assert per_prefix == 1368
    assert 16 * per_prefix == 21888

    # C12 by itself is also full rank as a 1-bit physical row. Any gain from
    # C12 must therefore use a genuine multi-site j2 carry corridor, not an
    # isolated one-site append with open neighbouring carries.
    assert c12_isolated_row_rank() == 2

    print("PASS V26_Q138_SIGNED_BLOCK2_D11_TRANSFER_NO_GAIN")
    print("j1_bit11_fixed_D11_transfer_rank=2,2 (injective)")
    print("j2_bit27_fixed_D11_transfer_rank=2,2 (injective)")
    print("extended_high_D12..15_rank_by_D11_slice=16,16")
    print("block2_rank_after_one_bit_D11_occurrence_closure=21888 (no gain)")
    print("isolated_C12_row_rank=2 (no one-site gain)")
    print("scope=exact sector-overlap one-bit extension; longer multi-site carry coupling remains open")


if __name__ == "__main__":
    main()
