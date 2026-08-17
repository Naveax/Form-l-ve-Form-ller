#!/usr/bin/env python3
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S


def main():
    # Complete low occurrence-closed block:
    # rank(D0..5)=16*2^15=2^19 and the universal physical C12..14 bridge
    # contributes exactly 2^3, so n=2^22 on 23 physical S1 row bits.
    n = 2 ** 22
    assert 16 * (2 ** 15) * (2 ** 3) == n

    # New exact local bit0+gap theorem, universally lifted through the low W:
    # fixed D16 spaces 64n each, intersection63n.
    local0 = 64 * n
    local1 = 64 * n
    local_inter = 63 * n

    # Certified extended-block2 j1 D16 geometry for every fixed D12..15 prefix.
    j0 = j1 = 448
    jinter = 424

    # The j1 and local/high retained coordinate groups are disjoint once the
    # physical D sector is fixed, so the two D16 tensor-product sector spaces
    # intersect in the tensor product of their intersections.
    per_prefix = j0 * local0 + j1 * local1 - jinter * local_inter
    assert per_prefix == 30632 * n

    # Clean j2 bridge22..31 theorem keeps all 16 D12..15 prefixes direct.
    center = 16 * per_prefix
    assert center == 3829 * (2 ** 29)
    assert center == 2055678722048

    # Physical row accounting: all44 S1 bits are now inside the merged factor.
    low = ({f'A{i}' for i in range(6)} |
           {f'B{i}' for i in range(6)} |
           {f'D{i}' for i in range(6)} |
           {f'C{i}' for i in range(12, 17)})
    high = ({f'A{i}' for i in range(12, 17)} |
            {f'B{i}' for i in range(12, 17)} |
            {f'D{i}' for i in range(12, 17)} |
            {f'C{i}' for i in range(6)})
    assert len(low) == 23 and len(high) == 21
    assert low.isdisjoint(high)
    assert len(low | high) == 44

    # Compare to previous center 171*2^34 = (1368*32)*16*n.
    old_center = 171 * (2 ** 34)
    assert old_center == 16 * (1368 * 32) * n
    assert old_center > center
    gain = old_center / center
    assert abs(gain - (5472 / 3829)) < 1e-15

    # Recount the complete frozen HT tree. S1 receives the new center rank;
    # S2 keeps 31*2^35. Every other node uses the existing generic envelope.
    leaf_exp = 44
    s1_dim = center * (2 ** leaf_exp)
    assert s1_dim == 3829 * (2 ** 73)
    s2_dim = 31 * (2 ** 79)
    comp1 = frozenset(set(range(32)) - set(S.S1))
    comp2 = frozenset(set(range(32)) - set(S.S2))

    def dim(A):
        F = frozenset(A)
        if F in (S.S1, comp1):
            return s1_dim
        if F in (S.S2, comp2):
            return s2_dim
        return S.generic_dim(F)

    vals = [dim(A) for A in S.nodes()]
    mx = max(vals)
    assert mx == s1_dim
    assert s2_dim < s1_dim
    assert max(S.generic_dim(A) for A in S.nodes()) == 2 ** 88  # old fully generic baseline
    # Noncritical nodes on the frozen tree remain below the new S1 value by
    # the same signed85 node accounting; explicitly exclude the two critical pairs.
    noncritical = []
    for A in S.nodes():
        F = frozenset(A)
        if F not in (S.S1, comp1, S.S2, comp2):
            noncritical.append(S.generic_dim(F))
    assert max(noncritical) <= 2 ** 80

    W = math.log2(s1_dim)
    expected = 73 + math.log2(3829)
    assert abs(W - expected) < 1e-12
    oldW = 78 + math.log2(171)
    assert oldW > W

    print('PASS V26_Q138_FULL_S1_GAP_RANK3829')
    print('low_23bit_rank=n=2^22')
    print('bit0_gap_D16_local_geometry=64n,64n intersection63n')
    print('j1_D16_geometry=448,448 intersection424')
    print('per_D12..15_prefix_rank=30632*n')
    print('sixteen_high_prefixes_direct')
    print('new_S1_center_rank=3829*2^29=%d' % center)
    print('old_center_rank=171*2^34=%d' % old_center)
    print('exact_center_gain=5472/3829=%.15f' % gain)
    print('all_44_S1_physical_bits_consumed; raw_bits=0')
    print('new_factor_dimension=3829*2^73')
    print('W_repr(1)<=73+log2(3829)=%.15f' % W)
    print('improvement_bits=%.15f' % (oldW - W))
    print('complete_frozen_HT_tree_recount=S1 remains controlling node')
    print('scope=exact representation existence only; coefficient-aware factor-generation and arithmetic-work ledgers are NOT lowered here')


if __name__ == '__main__':
    main()
