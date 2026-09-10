#!/usr/bin/env python3
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_group_output_minimal_linear_factorization_exact_overlap as M

PHYS_N = M.PHYS_N
GROUPS = 250
assert PHYS_N == 149


def xor_span_nonzero(basis):
    vals = [0]
    for b in basis:
        vals += [x ^ int(b) for x in vals]
    assert len(vals) == 1 << len(basis)
    assert len(set(vals)) == len(vals)
    return tuple(vals[1:])


def direction_digest(d):
    return hashlib.sha256(int(d).to_bytes(19, 'big')).hexdigest()[:20]


def synthetic_dual_regression():
    # Four subspaces of GF(2)^4 represented by row bases. Kernel enumeration
    # must recover pair-union ranks and the exact largest non-full subset size.
    n = 4
    spaces = (
        (0b0001, 0b0010, 0b0100),
        (0b0001, 0b0010, 0b1000),
        (0b0001, 0b0100, 0b1000),
        (0b0010, 0b0100, 0b1000),
    )
    kernels = []
    for rows in spaces:
        k = M.B.homogeneous_kernel(rows, n)
        assert len(k) == 1
        kernels.append(set(xor_span_nonzero(k)))
    pair = Counter()
    for i in range(len(spaces)):
        for j in range(i + 1, len(spaces)):
            inter_nonzero = kernels[i] & kernels[j]
            dim = (len(inter_nonzero) + 1).bit_length() - 1
            assert (1 << dim) == len(inter_nonzero) + 1
            pair[n - dim] += 1
    assert pair == {4: 6}
    coverage = Counter()
    for ks in kernels:
        coverage.update(ks)
    assert max(coverage.values()) == 1
    return {'groups': 4, 'pair_union_rank_histogram': dict(pair), 'max_nonfull_subset_size': 1}


