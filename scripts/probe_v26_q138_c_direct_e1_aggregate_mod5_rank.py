#!/usr/bin/env python3
import sys
from pathlib import Path

import numpy as np
from flint import nmod_mat

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_bc_direct_e1_aggregate_mod3_rank as G

P = 5
MAX_COLUMNS = 4096
CHECKPOINT = 2048


def add_signed_mod5(digits, positive, negative):
    # digits[k] is the exact row mask currently carrying residue k mod 5.
    # Adding +1 rotates positive rows upward; adding -1 rotates negative rows
    # downward. All masks remain disjoint and cover the full 2048-row universe.
    used = positive | negative
    keep = (~used) & G.ALL
    old = digits
    return [
        (old[k] & keep)
        | (old[(k - 1) % P] & positive)
        | (old[(k + 1) % P] & negative)
        for k in range(P)
    ]


def aggregate_column_mod5(groups):
    digits = [G.ALL, 0, 0, 0, 0]
    for sdesc, arr in groups:
        sm = G.support_mask(sdesc)
        if not sm:
            continue
        for pd in arr:
            q = G.phase_bits(pd)
            neg = sm & q
            pos = sm & (q ^ G.ALL)
            digits = add_signed_mod5(digits, pos, neg)
    cover = 0
    for d in digits:
        assert not (cover & d)
        cover |= d
    assert cover == G.ALL
    return digits


def write_column(M, j, digits):
    # Residue zero is already the uint8 default. Set only nonzero row entries.
    for value in range(1, P):
        mask = digits[value]
        while mask:
            b = mask & -mask
            M[b.bit_length() - 1, j] = value
            mask ^= b


def rank_mod5(M, ncols):
    rows = M[:, :ncols].tolist()
    return nmod_mat(rows, P).rank()


def main():
    pred, groups, phases, order = G.prepare('C')
    M = np.zeros((G.NROW, MAX_COLUMNS), dtype=np.uint8)
    y = 0
    prev_gray = 0
    nonzero_columns = 0

    for i in range(MAX_COLUMNS):
        if i:
            gray = i ^ (i >> 1)
            delta = gray ^ prev_gray
            src = delta.bit_length() - 1
            j = order[src]
            old_y = y
            y ^= 1 << j
            for sdesc, _arr in groups:
                sdesc[2] ^= sdesc[1][j]
            for _gi, pd in phases:
                G.phase_flip(pd, j, old_y)
            prev_gray = gray

        digits = aggregate_column_mod5(groups)
        if digits[0] != G.ALL:
            nonzero_columns += 1
        write_column(M, i, digits)

        if i + 1 in (64, 256, 512, 1024, 1536):
            print('columns_built', i + 1,
                  'nonzero_mod5_columns', nonzero_columns, flush=True)

        if i + 1 == CHECKPOINT:
            r = rank_mod5(M, CHECKPOINT)
            print('position C',
                  'predecessor_witness_hex', hex(pred),
                  'columns_examined', CHECKPOINT,
                  'nonzero_mod5_columns', nonzero_columns,
                  'rank_F5', r, flush=True)
            if r == G.NROW:
                print('PASS PROBE V26_Q138_C_DIRECT_E1_AGGREGATE_MOD5_FULL_RANK')
                print('theorem=reachable-predecessor complete direct-e1 C aggregate has rank_F5=2048, hence exact rank_Q=2048')
                print('consequence=the mod3 zero image is prime-specific divisibility, not rational aggregate cancellation')
                return

    r = rank_mod5(M, MAX_COLUMNS)
    print('position C',
          'predecessor_witness_hex', hex(pred),
          'columns_examined', MAX_COLUMNS,
          'nonzero_mod5_columns', nonzero_columns,
          'rank_F5', r, flush=True)
    if r == G.NROW:
        print('PASS PROBE V26_Q138_C_DIRECT_E1_AGGREGATE_MOD5_FULL_RANK')
        print('theorem=reachable-predecessor complete direct-e1 C aggregate has rank_F5=2048, hence exact rank_Q=2048')
        print('consequence=the mod3 zero image is prime-specific divisibility, not rational aggregate cancellation')
    else:
        print('PASS PROBE V26_Q138_C_DIRECT_E1_AGGREGATE_MOD5_LOWER_BOUND')
        print('scope=exact F5 lower bound on the same deterministic sampled-column family; non-full result is not an upper bound')


if __name__ == '__main__':
    main()
