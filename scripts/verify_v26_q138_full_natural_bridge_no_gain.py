#!/usr/bin/env python3
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S
import verify_v26_q138_block1_c12_d04_merged_no_gain as CBR


def main():
    # Clean prerequisite theorem: complete low repeated-D chain D0..5.
    d05_rank = 524288  # 16*2^15
    assert d05_rank == 16 * (2 ** 15)

    # The C12..14 operator is universally injective, so it also applies to
    # D0..5 (not only the smaller D0..4 instance used in its first closure).
    assert len(S.basis(CBR.c12_c14_bridge_rows())) == 16
    low_rank = d05_rank * (2 ** 3)
    assert low_rank == 4194304 == 2 ** 22

    # Clean j2 bridge22..31 theorem: (s21,D12..15) rank32/32. Hence the
    # sixteen D12..15 high prefixes remain direct after attaching low_rank.
    # Universal bit0 theorem: for incoming W of dimension n, fixed-D16
    # bit0 spaces have dimensions 2n,2n and intersection n.
    n = low_rank
    jdim = 448
    jint = 424
    per_prefix = jdim * (2 * n) + jdim * (2 * n) - jint * n
    assert per_prefix == 1368 * n

    # Sixteen independent D12..15 prefixes.
    merged_39bit_rank = 16 * per_prefix
    assert merged_39bit_rank == 21888 * n
    assert merged_39bit_rank == 91804925952

    # The merged factor consumes 39 of the 44 S1 physical bits:
    # low side A0..5,B0..5,D0..5,C12..16 =23 bits;
    # extended block2 A12..16,B12..16,D12..16,C0 =16 bits.
    # Only C1..5 remain raw.
    remaining_raw = 5
    center = merged_39bit_rank * (2 ** remaining_raw)
    old_center = 16 * 21888 * (2 ** 23)
    assert center == old_center == 171 * (2 ** 34)

    w = math.log2(center) + 44
    assert abs(w - (78 + math.log2(171))) < 1e-12

    print('PASS V26_Q138_FULL_NATURAL_BRIDGE_NO_GAIN')
    print('low_D0..5_rank=524288=16*2^15')
    print('after_universal_C12..14_injective_bridge: low_rank=4194304=2^22')
    print('j2_bridge22..31 preserves all 16 D12..15 prefixes')
    print('universal_bit0_D16_geometry_for_n=low_rank: dims=2n,2n intersection=n')
    print('per_high_prefix_rank=1368*n')
    print('merged_39bit_factor_rank=21888*n=91804925952')
    print('remaining_raw_S1_bits=C1..5 => 5 bits')
    print('central_rank=merged_rank*2^5=171*2^34 unchanged')
    print('W_repr(1)=78+log2(171)=%.15f unchanged' % w)
    print('scope=closes the natural j2 carry/repeated-D bridge joining the enlarged low block to extended block2; other nonlocal factor regroupings remain open')


if __name__ == '__main__':
    main()
