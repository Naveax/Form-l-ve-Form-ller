#!/usr/bin/env python3
import itertools
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S


def idx(a, b):
    return (a << 1) | b


def matmul(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), Fraction(0))
             for j in range(len(B[0]))]
            for i in range(len(A))]


def matpow(A, n):
    R = [[Fraction(int(i == j)) for j in range(len(A))] for i in range(len(A))]
    B = A
    while n:
        if n & 1:
            R = matmul(R, B)
        B = matmul(B, B)
        n >>= 1
    return R


def retained_j1_pair_transfer():
    """One j1 site with A,B,D,k,q all retained on the S1 split.

    The actual local inputs are u=A, v=k xor B, w=q xor D. In the Gram
    product the retained assignment is shared between the two row copies.
    """
    M = [[Fraction(0) for _ in range(4)] for __ in range(4)]
    for sold, soldp, snew, snewp in itertools.product((0, 1), repeat=4):
        z = Fraction(0)
        for A, B, D, k, q in itertools.product((0, 1), repeat=5):
            v = k ^ B
            w = q ^ D
            z += S.T(snew, sold, A, v, w) * S.T(snewp, soldp, A, v, w)
        M[idx(sold, soldp)][idx(snew, snewp)] = z
    return M


def endpoint_gram():
    T6 = matpow(retained_j1_pair_transfer(), 6)
    labels = list(itertools.product((0, 1), repeat=2))  # (s5,s11)
    G = []
    for s5, s11 in labels:
        G.append([T6[idx(s5, s5p)][idx(s11, s11p)]
                  for s5p, s11p in labels])
    return G


def main():
    G = endpoint_gram()
    rows = [{j: x for j, x in enumerate(row) if x} for row in G]
    r = len(S.basis(rows))
    assert r == 4, r

    # Normalization-independent display: the actual retained B,D redundancy
    # contributes a common positive scalar. Divide by the first off-diagonal
    # scale convention only for the human-readable matrix statement.
    assert G[0][0] and G[0][3]
    ratio = G[0][0] / G[0][3]
    assert ratio == 64
    assert G[1][1] / G[1][2] == 64

    print('PASS V26_Q138_J1_GAP6_11_INJECTIVE')
    print('rows=(sigma1_5,sigma1_11) dimension=4')
    print('sites6..11: A,B,D,k,q all retained on S1 split')
    print('exact_endpoint_Gram_rank=4/4')
    print('diagonal_to_cross_ratio=64; equivalent normalized Gram has diag32 cross1/2')
    print('consequence=retained-only j1 carry gap is injective and gives no direct reduction below center 3829*2^29')
    print('scope=closes the direct six-site retained j1 carry-gap probe only; other nonlocal retained-coordinate regroupings remain open')


if __name__ == '__main__':
    main()
