#!/usr/bin/env python3
import json, os
from collections import Counter
from pathlib import Path

M4=Path(os.environ.get('C916_M4_AUTHORITY','authorities/m4/c916_e0_first_dyadic_four_separator_complete_authority.json'))
SUB=Path(os.environ.get('C916_SUBSET_AUTHORITY','authorities/subset/c916_e0_first_dyadic_m4_subset_pair_relation_authority.json'))
EQ=Path(os.environ.get('C916_EQUAL_AUTHORITY','authorities/equal/c916_e0_first_dyadic_m4_equal_pair_relation_authority.json'))
SAMPLE=Path(os.environ.get('C916_SAMPLE_AUTHORITY','authorities/sample/c916_e0_first_dyadic_m4_overlap_nonzero_cross_stratified_sample.json'))
RARE=Path(os.environ.get('C916_RARE_AUTHORITY','authorities/rare/c916_e0_first_dyadic_m4_overlap_nonzero_cross_rare_shapes.json'))

def load(p): assert p.is_file(),p; return json.loads(p.read_text())

def bit(mask,cols,i,j): return (int(mask,16)>>(i*cols+j))&1

def pair_invariant(mask,rows,cols):
    for i in range(rows):
        for j in range(cols):
            b=bit(mask,cols,i,j)
            if b!=bit(mask,cols,rows-1-i,j): return False
            if b!=bit(mask,cols,i,cols-1-j): return False
    return True

def col_invariant(mask,rows,cols):
    for i in range(rows):
        for j in range(cols):
            if bit(mask,cols,i,j)!=bit(mask,cols,i,cols-1-j): return False
    return True

def qmap(n,i): return min(i,n-1-i)

def quotient_mask(mask,rows,cols,reflect_rows=True):
    qr=(rows+1)//2 if reflect_rows else rows; qc=(cols+1)//2; out=0
    for i in range(rows):
        for j in range(cols):
            if bit(mask,cols,i,j):
                qi=qmap(rows,i) if reflect_rows else i; qj=qmap(cols,j)
                out|=1<<(qi*qc+qj)
    return qr,qc,out

def summarize_pair(rows):
    qhist=Counter(); shape=Counter()
    for r in rows:
        nr=int(r.get('rows',r.get('left_image_size'))); nc=int(r.get('cols',r.get('right_image_size'))); mask=r.get('relation_mask_hex',r.get('mask_hex'))
        assert nr in (7,9) and nc in (7,9) and pair_invariant(mask,nr,nc), (r,nr,nc)
        qr,qc,q=quotient_mask(mask,nr,nc,True); qhist[(f'{qr}x{qc}',f'{q:x}')]+=1; shape[f'{nr}x{nc}']+=1
    return {'rows':len(rows),'shape_histogram':dict(sorted(shape.items())),'distinct_quotient_masks':len(qhist),'quotient_mask_histogram':[{'shape':k[0],'mask_hex':k[1],'count':v} for k,v in sorted(qhist.items())]}

def analyze():
    m4,sub,eq,sample,rare=map(load,(M4,SUB,EQ,SAMPLE,RARE))
    ph=Counter(); qparent=Counter()
    for r in m4['four_parent_relations']:
        cols=int(r['cols']); zi=int(r['zero_index']); assert cols in (7,9) and zi==cols//2; assert col_invariant(r['mask_hex'],4,cols)
        qr,qc,q=quotient_mask(r['mask_hex'],4,cols,False); assert qr==4 and qc in (4,5); ph[cols]+=1; qparent[(f'4x{qc}',f'{q:x}')]+=1
    ssum=summarize_pair(sub['relations']); esum=summarize_pair(eq['relations']); sampsum=summarize_pair(sample['results']); raresum=summarize_pair(rare['results'])
    out={'position':'C','physical_shared_dimension':149,'m4_label_orbits':{'7':[2,2,2,1],'9':[2,2,2,2,1]},'zero_label_is_reflection_fixed_center':True,
         'four_parent_relations':len(m4['four_parent_relations']),'four_parent_shape_histogram':dict(sorted(ph.items())),'four_parent_distinct_quotient_masks':len(qparent),'four_parent_quotient_mask_histogram':[{'shape':k[0],'mask_hex':k[1],'count':v} for k,v in sorted(qparent.items())],
         'subset_authority':ssum,'equal_authority':esum,'overlap_stratified_sample':sampsum,'overlap_rare_shape_authority':raresum,
         'decision':'M4_MEASURED_VALUE_AUTHORITIES_FACTOR_THROUGH_INDEPENDENT_SIGN_REFLECTION_ORBITS'}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_SIGN_REFLECTION_QUOTIENT')
    print('theorem=every measured unary m4 domain and every measured m4-m4 value relation is invariant under independently reflecting either m4 label index i to n-1-i; therefore these selected factor models admit an exact 7-to-4 and 9-to-5 weighted orbit quotient')
    print('important=this statement is authority-scoped; unmeasured overlap 7x7 relations are not asserted until their full authority is frozen')
    print('ALPHA_PASS=0'); return out

if __name__=='__main__': analyze()
