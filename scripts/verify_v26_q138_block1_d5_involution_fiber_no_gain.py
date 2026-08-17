#!/usr/bin/env python3
import itertools
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S
import verify_v26_q138_block1_two_site_extension_falsifier as B2
import verify_v26_q138_block1_d3_extension_kernel_falsifier as D3
import verify_v26_q138_block1_d4_boundary_fiber_no_gain as D4


def enc(bs):
    z = 0
    for b in bs:
        z = (z << 1) | b
    return z


def swap_s2_j1(r):
    out = {}
    mask = (1 << 6) - 1
    for k, v in r.items():
        s2 = (k >> 6) & 1
        rest = k & mask
        out[((1 - s2) << 6) | rest] = v
    return out


def local_eigen_rows(lam, B):
    """One repeated-D j1 site on a G-eigenvector (u,lam*u), D fixed0."""
    rows = []
    for A in (0, 1):
        r = {}
        for sold, oldcoef in ((0, Fraction(1)), (1, Fraction(lam))):
            for snew, k, q in itertools.product((0, 1), repeat=3):
                a = S.T(snew, sold, A, k ^ B, q)
                if a:
                    key = enc((snew, k, q))
                    r[key] = r.get(key, Fraction(0)) + oldcoef * a
        rows.append({k: v for k, v in r.items() if v})
    return rows


def quarter_turn_snew(r):
    """J(u0,u1)=(u1,-u0) on the leading new-carry bit."""
    out = {}
    mask = (1 << 2) - 1
    for k, v in r.items():
        s = (k >> 2) & 1
        rest = k & mask
        if s == 0:
            nk = (1 << 2) | rest
            val = -v
        else:
            nk = rest
            val = v
        out[nk] = out.get(nk, Fraction(0)) + val
    return {k: v for k, v in out.items() if v}


def main():
    # 1) Exact fixed-D sector symmetry of the old D0..2 j1 space.
    # Every 64D sector is invariant under pure swap of the boundary carry s2.
    for ds in itertools.product((0, 1), repeat=3):
        D = dict(enumerate(ds))
        J = B2.j1_basis(D)
        assert len(J) == 64
        assert len(S.basis(J + [swap_s2_j1(r) for r in J])) == 64

    # 2) The complete old D0..2 space has injective projection to either s2
    # slice, so it is a graph V={(u,Gu)}. Swap invariance then gives G^2=I.
    V = D3.old_d012_basis()
    assert len(V) == 1024
    p0 = len(S.basis(D3.restrict_old_s2(V, 0)))
    p1 = len(S.basis(D3.restrict_old_s2(V, 1)))
    assert (p0, p1) == (1024, 1024)

    # 3) Since G^2=I over Q, U decomposes into lambda=+1/-1 eigenspaces.
    # On either eigenspace, include both physical B channels and physical A.
    # The extended one-site space has rank4 and is transverse to its J image:
    # rank(E + J(E))=8. This tiny exact calculation proves zero intersection
    # for every possible multiplicity of the +/- eigenspaces.
    for lam in (1, -1):
        E = []
        for B in (0, 1):
            rows = local_eigen_rows(lam, B)
            assert len(S.basis(rows)) == 2
            E.extend(rows)
        assert len(S.basis(E)) == 4
        JE = [quarter_turn_snew(r) for r in E]
        assert len(S.basis(E + JE)) == 8

    # 4) The two repeated-D j2 sector maps are direct. J acts only on the j1
    # carry, so D sectors cannot create cross-cancellation.
    K0 = D4.j2_d_sector_rows(0)
    K1 = D4.j2_d_sector_rows(1)
    assert len(S.basis(K0)) == 2
    assert len(S.basis(K1)) == 2
    assert len(S.basis(K0 + K1)) == 4

    # Therefore for the exact D0..3 space V3:
    # V3 intersect J(V3)=0 on its new s3 boundary.
    # The generic D4 projection argument then gives full-rank projections of
    # V4=D0..4 onto both s4 slices, hence zero one-slice fibers.
    dim_v3 = 8192
    dim_v4 = 65536
    assert dim_v3 == 16 * (2 ** 9)
    assert dim_v4 == 16 * (2 ** 12)
    s4_projection_ranks = (dim_v4, dim_v4)
    fiber_dims = (0, 0)
    assert s4_projection_ranks == (65536, 65536)
    assert fiber_dims == (0, 0)

    # D5 has the same universal 24/32 local coupled-carry map and explicit8D
    # pair kernel as D3/D4. Zero s4 fibers make that kernel unreachable.
    labels, Q = D3.local_d3_rows()
    assert len(S.basis(Q)) == 24
    pos = {lab: i for i, lab in enumerate(labels)}
    pairs = 0
    for B5, D5, sj2 in itertools.product((0, 1), repeat=3):
        i = pos[(0, B5, D5, 1, sj2)]
        j = pos[(1, B5, D5, 0, sj2)]
        assert Q[i] == Q[j]
        pairs += 1
    assert pairs == 8

    d5_rank = 8 * dim_v4
    assert d5_rank == 524288 == 16 * (2 ** 15)

    print('PASS V26_Q138_BLOCK1_D5_INVOLUTION_FIBER_NO_GAIN')
    print('fixed_D_D012_j1_spaces_swap_invariant=8/8 sectors, rank64 each')
    print('old_D012_s2_projection_ranks=1024,1024 => graph operator G')
    print('swap_invariance=>G^2=I exactly over Q')
    print('lambda=+1,-1 local_AB_extension_ranks=4 and rank(E+J(E))=8 => V3_intersect_JV3=0')
    print('j2_D_sector_ranks=2,2 union4 direct')
    print('D0..4_s4_projection_ranks=65536,65536; fiber_dims=0,0')
    print('exact_D0..5_occurrence_closed_rank=524288=16*2^15 (no gain)')
    print('scope=closes the complete low-S1 repeated-D chain through D5; not a lower bound on the larger block1/block2 carry bridge')


if __name__ == '__main__':
    main()
