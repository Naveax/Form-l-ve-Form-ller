#!/usr/bin/env python3

BUDGET = 1 << 44

# Current admitted single-leaf dyadic envelopes after the clean B/C
# second-integer-lift certificate merged in PR #117.
# This verifier certifies exact four-sequence convolution arithmetic only.
A = [1, 41, 564, 1761] + [2048] * 12
B = [36, 748] + [2048] * 14
C = [84, 916] + [2048] * 14
D = [1, 20, 173, 838, 1958] + [2048] * 11


def conv4_layer(k: int) -> int:
    total = 0
    for i in range(k + 1):
        for j in range(k - i + 1):
            for q in range(k - i - j + 1):
                r = k - i - j - q
                total += A[i] * B[j] * C[q] * D[r]
    return total


def main() -> None:
    layers = [conv4_layer(k) for k in range(10)]
    expected = [
        3_024,
        280_272,
        11_483_584,
        273_032_624,
        4_207_035_504,
        44_830_527_280,
        344_669_648_352,
        1_964_027_333_680,
        8_456_851_951_776,
        28_140_806_593_696,
    ]
    assert layers == expected, (layers, expected)

    total_k0_k8 = sum(layers[:9])
    margin_after_k8 = BUDGET - total_k0_k8
    cumulative_k0_k9 = total_k0_k8 + layers[9]
    k9_deficit = cumulative_k0_k9 - BUDGET

    assert total_k0_k8 == 10_814_871_296_096
    assert margin_after_k8 == 6_777_314_748_320
    assert layers[9] == 28_140_806_593_696
    assert cumulative_k0_k9 == 38_955_677_889_792
    assert k9_deficit == 21_363_491_845_376

    # Immediate predecessor: B1<=748, C1<=936.
    prev_total_k0_k8 = 10_938_830_935_616
    prev_margin_after_k8 = 6_653_355_108_800
    prev_k9_layer = 28_420_855_930_176
    prev_cumulative_k0_k9 = 39_359_686_865_792
    prev_k9_deficit = 21_767_500_821_376

    assert prev_total_k0_k8 - total_k0_k8 == 123_959_639_520
    assert margin_after_k8 - prev_margin_after_k8 == 123_959_639_520
    assert prev_k9_layer - layers[9] == 280_049_336_480
    assert prev_cumulative_k0_k9 - cumulative_k0_k9 == 404_008_976_000
    assert prev_k9_deficit - k9_deficit == 404_008_976_000

    # Older B1<=812, C1<=972 table retained as a second consistency check.
    old_total_k0_k8 = 11_651_939_386_272
    old_k9_layer = 29_952_328_904_800
    old_cumulative_k0_k9 = 41_604_268_291_072
    old_k9_deficit = 24_012_082_246_656

    assert old_total_k0_k8 - total_k0_k8 == 837_068_090_176
    assert old_k9_layer - layers[9] == 1_811_522_311_104
    assert old_cumulative_k0_k9 - cumulative_k0_k9 == 2_648_590_401_280
    assert old_k9_deficit - k9_deficit == 2_648_590_401_280

    assert total_k0_k8 < BUDGET
    assert cumulative_k0_k9 > BUDGET
    assert layers[9] > margin_after_k8

    print('leaf_envelopes', {'A': A[:6], 'B': B[:6], 'C': C[:6], 'D': D[:6]})
    print('layers_k0_k9', layers)
    print('sum_k0_k8', total_k0_k8)
    print('budget_2^44', BUDGET)
    print('margin_after_k8', margin_after_k8)
    print('k9_layer', layers[9])
    print('cumulative_k0_k9', cumulative_k0_k9)
    print('k9_deficit', k9_deficit)
    print('improvement_vs_748_936_k0_k8', prev_total_k0_k8 - total_k0_k8)
    print('improvement_vs_748_936_k9_layer', prev_k9_layer - layers[9])
    print('improvement_vs_748_936_cumulative_k0_k9', prev_cumulative_k0_k9 - cumulative_k0_k9)
    print('PASS V26_Q138_BC748_916_K9_CONVOLUTION')
    print('scope=exact convolution of admitted leaf envelopes after B1<=748,C1<=916; k8 passes with larger margin; k9 still fails; arithmetic-only')
    print('not_included=complete dyadic tail, W_repr improvement, arithmetic-work theorem, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
