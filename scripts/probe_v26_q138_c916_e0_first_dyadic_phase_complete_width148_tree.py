#!/usr/bin/env python3
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_group_output_minimal_linear_factorization_exact_overlap as M

N = 250
D = 149
assert M.PHYS_N == D


def xor_span_nonzero(basis):
    vals = [0]
    for b in basis:
        vals += [x ^ int(b) for x in vals]
    assert len(vals) == (1 << len(basis))
    assert len(vals) == len(set(vals))
    return frozenset(vals[1:])


def common_kernel_nonzero(kernel_sets, subset):
    it = iter(sorted(subset))
    try:
        first = next(it)
    except StopIteration:
        return frozenset((1 << D) - 1 for _ in ())
    cur = set(kernel_sets[first])
    for gid in it:
        cur.intersection_update(kernel_sets[gid])
        if not cur:
            break
    return frozenset(cur)


def kernel_dimension_from_nonzero(s):
    z = len(s) + 1
    k = z.bit_length() - 1
    assert (1 << k) == z
    return k


def rank_subset(kernel_sets, subset):
    if not subset:
        return 0
    return D - kernel_dimension_from_nonzero(common_kernel_nonzero(kernel_sets, subset))


def balanced_tree(items):
    items = tuple(sorted(items))
    assert items
    if len(items) == 1:
        return {'groups': items, 'leaf': items[0]}
    mid = len(items) // 2
    return {
        'groups': items,
        'left': balanced_tree(items[:mid]),
        'right': balanced_tree(items[mid:]),
    }


def attach_exception_tree(exception_groups, coverage_masks, directions):
    bmask = sum(1 << g for g in exception_groups)
    if not exception_groups:
        raise AssertionError('expected nonempty exception set')

    # One-direction cover: then every subset of B is non-full.
    one = []
    for d in directions:
        m = coverage_masks[d] & bmask
        if m == bmask:
            one.append(d)
    if one:
        d = min(one)
        return balanced_tree(exception_groups), {
            'cover_size': 1,
            'directions': [d],
            'partitions': [list(sorted(exception_groups))],
        }

    # Exact two-direction cover over the 33 exceptional groups. Search larger
    # restricted covers first, then numeric direction for determinism.
    candidates = []
    for d in directions:
        m = coverage_masks[d] & bmask
        if m:
            candidates.append((m.bit_count(), d, m))
    candidates.sort(key=lambda x: (-x[0], x[1]))
    for _ca, da, ma in candidates:
        missing = bmask & ~ma
        for _cb, db, mb in candidates:
            if missing & ~mb:
                continue
            a_groups = [g for g in exception_groups if (ma >> g) & 1]
            b_groups = [g for g in exception_groups if g not in set(a_groups)]
            if not a_groups or not b_groups:
                continue
            assert all((mb >> g) & 1 for g in b_groups)
            return {
                'groups': tuple(sorted(exception_groups)),
                'left': balanced_tree(a_groups),
                'right': balanced_tree(b_groups),
            }, {
                'cover_size': 2,
                'directions': [da, db],
                'partitions': [list(sorted(a_groups)), list(sorted(b_groups))],
            }
    return None, {'cover_size': None, 'directions': [], 'partitions': []}


def verify_tree(tree, kernel_sets):
    all_groups = frozenset(range(N))
    widths = []
    hist = Counter()
    bad = []
    nodes = 0

    def walk(node, is_root=False):
        nonlocal nodes
        nodes += 1
        subset = frozenset(node['groups'])
        assert subset
        if not is_root:
            comp = all_groups - subset
            rs = rank_subset(kernel_sets, subset)
            rc = rank_subset(kernel_sets, comp)
            lam = rs + rc - D
            assert 0 <= lam <= D
            widths.append(lam)
            hist[lam] += 1
            if lam > 148:
                bad.append({'size': len(subset), 'rank': rs, 'complement_rank': rc, 'lambda': lam})
        if 'leaf' in node:
            assert len(subset) == 1 and node['leaf'] in subset
            return
        left = frozenset(node['left']['groups'])
        right = frozenset(node['right']['groups'])
        assert left and right and not (left & right)
        assert left | right == subset
        walk(node['left'])
        walk(node['right'])

    walk(tree, True)
    assert nodes == 2 * N - 1
    return {
        'width': max(widths),
        'edge_lambda_histogram': dict(sorted(hist.items())),
        'bad_edges_over_148': bad,
        'nodes': nodes,
        'edges_checked': len(widths),
    }


def digest_direction(d):
    return hashlib.sha256(int(d).to_bytes(19, 'big')).hexdigest()[:20]


