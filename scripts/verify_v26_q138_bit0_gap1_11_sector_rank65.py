#!/usr/bin/env python3
import itertools
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S
import verify_v26_q138_j2_gap1_11_rank66 as GAP


def pidx(a, b):
    return (a << 1) | b


def bit0_start(D, C0, Dp, C0p, fixed_v=None):
    """Paired-carry Gram start from the special j2 bit0 tensor."""
    z = [Fraction(0) for _ in range(4)]
    vs = (fixed_v,) if fixed_v is not None else (0, 1)
    for v312 in vs:
        for u40 in (0, 1):
            for s0, s0p in itertools.product((0, 1), repeat=2):
                z[pidx(s0, s0p)] += (
                    S.T0(s0, C0, D, u40 ^ v312)
                    * S.T0(s0p, C0p, Dp, u40 ^ v312)
                )
    return z


def chain_paths():
    P = {(C, Cp): GAP.physical_c_pair_transfer(C, Cp)
         for C, Cp in itertools.product((0, 1), repeat=2)}
    R6 = GAP.matpow(GAP.retained_c_pair_transfer(), 6)
    paths = {}
    I = [[Fraction(int(i == j)) for j in range(4)] for i in range(4)]
    for Cs in itertools.product((0, 1), repeat=5):
        for Csp in itertools.product((0, 1), repeat=5):
            A = I
            for C, Cp in zip(Cs, Csp):
                A = GAP.matmul(A, P[(C, Cp)])
            paths[(Cs, Csp)] = GAP.matmul(A, R6)
    return paths


def labels():
    return [(D,) + Cs for D in (0, 1)
            for Cs in itertools.product((0, 1), repeat=6)]


def gram(paths, fixed_q=None):
    """Exact Gram of rows (D16,C0..C5).

    If fixed_q=(v312,s11), keep that shared retained slice fixed. Otherwise
    sum both retained v312 values and both retained terminal s11 values.
    """
    L = labels()
    G = []
    for rowlab in L:
        D, C0, *tail = rowlab
        tail = tuple(tail)
        row = []
        for collab in L:
            Dp, C0p, *tailp = collab
            tailp = tuple(tailp)
            if fixed_q is None:
                start = bit0_start(D, C0, Dp, C0p)
                ends = (0, 3)  # shared retained s11=0 or1
            else:
                v312, s11 = fixed_q
                start = bit0_start(D, C0, Dp, C0p, fixed_v=v312)
                ends = (pidx(s11, s11),)
            A = paths[(tail, tailp)]
            z = Fraction(0)
            for a in range(4):
                if start[a]:
                    z += start[a] * sum((A[a][e] for e in ends), Fraction(0))
            row.append(z)
        G.append(row)
    return G


def sparse(M):
    return [{j: x for j, x in enumerate(row) if x} for row in M]


def rank(M):
    return len(S.basis(sparse(M)))


def fixed_D_rank(M, D):
    L = labels()
    inds = [i for i, q in enumerate(L) if q[0] == D]
    return rank([[M[i][j] for j in inds] for i in inds])


def main():
    paths = chain_paths()

    G = gram(paths)
    r0 = fixed_D_rank(G, 0)
    r1 = fixed_D_rank(G, 1)
    ru = rank(G)
    assert (r0, r1, ru) == (64, 64, 65), (r0, r1, ru)
    assert r0 + r1 - ru == 63

    # The same 63D left-kernel/sector relation must hold independently of the
    # two shared retained coordinates q=(v3_12,s11). Exact Gram row-space
    # equality is a convenient certificate: for a symmetric Gram matrix its
    # row space is the orthogonal complement of the left kernel.
    fixed = {}
    for q in itertools.product((0, 1), repeat=2):
        Q = gram(paths, fixed_q=q)
        assert fixed_D_rank(Q, 0) == 64
        assert fixed_D_rank(Q, 1) == 64
        assert rank(Q) == 65
        fixed[q] = sparse(Q)

    qs = list(fixed)
    for i in range(len(qs)):
        for j in range(i + 1, len(qs)):
            # rank65 union means the two 65D Gram row spaces are identical,
            # hence the 63D sector kernel is literally the same coefficient
            # subspace in every shared q slice.
            assert len(S.basis(fixed[qs[i]] + fixed[qs[j]])) == 65

    print('PASS V26_Q138_BIT0_GAP1_11_SECTOR_RANK65')
    print('physical_rows=(D16,C0..C5) dimension=128')
    print('fixed_D16_ranks=64,64')
    print('D16_union_rank=65 intersection=63')
    print('for_all_four_fixed_(v3_12,s11)_slices: ranks=64,64 union65')
    print('fixed_q_Gram_row_spaces_identical=>same_63D_sector_kernel')
    print('universal_lift_for_any_incoming_W_on_shared_q: dims=64*n,64*n intersection=63*n')
    print('scope=exact local sector theorem; global S1 improvement requires combination with the certified D16 j1 and high-prefix geometry')


if __name__ == '__main__':
    main()
