#!/usr/bin/env python3
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_factor_generation85 as F
import verify_v26_q138_double_round_signed85 as S


def main():
    R = 3829 * (2 ** 29)
    assert R == 2055678722048
    rlog = math.log2(R)
    assert abs(rlog - (29 + math.log2(3829))) < 1e-12

    physical_rows = 2 ** 44
    leaf_states = 2 ** 44
    central_columns = 2 ** 51  # exact S1/complement central graph boundary
    assert F.gb(S.S1) == 51

    # Coefficient-aware materialized left/right factor table at the new rank.
    table = R * leaf_states
    table_exp = math.log2(table)
    assert table == 3829 * (2 ** 73)
    assert abs(table_exp - (73 + math.log2(3829))) < 1e-12

    # Generic exact row-basis construction without materializing the full
    # 2^44 x 2^51 central matrix:
    # scan physical rows and columns through the exact central-entry oracle,
    # keep a pivot minor/inverse of size at most R x R, and retain actual
    # physical rows as the row basis. If the true rank is r<R, every bound only
    # decreases. Arithmetic work may be astronomical; this ledger is memory/message.
    pivot_square = R * R
    assert math.log2(pivot_square) == 2 * rlog
    assert pivot_square < table

    # Even materializing one complete physical central row is far below table.
    assert central_columns < table

    # The physical-row -> rank-coordinate transform has at most 2^44 * R
    # scalars, exactly the same envelope as the materialized factor table.
    transform = physical_rows * R
    assert transform == table

    # Selected rank basis consists of actual physical S1 rows, so one right
    # factor entry can reuse the clean 21-site complement contraction. Its
    # coefficient-aware message peak remains80; leaf generation remains44.
    root, sets = F.walk(F.RIGHT_TREE, True)
    assert root == F.COMP
    peak = max(F.ccost(A) for A in sets + [{i} for i in F.COMP])
    assert peak == 80
    assert max(peak, 51, 44, math.log2(pivot_square)) < table_exp

    print('PASS V26_Q138_FACTOR_GENERATION_RANK3829')
    print('central_rank_upper_bound=3829*2^29 log2=%.15f' % rlog)
    print('materialized_factor=3829*2^73 log2=%.15f' % table_exp)
    print('streaming_exact_Gaussian_pivot_inverse_log2=%.15f' % math.log2(pivot_square))
    print('physical_to_rank_transform_entries=2^44*R = factor-table envelope')
    print('single_physical_central_row=2^51 entries')
    print('right_complement_entry_generation_peak=80')
    print('W_factor_gen<=%.15f' % table_exp)
    print('scope=coefficient-aware materialized-factor memory/message constructivity; arithmetic work is not bounded/reduced')


if __name__ == '__main__':
    main()
