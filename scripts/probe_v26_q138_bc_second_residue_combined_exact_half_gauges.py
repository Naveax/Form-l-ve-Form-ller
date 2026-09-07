#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import verify_v26_q138_predecessor_leaf_bc_second_residue_support_frequency_nesting as N
import verify_v26_q138_predecessor_leaf_bc_second_residue_rank812_972 as R
import probe_v26_q138_bc_second_residue_fixed_predecessor_specialization as F
import probe_v26_q138_bc_second_residue_e0_joint_enumeration as J
import probe_v26_q138_bc_second_residue_half_exact_right21 as H


def in_span(B, x):
    y = x
    while y:
        p = y.bit_length() - 1
        if p not in B:
            return False
        y ^= B[p]
    return True


def union_in_order(*Bs):
    out = {}
    for B0 in Bs:
        for v in B0.values():
            S.insert(out, v)
    return out


def main():
    uniform = {'B': 812, 'C': 972}
    previous_witness = {'B': 808, 'C': 972}

    for pos in 'BC':
        pred = F.WITNESS[pos]
        Eold = F.specialized_e0_basis(pos, pred)
        Ejoint = J.joint_e0_basis(pos, pred)
        Hexact = H.exact_half_basis(pos, pred)

        expected_e = 272 if pos == 'B' else 388
        expected_h = 128 if pos == 'B' else 136
        assert len(Eold) == expected_e
        assert len(Ejoint) == expected_e
        assert len(Hexact) == expected_h

        # The joint e0 construction is a different binary-lift gauge for the
        # same fixed-predecessor GF(2) e0 correction space.
        assert all(in_span(Eold, v) for v in Ejoint.values())
        assert all(in_span(Ejoint, v) for v in Eold.values())

        support = N.weight120_union(pos)
        expected_support = 668 if pos == 'B' else 788
        assert len(support) == expected_support

        variants = [
            ('oldE_then_exactH', union_in_order(Eold, Hexact)),
            ('exactH_then_oldE', union_in_order(Hexact, Eold)),
            ('jointE_then_exactH', union_in_order(Ejoint, Hexact)),
            ('exactH_then_jointE', union_in_order(Hexact, Ejoint)),
        ]

        records = []
        for name, B0 in variants:
            qr, comp = R.quotient_rank(B0, support)
            total = len(support) + qr
            records.append((total, qr, len(B0), name, comp))
            print(
                'position', pos,
                'variant', name,
                'combined_GF2_basis_dim', len(B0),
                'Walsh_complement_coordinates', comp,
                'exact_ZZ_quotient_rank', qr,
                'second_lift_rank<=', total,
                flush=True,
            )

        best = min(records)
        print(
            'position', pos,
            'best_variant', best[3],
            'best_combined_GF2_basis_dim', best[2],
            'best_exact_ZZ_quotient_rank', best[1],
            'best_explicit_witness_second_lift_rank<=', best[0],
            'previous_best_witness_or_uniform', previous_witness[pos],
            'witness_gain', previous_witness[pos] - best[0],
            'current_uniform_bound', uniform[pos],
            flush=True,
        )

    print('PASS V26_Q138_BC_SECOND_RESIDUE_COMBINED_EXACT_HALF_GAUGES')
    print('scope=explicit max-overlap predecessor witnesses; exact half plus two e0 binary-lift gauges')
    print('claim=best printed rank is an explicit-witness upper bound only; no uniform 812/972 replacement')


if __name__ == '__main__':
    main()
