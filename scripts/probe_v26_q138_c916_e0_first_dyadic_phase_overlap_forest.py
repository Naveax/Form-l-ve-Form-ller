#!/usr/bin/env python3
import io
import json
import sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from probe_v26_q138_c916_e0_post_gauss_physical_phase_common import *


def component_growth_regression():
    nodes = tuple(range(6))
    weights = {
        (0, 1): 0,
        (1, 2): 2,
        (2, 3): 4,
        (3, 4): 0,
        (4, 5): 2,
    }

    def components(threshold):
        remaining = set(nodes)
        out = []
        while remaining:
            seed = min(remaining)
            remaining.remove(seed)
            comp = [seed]
            while True:
                added = None
                for u in sorted(remaining):
                    for v in comp:
                        key = tuple(sorted((u, v)))
                        w = weights.get(key)
                        if w is not None and w <= threshold:
                            added = u
                            break
                    if added is not None:
                        break
                if added is None:
                    break
                remaining.remove(added)
                comp.append(added)
            out.append(tuple(sorted(comp)))
        return tuple(out)

    assert components(0) == ((0, 1), (2,), (3, 4), (5,))
    assert components(2) == ((0, 1, 2), (3, 4, 5))
    assert components(4) == ((0, 1, 2, 3, 4, 5),)
    return 3


def build_term_anchors():
    with redirect_stdout(io.StringIO()):
        pair_authority = R.analyze()
    pair_groups = {g['group_id']: g for g in pair_authority['groups']}
    assert len(pair_groups) == 147

    e0, _e1, _half = C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    for zc in range(4):
        for zs, cls in e0[zc]:
            can = C.P.U.H.support_for(POS, zs, cls)
            if can is not None:
                grouped[can].append((zs, cls))
    assert len(grouped) == 250

    anchors = []
    mate_count = 0
    for gid, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        m = len(sectors)
        _projection_rank, transforms = physical_group_transforms(can, sectors)
        for t in transforms:
            t['group_id'] = gid
            t['multiplicity'] = m

        if m == 1:
            t = transforms[0]
            t['role'] = 'singleton_anchor'
            anchors.append(t)
            continue

        authority = pair_groups[gid]
        assert authority['multiplicity'] == m
        touched = set()
        for pair_slot, selected in enumerate(authority['selected_pairs']):
            i, j = selected['pair']
            assert i not in touched and j not in touched
            touched.update((i, j))
            a = transforms[i]
            a['role'] = 'pair_anchor'
            a['pair_slot'] = pair_slot
            a['mate_sector_index'] = j
            anchors.append(a)
            mate_count += 1
        assert touched == set(range(m))

    anchors.sort(key=lambda t: (t['group_id'], t['sector_index']))
    assert len(anchors) == 340
    assert sum(t['role'] == 'singleton_anchor' for t in anchors) == 103
    assert sum(t['role'] == 'pair_anchor' for t in anchors) == 237
    assert mate_count == 237
    assert len({(t['group_id'], t['sector_index']) for t in anchors}) == 340
    return anchors


def anchor_id(t):
    return (t['group_id'], t['sector_index'])


