#!/usr/bin/env python3
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_phase_complete_width148_tree as W

M = W.M
N = W.N
D = W.D
assert N == 250 and D == 149
FULL_GROUP_MASK = (1 << N) - 1


def plane_digest(plane):
    h = hashlib.sha256()
    for x in plane:
        h.update(int(x).to_bytes(19, 'big'))
    return h.hexdigest()[:20]


def planes_of_kernel(nonzero_kernel):
    vals = sorted(int(x) for x in nonzero_kernel)
    out = []
    s = set(vals)
    for i, a in enumerate(vals):
        for b in vals[i + 1:]:
            c = a ^ b
            assert c and c in s
            p = tuple(sorted((a, b, c)))
            if a == p[0] and b == p[1]:
                out.append(p)
    expected = ((len(vals) + 1 - 1) * (len(vals) + 1 - 2)) // 6
    # If kernel dimension is k, number of 2D subspaces is
    # ((2^k-1)(2^k-2))/6. Here len(vals)=2^k-1.
    assert len(out) == (len(vals) * (len(vals) - 1)) // 6
    assert len(out) == len(set(out))
    return tuple(out)


def kernel_dimension(nonzero_kernel):
    return W.kernel_dimension_from_nonzero(nonzero_kernel)


def coverage_from_plane(plane, line_coverage):
    a, b, c = plane
    m = line_coverage[a] & line_coverage[b]
    assert m == (m & line_coverage[c])
    assert m
    return m


def groups_from_mask(mask):
    return [g for g in range(N) if (mask >> g) & 1]


def maximal_restricted_options(group, uncovered, planes_by_group, plane_masks, chosen):
    # Exact dominance pruning for set-cover search. If one candidate covers a
    # subset of the currently uncovered groups covered by another candidate,
    # the smaller option can never be uniquely useful at the same search node.
    reps = {}
    for p in planes_by_group[group]:
        if p in chosen:
            continue
        r = plane_masks[p] & uncovered
        if not r:
            continue
        old = reps.get(r)
        if old is None or p < old:
            reps[r] = p
    ordered = sorted(reps.items(), key=lambda kv: (-kv[0].bit_count(), kv[1]))
    kept = []
    for r, p in ordered:
        if any((r | kr) == kr for kr, _kp in kept):
            continue
        kept.append((r, p))
    return tuple(p for _r, p in kept)


def exact_extra_cover(uncovered, depth, planes_by_group, plane_masks, chosen):
    if not uncovered:
        return ()
    if depth == 0:
        return None
    ugroups = groups_from_mask(uncovered)
    g = min(
        ugroups,
        key=lambda x: (
            sum(1 for p in planes_by_group[x] if p not in chosen),
            x,
        ),
    )
    options = maximal_restricted_options(
        g, uncovered, planes_by_group, plane_masks, chosen
    )
    if depth == 1:
        for p in options:
            if uncovered & ~plane_masks[p] == 0:
                return (p,)
        return None
    for p in options:
        new_uncovered = uncovered & ~plane_masks[p]
        got = exact_extra_cover(
            new_uncovered,
            depth - 1,
            planes_by_group,
            plane_masks,
            chosen | {p},
        )
        if got is not None:
            return (p,) + got
    return None


def minimum_cover_at_most_three(forced, planes_by_group, plane_masks):
    forced = tuple(sorted(set(forced)))
    if len(forced) > 3:
        return None
    covered = 0
    for p in forced:
        covered |= plane_masks[p]
    uncovered = FULL_GROUP_MASK & ~covered
    if not uncovered:
        return forced
    slots = 3 - len(forced)
    for extra_count in range(1, slots + 1):
        got = exact_extra_cover(
            uncovered,
            extra_count,
            planes_by_group,
            plane_masks,
            set(forced),
        )
        if got is not None:
            return forced + got
    return None


def tree_from_cover(cover, plane_masks):
    remaining = FULL_GROUP_MASK
    blocks = []
    for p in cover:
        bmask = remaining & plane_masks[p]
        assert bmask
        block = groups_from_mask(bmask)
        blocks.append(block)
        remaining &= ~bmask
    assert remaining == 0
    assert 1 <= len(blocks) <= 3

    trees = [W.balanced_tree(block) for block in blocks]
    if len(trees) == 1:
        return trees[0], blocks
    if len(trees) == 2:
        return {
            'groups': tuple(range(N)),
            'left': trees[0],
            'right': trees[1],
        }, blocks
    right_groups = tuple(sorted(blocks[1] + blocks[2]))
    right = {
        'groups': right_groups,
        'left': trees[1],
        'right': trees[2],
    }
    return {
        'groups': tuple(range(N)),
        'left': trees[0],
        'right': right,
    }, blocks


