#!/usr/bin/env python3
import os
import sqlite3
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_ad_third_direct_e2_condition_group_rank1 as G
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T

MASK = (1 << 128) - 1
S = sorted(A.S1)
R = A.R1


def eval_map(M, x):
    z = 0
    for j, (m, b) in enumerate(M):
        z |= ((((m & x).bit_count() & 1) ^ b) << j)
    return z


def eval_linear_map(M, x):
    z = 0
    for j, (m, _b) in enumerate(M):
        z |= (((m & x).bit_count() & 1) << j)
    return z


def eq_on_condition(B, M, U):
    return all(G.implied_zero(B, m ^ u, b ^ c)
               for (m, b), (u, c) in zip(M, U))


def active(cond, x):
    return all((((row & MASK) & x).bit_count() & 1) == ((row >> 128) & 1)
               for row in cond)


def gray_points(x0, y0, basis, dy):
    x = x0
    y = y0
    yield x, y
    prev = 0
    for k in range(1, 1 << len(basis)):
        g = k ^ (k >> 1)
        d = g ^ prev
        j = (d & -d).bit_length() - 1
        x ^= basis[j]
        y ^= dy[j]
        yield x, y
        prev = g


def main():
    raw, _ = P.direct_supports('D')
    C = Counter(can for _typ, _zs, can in raw)
    odd = [can for can, n in C.items() if n & 1]
    assert len(odd) == 12363

    groups = defaultdict(list)
    for can in odd:
        cond = P.canonical_condition(I.input_condition(can))
        groups[cond].append(can)
    assert len(groups) == 8629
    assert Counter(map(len, groups.values())) == Counter({1: 4895, 2: 3734})

    data = []
    dimdist = Counter()
    total_incidence = 0
    for cond, cans in groups.items():
        eq = [(row & MASK, (row >> 128) & 1) for row in cond]
        sol = T.rref(eq, n=128)
        assert sol is not None
        rank, x0, basis = sol[:3]
        assert rank == len(cond)
        B = G.affine_basis(cond)
        M = G.singleton_side_map(cans[0], S, R)
        for can in cans[1:]:
            U = G.singleton_side_map(can, S, R)
            assert eq_on_condition(B, M, U)
        y0 = eval_map(M, x0)
        dy = [eval_linear_map(M, d) for d in basis]
        dimdist[len(basis)] += 1
        total_incidence += 1 << len(basis)
        data.append((cond, M, x0, tuple(basis), y0, tuple(dy)))

    print('D_condition_groups', len(data),
          'condition_free_dimension_distribution', dict(sorted(dimdist.items())),
          'total_group_point_incidences', total_incidence, flush=True)

    fd, dbpath = tempfile.mkstemp(prefix='v26_d_labels_', suffix='.sqlite3')
    os.close(fd)
    try:
        con = sqlite3.connect(dbpath)
        cur = con.cursor()
        cur.execute('PRAGMA journal_mode=OFF')
        cur.execute('PRAGMA synchronous=OFF')
        cur.execute('PRAGMA temp_store=FILE')
        cur.execute('PRAGMA locking_mode=EXCLUSIVE')
        cur.execute('PRAGMA cache_size=-500000')
        cur.execute('CREATE TABLE rec (x BLOB NOT NULL, y INTEGER NOT NULL)')

        batch = []
        inserted = 0
        for gi, (_cond, _M, x0, basis, y0, dy) in enumerate(data, 1):
            for x, y in gray_points(x0, y0, basis, dy):
                batch.append((x.to_bytes(16, 'big'), y))
                if len(batch) >= 100000:
                    cur.executemany('INSERT INTO rec VALUES (?,?)', batch)
                    inserted += len(batch)
                    batch.clear()
            if gi % 500 == 0:
                print('enumerated_groups', gi, 'inserted_records', inserted + len(batch), flush=True)
        if batch:
            cur.executemany('INSERT INTO rec VALUES (?,?)', batch)
            inserted += len(batch)
            batch.clear()
        con.commit()
        assert inserted == total_incidence
        print('sqlite_inserted_records', inserted,
              'db_bytes_before_index', os.path.getsize(dbpath), flush=True)

        cur.execute('CREATE INDEX rec_xy ON rec(x,y)')
        con.commit()
        print('db_bytes_after_index', os.path.getsize(dbpath), flush=True)

        # The index orders equal x and y together. Deduplicate identical labels
        # produced by multiple active condition groups before counting rows.
        q = '''
            SELECT x, COUNT(*) AS c
            FROM (SELECT DISTINCT x,y FROM rec)
            GROUP BY x
            ORDER BY c DESC
            LIMIT 1
        '''
        best_x_blob, best_count = cur.execute(q).fetchone()
        best_x = int.from_bytes(best_x_blob, 'big')
        labels = [r[0] for r in cur.execute(
            'SELECT DISTINCT y FROM rec WHERE x=? ORDER BY y', (best_x_blob,))]
        assert len(labels) == best_count

        # Independent direct recomputation on the maximizing witness.
        active_groups = 0
        direct_labels = set()
        for cond, M, _x0, _basis, _y0, _dy in data:
            if active(cond, best_x):
                active_groups += 1
                direct_labels.add(eval_map(M, best_x))
        assert direct_labels == set(labels)

        unique_x = cur.execute('SELECT COUNT(*) FROM (SELECT DISTINCT x FROM rec)').fetchone()[0]
        unique_xy = cur.execute('SELECT COUNT(*) FROM (SELECT DISTINCT x,y FROM rec)').fetchone()[0]

        print('D_union_distinct_predecessor_inputs', unique_x,
              'D_distinct_input_label_pairs', unique_xy, flush=True)
        print('D_exact_max_distinct_active_left_labels', best_count,
              'witness_x_hex', f'{best_x:032x}',
              'witness_active_condition_groups', active_groups, flush=True)
        print('D_witness_labels', labels, flush=True)
        print('PASS PROBE V26_Q138_AD_THIRD_D_EXACT_DISTINCT_LABEL_MAX')
        print('theorem_candidate=D_direct_e2_rank_Q(x)<=', best_count,
              'uniformly_over_all_128_bit_predecessor_inputs')
        print('complete_third_candidate_if_combined_by_sum<=', min(2048, best_count + 171),
              'using_inherited_e1_correction_rank<=171')
        print('scope=uniform row-count upper bound for D direct-e2 assembled matrix; '
              'right-row cancellations can only reduce rank further')
    finally:
        try:
            con.close()
        except Exception:
            pass
        try:
            os.unlink(dbpath)
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    main()
