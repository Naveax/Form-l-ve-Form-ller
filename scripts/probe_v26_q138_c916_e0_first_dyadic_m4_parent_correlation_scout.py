#!/usr/bin/env python3
import io
import json
import math
import sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_group_output_pair_dependency as D

E = D.E
S = D.S
P = D.P
POS = D.POS
PHYS_N = D.PHYS_N
assert PHYS_N == 149

PARENT_MULTS = (1, 2)
M4_MULT = 4
TOP_K = 8


def census_map(record):
    return {
        int(item['value']): int(item['multiplicity'])
        for item in record['value_multiplicity']
    }


def norm2(counts):
    return sum(int(v) * int(v) * int(n) for v, n in counts.items())


def build_authority():
    with redirect_stdout(io.StringIO()):
        even = E.analyze()
        singleton = S.analyze()

    census = {}
    for rec in even['groups']:
        gid = int(rec['group_id'])
        census[gid] = {
            'multiplicity': int(rec['multiplicity']),
            'image_size': int(rec['image_size']),
            'counts': census_map(rec),
        }
    for rec in singleton['groups']:
        gid = int(rec['group_id'])
        assert gid not in census
        census[gid] = {
            'multiplicity': 1,
            'image_size': int(rec['image_size']),
            'counts': census_map(rec),
        }
    assert sorted(census) == list(range(250))
    assert Counter(r['multiplicity'] for r in census.values()) == Counter({1:103, 2:57, 4:90})
    assert Counter(r['image_size'] for r in census.values() if r['multiplicity'] == 4) == Counter({7:88, 9:2})

    e0, _e1, _half = P.C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for zc in range(4):
        for zs, cls in e0[zc]:
            can = P.C.P.U.H.support_for(POS, zs, cls)
            if can is None:
                continue
            raw += 1
            grouped[can].append((zs, cls))
    ordered = list(sorted(grouped.items(), key=lambda kv: kv[0]))
    assert raw == 577 and len(ordered) == 250

    groups = {}
    tid = 0
    for gid, (can, sectors) in enumerate(ordered):
        group, tid = D.build_group_terms(gid, can, sectors, tid)
        assert group['multiplicity'] == census[gid]['multiplicity']
        if group['multiplicity'] == 1:
            assert len(group['terms']) == 2
        elif group['multiplicity'] == 2:
            assert len(group['terms']) == 2
        else:
            assert group['multiplicity'] == 4 and len(group['terms']) == 4
        groups[gid] = group
    assert tid == 680
    return census, groups


