from __future__ import annotations
import json
C=(0x61707865,0x3320646e,0x79622d32,0x6b206574)
LO,HI=1,1875

def rol(x,r):return ((x<<r)|(x>>(32-r))) & 0xffffffff
rows=[]
for r in range(1,32):
    cinv=all(rol(x,r)==x for x in C)
    pairs=[(c,rol(c,r)) for c in range(LO,HI+1) if LO <= rol(c,r) <= HI]
    same_key_generic=(rol(1,r)==1)
    d0=rol(0,r)^0;d1=rol(1,r)^1
    rx_key_difference_public_generic=(d0==d1)
    rows.append({'rotation':r,'constants_invariant':cinv,'source_counter_pair_count':len(pairs),'source_counter_pair_examples':[list(x) for x in pairs[:5]],'nonce_zero_compatible':True,'same_key_generic_direct_relation':same_key_generic,'rx_key_difference_public_generic':rx_key_difference_public_generic,'block_output_exposes_raw_permutation_without_key':False,'direct_all_essential':bool(cinv and pairs and same_key_generic)})
out={'milestone':'V26_SINGLE_KEY_ROTATIONAL_APPLICABILITY_AUDIT','rotations_tested':31,'constant_compatible_rotations':[x['rotation'] for x in rows if x['constants_invariant']],'same_key_generic_rotations':[x['rotation'] for x in rows if x['same_key_generic_direct_relation']],'rotations_with_source_counter_pairs':[x['rotation'] for x in rows if x['source_counter_pair_count']>0],'rx_public_generic_rotations':[x['rotation'] for x in rows if x['rx_key_difference_public_generic']],'direct_applicable_rotations':[x['rotation'] for x in rows if x['direct_all_essential']],'raw_permutation_oracle_available':False,'literature_same_key_source_observable_rx_construction_found':False,'stage1_gate':False,'status':'NOT_APPLICABLE_TO_FDS_SINGLE_KEY_SOURCE_MODEL','rows':rows}
print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
