#!/usr/bin/env python3
import math


def main():
    # Certified central mode ranks from the full S1 rank3829 theorem.
    low_center = 2 ** 22
    high_center = 16 * 30632
    assert high_center == 490112 == 3829 * (2 ** 7)

    # Physical predecessor-leaf bit counts in the two disjoint S1 blocks.
    low_counts = {'A': 6, 'B': 6, 'C': 5, 'D': 6}
    high_counts = {'A': 5, 'B': 5, 'C': 6, 'D': 5}
    assert sum(low_counts.values()) == 23
    assert sum(high_counts.values()) == 21

    # For a 32-bit predecessor-leaf vector, any k|(32-k) matricization has
    # rank at most 2^min(k,32-k). All k here are <=6.
    low_leaf = 2 ** sum(low_counts.values())
    high_leaf = 2 ** sum(high_counts.values())
    assert low_leaf == 2 ** 23
    assert high_leaf == 2 ** 21

    # Hadamard-product rank submultiplicativity gives full-star mode bounds.
    low_star = low_center * low_leaf
    high_star = high_center * high_leaf
    assert low_star == 2 ** 45
    assert high_star == 3829 * (2 ** 28)

    # Separately forming complete low and high channel systems and taking
    # their Cartesian joint exactly reproduces the current factor envelope.
    joint = low_star * high_star
    factor = 3829 * (2 ** 73)
    assert joint == factor
    assert factor == 36163882525815743046483968

    print('PASS V26_Q138_D1_LOW_HIGH_STAR_PRODUCT_BARRIER')
    print('low_center_rank=2^22 low_leaf_rank<=2^23 low_star_rank<=2^45')
    print('high_center_rank<=490112=3829*2^7 high_leaf_rank<=2^21')
    print('high_star_rank<=3829*2^28 log2=%.15f' % math.log2(high_star))
    print('independent_low_x_high_joint=3829*2^73 log2=%.15f' % math.log2(joint))
    print('consequence=separate complete low/high basis materialization cannot beat current factor envelope')
    print('next=interleave predecessor-leaf complement contraction before low/high Cartesian joint')
    print('scope=scoped exact structural work gate; not an unrestricted arithmetic lower bound')


if __name__ == '__main__':
    main()
