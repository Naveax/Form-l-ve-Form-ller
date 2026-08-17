#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_bc_input_activity_no_gain as N
import probe_v26_q138_predecessor_leaf_bc_half_correction_fullrank_witness as H
import probe_v26_q138_predecessor_leaf_bc_half_correction_active_fast as F

ALL=(1<<2048)-1


def basis_insert(B,x):
    y=x
    while y:
        p=y.bit_length()-1
        if p not in B:
            B[p]=y
            return True
        y ^= B[p]
    return False


def basis_list(vs):
    B={}
    for v in vs:
        basis_insert(B,v)
    return list(B.values())


def left_affine_basis(pos,z,x0,ibasis,base_qleft,cross):
    # Safe uniform affine-delta space: all y-induced linear characters,
    # all active-input-induced affine deltas, and the constant function.
    vs=[ALL]
    for f in cross:
        if f:
            vs.append(H.WALSH[f])
    for b in ibasis:
        qleft,_,_=H.sector_phase_data(pos,z,x0^b)
        d=qleft^base_qleft
        # Input deltas were independently certified affine by the parameter probe.
        vs.append(d)
    return basis_list(vs)


def support_masks(pos,x0):
    eq=H.common_support_data(pos,x0)
    masks=[]
    seen=set()
    for s in F.support_table(eq).values():
        if s and s not in seen:
            seen.add(s);masks.append(s)
    # Iterating every right syndrome over-approximates every input-dependent RHS
    # translation, since the homogeneous left masks are fixed.
    return eq,masks


def run(pos):
    can=N.residue_objects(pos)[0][-1]
    sol=T.rref(N.input_equations(can),n=128);assert sol is not None
    irank,x0,ibasis=sol
    assert irank==5 and len(ibasis)==123

    Q=[];A=[]
    for z in H.SECTORS:
        qleft,cross,_=H.sector_phase_data(pos,z,x0)
        Q.append(qleft)
        A.append(left_affine_basis(pos,z,x0,ibasis,qleft,cross))

    # Span containing 1 + sum(q_i) + sum_{i<j}q_i q_j for every
    # q_i=Q_i+a_i, a_i in A_i.  AND is multiplication in Boolean ANF
    # and distributes over XOR, so basis products suffice.
    gens=[ALL]
    for i in range(4):
        gens.append(Q[i]);gens.extend(A[i])
    for i in range(4):
        for j in range(i+1,4):
            gens.append(Q[i]&Q[j])
            gens.extend(a&Q[j] for a in A[i])
            gens.extend(Q[i]&b for b in A[j])
            gens.extend(a&b for a in A[i] for b in A[j])
    core_basis=basis_list(gens)

    eq,masks=support_masks(pos,x0)
    out={}
    for s in masks:
        for g in core_basis:
            basis_insert(out,s&g)
    lm_rank=T.gf2_rank([lm for lm,rm,rhs in eq],11)
    rm_rank=T.gf2_rank([rm for lm,rm,rhs in eq],21)
    print('position',pos,
          'active_input_dim',len(ibasis),
          'affine_dims',[len(a) for a in A],
          'unrestricted_half_core_span',len(core_basis),
          'support_equations',len(eq),'left_support_rank',lm_rank,
          'right_support_rank',rm_rank,'nonzero_left_cosets',len(masks),
          'uniform_supported_left_span_bound',len(out),flush=True)
    return len(out)


def main():
    vals={p:run(p) for p in 'BC'}
    print('PASS PROBE V26_Q138_BC_HALF_UNIFORM_LEFT_SPAN')
    print('results',vals)
    print('scope=uniform GF2 left-function span upper bound for the half-sector correction over every active predecessor input and every right assignment; correlations are safely over-approximated')

if __name__=='__main__':main()
