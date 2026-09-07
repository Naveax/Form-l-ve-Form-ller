#!/usr/bin/env python3

BUDGET = 1 << 44

A = [1, 41, 564, 1761] + [2048] * 12
D = [1, 20, 173, 838, 1958] + [2048] * 11


def cumulative_for(B, C) -> int:
    total = 0
    for k in range(10):
        for i in range(k + 1):
            for j in range(k - i + 1):
                for q in range(k - i - j + 1):
                    r = k - i - j - q
                    total += A[i] * B[j] * C[q] * D[r]
    return total


def cumulative_k0_k9(b2: int, c2: int) -> int:
    B = [36, 748, b2] + [2048] * 13
    C = [84, 936, c2] + [2048] * 13
    return cumulative_for(B, C)


def cumulative_equal_cap(cap: int, through_index: int) -> int:
    assert 2 <= through_index <= 9
    B = [36, 748] + [cap if i <= through_index else 2048 for i in range(2, 16)]
    C = [84, 936] + [cap if i <= through_index else 2048 for i in range(2, 16)]
    return cumulative_for(B, C)


def max_equal_cap(through_index: int) -> int:
    lo, hi = -1, 2049
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cumulative_equal_cap(mid, through_index) <= BUDGET:
            lo = mid
        else:
            hi = mid
    return lo


def bilinear_coefficients():
    f00 = cumulative_k0_k9(0, 0)
    f10 = cumulative_k0_k9(1, 0)
    f01 = cumulative_k0_k9(0, 1)
    f11 = cumulative_k0_k9(1, 1)
    cb = f10 - f00
    cc = f01 - f00
    cbc = f11 - f00 - cb - cc
    return f00, cb, cc, cbc


def formula(b2: int, c2: int) -> int:
    return 15_892_005_024_640 + 5_260_847_048 * b2 + 3_952_624_408 * c2 + 1_096_366 * b2 * c2


def max_b_for_fixed_c(c2: int) -> int:
    denom = 5_260_847_048 + 1_096_366 * c2
    numer = BUDGET - 15_892_005_024_640 - 3_952_624_408 * c2
    return numer // denom


def max_c_for_fixed_b(b2: int) -> int:
    denom = 3_952_624_408 + 1_096_366 * b2
    numer = BUDGET - 15_892_005_024_640 - 5_260_847_048 * b2
    return numer // denom


def main() -> None:
    coeff = bilinear_coefficients()
    expected = (15_892_005_024_640, 5_260_847_048, 3_952_624_408, 1_096_366)
    assert coeff == expected, (coeff, expected)

    for b2, c2 in [
        (0, 0), (1, 1), (180, 180), (181, 181),
        (323, 0), (324, 0), (0, 430), (0, 431),
        (1796, 0), (1796, 1796), (1796, 2048), (2048, 2048),
    ]:
        assert cumulative_k0_k9(b2, c2) == formula(b2, c2), (b2, c2)

    assert max_b_for_fixed_c(0) == 323
    assert max_c_for_fixed_b(0) == 430
    assert max_b_for_fixed_c(2048) == -852
    assert max_c_for_fixed_b(2048) == -1465

    assert formula(180, 180) == 17_585_952_145_120
    assert formula(180, 180) <= BUDGET
    assert BUDGET - formula(180, 180) == 6_233_899_296

    assert formula(181, 181) == 17_595_561_404_702
    assert formula(181, 181) > BUDGET
    assert formula(181, 181) - BUDGET == 3_375_360_286

    assert formula(323, 0) <= BUDGET < formula(324, 0)
    assert formula(0, 430) <= BUDGET < formula(0, 431)

    # Even complete elimination of only one index-2 contribution cannot pass
    # while the other remains generic2048.
    assert formula(0, 2048) - BUDGET == 6_394_793_767_808
    assert formula(2048, 0) - BUDGET == 9_074_033_735_528

    # The historical B direct-e2 support-only envelope1796 is structurally
    # useful but cannot by itself approach the product gate when C2/higher
    # residues remain generic.
    assert formula(1796, 0) - BUDGET == 7_748_300_278_432
    assert formula(1796, 2048) - BUDGET == 19_875_937_258_144

    # If the same cap is obtained simultaneously across several consecutive
    # B/C higher residues, the required threshold becomes much less severe.
    expected_equal_caps = {
        2: 180,
        3: 568,
        4: 623,
        5: 630,
        6: 631,
        7: 631,
        8: 631,
        9: 631,
    }
    got_equal_caps = {i: max_equal_cap(i) for i in range(2, 10)}
    assert got_equal_caps == expected_equal_caps, (got_equal_caps, expected_equal_caps)
    for i, cap in got_equal_caps.items():
        assert cumulative_equal_cap(cap, i) <= BUDGET
        assert cumulative_equal_cap(cap + 1, i) > BUDGET

    print('bilinear_formula', {
        'constant': coeff[0], 'B2': coeff[1], 'C2': coeff[2], 'B2*C2': coeff[3]
    })
    print('budget_2^44', BUDGET)
    print('threshold_if_C2_zero', {'B2_max': 323})
    print('threshold_if_B2_zero', {'C2_max': 430})
    print('threshold_equal_B2_C2', {'pass_max': 180, '181_deficit': 3_375_360_286})
    print('generic_other_side_no_nonnegative_solution', {
        'C2=2048_max_B2': max_b_for_fixed_c(2048),
        'B2=2048_max_C2': max_c_for_fixed_b(2048),
    })
    print('B2_1796_even_with_C2_zero_deficit', formula(1796, 0) - BUDGET)
    print('equal_cap_threshold_by_last_improved_index', got_equal_caps)
    print('PASS V26_Q138_K9_BC_INDEX2_SENSITIVITY')
    print('scope=exact separated-leaf k0..k9 arithmetic sensitivity with B1=748,C1=936; index2 bilinear thresholds plus equal repeated caps through B/C index9; no lower bound on true ranks and no complete-tail claim')


if __name__ == '__main__':
    main()
