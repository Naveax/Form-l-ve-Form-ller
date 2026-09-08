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
    C = [84, 916, c2] + [2048] * 13
    return cumulative_for(B, C)


def cumulative_equal_cap(cap: int, through_index: int) -> int:
    assert 2 <= through_index <= 9
    B = [36, 748] + [cap if i <= through_index else 2048 for i in range(2, 16)]
    C = [84, 916] + [cap if i <= through_index else 2048 for i in range(2, 16)]
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


EXPECTED_COEFF = (
    15_658_378_343_680,
    5_177_652_568,
    3_952_624_408,
    1_096_366,
)


def formula(b2: int, c2: int) -> int:
    f00, cb, cc, cbc = EXPECTED_COEFF
    return f00 + cb * b2 + cc * c2 + cbc * b2 * c2


def max_b_for_fixed_c(c2: int) -> int:
    f00, cb, cc, cbc = EXPECTED_COEFF
    return (BUDGET - f00 - cc * c2) // (cb + cbc * c2)


def max_c_for_fixed_b(b2: int) -> int:
    f00, cb, cc, cbc = EXPECTED_COEFF
    return (BUDGET - f00 - cb * b2) // (cc + cbc * b2)


def main() -> None:
    coeff = bilinear_coefficients()
    assert coeff == EXPECTED_COEFF, (coeff, EXPECTED_COEFF)

    for b2, c2 in [
        (0, 0), (1, 1), (206, 206), (207, 207),
        (373, 0), (374, 0), (0, 489), (0, 490),
        (1796, 0), (1796, 2048), (2048, 0), (0, 2048), (2048, 2048),
    ]:
        assert cumulative_k0_k9(b2, c2) == formula(b2, c2), (b2, c2)

    assert max_b_for_fixed_c(0) == 373
    assert max_c_for_fixed_b(0) == 489
    assert max_b_for_fixed_c(2048) == -831
    assert max_c_for_fixed_b(2048) == -1399

    assert BUDGET - formula(373, 0) == 2_543_292_872
    assert formula(374, 0) - BUDGET == 2_634_359_696
    assert BUDGET - formula(0, 489) == 974_365_224
    assert formula(0, 490) - BUDGET == 2_978_259_184

    assert formula(206, 206) == 17_585_740_788_312
    assert BUDGET - formula(206, 206) == 6_445_256_104
    assert formula(207, 207) == 17_595_323_864_446
    assert formula(207, 207) - BUDGET == 3_137_820_030

    assert formula(0, 2048) - BUDGET == 6_161_167_086_848
    assert formula(2048, 0) - BUDGET == 8_670_024_758_528
    assert formula(1796, 0) - BUDGET == 7_365_256_311_392
    assert formula(1796, 2048) - BUDGET == 19_492_893_291_104

    expected_equal_caps = {
        2: 206,
        3: 588,
        4: 643,
        5: 649,
        6: 650,
        7: 650,
        8: 650,
        9: 650,
    }
    got_equal_caps = {i: max_equal_cap(i) for i in range(2, 10)}
    assert got_equal_caps == expected_equal_caps, (got_equal_caps, expected_equal_caps)
    for i, cap in got_equal_caps.items():
        assert cumulative_equal_cap(cap, i) <= BUDGET
        assert cumulative_equal_cap(cap + 1, i) > BUDGET

    old_equal_caps = {2: 180, 3: 568, 4: 623, 5: 630, 6: 631, 7: 631, 8: 631, 9: 631}
    assert expected_equal_caps[2] - old_equal_caps[2] == 26
    assert expected_equal_caps[3] - old_equal_caps[3] == 20
    assert expected_equal_caps[4] - old_equal_caps[4] == 20
    assert expected_equal_caps[5] - old_equal_caps[5] == 19
    assert all(expected_equal_caps[i] - old_equal_caps[i] == 19 for i in range(6, 10))

    print('bilinear_formula', {
        'constant': coeff[0], 'B2': coeff[1], 'C2': coeff[2], 'B2*C2': coeff[3]
    })
    print('budget_2^44', BUDGET)
    print('threshold_if_C2_zero', {'B2_max': 373})
    print('threshold_if_B2_zero', {'C2_max': 489})
    print('threshold_equal_B2_C2', {'pass_max': 206, '207_deficit': 3_137_820_030})
    print('generic_other_side_no_nonnegative_solution', {
        'C2=2048_max_B2': max_b_for_fixed_c(2048),
        'B2=2048_max_C2': max_c_for_fixed_b(2048),
    })
    print('B2_1796_even_with_C2_zero_deficit', formula(1796, 0) - BUDGET)
    print('equal_cap_threshold_by_last_improved_index', got_equal_caps)
    print('PASS V26_Q138_K9_BC748_916_SENSITIVITY')
    print('scope=exact separated-leaf k0..k9 arithmetic sensitivity with B1=748,C1=916; index2 bilinear thresholds plus equal repeated caps through B/C index9')
    print('not_included=no lower bound on true ranks, no complete dyadic tail, no W_repr or arithmetic-work theorem, no alpha/ranking/full-round claim')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
