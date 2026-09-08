#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_reachable_joint_sign_span as P
import probe_v26_q138_bc_uniform_half_lift_third_carry as H
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S

POS = 'C'
K9_REPEATED_TARGET = 650
FULL = 2048


def analyze():
    raw, groups = P.grouped_data(POS)
    assert raw == 577
    assert len(groups) == 250

    reachable = {}
    records = []
    correlated = 0
    full_product = 0

    for group_id, (can, sectors) in enumerate(groups):
        qbits, cols = P.aggregate_phase(POS, sectors)
        local, st = P.reachable_local_basis(can, qbits, cols)
        correlated += st['mode'] == 'correlated_image'
        full_product += st['mode'] == 'full_product'
        for v in local.values():
            S.insert(reachable, v)

        pivot_rows, constraint_rank, r0, null_basis = P.support_affine_map(can)
        offset, image_basis = P.joint_image(pivot_rows, cols, r0, null_basis)
        assert len(pivot_rows) == st['support_rank']
        assert len(image_basis) == st['joint_image_rank']
        assert constraint_rank == st['constraint_rank']
        records.append((group_id, qbits, pivot_rows, offset, image_basis, st))

    assert correlated == 111
    assert full_product == 139
    assert len(reachable) == 388

    items, piv = H.coordinate_solver(reachable)
    assert len(items) == 388

    support = P.N.weight120_union(POS)
    assert len(support) == 788
    qr, comp = P.R.quotient_rank(reachable, support)
    assert qr == 128
    assert comp == 1260
    assert len(support) + qr == 916

    carry_span = {}
    coord_cache = {0: 0}
    carry_cache = {0: 0}
    total_fibers = 0
    scalar_fibers = 0
    total_anf_coefficients = 0
    carry_evaluations = 0
    max_fiber_dim = 0
    max_group_image_rank = 0
    saturation = None

    def eval_carry(vec):
        nonlocal carry_evaluations
        coeff = coord_cache.get(vec)
        if coeff is None:
            coeff = H.coordinates(vec, piv)
            assert coeff is not None, 'reachable local e0 vector escaped C916 basis'
            coord_cache[vec] = coeff
        carry = carry_cache.get(coeff)
        if carry is None:
            carry = H.xor_lift_carry(coeff, items, vec)
            carry_cache[coeff] = carry
        carry_evaluations += 1
        return carry

    for group_id, qbits, pivot_rows, offset, image_basis, st in records:
        support_rank = len(pivot_rows)
        support_mask_bits = (1 << support_rank) - 1
        max_group_image_rank = max(max_group_image_rank, len(image_basis))
        eq_masks = H.support_projection_equations(image_basis, support_rank)
        offset_support = offset & support_mask_bits

        for sigma in range(1 << support_rank):
            target = sigma ^ offset_support
            eq = [
                (eq_masks[e], (target >> e) & 1)
                for e in range(support_rank)
            ]
            fib = P.Top.rref(eq, n=len(image_basis))
            if fib is None:
                continue
            total_fibers += 1
            coeff0, coeff_null = fib[1], fib[2]
            max_fiber_dim = max(max_fiber_dim, len(coeff_null))

            state0 = offset ^ H.state_from_coeff(image_basis, coeff0)
            dirs = [H.state_from_coeff(image_basis, d) for d in coeff_null]
            assert (state0 & support_mask_bits) == sigma
            assert all((d & support_mask_bits) == 0 for d in dirs)

            smask = P.support_mask(pivot_rows, sigma)
            assert smask != 0

            def vec_at(state, scalar):
                freq = state >> support_rank
                vec = smask & (qbits ^ S.WALSH[freq])
                if scalar:
                    vec ^= smask
                return vec

            for scalar in (0, 1):
                scalar_fibers += 1
                c0 = eval_carry(vec_at(state0, scalar))
                S.insert(carry_span, c0)
                total_anf_coefficients += 1

                singles = []
                linear = []
                for d in dirs:
                    ci = eval_carry(vec_at(state0 ^ d, scalar))
                    singles.append(ci)
                    li = ci ^ c0
                    linear.append(li)
                    S.insert(carry_span, li)
                    total_anf_coefficients += 1

                quadratic = {}
                for a in range(len(dirs)):
                    for b in range(a + 1, len(dirs)):
                        cij = eval_carry(vec_at(state0 ^ dirs[a] ^ dirs[b], scalar))
                        q = cij ^ singles[a] ^ singles[b] ^ c0
                        quadratic[(a, b)] = q
                        S.insert(carry_span, q)
                        total_anf_coefficients += 1

                # Exact degree bound: on a fixed support-syndrome fiber the
                # local truth vector is affine-linear in the frequency state;
                # coordinates in the fixed global basis stay affine-linear;
                # xor_lift_carry is quadratic in those coordinates. These
                # deterministic higher-weight probes are regression checks.
                probes = []
                k = len(dirs)
                if k:
                    probes.append((1 << k) - 1)
                    probes.append(sum(1 << j for j in range(0, k, 2)))
                    probes.append(sum(1 << j for j in range(1, k, 2)))
                for mask in dict.fromkeys(probes):
                    predicted = c0
                    for j, l in enumerate(linear):
                        if (mask >> j) & 1:
                            predicted ^= l
                    for (a, b), q in quadratic.items():
                        if ((mask >> a) & 1) and ((mask >> b) & 1):
                            predicted ^= q
                    state = state0
                    for j, d in enumerate(dirs):
                        if (mask >> j) & 1:
                            state ^= d
                    actual = eval_carry(vec_at(state, scalar))
                    assert predicted == actual, (group_id, sigma, scalar, mask)

                if len(carry_span) == FULL:
                    saturation = {
                        'group_id': group_id,
                        'support_syndrome': sigma,
                        'scalar': scalar,
                    }
                    break
            if saturation is not None:
                break
        if saturation is not None:
            break

    out = {
        'position': POS,
        'raw_e0_sectors': raw,
        'support_groups': len(groups),
        'correlated_groups': correlated,
        'full_product_groups': full_product,
        'reachable_e0_basis_dim': len(items),
        'support_Walsh_dim': len(support),
        'reachable_exact_ZZ_quotient': qr,
        'reachable_second_lift_total': len(support) + qr,
        'max_group_joint_image_rank': max_group_image_rank,
        'support_syndrome_fibers_processed': total_fibers,
        'scalar_fibers_processed': scalar_fibers,
        'max_frequency_fiber_dimension': max_fiber_dim,
        'degree2_ANF_coefficients_inserted': total_anf_coefficients,
        'carry_evaluations': carry_evaluations,
        'unique_local_vectors_cached': len(coord_cache),
        'unique_coordinate_masks_cached': len(carry_cache),
        'reachable_e0_own_third_carry_GF2_span': len(carry_span),
        'k9_repeated_target': K9_REPEATED_TARGET,
        'target_met_by_e0_own_carry_span': len(carry_span) <= K9_REPEATED_TARGET,
        'saturation': saturation,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_REACHABLE_E0_OWN_THIRD_CARRY')
    print('scope=C only; exact degree<=2 fiber interpolation of basis-lift carry for each individually reachable grouped-e0 local correction in the C916 global reachable basis')
    print('important=this is grouped-e0 own basis-lift carry only; it does not include carry from summing different e0 groups, support-only/e1 carry, e0-support cross-carry, half cross-carry, or complete C2')
    print('not_included=complete C2, complete leaf, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


def main():
    analyze()


if __name__ == '__main__':
    main()
