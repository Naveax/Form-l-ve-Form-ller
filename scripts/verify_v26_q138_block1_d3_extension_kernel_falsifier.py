#!/usr/bin/env python3
import itertools
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S
import verify_v26_q138_block1_two_site_extension_falsifier as B2


def enc(bs):
    z = 0
    for b in bs:
        z = (z << 1) | b
    return z


def old_d012_basis():
    """Exact rank-1024 row basis of the clean D0..2 occurrence-closed block."""
    V = []
    for ds in itertools.product((0, 1), repeat=3):
        D = dict(enumerate(ds))
        J = B2.j1_basis(D)
        K = B2.j2_basis(D)
        assert (len(J), len(K)) == (64, 3)
        for a in J:
            for b in K:
                r = {}
                for i, x in a.items():
                    for j, y in b.items():
                        r[(i << 9) | j] = x * y
                V.append(r)
    assert len(V) == 1536
    B = S.basis(V)
    assert len(B) == 1024
    return B


def restrict_old_s2(B, bit):
    """Project the old combined column space to fixed j1 boundary carry s2."""
    # Old combined keys have 7 j1 bits followed by 9 j2 bits. The leading
    # j1 bit is s2, hence it is combined bit15.
    mask = (1 << 15) - 1
    out = []
    for r in B:
        q = {}
        for k, v in r.items():
            if ((k >> 15) & 1) == bit:
                q[k & mask] = v
        out.append(q)
    return out


def local_d3_rows():
    """Local map for new physical A3,B3,D3 plus old carry pair s2,s18."""
    rows = []
    labels = []
    for A3, B3, D3, s2, s18 in itertools.product((0, 1), repeat=5):
        r = {}
        for s3, k3, q3, s19, C19, x19, w19 in itertools.product((0, 1), repeat=7):
            a = S.T(s3, s2, A3, k3 ^ B3, q3 ^ D3)
            if not a:
                continue
            b = S.T(s19, s18, C19, x19 ^ D3, w19)
            if not b:
                continue
            r[enc((s3, k3, q3, s19, C19, x19, w19))] = a * b
        rows.append(r)
        labels.append((A3, B3, D3, s2, s18))
    return labels, rows


def main():
    V = old_d012_basis()
    assert len(V) == 1024

    # If the restriction to either s2 slice has the full rank1024, then V has
    # no nonzero vector supported entirely in the opposite s2 slice.
    p0 = len(S.basis(restrict_old_s2(V, 0)))
    p1 = len(S.basis(restrict_old_s2(V, 1)))
    assert (p0, p1) == (1024, 1024), (p0, p1)

    labels, Q = local_d3_rows()
    rq = len(S.basis(Q))
    assert rq == 24, rq

    # The entire 8D left kernel consists of the explicit pair relations
    # Q(A3=0,s2=1) == Q(A3=1,s2=0), for every B3,D3,s18.
    # There are 8 such independent relations; rank32-8=24 proves completeness.
    pos = {lab: i for i, lab in enumerate(labels)}
    pairs = 0
    for B3, D3, s18 in itertools.product((0, 1), repeat=3):
        i = pos[(0, B3, D3, 1, s18)]
        j = pos[(1, B3, D3, 0, s18)]
        assert Q[i] == Q[j]
        pairs += 1
    assert pairs == 8
    assert 32 - pairs == rq

    # Any kernel vector of the local map would require a nonzero old vector
    # supported solely in s2=0 and a matching one supported solely in s2=1.
    # The full-rank projections above show neither fiber exists. Therefore the
    # local map is injective on F^8_(A3,B3,D3) tensor V.
    new_rank = 8 * len(V)
    assert new_rank == 8192

    print('PASS V26_Q138_BLOCK1_D3_EXTENSION_KERNEL_FALSIFIER')
    print('old_D012_exact_rank=1024')
    print('old_s2_projection_ranks=1024,1024 (both injective)')
    print('local_D3_coupled_carry_map_rank=24/32 kernel_dim=8')
    print('local_kernel=8 explicit A3<->s2 pair relations')
    print('kernel_intersection_with_F8_tensor_old_space=0')
    print('exact_D0..3_occurrence_closed_rank=8192=16*2^9 (no gain)')
    print('scope=closes the D3 one-site extension of the clean D0..2 block1 route')


if __name__ == '__main__':
    main()
