#!/usr/bin/env python3
from fractions import Fraction
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S

P = 65521
WITNESS_COLUMNS = [
    1158378339, 230309692, 2851524784, 3281825644,
    3529366735, 3868809751, 1623810251, 3591101243,
    1707518819, 1805191980, 3566883771, 1726839468,
    2079119511, 3671210287, 3137574220, 1529516187,
    441890803, 978703611, 2325764495, 248965911,
    1727881456, 3510200051, 2616017823, 116132656,
    2334969100, 801139136, 3696962032, 3501473116,
    3721048172, 2648395712, 1259945216, 1795025664,
]


def qmod(x):
    x = Fraction(x)
    d = x.denominator % P
    assert d != 0
    return (x.numerator % P) * pow(d, P - 2, P) % P


def bits32(z):
    return tuple((z >> (31 - i)) & 1 for i in range(32))


def bridge_entry(s21, prefix, col):
    """Exact coefficient for one retained-column witness.

    Bits22..27 keep (C_i,x_i,D_{i-16},w_i) as retained columns.
    Bits28..31 keep (C_i,w_i); physical D12..15 are in `prefix`.
    Internal carries are deterministic from the T parity equation. Terminal
    carry s32 is fixed0.
    """
    b = bits32(col)
    pos = 0
    gap = []
    for _ in range(6):
        C, x, Dcol, w = b[pos:pos + 4]
        pos += 4
        gap.append((C, x, Dcol, w))
    high = []
    for _ in range(4):
        C, w = b[pos:pos + 2]
        pos += 2
        high.append((C, w))
    assert pos == 32

    Dp = tuple((prefix >> (3 - j)) & 1 for j in range(4))
    sold = s21
    coeff = Fraction(1)

    for C, x, Dcol, w in gap:
        v = x ^ Dcol
        snew = sold ^ C ^ v ^ w
        q = S.T(snew, sold, C, v, w)
        if not q:
            return Fraction(0)
        coeff *= q
        sold = snew

    for j, (C, w) in enumerate(high):
        v = Dp[j]
        snew = sold ^ C ^ v ^ w
        q = S.T(snew, sold, C, v, w)
        if not q:
            return Fraction(0)
        coeff *= q
        sold = snew

    return coeff if sold == 0 else Fraction(0)


def rank_mod_dense(M):
    A = [[qmod(x) for x in row] for row in M]
    n = len(A)
    m = len(A[0]) if n else 0
    r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if A[i][c]), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], P - 2, P)
        A[r] = [(x * inv) % P for x in A[r]]
        for i in range(n):
            if i == r or not A[i][c]:
                continue
            a = A[i][c]
            A[i] = [(A[i][j] - a * A[r][j]) % P for j in range(m)]
        r += 1
        if r == n:
            break
    return r


def main():
    assert len(WITNESS_COLUMNS) == 32
    assert len(set(WITNESS_COLUMNS)) == 32

    rows = []
    for s21 in (0, 1):
        for prefix in range(16):
            rows.append([bridge_entry(s21, prefix, c) for c in WITNESS_COLUMNS])

    r = rank_mod_dense(rows)
    assert r == 32, r

    # The full domain is exactly (s21,D12,D13,D14,D15), dimension32. A
    # 32x32 minor of rank32 modulo an odd prime is an exact-Q nonzero minor:
    # all coefficients are dyadic, so reduction modulo P is valid.
    print('PASS V26_Q138_J2_BRIDGE22_31_INJECTIVE')
    print('domain=(s21,D12..15) dimension=32')
    print('retained_witness_columns=32')
    print('mod_prime=%d witness_minor_rank=32' % P)
    print('exact_Q_bridge_rank=32/32 injective')
    print('consequence=D12..15 high prefixes remain direct after attaching the lower s21 carry')
    print('scope=closes rank loss inside j2 bits22..31 only; D16/bit0/shared-v3_12 coupling remains a separate question')


if __name__ == '__main__':
    main()
