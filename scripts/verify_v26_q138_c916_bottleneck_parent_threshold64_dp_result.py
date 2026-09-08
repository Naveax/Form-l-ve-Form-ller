#!/usr/bin/env python3
import probe_v26_q138_c916_bottleneck_parent_threshold64_dp as P


def main():
    out = P.analyze()
    assert out['position'] == 'C'
    assert out['order'] == 'multiplicity_then_function'
    assert out['parent'] == {'lo': 166, 'hi': 250, 'size': 84}
    assert out['target_bits'] == 64
    assert out['direct_root_splits_le_64'] == 36
    assert out['threshold64_feasible'] is True
    assert out['witness']['lo'] == 166 and out['witness']['hi'] == 250
    assert out['witness']['split'] == 167
    assert out['witness_edge_count'] == 166
    assert out['witness_max_safe_bits'] == 59
    assert out['witness_max_depth'] == 22
    assert out['interval_costs_evaluated'] == 1534
    assert out['feasibility_states_cached'] == 166
    assert out['oracle_cache_entries'] == 1534
    worst = out['worst_witness_edges']
    assert worst[0]['lo'] == 179 and worst[0]['hi'] == 250
    assert worst[0]['safe_evaluation_bits'] == 59
    assert worst[0]['function_lambda'] == 63
    assert worst[0]['digest'] == '95b3fcf51ed806d0'
    assert worst[1]['lo'] == 179 and worst[1]['hi'] == 244
    assert worst[1]['safe_evaluation_bits'] == 59
    assert worst[1]['digest'] == '4809b3aae6e11ab7'
    print('PASS V26_Q138_C916_BOTTLENECK_PARENT_THRESHOLD64_DP_RESULT')
    print('exact=threshold64 feasible; witness has 166 non-root edges, root split 167, actual max safe width 59, depth 22')
    print('decision=replace threshold sweep with exact minimax interval DP to determine the minimum fixed-order local width')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
