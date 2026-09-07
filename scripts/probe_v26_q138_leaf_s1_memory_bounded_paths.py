#!/usr/bin/env python3
from pathlib import Path
import sys

import opt_einsum as oe

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_leaf_s1_minor as M

OUT_ELEMS = 1 << 22  # 2048 x 2048 final minor
LIMITS = [1 << 24, 1 << 25, 1 << 26, 1 << 27]


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


def one_plan(args, optimize, memory_limit=None):
    path, info = oe.contract_path(
        *args,
        optimize=optimize,
        memory_limit=memory_limit,
    )
    return {
        'optimize': optimize,
        'memory_limit': memory_limit,
        'largest': int(info.largest_intermediate),
        'opt_cost': int(info.opt_cost),
        'path_len': len(path),
        'max_step_arity': max((len(step) for step in path), default=0),
    }


def main():
    results = {}
    words = (0, 0, 0, 0)  # values do not affect the tensor-network shapes

    for pos in 'ABCD':
        shift = 7 if pos == 'B' else 0
        S = {(i + shift) % 32 for i in M.BASE_S1}
        T = M.flow_complement_terminals(S)
        outlabs = [f'out_{i}' for i in sorted(S)] + [f'out_{i}' for i in T]
        assert len(outlabs) == 22
        factors, _opens = M.single_network(words, pos, S | set(T))
        args = path_args(factors, outlabs)

        plans = []
        # Baselines: diagnose the historical greedy path and a stronger
        # stochastic path search. These only plan contractions; no large
        # intermediate tensor is ever materialized by this probe.
        for opt in ('greedy', 'random-greedy-128'):
            p = one_plan(args, opt, None)
            plans.append(p)
            print('position', pos, 'plan', p, flush=True)

        # Force the optimizer to respect explicit element-count ceilings.
        # The final 2048x2048 output itself has 2^22 elements, so every limit
        # below starts with at least a 4x safety margin over the output size.
        for lim in LIMITS:
            for opt in ('greedy', 'random-greedy-128'):
                try:
                    p = one_plan(args, opt, lim)
                except Exception as exc:
                    p = {
                        'optimize': opt,
                        'memory_limit': lim,
                        'error': type(exc).__name__ + ':' + str(exc),
                    }
                plans.append(p)
                print('position', pos, 'plan', p, flush=True)

        finite = [p for p in plans if 'largest' in p]
        assert finite
        best = min(finite, key=lambda p: (p['largest'], p['opt_cost']))
        results[pos] = best
        print('position', pos,
              'final_output_elements', OUT_ELEMS,
              'best_plan', best,
              'best_over_output_ratio', best['largest'] / OUT_ELEMS,
              flush=True)

    print('summary', results, flush=True)
    print('PASS PROBE V26_Q138_LEAF_S1_MEMORY_BOUNDED_PATHS', flush=True)
    print('scope=path planning only; no coefficient contraction and no leaf-rank claim', flush=True)


if __name__ == '__main__':
    main()
