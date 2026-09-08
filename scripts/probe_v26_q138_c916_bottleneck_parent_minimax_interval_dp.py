#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_quadratic_function_space_separator as F
import probe_v26_q138_c916_evaluation_aware_recursive_tree_refined as E

LO = 166
HI = 250


def analyze():
    raw, groups = F.build_groups()
    assert raw == 577 and len(groups) == 250
    order = sorted(range(len(groups)), key=lambda i: (groups[i]['multiplicity'], groups[i]['function_rank'], i))
    oracle = E.EvaluationOracle(groups)

    cost_cache = {}
    def edge(lo, hi):
        key = (lo, hi)
        if key not in cost_cache:
            idx = frozenset(order[lo:hi])
            st = dict(oracle.stats(idx))
            cost_cache[key] = {
                'lo': lo,
                'hi': hi,
                'size': hi-lo,
                'safe_evaluation_bits': st['safe_evaluation_bits'],
                'generic_safe_evaluation_bits': st.get('generic_safe_evaluation_bits', st['safe_evaluation_bits']),
                'function_lambda': st['function_lambda'],
                'quadratic_residual_dim': st['quadratic_residual_dim'],
                'fiber_affine_residual': st['fiber_affine_residual'],
                'exact_override': st.get('exact_override', False),
                'digest': E.digest(idx),
            }
        return cost_cache[key]

    # dp[(lo, hi)] is the minimum possible maximum edge cost in a subtree
    # rooted at [lo,hi), INCLUDING the [lo,hi) edge itself.
    dp = {}
    choice = {}
    split_comparisons = 0

    for i in range(LO, HI):
        st = edge(i, i+1)
        dp[(i, i+1)] = st['safe_evaluation_bits']
        choice[(i, i+1)] = None

    for length in range(2, HI-LO):
        for lo in range(LO, HI-length+1):
            hi = lo + length
            own = edge(lo, hi)['safe_evaluation_bits']
            candidates = []
            for split in range(lo+1, hi):
                split_comparisons += 1
                lw = dp[(lo, split)]
                rw = dp[(split, hi)]
                candidates.append((
                    max(own, lw, rw),
                    max(lw, rw),
                    lw + rw,
                    abs((split-lo)-(hi-split)),
                    split,
                ))
            best = min(candidates)
            dp[(lo, hi)] = best[0]
            choice[(lo, hi)] = best[-1]

    # Root parent edge is retained from the global tree and is excluded from
    # the replacement-subtree objective. Only its two children and below count.
    root_candidates = []
    for split in range(LO+1, HI):
        split_comparisons += 1
        lw = dp[(LO, split)]
        rw = dp[(split, HI)]
        root_candidates.append((
            max(lw, rw),
            lw + rw,
            abs((split-LO)-(HI-split)),
            split,
            lw,
            rw,
        ))
    root_best = min(root_candidates)
    optimum = root_best[0]
    root_split = root_best[3]

    def build(lo, hi, root=False):
        if root:
            split = root_split
        else:
            split = choice[(lo, hi)]
        node = {'lo': lo, 'hi': hi, 'size': hi-lo, 'split': split}
        if not root:
            node['subtree_minimax_width'] = dp[(lo, hi)]
            node['edge'] = edge(lo, hi)
        if split is not None:
            node['left'] = build(lo, split)
            node['right'] = build(split, hi)
        return node

    witness = build(LO, HI, root=True)
    witness_edges = []
    seen = []
    max_depth = 0
    def verify(node, depth, root=False):
        nonlocal max_depth
        max_depth = max(max_depth, depth)
        lo, hi = node['lo'], node['hi']
        if not root:
            st = edge(lo, hi)
            assert node['edge'] == st
            assert node['subtree_minimax_width'] == dp[(lo, hi)]
            witness_edges.append(st)
        if node['split'] is None:
            assert hi-lo == 1
            seen.append(lo)
            return
        split = node['split']
        assert lo < split < hi
        verify(node['left'], depth+1)
        verify(node['right'], depth+1)

    verify(witness, 0, root=True)
    assert seen == list(range(LO, HI))
    assert len(witness_edges) == 2*(HI-LO)-2 == 166
    assert max(e['safe_evaluation_bits'] for e in witness_edges) == optimum

    width_hist = Counter(e['safe_evaluation_bits'] for e in witness_edges)
    worst = sorted(
        witness_edges,
        key=lambda e: (-e['safe_evaluation_bits'], -e['function_lambda'], -e['size'], e['lo']),
    )[:24]

    parent = edge(LO, HI)
    out = {
        'position': 'C',
        'order': 'multiplicity_then_function',
        'parent': parent,
        'local_leaves': HI-LO,
        'exact_minimax_safe_width': optimum,
        'root_split': root_split,
        'root_child_subtree_widths': [root_best[4], root_best[5]],
        'witness_edge_count': len(witness_edges),
        'witness_max_depth': max_depth,
        'witness_edge_width_histogram': dict(sorted(width_hist.items())),
        'worst_witness_edges': worst,
        'intervals_evaluated': len(cost_cache),
        'dp_states': len(dp),
        'split_comparisons': split_comparisons,
        'witness': witness,
        'oracle_cache_entries': len(oracle.cache),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_BOTTLENECK_PARENT_MINIMAX_INTERVAL_DP')
    print('scope=exact minimax over every contiguous binary tree on fixed multiplicity-then-function order inside parent [166,250); parent edge excluded from local objective')
    print('important=the reported width is the exact optimum for this fixed order and contiguous-tree class, not unrestricted branchwidth')
    print('next=substitute the exact minimax witness into the full C916 tree and re-evaluate all 498 non-root edges')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