def synthetic_cover_regression():
    full = (1 << 6) - 1
    p0 = (1, 2, 3)
    p1 = (4, 8, 12)
    p2 = (16, 32, 48)
    masks = {
        p0: 0b000111,
        p1: 0b011100,
        p2: 0b110000,
    }
    by_group = [[] for _ in range(6)]
    for p, m in masks.items():
        for g in range(6):
            if (m >> g) & 1:
                by_group[g].append(p)
    old_n = globals()['N']
    old_full = globals()['FULL_GROUP_MASK']
    try:
        globals()['N'] = 6
        globals()['FULL_GROUP_MASK'] = full
        got = minimum_cover_at_most_three((p0,), by_group, masks)
    finally:
        globals()['N'] = old_n
        globals()['FULL_GROUP_MASK'] = old_full
    assert got is not None and len(got) == 3
    return {'groups': 6, 'forced_planes': 1, 'minimum_cover': 3}


def analyze():
    regression = synthetic_cover_regression()
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
        assert kernel_dimension(ks) == D - rank
        kernel_sets.append(ks)
        for d in ks:
            line_coverage[d] |= 1 << gid
        if rank == 147:
            rank147_groups.append(gid)
    assert len(kernel_sets) == N
    assert len(rank147_groups) == 16

    # Each rank-147 group has a 2D kernel, hence exactly one possible 2D
    # common-kernel plane in any three-block cover. These planes are forced.
    forced_by_group = {}
    for gid in rank147_groups:
        planes = planes_of_kernel(kernel_sets[gid])
        assert len(planes) == 1
        forced_by_group[gid] = planes[0]
    forced_planes = tuple(sorted(set(forced_by_group.values())))

    plane_masks = {}
    planes_by_group = [[] for _ in range(N)]
    all_planes = set()
    if len(forced_planes) <= 3:
        for gid, ks in enumerate(kernel_sets):
            ps = planes_of_kernel(ks)
            planes_by_group[gid].extend(ps)
            all_planes.update(ps)
        for p in sorted(all_planes):
            plane_masks[p] = coverage_from_plane(p, line_coverage)
        for gid in range(N):
            for p in planes_by_group[gid]:
                assert (plane_masks[p] >> gid) & 1
        cover = minimum_cover_at_most_three(
            forced_planes, planes_by_group, plane_masks
        )
    else:
        for p in forced_planes:
            plane_masks[p] = coverage_from_plane(p, line_coverage)
        cover = None

    cert = None
    blocks = None
    if cover is not None:
        tree, blocks = tree_from_cover(cover, plane_masks)
        # Every assigned block must itself have common-kernel dimension >=2.
        for block in blocks:
            assert kernel_dimension(
                W.common_kernel_nonzero(kernel_sets, frozenset(block))
            ) >= 2
        cert = W.verify_tree(tree, kernel_sets)
        assert cert['nodes'] == 499 and cert['edges_checked'] == 498
        assert cert['width'] <= 147

    # Independent lower bound 147, as frozen in PR170.
    lower_witness = rank147_groups[0]
    complement = frozenset(range(N)) - {lower_witness}
    complement_rank = W.rank_subset(kernel_sets, complement)
    assert complement_rank == 149
    lower_lambda = 147 + complement_rank - D
    assert lower_lambda == 147

    if cert is not None:
        assert cert['width'] == 147
        decision = 'PHASE_COMPLETE_LINEAR_BRANCHWIDTH_EXACT_147'
        upper = 147
    elif len(forced_planes) > 3:
        decision = 'THREE_COMMON_2D_KERNEL_COVER_IMPOSSIBLE_WIDTH147_OPEN'
        upper = 148
    else:
        decision = 'NO_THREE_COMMON_2D_KERNEL_COVER_WIDTH147_OPEN'
        upper = 148

    forced_coverages = [plane_masks[p].bit_count() for p in forced_planes]
    out = {
        'position': 'C',
        'physical_shared_dimension': D,
        'support_groups': N,
        'support_multiplicity_histogram': mult_hist,
        'synthetic_cover_regression': regression,
        'minimal_rank_histogram': dict(sorted(rank_hist.items())),
        'rank147_groups': rank147_groups,
        'forced_rank147_plane_count': len(forced_planes),
        'forced_rank147_plane_digests': [plane_digest(p) for p in forced_planes],
        'forced_rank147_plane_coverages': forced_coverages,
        'enumerated_common_2d_planes': len(all_planes) if len(forced_planes) <= 3 else None,
        'three_plane_cover_exists': cover is not None,
        'minimum_common_2d_cover_size_at_most_3': len(cover) if cover is not None else None,
        'cover_plane_digests': [plane_digest(p) for p in cover] if cover is not None else [],
        'cover_plane_coverages': [plane_masks[p].bit_count() for p in cover] if cover is not None else [],
        'assigned_block_sizes': [len(b) for b in blocks] if blocks is not None else [],
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
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHASE_COMPLETE_WIDTH147_THREE_PLANE_COVER')
    print('criterion=three common-2D-kernel coverage blocks are sufficient for an exact width147 tree')
    print('forced=each rank147 group has one unique 2D kernel plane, so all distinct such planes are mandatory in any three-plane cover')
    print('certificate=any reported tree is independently checked on all 498 non-root edges')
    print('important=failure of the three-plane cover is not a proof that width147 is impossible')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
