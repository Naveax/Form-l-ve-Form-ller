#!/usr/bin/env python3
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_predecessor_leaf_bc_second_residue_correction_classes as C

MAX_K = 5


def span_mask(rows):
    vals = {0}
    for r in rows:
        vals |= {x ^ r for x in tuple(vals)}
    m = 0
    for x in vals:
        m |= 1 << x
    return m


def rows_from_mask(mask):
    return [x for x in range(1, 16) if (mask >> x) & 1]


def join(a, b):
    return span_mask(rows_from_mask(a) + rows_from_mask(b))


def class_from_mask(mask, P):
    rows = rows_from_mask(mask)
    qrank, K = C.kernel_basis(rows, n=4)
    n = 4 - qrank
    pr = C.polar_rank_on_kernel(K, P)
    assert pr % 2 == 0 and pr <= n
    irank = 128 - n
    return irank, n, pr


def main():
    sites, sig, P = C.setup()
    assert len(sites) == 124

    sig_types = Counter(span_mask(sig[z]) for z in sites)
    print('site_count', len(sites), 'distinct_signature_rowspaces', len(sig_types),
          'signature_type_multiplicities', dict(sorted(sig_types.items())), flush=True)

    dp = [defaultdict(int) for _ in range(MAX_K + 1)]
    dp[0][1] = 1

    for sm, mult in sig_types.items():
        nxt = [defaultdict(int) for _ in range(MAX_K + 1)]
        for k in range(MAX_K + 1):
            for R, ways in dp[k].items():
                maxj = min(mult, MAX_K - k)
                for j in range(maxj + 1):
                    R2 = R if j == 0 else join(R, sm)
                    nxt[k + j][R2] += ways * math.comb(mult, j)
        dp = nxt

    # Clean second-residue classifier regression oracle.
    expected_e0 = {0: 1, 1: 22, 2: 74, 3: 484}
    expected_e1 = {0: 0, 1: 102, 2: 2397, 3: 8196}
    expected_em1 = {0: 0, 1: 0, 2: 4, 3: 0}

    # Clean PR39 / run32135226810 direct-e2 class authority.  These checks
    # force the tiny rowspace DP to reproduce the prior large exact
    # enumeration, including the 1,152,040 weight119 class.
    expected_e2_classes = {
        2: Counter({(124, 4, 2): 4465, (125, 3, 0): 686}),
        3: Counter({(125, 3, 2): 66570, (126, 2, 0): 63174}),
        4: Counter({(127, 1, 0): 450840}),
        5: Counter({(128, 0, 0): 1_152_040}),
    }

    for k in range(MAX_K + 1):
        classes = Counter()
        exponents = Counter()
        e2_classes = Counter()
        for R, ways in dp[k].items():
            cls = class_from_mask(R, P)
            classes[cls] += ways
            _ir, n, pr = cls
            e = k - 3 + n - pr // 2
            exponents[e] += ways
            if e == 2:
                e2_classes[cls] += ways

        total = sum(exponents.values())
        assert total == math.comb(124, k), (k, total, math.comb(124, k))
        if k <= 3:
            assert exponents[0] == expected_e0[k], (k, exponents[0])
            assert exponents[1] == expected_e1[k], (k, exponents[1])
            assert exponents[-1] == expected_em1[k], (k, exponents[-1])
        if k in expected_e2_classes:
            assert e2_classes == expected_e2_classes[k], (k, e2_classes)

        relevant = {e: n for e, n in sorted(exponents.items()) if e <= 2}
        print('zero_count', k,
              'total_patterns', total,
              'reachable_rowspace_states', len(dp[k]),
              'class_distribution', dict(sorted(classes.items())),
              'exponent_distribution', dict(sorted(exponents.items())),
              'e2_class_distribution', dict(sorted(e2_classes.items())),
              'third_residue_relevant_e_le_2', relevant,
              flush=True)

    print('cutoff_proof', 'k>=6 => e>=k-3>=3', flush=True)
    print('PASS V26_Q138_BC_THIRD_RESIDUE_VALUATION_DP')
    print('crosscheck=clean PR39 run32135226810 direct-e2 class counts reproduced by rowspace multiplicity DP')
    print('scope=exact quotient-signature valuation-class counts through third residue; no support/rank/lift bound')
    print('next=use existing clean B direct-e2 support envelope1796 and focus new work on structured inherited second-lift correction')


if __name__ == '__main__':
    main()
