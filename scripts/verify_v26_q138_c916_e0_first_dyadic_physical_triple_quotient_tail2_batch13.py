#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_physical_triple_value_image as T
import verify_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_authority as Q
import verify_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_batch4 as G

TARGET = int(os.environ.get('C916_PHYSICAL_QUOTIENT_TAIL2_13_TARGET', '0'))
TARGETS = (
    {'source_index':0,'triple':(3,7,165),'raw_holes':16,'raw_hole_digest':'8a9d31b52b4a275b906ce15eede95b2296a5d19450d0acb350a7e86f6bb9113a','raw_image_digest':'46bfeb1a9b7799551982a6037e19151ab78bdd6ef559a9497dbab28c110c6ac3'},
    {'source_index':1,'triple':(3,7,181),'raw_holes':24,'raw_hole_digest':'9bde1dec2bab4539fdc7b7448a0b850e5d6b94221442c99083c54443e30f277f','raw_image_digest':'8d365e656f8947ac3421025fcc0e2a3895a0386295f7c5f82cb68e71247882fb'},
    {'source_index':2,'triple':(3,7,182),'raw_holes':16,'raw_hole_digest':'8a9d31b52b4a275b906ce15eede95b2296a5d19450d0acb350a7e86f6bb9113a','raw_image_digest':'46bfeb1a9b7799551982a6037e19151ab78bdd6ef559a9497dbab28c110c6ac3'},
    {'source_index':3,'triple':(3,7,183),'raw_holes':16,'raw_hole_digest':'8a9d31b52b4a275b906ce15eede95b2296a5d19450d0acb350a7e86f6bb9113a','raw_image_digest':'46bfeb1a9b7799551982a6037e19151ab78bdd6ef559a9497dbab28c110c6ac3'},
)

def analyze():
    assert 0 <= TARGET < len(TARGETS)
    expected=TARGETS[TARGET]; triple=tuple(expected['triple'])
    groups=Q.build_groups(triple)
    dist,stats=T.exact_joint_distribution(groups)
    image=set(dist); assert sum(dist.values())==(1<<T.PHYS_N)
    values=tuple(tuple(sorted({row[i] for row in image})) for i in range(3))
    assert tuple(map(len,values))==(7,7,7)
    raw_closure=Q.pairwise_closure(image,values)
    raw_holes=tuple(sorted(raw_closure-image))
    assert len(raw_holes)==expected['raw_holes']
    assert T.digest_rows([list(row) for row in raw_holes])==expected['raw_hole_digest']
    image_rows=[[list(key),int(dist[key])] for key in sorted(dist)]
    assert T.digest_rows(image_rows)==expected['raw_image_digest']
    maps,expected_qvalues=G.generalized_quotient_map(values)
    qimage={Q.qtuple(row,maps) for row in image}
    qvalues=tuple(tuple(sorted({row[i] for row in qimage})) for i in range(3))
    assert qvalues==expected_qvalues
    qclosure=Q.pairwise_closure(qimage,qvalues)
    qholes=tuple(sorted(qclosure-qimage))
    details=[]
    for q in qholes:
        raw_candidates=tuple(sorted(row for row in raw_closure if Q.qtuple(row,maps)==q))
        assert raw_candidates and all(row not in image for row in raw_candidates)
        details.append({'quotient_tuple':list(q),'raw_pairwise_closure_tuples_eliminated':len(raw_candidates),'raw_tuples':[list(row) for row in raw_candidates]})
    out={'position':'C','physical_shared_dimension':T.PHYS_N,'target':TARGET,'source_tail2_index':expected['source_index'],'triple':list(triple),'raw_exact_image_size':len(image),'raw_pairwise_closure_size':len(raw_closure),'raw_holes':len(raw_holes),'raw_hole_digest_sha256':expected['raw_hole_digest'],'raw_joint_distribution_digest_sha256':expected['raw_image_digest'],'quotient_alphabet_sizes':[len(v) for v in qvalues],'quotient_exact_image_size':len(qimage),'quotient_pairwise_closure_size':len(qclosure),'quotient_holes':len(qholes),'quotient_hole_tuples':[list(row) for row in qholes],'quotient_hole_digest_sha256':Q.digest_rows(qholes),'quotient_hole_details':details,'support_classes':stats['support_classes'],'cells_visited':stats['cells_visited'],'leaf_cells':stats['leaf_cells'],'walsh_evals':stats['walsh_evals'],'decision':'EXACT_PHYSICAL_TERNARY_OBSTRUCTION_DESCENDS_TO_SIGN_REFLECTION_QUOTIENT' if qholes else 'PHYSICAL_TERNARY_OBSTRUCTION_IS_SIGN_ONLY_AT_SIGN_REFLECTION_QUOTIENT'}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    if qholes:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_QUOTIENT_TAIL2_BATCH13_OBSTRUCTION')
    else:
        print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_QUOTIENT_TAIL2_BATCH13_SIGN_ONLY')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