def analyze():
    regression_cases = component_growth_regression()
    anchors = build_term_anchors()
    n = len(anchors)
    ids = tuple(anchor_id(t) for t in anchors)

    # The previous frozen canonical singleton root remains reproducible inside
    # this anchor set, but the forest itself is seeded by stable anchor order.
    canonical_singleton = min(
        (t for t in anchors if t['role'] == 'singleton_anchor'),
        key=anchor_id,
    )
    assert anchor_id(canonical_singleton) == (1, 0)
    assert canonical_singleton['physical_support_dimension'] == 140
    assert canonical_singleton['normalized_sign_polar_rank'] == 132

    support_cache = {}
    phase_cache = {}

    def pair_key(i, j):
        assert i != j
        return (i, j) if i < j else (j, i)

    def get_support(i, j):
        key = pair_key(i, j)
        if key in support_cache:
            return support_cache[key]
        left, right = anchors[key[0]], anchors[key[1]]
        relation, inter = support_relation(left, right, PHYS_N)
        if inter is None:
            rec = {
                'overlap': False,
                'relation': relation,
                'intersection_dimension': None,
                'intersection_codimension': None,
            }
        else:
            _rank, _x0, basis = inter
            rec = {
                'overlap': True,
                'relation': relation,
                'intersection_dimension': len(basis),
                'intersection_codimension': PHYS_N - len(basis),
            }
        support_cache[key] = rec
        return rec

    def get_phase(i, j):
        key = pair_key(i, j)
        if key in phase_cache:
            return phase_cache[key]
        sinfo = get_support(*key)
        assert sinfo['overlap']
        rec = compare_phases(anchors[key[0]], anchors[key[1]])
        assert rec['intersection_dimension'] == sinfo['intersection_dimension']
        assert rec['sign_difference_polar_rank'] is not None
        phase_cache[key] = rec
        return rec

    def exact_components(threshold):
        remaining = set(range(n))
        components = []
        forest_edges = []
        phase_before = len(phase_cache)
        support_before = len(support_cache)

        while remaining:
            seed = min(remaining, key=lambda i: ids[i])
            remaining.remove(seed)
            comp = [seed]

            while True:
                added_any = False
                # A no-addition pass is a certificate that no threshold edge
                # exists from this component to any remaining vertex: every
                # overlapping cross edge has then been evaluated or cached.
                for u in sorted(tuple(remaining), key=lambda i: ids[i]):
                    candidates = []
                    for v in comp:
                        sinfo = get_support(u, v)
                        if sinfo['overlap']:
                            candidates.append((
                                -sinfo['intersection_dimension'],
                                ids[v],
                                v,
                            ))
                    candidates.sort()
                    chosen = None
                    for _negdim, _vid, v in candidates:
                        prec = get_phase(u, v)
                        if prec['sign_difference_polar_rank'] <= threshold:
                            chosen = v
                            break
                    if chosen is None:
                        continue

                    remaining.remove(u)
                    comp.append(u)
                    edge_key = pair_key(u, chosen)
                    prec = phase_cache[edge_key]
                    sinfo = support_cache[edge_key]
                    forest_edges.append({
                        'left': list(ids[edge_key[0]]),
                        'right': list(ids[edge_key[1]]),
                        'difference_polar_rank': prec['sign_difference_polar_rank'],
                        'difference_type': prec['sign_difference_type'],
                        'intersection_dimension': sinfo['intersection_dimension'],
                        'intersection_codimension': sinfo['intersection_codimension'],
                    })
                    added_any = True

                if not added_any:
                    break

            components.append(tuple(sorted(comp, key=lambda i: ids[i])))

        return {
            'threshold': threshold,
            'components': components,
            'forest_edges': forest_edges,
            'new_phase_evaluations': len(phase_cache) - phase_before,
            'new_support_evaluations': len(support_cache) - support_before,
        }

    rank0 = exact_components(0)
    rank2 = exact_components(2)
    if len(rank2['components']) == 1:
        rank4 = {
            'threshold': 4,
            'components': rank2['components'],
            'forest_edges': rank2['forest_edges'],
            'new_phase_evaluations': 0,
            'new_support_evaluations': 0,
            'inferred_from_rank2_connected': True,
        }
    else:
        rank4 = exact_components(4)
        rank4['inferred_from_rank2_connected'] = False

    def component_summary(run):
        comps = run['components']
        sizes = sorted((len(c) for c in comps), reverse=True)
        roots = [list(ids[c[0]]) for c in comps]
        edge_rank_hist = Counter(
            e['difference_polar_rank'] for e in run['forest_edges']
        )
        edge_type_hist = Counter(e['difference_type'] for e in run['forest_edges'])
        edge_codim_hist = Counter(e['intersection_codimension'] for e in run['forest_edges'])
        assert len(run['forest_edges']) == n - len(comps)
        return {
            'component_count': len(comps),
            'component_size_histogram': dict(sorted(Counter(sizes).items())),
            'component_sizes_descending': sizes,
            'component_roots': roots,
            'forest_edges': len(run['forest_edges']),
            'forest_edge_polar_rank_histogram': dict(sorted(edge_rank_hist.items())),
            'forest_edge_type_histogram': dict(sorted(edge_type_hist.items())),
            'forest_edge_intersection_codimension_histogram': dict(sorted(edge_codim_hist.items())),
            'new_phase_evaluations': run['new_phase_evaluations'],
            'new_support_evaluations': run['new_support_evaluations'],
        }

    s0 = component_summary(rank0)
    s2 = component_summary(rank2)
    s4 = component_summary(rank4)

    if s2['component_count'] == 1:
        decision = 'FIRST_DYADIC_ANCHOR_PHASE_GRAPH_CONNECTED_WITH_POLAR_RANK_LE_2'
    elif s4['component_count'] == 1:
        decision = 'FIRST_DYADIC_ANCHOR_PHASE_GRAPH_REQUIRES_POLAR_RANK4_EDGES'
    else:
        decision = 'FIRST_DYADIC_ANCHOR_PHASE_GRAPH_MULTIPLE_SUPPORT_COMPONENTS'

    cached_rank_hist = Counter(
        rec['sign_difference_polar_rank'] for rec in phase_cache.values()
    )
    cached_type_hist = Counter(rec['sign_difference_type'] for rec in phase_cache.values())
    cached_codim_hist = Counter(
        support_cache[key]['intersection_codimension'] for key in phase_cache
    )

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'component_growth_regression_cases': regression_cases,
        'first_dyadic_term_anchors': n,
        'singleton_anchors': 103,
        'pair_anchors': 237,
        'stable_first_anchor': list(ids[0]),
        'canonical_singleton_anchor': list(anchor_id(canonical_singleton)),
        'rank0': s0,
        'rank_le_2': s2,
        'rank_le_4': s4,
        'rank_le_4_inferred_from_rank_le_2_connected': rank4.get('inferred_from_rank2_connected', False),
        'total_unique_phase_edges_evaluated': len(phase_cache),
        'total_unique_support_pairs_evaluated': len(support_cache),
        'evaluated_phase_edge_polar_rank_histogram': dict(sorted(cached_rank_hist.items())),
        'evaluated_phase_edge_type_histogram': dict(sorted(cached_type_hist.items())),
        'evaluated_phase_edge_intersection_codimension_histogram': dict(sorted(cached_codim_hist.items())),
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHASE_OVERLAP_FOREST')
    print('scope=exact connected components and deterministic spanning forests of the 340 first-dyadic term anchors under physical-support-overlap edges with intrinsic sign-difference polar-rank thresholds 0, 2, and when necessary 4')
    print('algorithm=a component is finalized only after a no-addition pass has exhausted every physical-overlap cross edge from that component to all remaining anchors, so the reported threshold component counts are exact despite lazy phase evaluation')
    print('important=forest connectivity is a phase-chart coverage result; it is not yet a complete separator message-count theorem or a proof of globally path-independent affine corrections')
    print('next=if rank<=2 is connected, test cycle/path consistency and factor a common phase section along the frozen forest before message-state assembly; otherwise characterize the necessary rank-4 bridges or multiple chart roots')
    print('not_included=complete grouped-e0 carry separator, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
