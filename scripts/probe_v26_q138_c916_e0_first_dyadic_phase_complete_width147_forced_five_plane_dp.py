#!/usr/bin/env python3
import hashlib
import itertools
import json
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_phase_complete_width147_three_plane_cover as P

W = P.W
M = P.M
N = P.N
D = P.D
FULL_GROUP_MASK = (1 << N) - 1
assert N == 250 and D == 149


def mask_groups(mask):
    return tuple(g for g in range(N) if (mask >> g) & 1)


def kernel_dim(nonzero):
    return W.kernel_dimension_from_nonzero(nonzero)


def intersect_nonzero(spaces, block_mask):
    ids = [i for i in range(len(spaces)) if (block_mask >> i) & 1]
    assert ids
    cur = set(spaces[ids[0]])
    for i in ids[1:]:
        cur.intersection_update(spaces[i])
        if not cur:
            break
    return frozenset(cur)


def combine(left, right):
    lg = frozenset(left['groups'])
    rg = frozenset(right['groups'])
    assert lg and rg and not (lg & rg)
    return {
        'groups': tuple(sorted(lg | rg)),
        'left': left,
        'right': right,
    }


def solve_upper_tree(block_trees, block_kernels):
    m = len(block_trees)
    assert 2 <= m <= 8
    full = (1 << m) - 1

    @lru_cache(None)
    def kdim(mask):
        assert mask
        return kernel_dim(intersect_nonzero(block_kernels, mask))

    @lru_cache(None)
    def admissible(mask):
        assert 0 < mask < full
        return kdim(mask) + kdim(full ^ mask) >= 2

    split = {}

    @lru_cache(None)
    def good(mask):
        if mask & (mask - 1) == 0:
            return True
        if mask != full and not admissible(mask):
            return False
        first = mask & -mask
        sub = (mask - 1) & mask
        while sub:
            if (sub & first) and sub != mask:
                other = mask ^ sub
                if good(sub) and good(other):
                    split[mask] = (sub, other)
                    return True
            sub = (sub - 1) & mask
        return False

    def build(mask):
        if mask & (mask - 1) == 0:
            i = mask.bit_length() - 1
            return block_trees[i]
        a, b = split[mask]
        return combine(build(a), build(b))

    ok = good(full)
    if not ok:
        return None, {
            'proper_subset_count': full - 1,
            'admissible_proper_subset_count': sum(
                1 for x in range(1, full) if admissible(x)
            ),
        }
    tree = build(full)
    return tree, {
        'proper_subset_count': full - 1,
        'admissible_proper_subset_count': sum(
            1 for x in range(1, full) if admissible(x)
        ),
    }


def partition_from_order(order, plane_masks, kernel_sets):
    remaining = FULL_GROUP_MASK
    block_masks = []
    block_planes = []
    for plane in order:
        bm = remaining & plane_masks[plane]
        if bm:
            block_masks.append(bm)
            block_planes.append(plane)
            remaining &= ~bm
    if remaining:
        return None
    assert sum(x.bit_count() for x in block_masks) == N
    union = 0
    for bm in block_masks:
        assert not (union & bm)
        union |= bm
    assert union == FULL_GROUP_MASK

    block_groups = [mask_groups(bm) for bm in block_masks]
    block_kernels = []
    block_trees = []
    for plane, groups in zip(block_planes, block_groups):
        ks = W.common_kernel_nonzero(kernel_sets, frozenset(groups))
        assert kernel_dim(ks) >= 2
        assert all(x in ks for x in plane)
        block_kernels.append(ks)
        block_trees.append(W.balanced_tree(groups))
    return {
        'block_masks': tuple(block_masks),
        'block_planes': tuple(block_planes),
        'block_groups': tuple(block_groups),
        'block_kernels': tuple(block_kernels),
        'block_trees': tuple(block_trees),
    }


def digest_partition(block_masks):
    h = hashlib.sha256()
    for bm in block_masks:
        h.update(int(bm).to_bytes(32, 'big'))
    return h.hexdigest()[:20]


def synthetic_upper_dp_regression():
    # Three blocks sharing one 2D plane. Every proper upper cut has k>=2 on
    # both sides, so the DP must find a tree.
    plane = frozenset({1, 2, 3})
    block_kernels = (plane, plane, plane)
    block_trees = (
        {'groups': (0,), 'leaf': 0},
        {'groups': (1,), 'leaf': 1},
        {'groups': (2,), 'leaf': 2},
    )
    tree, stats = solve_upper_tree(block_trees, block_kernels)
    assert tree is not None
    assert frozenset(tree['groups']) == frozenset({0, 1, 2})
    assert stats['proper_subset_count'] == 6
    assert stats['admissible_proper_subset_count'] == 6
    return {'blocks': 3, 'admissible_proper_subsets': 6}


