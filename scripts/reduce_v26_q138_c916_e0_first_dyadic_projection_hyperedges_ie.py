#!/usr/bin/env python3
import glob, json, math, os
from pathlib import Path

PAIRWISE_TOTAL = 667251639197063986752771721653766635157388976602589789841148591163677039001600000
BONFERRONI_LOWER = 2722414587159602541040697551354574968461239522793839001600000
BONFERRONI_UPPER = 441205873912093509972717475553434060732158565102084857212293988604025199001600000
SHARDS = int(os.environ.get('C916_IE_SHARDS', '4'))
GLOB = os.environ.get('C916_IE_GLOB', 'results/ie_shard_*.json')
OUT = Path(os.environ.get('C916_IE_REDUCED_OUT', 'out/c916_projection_hyperedges_ie_exact.json'))
ZERO_EVENT_PAIRS = (
    (0,7), (0,8), (1,3), (2,5), (2,6), (2,9), (2,10),
    (3,7), (3,8), (5,9), (5,10), (6,9), (6,10),
)


def analyze():
    paths = sorted(glob.glob(GLOB))
    assert len(paths) == SHARDS, (len(paths), SHARDS, paths)
    rows = [json.loads(Path(p).read_text()) for p in paths]
    assert {int(r['shard']) for r in rows} == set(range(SHARDS))
    assert {int(r['shards']) for r in rows} == {SHARDS}
    assert {int(r['pairwise_exact_baseline_count']) for r in rows} == {PAIRWISE_TOTAL}
    assert {tuple(r['hard_profiles']) for r in rows} == {(251, 288, 302)}
    assert {int(r['event_pair_zero_authority_run']) for r in rows} == {34826179077}
    assert {tuple(tuple(p) for p in r['zero_event_pairs']) for r in rows} == {ZERO_EVENT_PAIRS}
    assert {int(r['full_ie_subset_terms']) for r in rows} == {4096}
    assert {int(r['admissible_ie_subset_terms']) for r in rows} == {384}
    assert {int(r['zero_pair_pruned_terms']) for r in rows} == {3712}

    total_terms = sum(int(r['assigned_subset_terms']) for r in rows)
    total_even = sum(int(r['assigned_even_terms']) for r in rows)
    total_odd = sum(int(r['assigned_odd_terms']) for r in rows)
    assert total_terms == 384
    assert total_even == total_odd == 192

    plus = sum(int(r['global_ie_plus_partial']) for r in rows)
    minus = sum(int(r['global_ie_minus_partial']) for r in rows)
    exact = plus - minus
    assert 0 < exact < PAIRWISE_TOTAL
    assert BONFERRONI_LOWER <= exact <= BONFERRONI_UPPER

    log2 = math.log2(exact)
    result = {
        'position': 'C',
        'physical_shared_dimension': 149,
        'projection_events': 12,
        'projection_minimal_empty_triples': 5,
        'projection_minimal_empty_quadruples': 7,
        'full_inclusion_exclusion_subset_terms': 4096,
        'exact_zero_pair_pruned_terms': 3712,
        'evaluated_inclusion_exclusion_subset_terms': 384,
        'evaluated_even_terms': total_even,
        'evaluated_odd_terms': total_odd,
        'zero_event_pairs': [list(p) for p in ZERO_EVENT_PAIRS],
        'event_pair_zero_authority_run': 34826179077,
        'ie_even_sum': plus,
        'ie_odd_sum': minus,
        'exact_count': exact,
        'exact_log2': log2,
        'state_bits': exact.bit_length(),
        'pairwise_exact_baseline_count': PAIRWISE_TOTAL,
        'gain_vs_pairwise_exact_log2_bits': math.log2(PAIRWISE_TOTAL) - log2,
        'bonferroni_lower_authority': BONFERRONI_LOWER,
        'bonferroni_upper_authority': BONFERRONI_UPPER,
        'bonferroni_authority_run': 34826179077,
        'shards': SHARDS,
        'shard_signed_partials': [
            {'shard': int(r['shard']), 'signed_partial': int(r['global_signed_partial'])}
            for r in sorted(rows, key=lambda x: int(x['shard']))
        ],
        'decision': 'C916_250WAY_COMPLETE_M4_PAIRWISE_PLUS_12_PROJECTION_HYPEREDGES_SPARSE_IE_EXACT',
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print('result', json.dumps(result, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PROJECTION_HYPEREDGES_SPARSE_IE_EXACT')
    print('scope=all 4005 exact m4 pairwise value factors plus five minimal-empty projection triples and seven minimal-empty projection quadruples; 3712 of the 4096 IE subsets vanish exactly because they contain one of 13 exact zero event-pair intersections, and the remaining 384 terms are counted exactly')
    print('boundary=all-order affine intersection and any further higher-order physical-image constraint remain outside this finite-hyperedge model')
    print('ALPHA_PASS=0')
    return result


if __name__ == '__main__':
    analyze()
