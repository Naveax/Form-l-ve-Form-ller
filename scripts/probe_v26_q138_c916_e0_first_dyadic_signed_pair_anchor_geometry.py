#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_same_support_integer_coefficients as C
import probe_v26_q138_c916_e0_first_dyadic_pair_residual as D
import probe_v26_q138_c916_e0_complete_first_dyadic_fiber_geometry as G

POS = 'C'


def analyze():
    pair_out = D.analyze()
    pair_groups = {g['group_id']: g for g in pair_out['groups']}
    assert len(pair_groups) == 147

    e0, _e1, _half = C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for k in range(4):
        for zs, cls in e0[k]:
            can = C.P.U.H.support_for(POS, zs, cls)
            if can is not None:
                raw += 1
                grouped[can].append((zs, cls))
    assert raw == 577 and len(grouped) == 250

    anchor_polar = Counter()
    anchor_local_to_all = Counter()
    anchor_local_local = Counter()
    anchor_local_linear = Counter()
    anchor_category = Counter()
    anchor_category_by_mult = defaultdict(Counter)
    anchor_polar_by_mult = defaultdict(Counter)
    anchor_polar_by_pair_slot = defaultdict(Counter)
    diff_category = Counter()
    joint_category = Counter()
    compact = []
    count = 0

    for gid, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        m = len(sectors)
        if m == 1:
            continue
        pg = pair_groups[gid]
        assert pg['multiplicity'] == m

        _srank, x0, support_basis = C.X.support_param(can)
        d = len(support_basis)
        projection_rank, local_coeffs = G.local_fiber_coeff_basis(support_basis)

        sigs = []
        for zs, _cls in sectors:
            sig, sd, _nbits = C.X.restricted_phase_signature(C.phase_tuple(zs), x0, support_basis)
            assert sd == d
            sigs.append(sig)

        records = []
        for slot, selected in enumerate(pg['selected_pairs']):
            i, j = selected['pair']
            anchor = G.form_geometry(sigs[i], d, local_coeffs)
            diff = G.form_geometry(sigs[i] ^ sigs[j], d, local_coeffs)
            assert diff['polar_rank'] == selected['difference_polar_rank'] == 2

            anchor_polar[anchor['polar_rank']] += 1
            anchor_local_to_all[anchor['local_to_all_polar_rank']] += 1
            anchor_local_local[anchor['local_local_polar_rank']] += 1
            anchor_local_linear[anchor['local_linear_rank']] += 1
            anchor_category[anchor['category']] += 1
            anchor_category_by_mult[m][anchor['category']] += 1
            anchor_polar_by_mult[m][anchor['polar_rank']] += 1
            anchor_polar_by_pair_slot[(m, slot)][anchor['polar_rank']] += 1
            diff_category[diff['category']] += 1
            joint_category[(anchor['category'], diff['category'])] += 1
            count += 1

            records.append({
                'pair': [i, j],
                'slot': slot,
                'anchor': anchor,
                'difference': diff,
            })

        compact.append({
            'group_id': gid,
            'multiplicity': m,
            'support_free_dimension': d,
            'shared_projection_rank': projection_rank,
            'local_fiber_dimension': len(local_coeffs),
            'terms': records,
        })

    assert count == 237
    assert sum(anchor_category.values()) == 237
    assert sum(diff_category.values()) == 237

    out = {
        'position': POS,
        'signed_pair_terms': count,
        'multi_support_groups': len(compact),
        'anchor_polar_rank_histogram': dict(sorted(anchor_polar.items())),
        'anchor_local_to_all_polar_rank_histogram': dict(sorted(anchor_local_to_all.items())),
        'anchor_local_local_polar_rank_histogram': dict(sorted(anchor_local_local.items())),
        'anchor_local_linear_rank_histogram': dict(sorted(anchor_local_linear.items())),
        'anchor_fiber_category_histogram': dict(sorted(anchor_category.items())),
        'anchor_fiber_category_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(anchor_category_by_mult.items())
        },
        'anchor_polar_rank_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(anchor_polar_by_mult.items())
        },
        'anchor_polar_rank_by_pair_slot': {
            f'{m}:{slot}': dict(sorted(h.items()))
            for (m, slot), h in sorted(anchor_polar_by_pair_slot.items())
        },
        'difference_fiber_category_histogram': dict(sorted(diff_category.items())),
        'anchor_difference_joint_category_histogram': {
            f'{a}|{d}': n for (a, d), n in sorted(joint_category.items())
        },
        'anchors_descending_to_shared_quotient': anchor_category['descends_to_shared_quotient'],
        'groups': compact,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_SIGNED_PAIR_ANCHOR_GEOMETRY')
    print('scope=exact common-support fiber geometry of the anchor phase qi in every selected signed pair residual (-1)^qi * 1[qi xor qj = 0]')
    print('important=the rank2 equality difference is only one factor of each pair residual; anchor-phase complexity must also be represented')
    print('next=combine anchor and equality geometries in a joint representation over the common 11 local-left variables before separator-state counting')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
