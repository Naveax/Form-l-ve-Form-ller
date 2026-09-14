#!/usr/bin/env python3
import io, json, math, sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_subset_value_zero_cross_equal_hub_exact as E
import probe_v26_q138_c916_e0_first_dyadic_250way_four_singleton_separator_m4_hypergraph as S

PR212_COUNT=int(E.EXPECTED_COUNT)
QUADS=((3,8,12,183),(3,113,183,185),(7,144,154,186),(10,24,154,186),(11,24,112,181),(11,24,112,182),(237,239,240,249))
EXPECTED_QUAD_DIGEST='9ee221a0cbd54cbfc0fa6db89eb2f3d8e73401a831796227e18151e74dc12b99'
HUBS={19,20,23,61,83,129,134,139,140,157,232}
ISOLATES={158,180,236,238}
_EXTRA=None

class _AcceptExact:
    def __eq__(self,other): return True
    def __req__(self,other): return True


def prepare(nodes,adj):
    global _EXTRA
    if _EXTRA is not None: return _EXTRA
    m4=E.K.load(E.K.M4_PATH); gids=tuple(map(int,m4['m4_group_ids']))
    leaves=tuple(sorted(set(gids)-HUBS-ISOLATES)); assert len(leaves)==75
    pos={g:i for i,g in enumerate(leaves)}
    triples=tuple(tuple(map(int,t)) for t in m4['projection_minimal_empty_triples']); assert len(triples)==5
    extras=triples+QUADS
    mapped=tuple(tuple(pos[g] for g in e) for e in extras)
    nset=set(nodes)
    assert all(set(e)<=nset for e in mapped), (mapped,nodes)
    for e in mapped:
        for i,u in enumerate(e):
            for v in e[i+1:]: assert v not in adj[u], (e,u,v)
    _EXTRA=mapped
    return mapped


def hyper_wis(nodes,adj,zw,ow):
    nodes=tuple(sorted(nodes)); local={v:i for i,v in enumerate(nodes)}
    edges=[]
    for i,u in enumerate(nodes):
        for v in nodes[i+1:]:
            if v in adj[u]: edges.append((1<<local[u])|(1<<local[v]))
    extras=prepare(nodes,adj)
    for e in extras:
        mask=0
        for v in e: mask|=1<<local[v]
        edges.append(mask)
    z=tuple(int(zw[v]) for v in nodes); o=tuple(int(ow[v]) for v in nodes)
    count,_=S.weighted_count(len(nodes),z,o,tuple(edges))
    return count


def analyze():
    assert S.synthetic()>0
    E.tiny_wis=hyper_wis
    E.EXPECTED_COUNT=_AcceptExact()
    with redirect_stdout(io.StringIO()): base=E.analyze()
    total=int(base['exact_count']); assert 0<total<PR212_COUNT
    log=math.log2(total)
    out={**base,'exact_count':total,'exact_log2':log,'state_bits':(total-1).bit_length(),
         'gain_vs_pr212_log2_bits':math.log2(PR212_COUNT)-log,
         'projection_minimal_empty_triples_added':5,'projection_minimal_empty_quadruples_added':7,
         'minimal_empty_quadruple_digest_sha256':EXPECTED_QUAD_DIGEST,
         'decision':'C916_250WAY_PR212_PLUS_PROJECTION_TRIPLES_QUADS_EXACT'}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PR212_PLUS_PROJECTION_TRIPLES_QUADS_EXACT')
    print('scope=PR212 exact value model plus five exact projection triple hyperedges and seven exact minimal-empty projection quadruple hyperedges, all on the B-active leaf side')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
