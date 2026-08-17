#!/usr/bin/env python3
import itertools,sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as B
import probe_v26_q138_predecessor_leaf_ad_affine_fourier_union as F
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H

S=sorted(A.S1); left_ext=[128+i for i in S]; left_set=set(left_ext)
right_ext=[i for i in range(160) if i not in left_set]
ALL=(1<<2048)-1

WALSH=[]
for f in range(1<<11):
    z=0
    for x in range(1<<11):
        if (f&x).bit_count()&1:z|=1<<x
    WALSH.append(z)


def generalized_substitution(pos,Cmask,extras):
    FF=D.full_forms(pos)
    E=D.equations(FF,Cmask,hom=False)+list(extras)
    rows=[m|((rhs&1)<<D.GN) for m,rhs in E]
    ints=A.internal_cols();r=0;piv=[]
    for col in ints:
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        piv.append(col);r+=1
    ec=A.ext_cols();eindex={col:i for i,col in enumerate(ec)}
    subs={}
    for row,p in zip(rows[:r],piv):
        m=0
        for col,ei in eindex.items():
            if (row>>col)&1:m|=1<<ei
        subs[p]=(m,(row>>D.GN)&1)
    for col in ints:
        if col not in subs:subs[col]=(0,0)
    return FF,subs,r,eindex


def left_chirp_and_cross(pos,Cmask,extras):
    FF,subs,rank,eindex=generalized_substitution(pos,Cmask,extras)
    qbits=0;cross_cols=[0]*len(right_ext)
    ridx={e:k for k,e in enumerate(right_ext)}
    for j in range(1,5):
        for i in range(31):
            X=T.xx(FF[j,i,'u'],FF[j,i,'w'])
            Y=T.xx(FF[j,i,'v'],FF[j,i,'w'])
            xm,xc=A.sub_form(X,subs,eindex);ym,yc=A.sub_form(Y,subs,eindex)
            xl=yl=0
            for q,e in enumerate(left_ext):
                if (xm>>e)&1:xl|=1<<q
                if (ym>>e)&1:yl|=1<<q
            for e in right_ext:
                v=0
                if (ym>>e)&1:v^=xl
                if (xm>>e)&1:v^=yl
                cross_cols[ridx[e]]^=v
            for x in range(1<<11):
                a=((xl&x).bit_count()&1)^xc
                b=((yl&x).bit_count()&1)^yc
                if a&b:qbits^=1<<x
    Bc={}
    for v in cross_cols:
        x=v
        while x:
            p=x.bit_length()-1
            if p not in Bc:Bc[p]=x;break
            x^=Bc[p]
    return qbits,list(Bc.values()),rank


def canonical_sign_vector(qbits,f):
    z=qbits^WALSH[f]
    zc=z^ALL
    return min(z,zc)


def main():
    e0,e1,half=H.classify_patterns()
    for pos in 'BC':
        factors=set();cross_dist=Counter();support_freq_union=set();consistent=0
        for k in range(4):
            for zs,cls in e0[k]:
                can=H.support_for(pos,zs,cls)
                if can is None:continue
                consistent+=1
                Cmask=D.carries(zs)
                sol=A.internal_null(pos,Cmask)
                dirs,pr=B.radical_directions(pos,sol[2])
                assert (sol[0],len(sol[2]),pr)==cls
                FF=D.full_forms(pos)
                extras=[A.derivative_form(FF,A.map_internal_to_full(d)) for d in dirs]
                qbits,crossB,rank=left_chirp_and_cross(pos,Cmask,extras)
                cross_dist[len(crossB)]+=1
                SF=F.enumerate_space(F.rowspace_basis(can,F.S));support_freq_union|=SF
                CF=F.enumerate_space(crossB)
                shifts={a^b for a in SF for b in CF}
                for f in shifts:factors.add(canonical_sign_vector(qbits,f))
        expected=581 if pos=='B' else 577
        assert consistent==expected,(pos,consistent)
        print('position',pos,'e0_consistent_sectors',consistent,
              'support_frequency_union',len(support_freq_union),
              'cross_rank_distribution',dict(sorted(cross_dist.items())),
              'distinct_sign_left_factors_up_to_scalar',len(factors),
              'uniform_e0_negative_sign_rank_bound_by_factor_count',len(factors)+len(support_freq_union),flush=True)

    print('PASS PROBE V26_Q138_BC_E0_SIGN_LEFT_FACTORS')
    print('scope=uniform left-factor-count upper bound for raw e0 negative-sign correction; exact Q-span may be smaller; half-sector correction excluded')

if __name__=='__main__':main()
