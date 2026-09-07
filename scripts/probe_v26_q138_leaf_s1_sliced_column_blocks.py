#!/usr/bin/env python3
from pathlib import Path
import sys

import opt_einsum as oe

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_leaf_s1_minor as M

ROW_BITS = 11
COL_BITS = 11
CAP_EXPS = (22, 23, 24, 25, 26, 27, 28, 30, 32)


def path_args(factors, outlabs):
    ids = {}
    q = 0
    for A, ls in factors:
        for x in ls:
            if x not in ids:
                ids[x] = q
                q += 1
    args = []
    for A, ls in factors:
        args.extend([A, [ids[x] for x in ls]])
    args.append([ids[x] for x in outlabs])
    return args


def plan(args, optimize, memory_limit=None):
    kwargs = {'optimize': optimize}
    if memory_limit is not None:
        kwargs['memory_limit'] = memory_limit
    path, info = oe.contract_path(*args, **kwargs)
    return {
        'optimize': optimize,
        'memory_limit': memory_limit,
        'largest': int(info.largest_intermediate),
        'opt_cost': int(info.opt_cost),
        'path_len': len(path),
        'max_step_arity': max((len(step) for step in path), default=0),
    }


def add_record(records, pos, b, blocks, output_elements, p):
    rec = {
        'b_open_column_bits': b,
        'fixed_column_bits': COL_BITS - b,
        'blocks': blocks,
        'output_elements_per_block': output_elements,
        **p,
        'estimated_total_cost': p['opt_cost'] * blocks,
    }
    records.append(rec)
    print('position', pos, 'record', rec, flush=True)


def main():
    words = (0, 0, 0, 0)  # factor shapes only; values do not affect path topology
    summary = {}

    for pos in 'ABCD':
        shift = 7 if pos == 'B' else 0
        S = {(i + shift) % 32 for i in M.BASE_S1}
        T = list(M.flow_complement_terminals(S))
        assert len(S) == ROW_BITS and len(T) == COL_BITS and set(T).isdisjoint(S)
        rowlabs = [f'out_{i}' for i in sorted(S)]
        records = []

        for b in range(COL_BITS + 1):
            # Keep all 11 row bits and only b column-side bits open. The other
            # 11-b column bits are fixed. Their values change tensor entries but
            # not shapes, so one planned path is reusable across all 2^(11-b)
            # exact column blocks.
            open_t = T[:b]
            openbits = S | set(open_t)
            outlabs = rowlabs + [f'out_{i}' for i in open_t]
            factors, _opens = M.single_network(words, pos, openbits)
            args = path_args(factors, outlabs)
            blocks = 1 << (COL_BITS - b)
            output_elements = 1 << (ROW_BITS + b)

            # Uncapped binary baselines. These explain why the first version of
            # this probe had an empty practical Pareto set.
            for opt in ('greedy', 'random-greedy'):
                p = plan(args, opt)
                add_record(records, pos, b, blocks, output_elements, p)

            # Actual practical search: let greedy use high-arity contractions
            # when necessary to obey an explicit element ceiling. We record the
            # resulting arity and work instead of incorrectly rejecting it.
            for cap_exp in CAP_EXPS:
                cap = 1 << cap_exp
                if output_elements > cap:
                    continue
                p = plan(args, 'greedy', memory_limit=cap)
                add_record(records, pos, b, blocks, output_elements, p)

        # For each ceiling choose the least estimated total block work among all
        # planned paths that actually fit. This is the execution-design Pareto
        # table for the next exact numerical minor contraction.
        pareto = {}
        for cap_exp in CAP_EXPS:
            cap = 1 << cap_exp
            feasible = [r for r in records if r['largest'] <= cap]
            if feasible:
                best = min(
                    feasible,
                    key=lambda r: (
                        r['estimated_total_cost'],
                        r['largest'],
                        r['max_step_arity'],
                        r['blocks'],
                    ),
                )
                pareto[cap_exp] = best
        assert pareto, (pos, 'empty memory-capped Pareto set')
        summary[pos] = pareto
        print('position', pos, 'pareto', pareto, flush=True)

    print('summary', summary, flush=True)
    print('PASS PROBE V26_Q138_LEAF_S1_SLICED_COLUMN_BLOCKS_MEMORY_CAPPED', flush=True)
    print('scope=path-only row/column block slicing tradeoff with explicit memory ceilings; no numerical contraction and no leaf-rank claim', flush=True)


if __name__ == '__main__':
    main()