def analyze():
    regression = synthetic_dual_regression()
    records, mult_hist = M.build_closed_spaces()
    assert len(records) == GROUPS
    assert mult_hist == {1: 103, 2: 57, 4: 90}
    assert all(r['exact'] for r in records)

    kernels = []
    kernel_sets = []
    kernel_dim_hist = Counter()
    coverage = Counter()
    coverage_groups = defaultdict(list)
    minimal_rank_hist = Counter()

    for rec in records:
        gid = int(rec['group_id'])
        basis = tuple(int(x) for x in rec['minimal_basis'])
        rank = int(rec['lower_rank'])
        assert rank == len(basis) == rec['upper_rank']
        minimal_rank_hist[rank] += 1
        kernel = tuple(M.B.homogeneous_kernel(basis, PHYS_N))
        assert len(kernel) == PHYS_N - rank
        kernel_dim_hist[len(kernel)] += 1
        nonzero = set(xor_span_nonzero(kernel))
        assert len(nonzero) == (1 << len(kernel)) - 1
        kernels.append(kernel)
        kernel_sets.append(nonzero)
        for d in nonzero:
            coverage[d] += 1
            coverage_groups[d].append(gid)

    pair_hist = Counter()
    nonfull_pairs = 0
    max_pair_kernel_intersection_dim = 0
    max_pair_examples = []
    for i in range(GROUPS):
        for j in range(i + 1, GROUPS):
            inter_nonzero = kernel_sets[i] & kernel_sets[j]
            size_with_zero = len(inter_nonzero) + 1
            dim = size_with_zero.bit_length() - 1
            assert (1 << dim) == size_with_zero
            union_rank = PHYS_N - dim
            pair_hist[union_rank] += 1
            if dim:
                nonfull_pairs += 1
                if dim > max_pair_kernel_intersection_dim:
                    max_pair_kernel_intersection_dim = dim
                    max_pair_examples = [(i, j)]
                elif dim == max_pair_kernel_intersection_dim and len(max_pair_examples) < 12:
                    max_pair_examples.append((i, j))
    assert sum(pair_hist.values()) == GROUPS * (GROUPS - 1) // 2

    coverage_hist = Counter(coverage.values())
    max_coverage = max(coverage.values())
    max_dirs = sorted(d for d, c in coverage.items() if c == max_coverage)
    witness_d = max_dirs[0]
    witness_groups = tuple(sorted(coverage_groups[witness_d]))
    assert len(witness_groups) == max_coverage

    # Exact extremal fact: a group subset has union rank < 149 iff all of its
    # minimal row spaces share some nonzero annihilator d. Therefore the largest
    # non-full subset size is exactly max_d coverage(d).
    max_nonfull_subset_size = max_coverage
    saturation_threshold = max_nonfull_subset_size + 1
    assert saturation_threshold <= GROUPS

    # Standard balanced-edge lemma for subcubic branch-decomposition trees:
    # with n leaves, some edge has at least ceil(n/3) leaves on each side.
    balanced_edge_min_side = (GROUPS + 2) // 3
    branchwidth_exact = max_nonfull_subset_size < balanced_edge_min_side
    if branchwidth_exact:
        decision = 'PHASE_COMPLETE_LINEAR_BRANCHWIDTH_EXACT149_BY_DUAL_COVERAGE'
        branchwidth = PHYS_N
    else:
        decision = 'PHASE_COMPLETE_LINEAR_BRANCHWIDTH_DUAL_COVERAGE_INCONCLUSIVE'
        branchwidth = None

    global_basis = M.B.canonical_basis(
        row for rec in records for row in rec['minimal_basis']
    )
    assert len(global_basis) == PHYS_N

    out = {
        'position': 'C',
        'physical_shared_dimension': PHYS_N,
        'support_groups': GROUPS,
        'support_multiplicity_histogram': mult_hist,
        'synthetic_dual_regression': regression,
        'global_minimal_union_rank': len(global_basis),
        'minimal_rank_histogram': dict(sorted(minimal_rank_hist.items())),
        'kernel_dimension_histogram': dict(sorted(kernel_dim_hist.items())),
        'pair_count': GROUPS * (GROUPS - 1) // 2,
        'pair_union_rank_histogram': dict(sorted(pair_hist.items())),
        'nonfull_pair_count': nonfull_pairs,
        'max_pair_kernel_intersection_dimension': max_pair_kernel_intersection_dim,
        'max_pair_examples': [list(x) for x in max_pair_examples],
        'unique_nonzero_kernel_directions': len(coverage),
        'kernel_direction_coverage_histogram': dict(sorted(coverage_hist.items())),
        'max_nonzero_kernel_direction_coverage': max_coverage,
        'max_coverage_direction_count': len(max_dirs),
        'max_coverage_direction_digest': direction_digest(witness_d),
        'max_coverage_example_groups': list(witness_groups),
        'max_nonfull_group_subset_size': max_nonfull_subset_size,
        'all_subsets_of_size_at_least': saturation_threshold,
        'all_such_subsets_span_full_149': True,
        'balanced_edge_min_side_for_250_leaf_subcubic_tree': balanced_edge_min_side,
        'phase_complete_linear_branchwidth_exact': branchwidth_exact,
        'phase_complete_linear_branchwidth': branchwidth,
        'decision': decision,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHASE_COMPLETE_LINEAR_BRANCHWIDTH')
    print('scope=exact dual-kernel coverage geometry of the 250 exact minimal linear-factorization row spaces from PR168')
    print('theorem=max coverage of a nonzero common annihilator is exactly the maximum cardinality of a group subset whose union row rank is below 149')
    print('branchwidth_rule=if that maximum is below ceil(250/3)=84, the balanced-edge lemma forces both sides of some edge in every subcubic 250-leaf branch decomposition to have full rank149, hence lambda149 and exact linear branchwidth149')
    print('important=this concerns phase-complete linear factorization spaces only; it does not rule out nonlinear compression or prove the full C2 representation bound')
    print('not_included=exact all-250 nonlinear joint image, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
