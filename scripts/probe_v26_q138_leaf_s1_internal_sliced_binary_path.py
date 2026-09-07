#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import sys

import numpy as np
import opt_einsum as oe

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_leaf_s1_minor as M

ROW_BITS = 11
COL_BITS = 11
TARGET_POS = 'C'
B_OPEN_VALUES = (0, 2, 7)
CAP_EXPS = (28, 30, 32)
MAX_INTERNAL_SLICES = 24
LOOKAHEAD = 8


def path_args(factors, outlabs):
    ids = {}
    q = 0
    for _A, ls in factors:
        for x in ls:
            if x not in ids:
                ids[x] = q
                q += 1
    args = []
    for A, ls in factors:
        args.extend([A, [ids[x] for x in ls]])
    args.append([ids[x] for x in outlabs])
    return ids, args


def binary_plan(factors, outlabs):
    ids, args = path_args(factors, outlabs)
    path, info = oe.contract_path(*args, optimize='greedy')
    max_arity = max((len(step) for step in path), default=0)
    assert max_arity <= 2, max_arity
    return ids, path, {
        'largest': int(info.largest_intermediate),
        'opt_cost': int(info.opt_cost),
        'path_len': len(path),
        'max_step_arity': max_arity,
    }


def symbolic_peak(factors, outlabs, path):
    """Replay the existing pairwise tensordot semantics using label sets.

    normalize_edges() makes every summed internal label degree two. The current
    numerical executor contracts every common label of each selected pair, so a
    set replay is exact for intermediate shape accounting. Open logical output
    names are never candidates for internal slicing.
    """
    work = [set(ls) for _A, ls in factors]
    best_size = -1
    best_labels = set()
    for step in path:
        assert len(step) == 2, step
        i, j = sorted(step, reverse=True)
        B = work.pop(i)
        A = work.pop(j)
        common = A & B
        C = (A | B) - common
        work.append(C)
        size = 1 << len(C)
        if size > best_size:
            best_size = size
            best_labels = set(C)
    assert len(work) == 1
    assert work[0] == set(outlabs), (sorted(work[0]), sorted(outlabs))
    return best_size, best_labels


def slice_label_zero(factors, label):
    """Fix one summed binary internal label to zero for topology/path planning.

    The full exact contraction is recovered by summing the same sliced network
    over both values of every selected label. Values do not affect path shapes,
    so zero is sufficient for planning and the final work estimate multiplies by
    2**number_of_internal_slices.
    """
    out = []
    hits = 0
    for A, ls0 in factors:
        ls = list(ls0)
        if label in ls:
            axis = ls.index(label)
            A = np.take(A, 0, axis=axis)
            ls.pop(axis)
            hits += 1
        out.append((A, ls))
    assert hits == 2, (label, hits)
    return out


def internal_frontier_candidates(factors, outlabs, peak_labels):
    counts = Counter(x for _A, ls in factors for x in ls)
    outs = set(outlabs)
    return sorted(
        x for x in peak_labels
        if x not in outs and not x.startswith('out') and counts[x] == 2
    )


def shortlist(labels, n=LOOKAHEAD):
    labels = sorted(labels)
    if len(labels) <= n:
        return labels
    if n == 1:
        return [labels[len(labels) // 2]]
    idx = [round(i * (len(labels) - 1) / (n - 1)) for i in range(n)]
    return list(dict.fromkeys(labels[i] for i in idx))


def run_case(pos, b_open):
    words = (0, 0, 0, 0)  # shapes only; fixed values do not affect path topology
    shift = 7 if pos == 'B' else 0
    S = {(i + shift) % 32 for i in M.BASE_S1}
    T = list(M.flow_complement_terminals(S))
    assert len(S) == ROW_BITS and len(T) == COL_BITS and set(T).isdisjoint(S)

    open_t = T[:b_open]
    openbits = S | set(open_t)
    outlabs = [f'out_{i}' for i in sorted(S)] + [f'out_{i}' for i in open_t]
    factors, _opens = M.single_network(words, pos, openbits)

    blocks = 1 << (COL_BITS - b_open)
    output_elements = 1 << (ROW_BITS + b_open)
    sliced = []
    records = []

    for k in range(MAX_INTERNAL_SLICES + 1):
        _ids, path, plan = binary_plan(factors, outlabs)
        peak_size, peak_labels = symbolic_peak(factors, outlabs, path)
        assert peak_size == plan['largest'], (peak_size, plan['largest'])

        rec = {
            'position': pos,
            'b_open_column_bits': b_open,
            'fixed_column_bits': COL_BITS - b_open,
            'column_blocks': blocks,
            'output_elements_per_block': output_elements,
            'internal_slices': k,
            'slice_assignments': 1 << k,
            'sliced_labels': tuple(sliced),
            **plan,
            'estimated_total_cost': plan['opt_cost'] * blocks * (1 << k),
        }
        records.append(rec)
        print('record', rec, flush=True)

        if k == MAX_INTERNAL_SLICES:
            break

        candidates = internal_frontier_candidates(factors, outlabs, peak_labels)
        if not candidates:
            print('no_internal_frontier_candidate', pos, b_open, k, flush=True)
            break

        best = None
        for label in shortlist(candidates):
            trial = slice_label_zero(factors, label)
            _trial_ids, trial_path, trial_plan = binary_plan(trial, outlabs)
            trial_peak, _trial_labels = symbolic_peak(trial, outlabs, trial_path)
            assert trial_peak == trial_plan['largest']
            key = (trial_plan['largest'], trial_plan['opt_cost'], label)
            if best is None or key < best[0]:
                best = (key, label, trial, trial_plan)
        assert best is not None
        _key, label, factors, trial_plan = best
        sliced.append(label)
        print(
            'choose_internal_slice',
            'position', pos,
            'b_open', b_open,
            'k_next', k + 1,
            'label', label,
            'next_largest', trial_plan['largest'],
            'next_opt_cost', trial_plan['opt_cost'],
            flush=True,
        )

    pareto = {}
    for cap_exp in CAP_EXPS:
        cap = 1 << cap_exp
        feasible = [
            r for r in records
            if r['largest'] <= cap and r['output_elements_per_block'] <= cap
        ]
        if feasible:
            pareto[cap_exp] = min(
                feasible,
                key=lambda r: (
                    r['estimated_total_cost'],
                    r['largest'],
                    r['internal_slices'],
                ),
            )
    print('case_pareto', pos, b_open, pareto, flush=True)
    return records, pareto


def main():
    summary = {}
    for b_open in B_OPEN_VALUES:
        _records, pareto = run_case(TARGET_POS, b_open)
        summary[b_open] = pareto

    print('summary', summary, flush=True)
    print('PASS PROBE V26_Q138_LEAF_S1_INTERNAL_SLICED_BINARY_PATH', flush=True)
    print(
        'scope=path-only exact internal-index slicing plus output-column blocks; '
        'all contraction steps binary; total work includes 2^k internal slice assignments; '
        'no numerical contraction and no leaf-rank claim',
        flush=True,
    )


if __name__ == '__main__':
    main()
