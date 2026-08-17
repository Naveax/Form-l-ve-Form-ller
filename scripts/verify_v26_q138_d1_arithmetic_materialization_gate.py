#!/usr/bin/env python3
import math


def main():
    n = 2 ** 22

    # Per fixed D12..15 prefix, exact D16 tensor-sector geometry.
    j = 448
    j_inter = 424
    k = 64 * n
    k_inter = 63 * n

    common = j_inter * k_inter
    sector_total = j * k
    private_each = sector_total - common
    union = common + 2 * private_each

    assert common == 26712 * n
    assert private_each == 1960 * n
    assert union == 30632 * n
    assert union == j * k + j * k - j_inter * k_inter

    center = 16 * union
    assert center == 3829 * (2 ** 29)

    # Any method that explicitly materializes the coefficient-aware factor on
    # the four predecessor-leaf S1 coordinates must emit one scalar for each
    # rank-channel x 2^44 leaf assignment. This is an output-size lower bound
    # on scalar writes, independent of how cleverly entries are generated.
    factor_entries = center * (2 ** 44)
    assert factor_entries == 3829 * (2 ** 73)
    W = math.log2(factor_entries)
    assert abs(W - (73 + math.log2(3829))) < 1e-12

    separate_sector_channels = 2 * sector_total
    overlap_aware_channels = union
    formal_channel_reuse = separate_sector_channels / overlap_aware_channels
    assert formal_channel_reuse > 1

    common_fraction = common / union

    print('PASS V26_Q138_D1_ARITHMETIC_MATERIALIZATION_GATE')
    print('per_prefix_common_channels=26712*n')
    print('per_prefix_D16_private_channels=1960*n each')
    print('per_prefix_union=30632*n')
    print('common_fraction=%.15f' % common_fraction)
    print('separate_vs_overlap_aware_channel_ratio=%.15f' % formal_channel_reuse)
    print('full_center_rank=3829*2^29')
    print('explicit_factor_output_entries=3829*2^73=%d' % factor_entries)
    print('explicit_factor_output_log2=%.15f' % W)
    print('scope=arithmetic lower bound for explicit materialization only; scalar-on-the-fly contraction may avoid this output and remains open')


if __name__ == '__main__':
    main()
