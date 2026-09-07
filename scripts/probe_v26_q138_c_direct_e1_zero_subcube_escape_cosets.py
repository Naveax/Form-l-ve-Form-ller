#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_bc_direct_e1_aggregate_mod3_rank as G

SUBCUBE_BITS = 12
SUBCUBE_SIZE = 1 << SUBCUBE_BITS


def move_to(target_y, y, groups, phases):
    diff = y ^ target_y
    while diff:
        bit = diff & -diff
        j = bit.bit_length() - 1
        old_y = y
        y ^= 1 << j
        for sdesc, _arr in groups:
            sdesc[2] ^= sdesc[1][j]
        for _gi, pd in phases:
            G.phase_flip(pd, j, old_y)
        diff ^= bit
    return y


def gray_masks(uorder):
    out = []
    for i in range(SUBCUBE_SIZE):
        gray = i ^ (i >> 1)
        y = 0
        for src, j in enumerate(uorder):
            if (gray >> src) & 1:
                y |= 1 << j
        out.append(y)
    return out


def scan_coset(label, base_y, masks, y, groups, phases, global_basis, global_rank):
    local_basis = [None] * G.NROW
    local_rank = 0
    nonzero_columns = 0
    first_nonzero = None

    for i, umask in enumerate(masks):
        target = base_y ^ umask
        y = move_to(target, y, groups, phases)
        one, two = G.aggregate_column(groups)
        if one | two:
            nonzero_columns += 1
            if first_nonzero is None:
                first_nonzero = (i, y, one.bit_count(), two.bit_count())
            if G.insert_mod3(local_basis, one, two):
                local_rank += 1
            if G.insert_mod3(global_basis, one, two):
                global_rank += 1
                if global_rank == G.NROW:
                    print('coset', label,
                          'FULL_GLOBAL_RANK_F3', global_rank,
                          'columns_examined_in_coset', i + 1,
                          'right_beta_coordinate_mask', y,
                          flush=True)
                    return y, local_rank, global_rank, nonzero_columns, first_nonzero, True

    print('coset', label,
          'columns', SUBCUBE_SIZE,
          'nonzero_mod3_columns', nonzero_columns,
          'rank_F3', local_rank,
          'global_rank_F3', global_rank,
          'first_nonzero', first_nonzero,
          flush=True)
    return y, local_rank, global_rank, nonzero_columns, first_nonzero, False


def main():
    pred, groups, phases, order = G.prepare('C')
    uorder = order[:SUBCUBE_BITS]
    escape = order[SUBCUBE_BITS:]
    assert len(escape) == len(G.RIGHT) - SUBCUBE_BITS == 9
    masks = gray_masks(uorder)

    print('zero_subcube_coordinate_bits', [G.RIGHT[j] for j in uorder], flush=True)
    print('escape_coordinate_bits', [G.RIGHT[j] for j in escape], flush=True)

    global_basis = [None] * G.NROW
    global_rank = 0
    y = 0
    results = {}

    # Recheck the admitted exact-zero U on F3 using the same mutable-state
    # traversal that will be used for adjacent cosets. This is a guard against
    # state-transition mistakes in the escape scan; exact zero itself is already
    # certified separately over Z on main.
    y, lr, global_rank, nz, first, full = scan_coset(
        'U', 0, masks, y, groups, phases, global_basis, global_rank
    )
    assert lr == 0 and nz == 0 and not full
    results['U'] = (lr, nz, first)

    for j in escape:
        base = 1 << j
        label = f'U+e{G.RIGHT[j]}'
        y, lr, global_rank, nz, first, full = scan_coset(
            label, base, masks, y, groups, phases, global_basis, global_rank
        )
        results[label] = (lr, nz, first)
        if full:
            print('PASS PROBE V26_Q138_C_DIRECT_E1_ESCAPE_COSETS_FULL_RANK')
            print('theorem=the complete direct-e1 C aggregate has rank_F3=2048 at the deterministic reachable predecessor, hence exact rank_Q=2048')
            print('witness_escape_coset', label)
            print('predecessor_witness_hex', hex(pred))
            print('consequence=no uniform subgeneric rational-rank upper bound exists for the complete direct-e1 C aggregate')
            return

    print('results', results, flush=True)
    print('PASS PROBE V26_Q138_C_DIRECT_E1_ESCAPE_COSETS_LOWER_BOUND')
    print('global_rank_F3_lower_bound', global_rank)
    print('scope=U is the already-certified exact-zero 12-dimensional subcube; nonzero mod3 columns in adjacent single-bit cosets are exact nonzero witnesses, while a mod3-zero coset alone is not an exact-zero theorem')


if __name__ == '__main__':
    main()
