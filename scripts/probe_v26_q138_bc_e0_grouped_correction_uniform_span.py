#!/usr/bin/env python3
import sys
from collections import Counter,defaultdict
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as B
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import probe_v26_q138_predecessor_leaf_bc_e0_sign_left_factors as E

ALL=(1<<2048)-1
WALSH=E.WALSH
S=sorted(A.S1)


def insert(Ba,x):
    y=x
    while y:
        p=y.bit_length()-1
        if p not in Ba:
            Ba[p]=y;return True
        y^=Ba[p]
    return False


def row_basis(rows):
    Ba={}
    for x in rows:insert(Ba,x)
    return list(Ba.values())


def phase_data(pos,Cmask,extras):
    FF,subs,rank,eindex=E.generalized_substitution(pos,Cmask,extras)
    qbits=0;cross_cols=[0]*len(E.right_ext)
    ridx={e:k for k,e in enumerate(E.right_ext)}
    for j in range(1,5):
        for i in range(31):
            X=T.xx(FF[j,i,'u'],FF[j,i,'w'])
            Y=T.xx(FF[j,i,'v'],FF[j,i,'w'])
            xm,xc=A.sub_form(X,subs,eindex);ym,yc=A.sub_form(Y,subs,eindex)
            xl=yl=0
            for q,e in enumerate(E.left_ext):
                if (xm>>e)&1:xl|=1<<q
                if (ym>>e)&1:yl|=1<<q
            for e in E.right_ext:
                if (ym>>e)&1:cross_cols[ridx[e]]^=xl
                if (xm>>e)&1:cross_cols[ridx[e]]^=yl
            z=WALSH[xl]&WALSH[yl]
            if xc:z^=WALSH[yl]
            if yc:z^=WALSH[xl]
            if xc&yc:z^=ALL
            qbits^=z
    return qbits,cross_cols,rank


def left_basis(can):
    rows=[]
    for row in can:
        v=0
        for q,i in enumerate(S):
            if (row>>(128+i))&1:v|=1<<q
        if v:rows.append(v)
    return row_basis(rows)


def coset_masks(lb):
    out=[]
    for bits in range(1<<len(lb)):
        z=ALL
        for j,f in enumerate(lb):
            w=WALSH[f]
            z &= w if ((bits>>j)&1) else (w^ALL)
        if z:out.append(z)
    return out


def run(pos):
    e0,e1,half=H.classify_patterns()
    groups={}
    raw=0
    for k in range(4):
        for zs,cls in e0[k]:
            can=H.support_for(pos,zs,cls)
            if can is None:continue
            raw+=1
            Cmask=D.carries(zs)
            sol=A.internal_null(pos,Cmask)
            dirs,pr=B.radical_directions(pos,sol[2])
            assert (sol[0],len(sol[2]),pr)==cls
            FF=D.full_forms(pos)
            extras=[A.derivative_form(FF,A.map_internal_to_full(d)) for d in dirs]
            qbits,cols,rank=phase_data(pos,Cmask,extras)
            assert rank==128
            if can not in groups:
                groups[can]=[0,[0]*len(cols),0]
            g=groups[can];g[0]^=qbits;g[1]=[a^b for a,b in zip(g[1],cols)];g[2]+=1

    assert raw==(581 if pos=='B' else 577)
    expected_mult=Counter({1:103,4:91,2:57}) if pos=='B' else Counter({1:103,4:90,2:57})
    assert Counter(g[2] for g in groups.values())==expected_mult

    GB={};cross_dist=Counter();left_dist=Counter();zero_phase=0
    for can,(qbits,cols,mult) in groups.items():
        cb=row_basis(cols);cross_dist[len(cb)]+=1
        if qbits==0 and not cb:zero_phase+=1
        lb=left_basis(can);left_dist[len(lb)]+=1
        masks=coset_masks(lb)
        # The XOR of right-only phase parts is still just a scalar for every
        # fixed non-left assignment, hence the constant left function is safe.
        local=[qbits,ALL]+[WALSH[f] for f in cb]
        for s in masks:
            for g in local:insert(GB,s&g)

    print('position',pos,'raw_e0',raw,'canonical_support_groups',len(groups),
          'multiplicity_distribution',dict(expected_mult),
          'group_cross_rank_distribution',dict(sorted(cross_dist.items())),
          'group_left_support_rank_distribution',dict(sorted(left_dist.items())),
          'identically_zero_left_and_cross_groups',zero_phase,
          'uniform_grouped_e0_correction_left_span_bound',len(GB),flush=True)
    return len(GB)


def main():
    vals={p:run(p) for p in 'BC'}
    print('PASS PROBE V26_Q138_BC_E0_GROUPED_CORRECTION_UNIFORM_SPAN')
    print('results',vals)
    print('scope=uniform GF2 left-span bound after exact modulo2 aggregation of all raw-e0 sectors sharing the same canonical support')

if __name__=='__main__':main()
