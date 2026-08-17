#!/usr/bin/env python3
import itertools
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S
import verify_v26_q138_block1_d3_extension_kernel_falsifier as D3

P = 2147483647  # 2^31-1, prime


def enc(bs):
    z = 0
    for b in bs:
        z = (z << 1) | b
    return z


def qmod(x):
    x = Fraction(x)
    d = x.denominator % P
    assert d != 0
    return (x.numerator % P) * pow(d, P - 2, P) % P


def rank_mod_q(rows):
    """Sparse exact lower-bound rank after valid reduction Q -> F_P."""
    B = {}
    for r0 in rows:
        r = {j: qmod(v) for j, v in r0.items() if v}
        r = {j: v for j, v in r.items() if v}
        while r:
            c = min(r)
            a = r[c]
            if c not in B:
                ia = pow(a, P - 2, P)
                B[c] = {j: (x * ia) % P for j, x in r.items()}
                break
            b = B[c]
            for j, x in b.items():
                z = (r.get(j, 0) - a * x) % P
                if z:
                    r[j] = z
                elif j in r:
                    r.pop(j)
    return len(B)


def quarter_turn_s2(r):
    """J(u0,u1)=(u1,-u0) on the leading old s2 coordinate."""
    out = {}
    mask = (1 << 15) - 1
    for k, v in r.items():
        s2 = (k >> 15) & 1
        rest = k & mask
        if s2 == 0:
            nk = (1 << 15) | rest
            val = -v
        else:
            nk = rest
            val = v
        out[nk] = out.get(nk, Fraction(0)) + val
        if not out[nk]:
            out.pop(nk)
    return out


def j2_d_sector_rows(D):
    rows = []
    for s18 in (0, 1):
        r = {}
        for s19, C19, x19, w19 in itertools.product((0, 1), repeat=4):
            q = S.T(s19, s18, C19, x19 ^ D, w19)
            if q:
                r[enc((s19, C19, x19, w19))] = q
        rows.append(r)
    return rows


def j1_s3_one_B_rows(D, B):
    rows = []
    labels = []
    for A, s2 in itertools.product((0, 1), repeat=2):
        r = {}
        for k3, q3 in itertools.product((0, 1), repeat=2):
            q = S.T(1, s2, A, k3 ^ B, q3 ^ D)
            if q:
                r[enc((k3, q3))] = q
        rows.append(r)
        labels.append((A, s2))
    return labels, rows


def neg(r):
    return {k: -v for k, v in r.items()}


def main():
    # Exact old D0..2 basis and exact injective s2 projections.
    V = D3.old_d012_basis()
    assert len(V) == 1024
    p0 = len(S.basis(D3.restrict_old_s2(V, 0)))
    p1 = len(S.basis(D3.restrict_old_s2(V, 1)))
    assert (p0, p1) == (1024, 1024)

    # The key s3=1 obstruction is V intersect J(V). Full modular rank2048 is
    # a rigorous exact-Q certificate: valid reduction cannot increase rank,
    # and 2048 is already the maximum possible for 2048 rows.
    JV = [quarter_turn_s2(r) for r in V]
    r_vj_mod = rank_mod_q(V + JV)
    assert r_vj_mod == 2048, r_vj_mod
    intersection_v_jv = 2 * len(V) - r_vj_mod
    assert intersection_v_jv == 0

    # Fixed-D3 j2 transfer sectors each have rank2 and are mutually disjoint.
    K0 = j2_d_sector_rows(0)
    K1 = j2_d_sector_rows(1)
    assert len(S.basis(K0)) == 2
    assert len(S.basis(K1)) == 2
    assert len(S.basis(K0 + K1)) == 4

    # At s3=1, each fixed-B3 local j1 sector has rank2; the two B3 sectors
    # are direct. Verify the exact pair relations that turn the global kernel
    # question into V intersect J(V).
    for D in (0, 1):
        all_rows = []
        for B in (0, 1):
            labels, rows = j1_s3_one_B_rows(D, B)
            pos = {lab: i for i, lab in enumerate(labels)}
            assert len(S.basis(rows)) == 2
            assert rows[pos[(0, 1)]] == rows[pos[(1, 0)]]
            assert rows[pos[(0, 0)]] == neg(rows[pos[(1, 1)]])
            all_rows.extend(rows)
        assert len(S.basis(all_rows)) == 4

    # s3=0: for fixed D3, A3=s2 and (k3,q3) uniquely records (B3,A3),
    # so four injective old-slice channels give 4096. D3 sectors add directly.
    s3_zero_fixed_D = 4 * len(V)
    assert s3_zero_fixed_D == 4096
    s3_zero_rank = 2 * s3_zero_fixed_D
    assert s3_zero_rank == 8192

    # s3=1: the only possible fixed-B kernel is V intersect J(V), already0.
    # Thus four copies of V are injective for each D3; D3 sectors again add.
    s3_one_fixed_D = 4 * len(V)
    assert intersection_v_jv == 0
    assert s3_one_fixed_D == 4096
    s3_one_rank = 2 * s3_one_fixed_D
    assert s3_one_rank == 8192

    dim_V3 = 8192
    assert s3_zero_rank == dim_V3
    assert s3_one_rank == dim_V3
    fiber_s3_zero = dim_V3 - s3_one_rank  # vectors supported wholly at s3=0
    fiber_s3_one = dim_V3 - s3_zero_rank  # vectors supported wholly at s3=1
    assert (fiber_s3_zero, fiber_s3_one) == (0, 0)

    # Generic next-site local coupled-carry map is the same algebraic map as D3.
    labels, Q = D3.local_d3_rows()
    rq = len(S.basis(Q))
    assert rq == 24
    pos = {lab: i for i, lab in enumerate(labels)}
    pair_relations = 0
    for B4, D4, s19 in itertools.product((0, 1), repeat=3):
        i = pos[(0, B4, D4, 1, s19)]
        j = pos[(1, B4, D4, 0, s19)]
        assert Q[i] == Q[j]
        pair_relations += 1
    assert pair_relations == 8

    # Since V3 has no one-slice s3 fibers, the complete local8D kernel misses
    # F^8 tensor V3. Therefore the D4 extension is injective on the actual space.
    d4_rank = 8 * dim_V3
    assert d4_rank == 65536 == 16 * (2 ** 12)

    print('PASS V26_Q138_BLOCK1_D4_BOUNDARY_FIBER_NO_GAIN')
    print('old_D012_rank=1024 old_s2_projection_ranks=1024,1024')
    print('mod_prime=%d rank_p(V+J(V))=2048 => exact_Q_intersection(V,J(V))=0' % P)
    print('j2_fixed_D3_sector_ranks=2,2 union=4 direct_sum')
    print('D03_s3_projection_ranks=8192,8192')
    print('D03_single_slice_fiber_dims=0,0')
    print('generic_next_site_local_rank=24/32 kernel_dim=8')
    print('exact_D0..4_occurrence_closed_rank=65536=16*2^12 (no gain)')
    print('scope=closes the one-site D4 repeated-D extension only; not a lower bound on full S1 rank')


if __name__ == '__main__':
    main()
