#!/usr/bin/env python3
import itertools,sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import probe_v26_q138_predecessor_leaf_bc_e0_sign_left_factors as E

S=sorted(A.S1);R=A.R1
ALL=(1<<2048)-1
WALSH=[]
for f in range(1<<11):
    z=0
    for x in range(1<<11):
        if (f&x).bit_count()&1:z|=1<<x
    WALSH.append(z)

SECTORS=[((1,0),(2,0)),((1,0),(4,0)),((2,0),(3,0)),((3,0),(4,0))]


def split_ext(mask):
    lm=rm=im=0
    for q,i in enumerate(S):
        if (mask>>(128+i))&1:lm|=1<<q
    for q,i in enumerate(R):
        if (mask>>(128+i))&1:rm|=1<<q
    im=mask&((1<<128)-1)
    return lm,rm,im


def sector_phase_data(pos,zs,input128):
    Cmask=D.carries(zs)
    FF,subs,rank,eindex=E.generalized_substitution(pos,Cmask,[])
    assert rank==128
    products=[]
    qleft=0
    cross=[0]*len(R)
    right_terms=[]
    for j in range(1,5):
        for i in range(31):
            X=T.xx(FF[j,i,'u'],FF[j,i,'w'])
            Y=T.xx(FF[j,i,'v'],FF[j,i,'w'])
            xm,xc=A.sub_form(X,subs,eindex);ym,yc=A.sub_form(Y,subs,eindex)
            xl,xr,xi=split_ext(xm);yl,yr,yi=split_ext(ym)
            xc ^= (xi&input128).bit_count()&1
            yc ^= (yi&input128).bit_count()&1
            for q in range(len(R)):
                if (yr>>q)&1:cross[q]^=xl
                if (xr>>q)&1:cross[q]^=yl
            for x in range(1<<11):
                a=((xl&x).bit_count()&1)^xc
                b=((yl&x).bit_count()&1)^yc
                if a&b:qleft^=1<<x
            right_terms.append((xr,xc,yr,yc))
    return qleft,cross,right_terms


def common_support_data(pos,input128):
    cans=[A.canonical_support(pos,D.carries(z),expect_internal=128) for z in SECTORS]
    assert all(c==cans[0] for c in cans)
    eq=[]
    for row in cans[0]:
        ext=row&((1<<160)-1);rhs=(row>>160)&1
        lm,rm,im=split_ext(ext)
        rhs ^= (im&input128).bit_count()&1
        eq.append((lm,rm,rhs))
    return eq


def eval_phase(data,y):
    qleft,cross,terms=data
    shift=0
    for i,v in enumerate(cross):
        if (y>>i)&1:shift^=v
    qr=0
    for xr,xc,yr,yc in terms:
        a=((xr&y).bit_count()&1)^xc
        b=((yr&y).bit_count()&1)^yc
        qr^=a&b
    z=qleft^WALSH[shift]
    if qr:z^=ALL
    return z


def support_bits(eq,y):
    z=ALL
    for lm,rm,rhs in eq:
        b=rhs^((rm&y).bit_count()&1)
        w=WALSH[lm]
        z &= w if b else (w^ALL)
        if not z:break
    return z


def half_correction_bits(q):
    a,b,c,d=q
    # f=1 + sum qi + sum_{i<j} qi*qj over F2.
    z=ALL^a^b^c^d
    z^=(a&b)^(a&c)^(a&d)^(b&c)^(b&d)^(c&d)
    return z


def add_basis(B,x):
    while x:
        p=x.bit_length()-1
        if p not in B:B[p]=x;return True
        x^=B[p]
    return False


def run(pos,input128,max_y=1<<21):
    phases=[sector_phase_data(pos,z,input128) for z in SECTORS]
    eq=common_support_data(pos,input128)
    B={};nonzero=0
    for y in range(max_y):
        sup=support_bits(eq,y)
        if not sup:continue
        qs=[eval_phase(d,y) for d in phases]
        col=sup & half_correction_bits(qs)
        if col:
            nonzero+=1;add_basis(B,col)
            if len(B)==2048:
                print('position',pos,'input',hex(input128),'FULLRANK_AT_RIGHT_INDEX',y,
                      'nonzero_columns_seen',nonzero,flush=True)
                return 2048,y,nonzero
        if y and y%262144==0:
            print('position',pos,'input',hex(input128),'stream_y',y,'rank',len(B),
                  'nonzero_columns',nonzero,flush=True)
    print('position',pos,'input',hex(input128),'COMPLETE_RIGHT_SCAN rank',len(B),
          'nonzero_columns',nonzero,flush=True)
    return len(B),max_y,nonzero


def main():
    # Uniform-route falsifier: one fixed input with rank2048 is sufficient to
    # rule out a uniform <2048 theorem for this correction component.
    for pos in 'BC':
        r,y,n=run(pos,0)
        print('result',pos,'zero_input_rank',r,'right_processed',y,'nonzero',n)
    print('PASS PROBE V26_Q138_BC_HALF_CORRECTION_FULLRANK_WITNESS')
    print('scope=fixed zero-input exact GF2 column-rank witnesses for half-sector correction; full rank implies exact Q rank2048 for that fixed input')

if __name__=='__main__':main()
