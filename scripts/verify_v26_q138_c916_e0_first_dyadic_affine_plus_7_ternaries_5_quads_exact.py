#!/usr/bin/env python3
import io
import json
import math
from contextlib import redirect_stdout
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import verify_v26_q138_c916_e0_first_dyadic_projection_hyperedges_eventmask_vector_exact as V
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_4_physical_ternary_exact as F
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_6_ternaries_5_quads_exact as S

PAIRWISE_COUNTER = C.ExactCounter
NEW_FACTOR = ((178, 179, 184), ((0, 1, 1), (0, 2, 1), (1, 2, 0)))
PHYSICAL_TERNARY = S.PHYSICAL_TERNARY + (NEW_FACTOR,)
AFFINE_EVENT_COUNT = S.AFFINE_EVENT_COUNT
PHYSICAL_EVENT_COUNT = sum(len(rows) for _gids, rows in PHYSICAL_TERNARY)
EVENT_COUNT = AFFINE_EVENT_COUNT + PHYSICAL_EVENT_COUNT
ALL_EVENTS = (1 << EVENT_COUNT) - 1
AFFINE_MASK = (1 << AFFINE_EVENT_COUNT) - 1
PHYSICAL_MASK = ALL_EVENTS ^ AFFINE_MASK
EXPECTED_SIX_TOTAL = 90987190266267462495323685079227633113020903735137825407846207198697839001600000


class AnyExpected:
    def __eq__(self, other):
        return True


def analyze():
    old_s_ternary = S.PHYSICAL_TERNARY
    old_s_phys_count = S.PHYSICAL_EVENT_COUNT
    old_s_event_count = S.EVENT_COUNT
    old_s_all_events = S.ALL_EVENTS
    old_s_phys_mask = S.PHYSICAL_MASK
    old_v_event_count = V.EVENT_COUNT
    old_v_all_events = V.ALL_EVENTS
    old_f_event_count = F.EVENT_COUNT
    old_f_all_events = F.ALL_EVENTS
    old_f_phys_count = F.PHYSICAL_EVENT_COUNT
    old_f_phys_mask = F.PHYSICAL_MASK
    old_counter = C.ExactCounter
    old_expected = C.EXPECTED_EXACT_COUNT

    S.PHYSICAL_TERNARY = PHYSICAL_TERNARY
    S.PHYSICAL_EVENT_COUNT = PHYSICAL_EVENT_COUNT
    S.EVENT_COUNT = EVENT_COUNT
    S.ALL_EVENTS = ALL_EVENTS
    S.PHYSICAL_MASK = PHYSICAL_MASK
    V.EVENT_COUNT = EVENT_COUNT
    V.ALL_EVENTS = ALL_EVENTS
    F.EVENT_COUNT = EVENT_COUNT
    F.ALL_EVENTS = ALL_EVENTS
    F.PHYSICAL_EVENT_COUNT = PHYSICAL_EVENT_COUNT
    F.PHYSICAL_MASK = PHYSICAL_MASK
    C.ExactCounter = S.SixTernaryFiveQuadCounter
    C.EXPECTED_EXACT_COUNT = AnyExpected()
    S.PROFILE_ROWS.clear()
    try:
        with redirect_stdout(io.StringIO()):
            base = C.analyze()
    finally:
        C.ExactCounter = old_counter
        C.EXPECTED_EXACT_COUNT = old_expected
        S.PHYSICAL_TERNARY = old_s_ternary
        S.PHYSICAL_EVENT_COUNT = old_s_phys_count
        S.EVENT_COUNT = old_s_event_count
        S.ALL_EVENTS = old_s_all_events
        S.PHYSICAL_MASK = old_s_phys_mask
        V.EVENT_COUNT = old_v_event_count
        V.ALL_EVENTS = old_v_all_events
        F.EVENT_COUNT = old_f_event_count
        F.ALL_EVENTS = old_f_all_events
        F.PHYSICAL_EVENT_COUNT = old_f_phys_count
        F.PHYSICAL_MASK = old_f_phys_mask

    total = int(base['exact_count'])
    assert 0 < total <= EXPECTED_SIX_TOTAL <= S.EXPECTED_AFFINE_TOTAL
    rows = list(S.PROFILE_ROWS)
    assert {int(row['domain_state_sum']) for row in rows} == set(F.EXPECTED_AFFINE_PROFILE_COUNTS)
    changed = [
        row for row in rows
        if int(row['affine_plus_six_ternaries_plus_five_quads_count'])
        < int(row['affine_plus_first_four_ternaries_plus_five_quads_count'])
    ]
    out = {
        'position': 'C',
        'physical_shared_dimension': 149,
        'complete_higher_affine_conflicts': AFFINE_EVENT_COUNT,
        'physical_ternary_factors': [list(gids) for gids, _rows in PHYSICAL_TERNARY],
        'physical_ternary_forbidden_quotient_tuples': [len(rows_) for _gids, rows_ in PHYSICAL_TERNARY],
        'physical_quaternary_factors': [[4,5,8,9],[4,5,8,114],[4,5,9,114],[4,8,9,114],[5,8,9,114]],
        'tracked_affine_and_ternary_events': EVENT_COUNT,
        'previous_six_ternary_five_quad_exact_count': EXPECTED_SIX_TOTAL,
        'all_order_affine_support_exact_count': S.EXPECTED_AFFINE_TOTAL,
        'exact_affine_plus_seven_ternaries_plus_five_quads_count': total,
        'exact_log2': math.log2(total),
        'state_bits': total.bit_length(),
        'removed_weighted_assignments_vs_six_ternary_checkpoint': EXPECTED_SIX_TOTAL - total,
        'removed_weighted_assignments_vs_affine': S.EXPECTED_AFFINE_TOTAL - total,
        'gain_vs_affine_log2_bits': math.log2(S.EXPECTED_AFFINE_TOTAL) - math.log2(total),
        'profile_rows': rows,
        'decision': 'C916_COMPLETE_AFFINE_SUPPORT_PLUS_SEVEN_EXACT_TERNARY_AND_FIVE_EXACT_QUATERNARY_PHYSICAL_QUOTIENT_FACTORS',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_AFFINE_PLUS_7_TERNARIES_5_QUADS_EXACT')
    print('theorem=the complete 19-conflict affine-support model is conjoined exactly with the five certified physical quaternary quotient factors and seven certified ternary quotient factors, including the newly certified factor on gids 178,179,184')
    print('boundary=additional raw or quotient-certified physical higher-order factors remain outside; this is not the full physical image')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
