#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_bc_half_uniform_linear_state_relaxed_scalar as U
import probe_v26_q138_bc_uniform_half_lift_third_carry as H
import probe_v26_q138_bc_canonical_e0_half_third_carry_degree4 as C4
import probe_v26_q138_bc_e0_reachable_half_relaxed_zz as Z

POS = 'C'
MAX_DEGREE = 4
K9_REPEATED_TARGET = 650


def analyze():
    pos = POS
    st = H.half_state_setup(pos)
    halfB, hstats = H.relaxed_half_basis(st)
    assert len(halfB) == 144

    reachable, canonical, estats = Z.reachable_e0_basis(pos)
    assert len(reachable) == 388
    assert len(canonical) == 388

    reachable_union = S.union_basis(reachable, halfB)
    assert len(reachable_union) == len(reachable)
    assert set(reachable_union.values()) == set(reachable.values())

    items, piv = H.coordinate_solver(reachable)
    assert all(H.coordinates(v, piv) is not None for v in halfB.values())

    support = U.N.weight120_union(pos)
    assert len(support) == 788
    reachable_qr, comp = U.R.quotient_rank(reachable, support)
    canonical_qr, canonical_comp = U.R.quotient_rank(canonical, support)
    assert comp == canonical_comp
    assert canonical_qr == 148
    assert reachable_qr == 128
    assert len(support) + reachable_qr == 916

    pair_hull, pair_tests, pair_sat = H.pairwise_intersection_basis(items)
    print(
        'position', pos,
        'half_basis_stats', hstats,
        'reachable_grouped_e0_basis_dim', len(items),
        'reachable_exact_ZZ_quotient', reachable_qr,
        'reachable_second_lift_total', len(support) + reachable_qr,
        'canonical_exact_ZZ_quotient', canonical_qr,
        'Walsh_complement_coordinates', comp,
        'reachable_pairwise_intersections_tested', pair_tests,
        'reachable_pairwise_intersection_hull_GF2_dim<=', len(pair_hull),
        'reachable_pairwise_hull_saturation_pair', pair_sat,
        'k9_repeated_target', K9_REPEATED_TARGET,
        flush=True,
    )

    if len(pair_hull) <= K9_REPEATED_TARGET:
        print(
            'result',
            {
                'mode': 'pairwise_hull_target_met',
                'pairwise_hull': len(pair_hull),
                'second_lift_total': 916,
            },
            flush=True,
        )
        return {
            'mode': 'pairwise_hull_target_met',
            'pairwise_hull': len(pair_hull),
            'degree4_carry_span': None,
            'second_lift_total': 916,
        }

    image_basis = st['image_basis']
    syndrome_bits = st['syndrome_bits']
    syndrome_mask = st['syndrome_mask']
    eq_masks = H.support_projection_equations(image_basis, syndrome_bits)

    carry_span = {}
    coord_cache = {0: 0}
    carry_cache = {0: 0}
    feasible_fibers = 0
    nonzero_fibers = 0
    scalar_fibers = 0
    carry_evaluations = 0
    anf_coefficients = 0
    max_fiber_dim = 0
    max_subset_evaluations = 0

    def eval_carry(state, scalarpat, sm):
        nonlocal carry_evaluations
        freqs = U.unpack_freqs(state, syndrome_bits)
        qs = []
        for i in range(4):
            q = st['qbase'][i] ^ S.WALSH[freqs[i]]
            if (scalarpat >> i) & 1:
                q ^= S.ALL
            qs.append(q)
        vec = sm & U.E.half_correction(qs)
        carry_evaluations += 1

        coeff = coord_cache.get(vec)
        if coeff is None:
            coeff = H.coordinates(vec, piv)
            assert coeff is not None, 'half vector escaped reachable C=916 basis'
            coord_cache[vec] = coeff

        carry = carry_cache.get(coeff)
        if carry is None:
            carry = H.xor_lift_carry(coeff, items, vec)
            carry_cache[coeff] = carry
        return carry

    for sigma in range(1 << syndrome_bits):
        eq = [(eq_masks[e], (sigma >> e) & 1) for e in range(syndrome_bits)]
        fib = U.T.rref(eq, n=len(image_basis))
        if fib is None:
            continue
        feasible_fibers += 1
        coeff0, coeff_null = fib[1], fib[2]
        max_fiber_dim = max(max_fiber_dim, len(coeff_null))

        state0 = H.state_from_coeff(image_basis, coeff0)
        dirs = [H.state_from_coeff(image_basis, d) for d in coeff_null]
        assert (state0 & syndrome_mask) == sigma
        assert all((d & syndrome_mask) == 0 for d in dirs)

        synd = st['rhsbits'] ^ sigma
        sm = U.F.left_support_mask(st['eqs'], synd)
        if sm == 0:
            continue
        nonzero_fibers += 1

        masks = C4.subset_masks_upto(len(dirs), MAX_DEGREE)
        max_subset_evaluations = max(max_subset_evaluations, len(masks))

        for scalarpat in range(16):
            scalar_fibers += 1
            anf = {}
            for mask in masks:
                state = C4.state_with_mask(state0, dirs, mask)
                a = eval_carry(state, scalarpat, sm)
                if mask:
                    for sub in C4.proper_subsets(mask):
                        a ^= anf[sub]
                anf[mask] = a
                S.insert(carry_span, a)
                anf_coefficients += 1

            probes = []
            full = (1 << len(dirs)) - 1
            probes.append(full)
            if len(dirs) >= 5:
                probes.append((1 << 5) - 1)
            if len(dirs) >= 7:
                probes.append(sum(1 << j for j in range(0, len(dirs), 2)))
                probes.append(sum(1 << j for j in range(1, len(dirs), 2)))
            for mask in dict.fromkeys(probes):
                predicted = 0
                for mon, coef in anf.items():
                    if mon & ~mask == 0:
                        predicted ^= coef
                actual = eval_carry(
                    C4.state_with_mask(state0, dirs, mask),
                    scalarpat,
                    sm,
                )
                assert predicted == actual, (sigma, scalarpat, mask)

    out = {
        'mode': 'degree4_exact_relaxed_family',
        'reachable_pairwise_hull': len(pair_hull),
        'reachable_half_induced_third_carry_GF2_span': len(carry_span),
        'k9_repeated_target': K9_REPEATED_TARGET,
        'target_met_by_half_only_carry_span': len(carry_span) <= K9_REPEATED_TARGET,
        'second_lift_total': 916,
        'feasible_support_fibers': feasible_fibers,
        'nonzero_support_fibers': nonzero_fibers,
        'scalar_fibers': scalar_fibers,
        'max_fiber_dimension': max_fiber_dim,
        'max_subset_evaluations_per_scalar_fiber': max_subset_evaluations,
        'carry_evaluations': carry_evaluations,
        'ANF_coefficients_inserted': anf_coefficients,
        'unique_half_vectors_cached': len(coord_cache),
        'unique_coordinate_masks_cached': len(carry_cache),
    }
    print('result', out, flush=True)
    return out


def main():
    out = analyze()
    print('PASS V26_Q138_C916_REACHABLE_HALF_THIRD_CARRY')
    print('scope=C only; uniform relaxed half-only inherited third carry under the exact reachable-joint grouped-e0 basis that realizes the admitted C1<=916 ZZ quotient')
    print('important=degree<=4 interpolation is forced whenever the all-coordinate pairwise hull exceeds the current repeated k9 target 650')
    print('not_included=reachable grouped-e0 own carry, support-only lift carry, cross-carries, complete C2, complete leaf, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    main()