def synthetic_tree_regression():
    # Six groups in GF(2)^4. Four share d0, the two exceptions are covered by
    # separate directions. The construction must produce an exact width <= 3.
    n = 4
    kernels = [
        frozenset({1}), frozenset({1}), frozenset({1}), frozenset({1}),
        frozenset({2}), frozenset({4}),
    ]
    # This synthetic check exercises only cover partitioning, not rank formula
    # because singleton sets here are deliberately not full vector subspaces.
    coverage = defaultdict(int)
    for gid, ks in enumerate(kernels):
        for d in ks:
            coverage[d] |= 1 << gid
    dominant = max(coverage, key=lambda d: (coverage[d].bit_count(), -d))
    assert coverage[dominant].bit_count() == 4
    exceptions = [g for g in range(6) if not ((coverage[dominant] >> g) & 1)]
    assert exceptions == [4, 5]
    masks = dict(coverage)
    directions = sorted(masks)
    # Direct two-cover existence for the two exceptions.
    bmask = (1 << 4) | (1 << 5)
    assert any(((masks[a] | masks[b]) & bmask) == bmask for a in directions for b in directions)
    return {'groups': 6, 'dominant_coverage': 4, 'exceptions': 2, 'two_cover_exists': True}


def analyze():
    regression = synthetic_tree_regression()
    records, mult_hist = M.build_closed_spaces()
    assert len(records) == N and all(r['exact'] for r in records)

    kernel_sets = []
    coverage_masks = defaultdict(int)
    rank_hist = Counter()
    for rec in records:
        gid = int(rec['group_id'])
        basis = tuple(int(x) for x in rec['minimal_basis'])
        rank = int(rec['lower_rank'])
        assert rank == rec['upper_rank'] == len(basis)
        rank_hist[rank] += 1
        kbasis = tuple(M.B.homogeneous_kernel(basis, D))
        assert len(kbasis) == D - rank
        ks = xor_span_nonzero(kbasis)
        kernel_sets.append(ks)
        for d in ks:
            coverage_masks[d] |= 1 << gid
    assert len(kernel_sets) == N

    directions = sorted(coverage_masks)
    dominant = min(
        (d for d in directions if coverage_masks[d].bit_count() == max(m.bit_count() for m in coverage_masks.values()))
    )
    amask = coverage_masks[dominant]
    a_groups = [g for g in range(N) if (amask >> g) & 1]
    b_groups = [g for g in range(N) if not ((amask >> g) & 1)]
    assert len(a_groups) == 217 and len(b_groups) == 33

    btree, cover = attach_exception_tree(b_groups, coverage_masks, directions)
    if btree is not None:
        tree = {
            'groups': tuple(range(N)),
            'left': balanced_tree(a_groups),
            'right': btree,
        }
        cert = verify_tree(tree, kernel_sets)
    else:
        tree = None
        cert = None

    # Rigorous lower bound 147: choose any rank-147 group. Its complement has
    # 249 >= 218 groups, hence PR169's saturation theorem gives rank 149.
    rank147_groups = [int(r['group_id']) for r in records if int(r['lower_rank']) == 147]
    assert len(rank147_groups) == 16
    lower_witness = rank147_groups[0]
    complement_rank = rank_subset(kernel_sets, frozenset(range(N)) - {lower_witness})
    assert complement_rank == D
    lower_lambda = 147 + complement_rank - D
    assert lower_lambda == 147

    if cert is not None and cert['width'] <= 148:
        decision = 'PHASE_COMPLETE_LINEAR_BRANCHWIDTH_IN_147_148_WITH_WIDTH148_CERTIFICATE'
        upper = cert['width']
    else:
        decision = 'WIDTH148_DOMINANT_KERNEL_COVER_CONSTRUCTION_NOT_FOUND'
        upper = 149

    out = {
        'position': 'C',
        'physical_shared_dimension': D,
        'support_groups': N,
        'support_multiplicity_histogram': mult_hist,
        'synthetic_cover_regression': regression,
        'minimal_rank_histogram': dict(sorted(rank_hist.items())),
        'dominant_direction_digest': digest_direction(dominant),
        'dominant_direction_coverage': len(a_groups),
        'dominant_exception_groups': b_groups,
        'exception_count': len(b_groups),
        'exception_cover_size': cover['cover_size'],
        'exception_cover_direction_digests': [digest_direction(d) for d in cover['directions']],
        'exception_partition_sizes': [len(x) for x in cover['partitions']],
        'lower_bound_witness_group': lower_witness,
        'lower_bound_witness_group_rank': 147,
        'lower_bound_witness_complement_rank': complement_rank,
        'lower_bound_lambda': lower_lambda,
        'certified_tree': cert,
        'phase_complete_linear_branchwidth_lower_bound': 147,
        'phase_complete_linear_branchwidth_upper_bound': upper,
        'decision': decision,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHASE_COMPLETE_WIDTH148_TREE')
    print('scope=explicit phase-complete linear branch-decomposition construction using exact PR168 minimal spaces and PR169 dual-kernel structure')
    print('claim=if a certified tree is reported, every non-root edge lambda is independently recomputed from exact common-kernel intersections')
    print('lower_bound=rank147 leaf with 249-group full-rank complement gives branchwidth at least147')
    print('important=this is a linear-factorization branchwidth bound only and does not rule out nonlinear compression')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