def analyze():
    census, groups = build_authority()
    parents = tuple(g for g in range(250) if census[g]['multiplicity'] in PARENT_MULTS)
    m4s = tuple(g for g in range(250) if census[g]['multiplicity'] == M4_MULT)
    assert len(parents) == 160 and len(m4s) == 90

    norms = {g: norm2(census[g]['counts']) for g in range(250)}
    assert all(n > 0 for n in norms.values())

    cache = {}
    for g in range(250):
        assert D.group_inner(groups[g], groups[g], cache) == norms[g]

    zero_inner = 0
    relation_hist = Counter()
    parent_kind_hist = Counter()
    rho_bucket_hist = Counter()
    all_rows = []
    per_m4 = {}

    for mgid in m4s:
        rows = []
        for pgid in parents:
            inner = D.group_inner(groups[pgid], groups[mgid], cache)
            if inner == 0:
                zero_inner += 1
            rho2 = Fraction(inner * inner, norms[pgid] * norms[mgid])
            assert 0 <= rho2 < 1
            relation, inter = P.support_relation(
                groups[pgid]['projection_anchor'],
                groups[mgid]['projection_anchor'],
                PHYS_N,
            )
            relation_hist[relation] += 1
            pkind = 'singleton' if census[pgid]['multiplicity'] == 1 else 'm2'
            parent_kind_hist[pkind] += 1
            if rho2 == 0:
                bucket = '0'
            elif rho2 >= Fraction(1, 2):
                bucket = '[1/2,1)'
            elif rho2 >= Fraction(1, 4):
                bucket = '[1/4,1/2)'
            elif rho2 >= Fraction(1, 16):
                bucket = '[1/16,1/4)'
            else:
                bucket = '(0,1/16)'
            rho_bucket_hist[bucket] += 1
            row = {
                'm4_group_id': mgid,
                'm4_image_size': census[mgid]['image_size'],
                'parent_group_id': pgid,
                'parent_kind': pkind,
                'parent_image_size': census[pgid]['image_size'],
                'inner_product': int(inner),
                'rho2_numerator': int(rho2.numerator),
                'rho2_denominator': int(rho2.denominator),
                'projection_support_relation': relation,
                'projection_intersection_dimension': None if inter is None else len(inter[2]),
            }
            rows.append((rho2, abs(inner), -census[pgid]['image_size'], -pgid, row))
            all_rows.append((rho2, abs(inner), -mgid, -pgid, row))

        rows.sort(reverse=True)
        top = [r[-1] for r in rows[:TOP_K]]
        assert len(top) == TOP_K
        per_m4[mgid] = top

    pair_count = len(parents) * len(m4s)
    assert pair_count == 14400
    assert sum(relation_hist.values()) == pair_count
    assert sum(parent_kind_hist.values()) == pair_count
    assert parent_kind_hist == Counter({'singleton': 9270, 'm2': 5130})

    all_rows.sort(reverse=True)
    global_top = [r[-1] for r in all_rows[:40]]
    best_rho2 = all_rows[0][0]

    selected_candidates = []
    selected_pair_set = set()
    selected_parent_kind_hist = Counter()
    selected_relation_hist = Counter()
    for mgid in m4s:
        for rec in per_m4[mgid]:
            key = (int(rec['parent_group_id']), int(mgid))
            assert key not in selected_pair_set
            selected_pair_set.add(key)
            selected_candidates.append(rec)
            selected_parent_kind_hist[rec['parent_kind']] += 1
            selected_relation_hist[rec['projection_support_relation']] += 1
    assert len(selected_candidates) == len(m4s) * TOP_K == 720

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'parent_outputs': len(parents),
        'multiplicity4_outputs': len(m4s),
        'parent_m4_pairs': pair_count,
        'top_k_per_m4': TOP_K,
        'selected_exact_joint_candidate_pairs': len(selected_candidates),
        'zero_inner_product_pairs': zero_inner,
        'nonzero_inner_product_pairs': pair_count - zero_inner,
        'projection_support_relation_histogram': dict(sorted(relation_hist.items())),
        'correlation_squared_bucket_histogram': dict(sorted(rho_bucket_hist.items())),
        'maximum_exact_correlation_squared': {
            'numerator': int(best_rho2.numerator),
            'denominator': int(best_rho2.denominator),
            'float': float(best_rho2),
        },
        'selected_candidate_parent_kind_histogram': dict(sorted(selected_parent_kind_hist.items())),
        'selected_candidate_projection_relation_histogram': dict(sorted(selected_relation_hist.items())),
        'global_strongest_pairs_top40': global_top,
        'per_m4_top_candidates': {
            str(g): per_m4[g] for g in m4s
        },
        'term_inner_cache_entries': len(cache),
        'decision': 'M4_PARENT_CORRELATION_SCOUT_COMPLETE',
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_PARENT_CORRELATION_SCOUT')
    print('scope=exact inner-product/correlation scout over all 14400 pairs between the 160 singleton+m2 outputs and 90 multiplicity-4 outputs')
    print('purpose=rank a bounded set of structurally promising parents before expensive exact six-term joint-image evaluation; correlation is a heuristic ranking signal, not a joint-state theorem')
    print('validation=all 250 reconstructed group norms are cross-checked against frozen exact value censuses and every correlation obeys strict Cauchy inequality because no distinct proportional pair exists')
    print('next=run exact six-term joint-image censuses for the top parent candidates per m4 output and measure attachment factors against the selected 160-way tree state')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
