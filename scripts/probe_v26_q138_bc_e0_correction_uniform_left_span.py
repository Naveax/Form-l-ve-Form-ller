#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as B
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import probe_v26_q138_predecessor_leaf_bc_e0_sign_left_factors as E

ALL=(1<<2048)-1
WALSH=E.WALSH


def insert(Ba,x):
    y=x
    while y:
        p=y.bit_length()-1
        if p not in Ba:
            Ba[p]=y;return True
        y^=Ba[p]
    return False


def left_row_basis(can):
    rows=[]
    for row in can:
        v=0
        for q,i in enumerate(E.F.S):
            if (row>>(128+i))&1:v|=1<<q
        if v:rows.append(v)
    Ba={}
    for x in rows:insert(Ba,x)
    return list(Ba.values())


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
    global_basis={};sectors=0
    left_rank_dist={};cross_rank_dist={};max_cosets=0
    for k in range(4):
        for zs,cls in e0[k]:
            can=H.support_for(pos,zs,cls)
            if can is None:continue
            sectors+=1
            Cmask=D.carries(zs)
            sol=A.internal_null(pos,Cmask)
            dirs,pr=B.radical_directions(pos,sol[2])
            assert (sol[0],len(sol[2]),pr)==cls
            FF=D.full_forms(pos)
            extras=[A.derivative_form(FF,A.map_internal_to_full(d)) for d in dirs]
            qbits,crossB,rank=E.left_chirp_and_cross(pos,Cmask,extras)
            assert rank==128

            lb=left_row_basis(can)
            masks=coset_masks(lb)
            left_rank_dist[len(lb)]=left_rank_dist.get(len(lb),0)+1
            cross_rank_dist[len(crossB)]=cross_rank_dist.get(len(crossB),0)+1
            max_cosets=max(max_cosets,len(masks))

            # For any fixed predecessor/right assignment the quadratic sign bit
            # restricted to the left variables is qbits + affine.  Its affine
            # frequency lies in span(crossB), with an arbitrary right-only
            # constant.  A basis of the column-function family is therefore
            # qbits, 1, and the linear truth functions for a basis of crossB.
            local=[qbits,ALL]+[WALSH[f] for f in crossB]
            # Every fixed non-left assignment turns the support equations into
            # one of the cosets of the restricted left row space.  Enumerating
            # every coset safely over-approximates reachability/correlation.
            for s in masks:
                for g in local:insert(global_basis,s&g)

    assert sectors==(581 if pos=='B' else 577)
    print('position',pos,'e0_consistent_sectors',sectors,
          'left_support_rank_distribution',dict(sorted(left_rank_dist.items())),
          'cross_rank_distribution',dict(sorted(cross_rank_dist.items())),
          'max_left_cosets_per_sector',max_cosets,
          'uniform_e0_correction_left_span_bound',len(global_basis),flush=True)
    return len(global_basis)


def main():
    vals={p:run(p) for p in 'BC'}
    print('PASS PROBE V26_Q138_BC_E0_CORRECTION_UNIFORM_LEFT_SPAN')
    print('results',vals)
    print('scope=uniform GF2 left-span bound for the assembled raw-e0 negative-sign second-bit correction; all predecessor/right support cosets and affine phase shifts are safely over-approximated')

if __name__=='__main__':main()
