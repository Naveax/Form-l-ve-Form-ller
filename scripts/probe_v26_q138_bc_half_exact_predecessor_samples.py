#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import probe_v26_q138_bc_second_residue_reachable_predecessor_geometry as G
import probe_v26_q138_bc_second_residue_fixed_predecessor_specialization as F
import probe_v26_q138_bc_second_residue_half_exact_right21 as Q

SAMPLES_PER_POSITION = 4


def half_condition_solution(pos):
    _e0_groups, half_can = G.support_groups(pos)
    cond = G.predecessor_condition(half_can)
    sol = T.rref(cond, n=G.PRED_BITS)
    assert sol is not None
    particular, null = sol[1], sol[2]
    assert F.fixed_possible(half_can, particular)
    return half_can, particular, null


def sample_predecessors(pos):
    half_can, particular, null = half_condition_solution(pos)
    cand = [F.WITNESS[pos], particular]
    if null:
        cand.append(particular ^ null[0])
    if len(null) > 1:
        cand.append(particular ^ null[1])
        cand.append(particular ^ null[0] ^ null[1])
    if len(null) > 2:
        cand.append(particular ^ null[-1])

    out = []
    seen = set()
    for p in cand:
        if p in seen:
            continue
        assert F.fixed_possible(half_can, p), (pos, hex(p))
        seen.add(p)
        out.append(p)
        if len(out) == SAMPLES_PER_POSITION:
            break

    assert len(out) == SAMPLES_PER_POSITION, (pos, len(out), len(null))
    return out, len(null)


def main():
    all_ranks = {}
    for pos in 'BC':
        preds, nullity = sample_predecessors(pos)
        ranks = []
        print('position', pos, 'half_predecessor_affine_nullity', nullity,
              'sample_count', len(preds), flush=True)
        for idx, pred in enumerate(preds):
            HB = Q.exact_half_basis(pos, pred)
            rank = len(HB)
            ranks.append(rank)
            print('sample', pos, idx, 'predecessor_hex', hex(pred),
                  'exact_half_rank_F2', rank,
                  'is_current_witness', pred == F.WITNESS[pos], flush=True)
        hist = Counter(ranks)
        all_ranks[pos] = tuple(ranks)
        print('position', pos, 'sample_rank_distribution', dict(sorted(hist.items())),
              'sample_rank_min', min(ranks), 'sample_rank_max', max(ranks), flush=True)

    print('PASS V26_Q138_BC_HALF_EXACT_PREDECESSOR_SAMPLES')
    print('scope=deterministic sample of half-active predecessor affine classes; not a uniform theorem')
    print('B_sample_ranks', all_ranks['B'])
    print('C_sample_ranks', all_ranks['C'])
    print('next=if ranks are stable, prove predecessor-gauge invariance; if not, characterize worst-case half rank')


if __name__ == '__main__':
    main()