def analyze():
    regression = synthetic_upper_dp_regression()
    records, mult_hist = M.build_closed_spaces()
    assert len(records) == N and all(r['exact'] for r in records)

    kernel_sets = []
    line_coverage = defaultdict(int)
    rank_hist = Counter()
    rank147_groups = []
    for rec in records:
        gid = int(rec['group_id'])
        basis = tuple(int(x) for x in rec['minimal_basis'])
        rank = int(rec['lower_rank'])
        assert rank == rec['upper_rank'] == len(basis)
        rank_hist[rank] += 1
        kbasis = tuple(M.B.homogeneous_kernel(basis, D))
        assert len(kbasis) == D - rank
        ks = W.xor_span_nonzero(kbasis)
        kernel_sets.append(ks)
        for d in ks:
            line_coverage[d] |= 1 << gid
        if rank == 147:
            rank147_groups.append(gid)
    assert len(kernel_sets) == N and len(rank147_groups) == 16

    forced_by_group = {}
    for gid in rank147_groups:
        planes = P.planes_of_kernel(kernel_sets[gid])
        assert len(planes) == 1
        forced_by_group[gid] = planes[0]
    forced_planes = tuple(sorted(set(forced_by_group.values())))
    assert len(forced_planes) == 5

    plane_masks = {
        plane: P.coverage_from_plane(plane, line_coverage)
        for plane in forced_planes
    }
    forced_union = 0
    for plane in forced_planes:
        forced_union |= plane_masks[plane]
    uncovered_mask = FULL_GROUP_MASK & ~forced_union
    uncovered_groups = mask_groups(uncovered_mask)

    cert = None
    selected = None
    search_stats = Counter()
    seen_partitions = set()
    if not uncovered_groups:
        for order in itertools.permutations(forced_planes):
            search_stats['orders_examined'] += 1
            part = partition_from_order(order, plane_masks, kernel_sets)
            assert part is not None
            pd = digest_partition(part['block_masks'])
            if pd in seen_partitions:
                search_stats['duplicate_partitions'] += 1
                continue
            seen_partitions.add(pd)
            search_stats['unique_partitions'] += 1
            tree, dpstats = solve_upper_tree(
                part['block_trees'], part['block_kernels']
            )
            search_stats['dp_admissible_proper_subset_total'] += dpstats[
                'admissible_proper_subset_count'
            ]
            if tree is None:
                continue
            got = W.verify_tree(tree, kernel_sets)
            assert got['nodes'] == 499 and got['edges_checked'] == 498
            if got['width'] <= 147:
                cert = got
                selected = {
                    'order': order,
                    'partition_digest': pd,
                    'block_sizes': [len(x) for x in part['block_groups']],
                    'block_kernel_dimensions': [
                        kernel_dim(x) for x in part['block_kernels']
                    ],
                }
                break

    lower_witness = rank147_groups[0]
    complement_rank = W.rank_subset(
        kernel_sets, frozenset(range(N)) - {lower_witness}
    )
    assert complement_rank == 149
    lower_lambda = 147 + complement_rank - D
    assert lower_lambda == 147

    if cert is not None:
        assert cert['width'] == 147
        decision = 'PHASE_COMPLETE_LINEAR_BRANCHWIDTH_EXACT_147'
        upper = 147
    elif uncovered_groups:
        decision = 'FORCED_FIVE_2D_PLANES_DO_NOT_COVER_ALL_WIDTH147_OPEN'
        upper = 148
    else:
        decision = 'FORCED_FIVE_PLANE_ORDERED_PARTITION_DP_NO_WIDTH147_TREE'
        upper = 148

    out = {
        'position': 'C',
        'physical_shared_dimension': D,
        'support_groups': N,
        'support_multiplicity_histogram': mult_hist,
        'synthetic_upper_dp_regression': regression,
        'minimal_rank_histogram': dict(sorted(rank_hist.items())),
        'rank147_groups': rank147_groups,
        'forced_plane_count': len(forced_planes),
        'forced_plane_digests': [P.plane_digest(x) for x in forced_planes],
        'forced_plane_coverages': [plane_masks[x].bit_count() for x in forced_planes],
        'forced_plane_union_coverage': forced_union.bit_count(),
        'forced_plane_uncovered_count': len(uncovered_groups),
        'forced_plane_uncovered_groups': list(uncovered_groups),
        'search_stats': dict(sorted(search_stats.items())),
        'selected_partition': None if selected is None else {
            'order_plane_digests': [P.plane_digest(x) for x in selected['order']],
            'partition_digest': selected['partition_digest'],
            'block_sizes': selected['block_sizes'],
            'block_kernel_dimensions': selected['block_kernel_dimensions'],
        },
        'certified_tree': cert,
        'lower_bound_witness_group': lower_witness,
        'lower_bound_witness_group_rank': 147,
        'lower_bound_witness_complement_rank': complement_rank,
        'lower_bound_lambda': lower_lambda,
        'phase_complete_linear_branchwidth_lower_bound': 147,
        'phase_complete_linear_branchwidth_upper_bound': upper,
        'decision': decision,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHASE_COMPLETE_WIDTH147_FORCED_FIVE_PLANE_DP')
    print('scope=forced-five-2D-kernel-plane union plus exact ordered-partition upper-tree DP')
    print('certificate=any reported group tree is independently checked on all 498 non-root edges')
    print('important=no-certificate here is not a general impossibility theorem for width147')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
