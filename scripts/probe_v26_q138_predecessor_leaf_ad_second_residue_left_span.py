#!/usr/bin/env python3
import itertools,random,sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A

S=sorted(A.S1); R=A.R1


def affine_supports(pos):
    sites=[(j,i) for j in range(1,4) for i in range(31)]
    out=[]
    for z in itertools.combinations(sites,2):
        C=D.carries(z,ad=True)
        if A.internal_null(pos,C)[0]!=128:continue
        can=A.canonical_support(pos,C,expect_internal=128)
        if can is not None:out.append(can)
    FF=D.full_forms(pos)
    for z in sites:
        C=D.carries([z],ad=True);sol=A.internal_null(pos,C)
        if sol[0]!=127:continue
        der=A.derivative_form(FF,A.map_internal_to_full(sol[2][0]))
        can=A.canonical_support(pos,C,der,127)
        if can is not None:out.append(can)
    return out


def input_bits(words):
    z=0
    for g,w in enumerate(words):
        z |= (w & 0xffffffff) << (32*g)
    return z


def beta_system(can,words):
    ib=input_bits(words);eq=[]
    for row in can:
        im=row & ((1<<128)-1)
        bm=(row>>128)&((1<<32)-1)
        rhs=((row>>160)&1)^((im&ib).bit_count()&1)
        eq.append((bm,rhs))
    return T.rref(eq,n=32)


def left_truth(can,words):
    sol=beta_system(can,words)
    if sol is None:return 0
    _,beta0,_=sol
    y=0
    for i in R:y|=((beta0>>i)&1)<<i
    ib=input_bits(words);truth=0
    for q,xsmall in enumerate(range(1<<len(S))):
        beta=y
        for k,i in enumerate(S):beta|=((xsmall>>k)&1)<<i
        ok=True
        for row in can:
            im=row & ((1<<128)-1);bm=(row>>128)&((1<<32)-1)
            rhs=(row>>160)&1
            if (((im&ib).bit_count()+(bm&beta).bit_count())&1)!=rhs:
                ok=False;break
        if ok:truth|=1<<q
    return truth


def rank_int_vectors(vs):
    B={}
    for v in vs:
        x=v
        while x:
            p=x.bit_length()-1
            if p not in B:
                B[p]=x;break
            x^=B[p]
    return len(B)


def cases():
    out=[('zero',(0,0,0,0)),('ones',(0xffffffff,)*4)]
    for w in range(4):
        z=[0,0,0,0];z[w]=1;out.append((f'unit_w{w}',tuple(z)))
    rng=random.Random(138)
    for k in range(6):out.append((f'rand{k}',tuple(rng.getrandbits(32) for _ in range(4))))
    return out


def main():
    for pos in 'AD':
        supports=affine_supports(pos)
        assert len(supports)==(271 if pos=='A' else 274)
        vals=[]
        for name,words in cases():
            tv=[left_truth(can,words) for can in supports]
            nonzero=sum(bool(x) for x in tv);r=rank_int_vectors(tv)
            vals.append(r)
            print('position',pos,'case',name,'nonzero_affine_terms',nonzero,'left_factor_span_rank',r)
        print('position',pos,'rank_range',min(vals),max(vals),'raw_affine_terms',len(supports))
    print('PASS PROBE V26_Q138_AD_SECOND_RESIDUE_LEFT_SPAN')
    print('scope=fixed-mask exploratory left-factor spans only; no uniform theorem inferred')

if __name__=='__main__':main()
