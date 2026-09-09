#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_phase_overlap_forest as P


def main():
    out = P.analyze()

    assert out['position'] == 'C'
    assert out['physical_shared_dimension'] == 149
    assert out['first_dyadic_term_anchors'] == 340
    assert out['singleton_anchors'] == 103
    assert out['pair_anchors'] == 237
    assert out['component_growth_regression_cases'] == 3
    assert out['stable_first_anchor'] == [0, 0]
    assert out['canonical_singleton_anchor'] == [1, 0]

    r0 = out['rank0']
    assert r0['component_count'] == 9
    assert r0['component_sizes_descending'] == [325, 2, 2, 2, 2, 2, 2, 2, 1]
    assert r0['component_size_histogram'] == {1: 1, 2: 7, 325: 1}
    assert r0['forest_edges'] == 331
    assert r0['forest_edge_polar_rank_histogram'] == {0: 331}

    r2 = out['rank_le_2']
    assert r2['component_count'] == 5
    assert r2['component_sizes_descending'] == [332, 2, 2, 2, 2]
    assert r2['component_size_histogram'] == {2: 4, 332: 1}
    assert r2['component_roots'] == [[0, 0], [158, 0], [180, 0], [236, 0], [238, 0]]
    assert r2['forest_edges'] == 335
    assert r2['forest_edge_polar_rank_histogram'] == {0: 58, 2: 277}

    r4 = out['rank_le_4']
    assert r4['component_count'] == 5
    assert r4['component_sizes_descending'] == [332, 2, 2, 2, 2]
    assert r4['component_size_histogram'] == {2: 4, 332: 1}
    assert r4['component_roots'] == [[0, 0], [158, 0], [180, 0], [236, 0], [238, 0]]
    assert r4['forest_edges'] == 335
    assert r4['forest_edge_polar_rank_histogram'] == {0: 40, 2: 162, 4: 133}

    assert out['rank_le_4_inferred_from_rank_le_2_connected'] is False
    assert out['total_unique_support_pairs_evaluated'] == 57630
    assert out['total_unique_phase_edges_evaluated'] == 6502
    assert out['evaluated_phase_edge_polar_rank_histogram'] == {
        0: 337, 2: 2942, 4: 1993, 6: 1135, 8: 95,
    }
    assert out['evaluated_phase_edge_type_histogram'] == {
        'affine_nonconstant': 337,
        'quadratic_nonconstant': 6165,
    }
    assert out['decision'] == 'FIRST_DYADIC_ANCHOR_PHASE_GRAPH_MULTIPLE_SUPPORT_COMPONENTS'

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHASE_OVERLAP_FOREST_RESULT')
    print('anchors=340')
    print('rank0_components=9')
    print('rank_le_2_components=5')
    print('rank_le_4_components=5')
    print('rank_le_2_component_sizes=[332,2,2,2,2]')
    print('all_support_pairs=57630')
    print('evaluated_phase_edges=6502')
    print('decision=FIRST_DYADIC_ANCHOR_PHASE_GRAPH_MULTIPLE_SUPPORT_COMPONENTS')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
