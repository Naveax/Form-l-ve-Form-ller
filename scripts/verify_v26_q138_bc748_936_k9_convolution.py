#!/usr/bin/env python3

BUDGET = 1 << 44

# Current admitted single-leaf dyadic envelopes after the clean uniform
# B/C second-residue improvement at main ca1d87ebcd9bb41710e0155031ccc598de8ed3e7.
# This verifier certifies only exact four-sequence convolution arithmetic.
A = [1, 41, 564, 1761] + [2048] * 12
B = [36, 748] + [2048] * 14
C = [84, 936] + [2048] * 14
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
        280_992,
        11_542_464,
        275_107_184,
        4_247_967_584,
        45_333_814_960,
        348_805_355_152,
        1_987_672_008_800,
        8_552_484_855_456,
        28_420_855_930_176,
    ]
    assert layers == expected, (layers, expected)

    total_k0_k8 = sum(layers[:9])
    margin_after_k8 = BUDGET - total_k0_k8
    cumulative_k0_k9 = total_k0_k8 + layers[9]
    k9_deficit = cumulative_k0_k9 - BUDGET

    old_total_k0_k8 = 11_651_939_386_272
    old_margin_after_k8 = 5_940_246_658_144
    old_k9_layer = 29_952_328_904_800
    old_cumulative_k0_k9 = 41_604_268_291_072
    old_k9_deficit = 24_012_082_246_656

    assert total_k0_k8 == 10_938_830_935_616
    assert margin_after_k8 == 6_653_355_108_800
    assert layers[9] == 28_420_855_930_176
    assert cumulative_k0_k9 == 39_359_686_865_792
    assert k9_deficit == 21_767_500_821_376

    assert old_total_k0_k8 - total_k0_k8 == 713_108_450_656
    assert margin_after_k8 - old_margin_after_k8 == 713_108_450_656
    assert old_k9_layer - layers[9] == 1_531_472_974_624
    assert old_cumulative_k0_k9 - cumulative_k0_k9 == 2_244_581_425_280
    assert old_k9_deficit - k9_deficit == 2_244_581_425_280

    assert total_k0_k8 < BUDGET
    assert cumulative_k0_k9 > BUDGET
    assert layers[9] > margin_after_k8

    print("leaf_envelopes", {"A": A[:6], "B": B[:6], "C": C[:6], "D": D[:6]})
    print("layers_k0_k9", layers)
    print("sum_k0_k8", total_k0_k8)
    print("budget_2^44", BUDGET)
    print("margin_after_k8", margin_after_k8)
    print("k9_layer", layers[9])
    print("cumulative_k0_k9", cumulative_k0_k9)
    print("k9_deficit", k9_deficit)
    print("improvement_vs_812_972_k0_k8", old_total_k0_k8 - total_k0_k8)
    print("improvement_vs_812_972_k9_layer", old_k9_layer - layers[9])
    print("improvement_vs_812_972_cumulative_k0_k9", old_cumulative_k0_k9 - cumulative_k0_k9)
    print("PASS V26_Q138_BC748_936_K9_CONVOLUTION")
    print("scope=exact convolution of current admitted leaf envelopes after uniform B1<=748,C1<=936; k8 passes with larger margin; k9 still fails; no complete-tail or W_repr improvement claim")


if __name__ == "__main__":
    main()
