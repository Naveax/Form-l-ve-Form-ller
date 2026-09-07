#!/usr/bin/env python3
from pathlib import Path
import sys

import opt_einsum as oe

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_leaf_s1_minor as M

ROW_BITS = 11
COL_BITS = 11


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


def plan(args, optimize):
    path, info = oe.contract_path(*args, optimize=optimize)
    return {
        'optimize': optimize,
        'largest': int(info.largest_intermediate),
        'opt_cost': int(info.opt_cost),
        'path_len': len(path),
        'max_step_arity': max((len(step) for step in path), default=0),
    }


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

            for opt in ('greedy', 'random-greedy'):
                p = plan(args, opt)
                assert p['max_step_arity'] == 2
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

        # For several practical intermediate ceilings, find the lowest total
        # planned work among binary paths that fit the ceiling.
        pareto = {}
        for cap_exp in (22, 23, 24, 25, 26, 27, 28, 30, 32):
            cap = 1 << cap_exp
            feasible = [r for r in records if r['largest'] <= cap]
            if feasible:
                best = min(feasible, key=lambda r: (r['estimated_total_cost'], r['largest']))
                pareto[cap_exp] = best
        summary[pos] = pareto
        print('position', pos, 'pareto', pareto, flush=True)

    print('summary', summary, flush=True)
    print('PASS PROBE V26_Q138_LEAF_S1_SLICED_COLUMN_BLOCKS', flush=True)
    print('scope=path-only row/column block slicing tradeoff; no numerical contraction and no leaf-rank claim', flush=True)


if __name__ == '__main__':
    main()
