#!/usr/bin/env python3

BUDGET = 1 << 44

# Current admitted single-leaf dyadic envelopes.
# Provenance is maintained by the separate A/D, A-e3, and B/C authority files;
# this verifier certifies only the exact four-sequence convolution arithmetic.
A = [1, 41, 564, 1761] + [2048] * 12
B = [36, 812] + [2048] * 14
C = [84, 972] + [2048] * 14
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
        287_664,
        12_038_592,
        291_137_584,
        4_539_375_120,
        48_676_699_184,
        374_710_427_136,
        2_128_245_966_160,
        9_095_463_451_808,
        29_952_328_904_800,
    ]
    assert layers == expected, (layers, expected)

    total_k0_k8 = sum(layers[:9])
    margin_after_k8 = BUDGET - total_k0_k8
    cumulative_k0_k9 = total_k0_k8 + layers[9]
    k9_deficit = cumulative_k0_k9 - BUDGET

    assert total_k0_k8 == 11_651_939_386_272
    assert margin_after_k8 == 5_940_246_658_144
    assert layers[9] == 29_952_328_904_800
    assert cumulative_k0_k9 == 41_604_268_291_072
    assert k9_deficit == 24_012_082_246_656

    assert total_k0_k8 < BUDGET
    assert cumulative_k0_k9 > BUDGET
    assert layers[9] > margin_after_k8

    print("leaf_envelopes", {"A": A[:6], "B": B[:6], "C": C[:6], "D": D[:6]})
    print("layers_k0_k9", layers)
    print("sum_k0_k8", total_k0_k8)
    print("budget_2^44", BUDGET)
    print("margin_after_k8", margin_after_k8)
    print("cumulative_k0_k9", cumulative_k0_k9)
    print("k9_deficit", k9_deficit)
    print("PASS V26_Q138_SHARPENED_K9_CONVOLUTION")
    print("scope=exact convolution of current admitted leaf envelopes; k8 passes with sharpened A e3=1761; k9 still fails; no complete-tail or W_repr improvement claim")


if __name__ == "__main__":
    main()
