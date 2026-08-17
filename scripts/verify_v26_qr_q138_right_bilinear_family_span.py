#!/usr/bin/env python3
import itertools,sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_right_map_reachable_hull197 as H
import verify_v26_qr_q138_physical_rank_envelope27 as P

PRIME=1000000007


def modfrac(x,p=PRIME):return (x.numerator%p)*pow(x.denominator%p,p-2,p)%p

def add_mod(B,row,p=PRIME):
    r={j:v%p for j,v in row.items() if v%p}
    while r:
        c=min(r)
        if c not in B:
            z=pow(r[c],p-2,p);B[c]={j:(x*z)%p for j,x in r.items()};return True
        a=r[c];b=B[c]
        for j,x in b.items():
            z=(r.get(j,0)-a*x)%p
            if z:r[j]=z
            else:r.pop(j,None)
    return False

def add_q(B,row):
    r={j:Fraction(v) for j,v in row.items() if v}
    while r:
        c=min(r)
        if c not in B:
            z=1/r[c];B[c]={j:x*z for j,x in r.items()};return True
        a=r[c];b=B[c]
        for j,x in b.items():
            r[j]=r.get(j,Fraction(0))-a*x
            if not r[j]:r.pop(j,None)
    return False

def reduce_q(row,B):
    r={j:Fraction(v) for j,v in row.items() if v}
    while r:
        c=min(r);assert c in B,('outside span',c);a=r[c]
        for j,x in B[c].items():
            r[j]=r.get(j,Fraction(0))-a*x
            if not r[j]:r.pop(j,None)
    return True

def flat_prefix(V):
    return {z*1024+st:x for z,v in V.items() for st,x in v.items() if x}

def flat_closure(C):
    return {st*1024+o:x for st,row in C.items() for o,x in row.items() if x}

def flat_gram(G):
    return {i*64+j:x for i,row in enumerate(G) for j,x in row.items() if x}


def main():
    cert=sys.argv[1] if len(sys.argv)>1 else 'research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json'
    ctx=H.setup(cert);intA=ctx[6]
    PHYS=list(itertools.product((0,1),repeat=2));Ks={(a,b):H.transfer(ctx,4,(a,b,0)) for a,b in PHYS}
    prefixes=[];pkeys=[]
    for bits in itertools.product((0,1),repeat=8):
        u13,u23,u14,u24,u15,u25,u16,u26=bits;V=H.boundary(ctx,(u13,u23,0))
        for uv in ((u14,u24),(u15,u25),(u16,u26)):V={z:H.image(v,Ks[uv]) for z,v in V.items()}
        prefixes.append(V);pkeys.append(bits)
    closures=[];ckeys=[];close_ref=None
    for c in itertools.product((0,1),repeat=4):
        C7,close=P.closure7(ctx,*c)
        if close_ref is None:close_ref=close
        assert close==close_ref;closures.append(C7);ckeys.append(c)

    def witness_family(objs,flat):
        MB={};wit=[]
        for i,O in enumerate(objs):
            q=flat(O)
            if add_mod(MB,{j:modfrac(x) for j,x in q.items()}):wit.append(i)
        QB={}
        for i in wit:assert add_q(QB,flat(objs[i]))
        assert len(QB)==len(MB)==len(wit)
        for O in objs:reduce_q(flat(O),QB)
        return wit,QB

    pwit,PB=witness_family(prefixes,flat_prefix);cwit,CB=witness_family(closures,flat_closure)
    print('prefix_family_rank',len(pwit),'closure_family_rank',len(cwit),flush=True)

    # Bilinearity implies basis products span the full 256x16 physical Gram family.
    GBm={};products=[]
    for pi in pwit:
        for ci in cwit:
            G=P.gram_rows(intA,close_ref,prefixes[pi],closures[ci]);g=flat_gram(G);products.append((pi,ci,g))
            add_mod(GBm,{j:modfrac(x) for j,x in g.items()})
    gwit=[];seen={}
    for pi,ci,g in products:
        if add_mod(seen,{j:modfrac(x) for j,x in g.items()}):gwit.append((pi,ci,g))
    assert len(seen)==len(GBm)
    GQ={}
    for pi,ci,g in gwit:assert add_q(GQ,g)
    assert len(GQ)==len(GBm)
    for _,_,g in products:reduce_q(g,GQ)

    # Sanity against the complete physical rank distribution endpoints is handled
    # by the separate physical_rank_envelope27 verifier.
    print('PASS V26_QR_Q138_RIGHT_BILINEAR_FAMILY_SPAN')
    print('prefix_controls=8 prefix_family_rank='+str(len(PB)))
    print('closure_controls=4 closure_family_rank='+str(len(CB)))
    print('basis_product_count='+str(len(pwit)*len(cwit)))
    print('exact_right_gram_family_rank='+str(len(GQ)))
    print('prefix_witnesses='+','.join(str(i) for i in pwit))
    print('closure_witnesses='+','.join(str(i) for i in cwit))

if __name__=='__main__':main()
