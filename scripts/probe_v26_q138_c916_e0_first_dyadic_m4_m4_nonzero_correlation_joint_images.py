#!/usr/bin/env python3
import hashlib, io, json, math, sys
from collections import Counter
from contextlib import redirect_stdout
from itertools import product
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O
import probe_v26_q138_c916_e0_first_dyadic_singleton_m2_cross_joint_image as X

P=O.P
PHYS_N=O.PHYS_N
POS=O.POS
TARGETS=((141,247),(160,241))
assert PHYS_N==149

def signed_cells(terms, ambient, icache, mcache):
    terms=tuple(terms); n=len(terms); assert 1<=n<=8
    full=(1<<n)-1
    def exact(active,char):
        total=0
        for u in X.submasks(full ^ active):
            z=X.character_moment(terms,active|u,char,ambient,icache,mcache)
            total += -z if u.bit_count() & 1 else z
        return total
    out=Counter()
    for active in range(full+1):
        size=exact(active,0); assert size>=0
        if not size: continue
        chars={c:exact(active,c) for c in X.submasks(active)}
        div=1<<active.bit_count()
        for neg in X.submasks(active):
            num=sum(-w if (neg&c).bit_count()&1 else w for c,w in chars.items())
            assert num%div==0
            pop=num//div; assert pop>=0
            if pop: out[(active,neg)]+=pop
    assert sum(out.values())==1<<ambient
    return out

def pair_census(left,right,ambient,icache,mcache):
    lt,rt=tuple(left['terms']),tuple(right['terms'])
    assert len(lt)==len(rt)==4
    terms=lt+rt
    assert len({int(t['term_id']) for t in terms})==8
    counts=Counter()
    for (active,neg),pop in signed_cells(terms,ambient,icache,mcache).items():
        lv=rv=0
        for i,t in enumerate(terms):
            if not ((active>>i)&1): continue
            z=int(t['coefficient'])
            if (neg>>i)&1: z=-z
            if i<4: lv+=z
            else: rv+=z
        counts[(lv,rv)]+=pop
    lm,rm=Counter(),Counter()
    for (lv,rv),pop in counts.items():
        lm[lv]+=pop; rm[rv]+=pop
    return counts,dict(sorted(lm.items())),dict(sorted(rm.items()))

def synthetic():
    n=5
    anchors=[
        P.make_synthetic_anchor((),n,'linear'),
        P.make_synthetic_anchor(((1,0),),n,'quadratic'),
        P.make_synthetic_anchor(((2,1),),n,'one'),
        P.make_synthetic_anchor(((4,0),),n,'linear'),
        P.make_synthetic_anchor(((8,1),),n,'quadratic'),
        P.make_synthetic_anchor(((16,0),),n,'linear'),
        P.make_synthetic_anchor(((3,1),),n,'one'),
        P.make_synthetic_anchor(((5,0),),n,'quadratic'),
    ]
    def term(i,a,c):
        return {'term_id':i,'group_id':-1,'kind':'synthetic','coefficient':c,'anchor':a,'ambient_dimension':n}
    left={'terms':tuple(term(i+1,anchors[i],(1,-1,2,-2)[i]) for i in range(4))}
    right={'terms':tuple(term(i+5,anchors[i+4],(2,1,-2,-1)[i]) for i in range(4))}
    got,_,_=pair_census(left,right,n,{}, {})
    brute=Counter((X.eval_group(left,x),X.eval_group(right,x)) for x in range(1<<n))
    assert got==brute
    return {'cases':1,'domain_points_checked':1<<n,'joint_image_size':len(got)}

def relation_mask(counts,lvals,rvals):
    mask=bit=0
    for a in lvals:
        for b in rvals:
            if (a,b) in counts: mask|=1<<bit
            bit+=1
    return mask

def analyze():
    syn=synthetic()
    with redirect_stdout(io.StringIO()):
        census,groups=O.build_authority()
    assert all(census[g]['multiplicity']==4 for p in TARGETS for g in p)
    ic,mc={},{}
    rows=[]; digest=[]
    for left,right in TARGETS:
        counts,lm,rm=pair_census(groups[left],groups[right],PHYS_N,ic,mc)
        assert lm==census[left]['counts'] and rm==census[right]['counts']
        lvals=tuple(sorted(lm)); rvals=tuple(sorted(rm))
        cart=len(lvals)*len(rvals); size=len(counts)
        mask=relation_mask(counts,lvals,rvals)
        row={
            'left_group_id':left,'right_group_id':right,
            'left_image_size':len(lvals),'right_image_size':len(rvals),
            'cartesian_image_size':cart,'joint_image_size':size,
            'missing_cartesian_states':cart-size,
            'integer_bit_saving':(len(lvals)-1).bit_length()+(len(rvals)-1).bit_length()-(size-1).bit_length(),
            'exact_cardinality_gain_log2':math.log2(cart)-math.log2(size),
            'relation_mask_hex':f'{mask:x}',
        }
        rows.append(row)
        digest.append(f'{left}|{right}|{len(lvals)}x{len(rvals)}|{mask:x}')
    strict=sum(r['joint_image_size']<r['cartesian_image_size'] for r in rows)
    out={
        'position':POS,'physical_shared_dimension':PHYS_N,
        'target_pairs':len(TARGETS),'synthetic_eight_term_regression':syn,
        'pair_marginal_crosschecks':2*len(TARGETS),
        'strict_subcartesian_pairs':strict,
        'results':rows,
        'relation_digest_sha256':hashlib.sha256(('\n'.join(digest)+'\n').encode()).hexdigest(),
        'cached_support_intersections':len(ic),
        'cached_character_moments':len(mc),
        'decision':'M4_M4_NONZERO_CORRELATION_PAIR_JOINT_IMAGES_MEASURED',
    }
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_M4_NONZERO_CORRELATION_JOINT_IMAGES')
    print('scope=exact eight-term joint-image census for the only two m4-m4 pairs with nonzero full-domain inner product from PR185')
    print('important=these two pairs are a targeted gate, not an exhaustive m4-m4 joint-image census')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':
    analyze()
