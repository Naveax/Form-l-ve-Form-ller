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
    C = [[Fraction(0) for _ in range(len(B[0]))] for __ in range(len(A))]
    for i in range(len(A)):
        for k, a in enumerate(A[i]):
            if not a:
                continue
            for j, b in enumerate(B[k]):
                if b:
                    C[i][j] += a * b
    return C


def matpow(A, n):
    R = [[Fraction(int(i == j)) for j in range(len(A))] for i in range(len(A))]
    B = A
    while n:
        if n & 1:
            R = matmul(R, B)
        B = matmul(B, B)
        n >>= 1
    return R


def physical_c_pair_transfer(C, Cp):
    """Paired-carry Gram transfer for one physical C row bit.

    The two row copies have fixed C,C'. Retained v,w are shared and summed.
    Matrix indices are paired lower carry (t,t') -> higher carry (s,s').
    """
    M = [[Fraction(0) for _ in range(4)] for __ in range(4)]
    for t, tp, s, sp in itertools.product((0, 1), repeat=4):
        z = Fraction(0)
        for v, w in itertools.product((0, 1), repeat=2):
            z += S.T(s, t, C, v, w) * S.T(sp, tp, Cp, v, w)
        M[idx(t, tp)][idx(s, sp)] = z
    return M


def retained_c_pair_transfer():
    """Paired-carry Gram transfer when C,v,w are all retained columns."""
    M = [[Fraction(0) for _ in range(4)] for __ in range(4)]
    for t, tp, s, sp in itertools.product((0, 1), repeat=4):
        z = Fraction(0)
        for C, v, w in itertools.product((0, 1), repeat=3):
            z += S.T(s, t, C, v, w) * S.T(sp, tp, C, v, w)
        M[idx(t, tp)][idx(s, sp)] = z
    return M


def gram_matrix():
    """Exact M M^T for the complete j2 bits1..11 gap operator.

    Rows of M are (C1..C5,s0,s11), dimension128.
    Columns are all shared retained variables:
      bits1..5:  (v_i,w_i), 10 bits;
      bits6..11: (C_i,v_i,w_i), 18 bits.
    Thus M has 2^28 implicit columns. The Gram DP never materializes them.
    """
    P = {(C, Cp): physical_c_pair_transfer(C, Cp)
         for C, Cp in itertools.product((0, 1), repeat=2)}
    R6 = matpow(retained_c_pair_transfer(), 6)

    labels = []
    for Cs in itertools.product((0, 1), repeat=5):
        for s0, s11 in itertools.product((0, 1), repeat=2):
            labels.append((Cs, s0, s11))
    assert len(labels) == 128

    # Product transfer for every pair of five-bit physical C strings.
    paths = {}
    I = [[Fraction(int(i == j)) for j in range(4)] for i in range(4)]
    for Cs in itertools.product((0, 1), repeat=5):
        for Csp in itertools.product((0, 1), repeat=5):
            A = I
            for C, Cp in zip(Cs, Csp):
                A = matmul(A, P[(C, Cp)])
            paths[(Cs, Csp)] = matmul(A, R6)

    G = []
    for Cs, s0, s11 in labels:
        row = []
        for Csp, s0p, s11p in labels:
            row.append(paths[(Cs, Csp)][idx(s0, s0p)][idx(s11, s11p)])
        G.append(row)
    return G


def main():
    G = gram_matrix()
    assert len(G) == 128 and all(len(r) == 128 for r in G)

    # Over Q (equivalently R), rank(M M^T)=rank(M). Exact Fraction Gaussian
    # elimination therefore certifies the full 2^28-column operator rank.
    sparse_rows = [{j: x for j, x in enumerate(row) if x} for row in G]
    r = len(S.basis(sparse_rows))
    assert r == 66, r

    print('PASS V26_Q138_J2_GAP1_11_RANK66')
    print('gap_rows=(C1..C5,s0,s11) dimension=128')
    print('implicit_retained_columns=2^28')
    print('paired_carry_Gram_state_dimension=4')
    print('exact_Gram_rank=66')
    print('exact_gap_operator_rank=66/128 kernel_dim=62')
    print('scope=local carry-gap interface rank only; does NOT by itself lower the central S1 rank until the incoming 39-bit boundary space is intersected with this kernel')


if __name__ == '__main__':
    main()
