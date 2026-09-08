#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_predecessor_leaf_bc_second_residue_support_frequency_nesting as N
import verify_v26_q138_predecessor_leaf_bc_second_residue_rank812_972 as R
import probe_v26_q138_bc_e0_reachable_half_relaxed_zz as Z
import probe_v26_q138_bc_uniform_half_lift_third_carry as H

POS = 'C'
FULL = 2048


def xor_sumset(U):
    vals = tuple(sorted(U))
    out = set()
    for i, a in enumerate(vals):
        for b in vals[i:]:
            out.add(a ^ b)
            if len(out) == FULL:
                return out, (i, a, b)
    return out, None


def fourier_support(mask):
    return {i for i, x in enumerate(R.fwht(mask)) if x}


def shifted_union(U, V):
    out = set()
    for i, a in enumerate(sorted(U)):
        for b in V:
            out.add(a ^ b)
        if len(out) == FULL:
            return out, i
    return out, None


def analyze():
    U = N.weight120_union(POS)
    assert len(U) == 788

    support_sumset, support_sat = xor_sumset(U)

    reachable, canonical, estats = Z.reachable_e0_basis(POS)
    assert len(reachable) == 388
    assert len(canonical) == 388

    items = list(reachable.values())
    pair_hull, pair_tests, pair_sat = H.pairwise_intersection_basis(items)
    assert len(pair_hull) == 1848

    spectrum = set()
    spectrum_full_after = None
    spectrum_hist = []
    for i, v in enumerate(items):
        spectrum |= fourier_support(v)
        if i < 8 or (i + 1) % 32 == 0 or len(spectrum) == FULL:
            spectrum_hist.append((i + 1, len(spectrum)))
        if len(spectrum) == FULL:
            spectrum_full_after = i + 1
            break

    cross, cross_full_after_u = shifted_union(U, spectrum)

    out = {
        'position': POS,
        'support_frequency_dim': len(U),
        'support_carry_xor_sumset_size': len(support_sumset),
        'support_carry_sumset_saturated': len(support_sumset) == FULL,
        'support_carry_saturation_witness': support_sat,
        'reachable_sign_basis_dim': len(items),
        'reachable_sign_pairwise_truth_hull_dim': len(pair_hull),
        'reachable_sign_pairwise_pairs_tested': pair_tests,
        'reachable_sign_pairwise_saturation_pair': pair_sat,
        'reachable_sign_fourier_union_size': len(spectrum),
        'reachable_sign_fourier_union_full_after_basis_vectors': spectrum_full_after,
        'support_times_sign_shift_union_size': len(cross),
        'support_times_sign_shift_union_saturated': len(cross) == FULL,
        'support_times_sign_shift_union_full_after_support_index': cross_full_after_u,
        'spectrum_growth_samples': spectrum_hist,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_COARSE_CARRY_OBSTRUCTION')
    print('scope=coarse componentwise third-carry diagnostics for C916: support-only Walsh sumset, reachable-sign ambient pairwise truth hull, and support-times-sign Fourier product envelope')
    print('important=any saturation here is an obstruction to the corresponding componentwise ambient-envelope route, not a lower bound on the true joint realized C2 span')
    print('not_included=no exact joint second-lift carry, no complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


def main():
    analyze()


if __name__ == '__main__':
    main()
