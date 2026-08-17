#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_bc_input_activity_no_gain as N
import probe_v26_q138_predecessor_leaf_bc_half_correction_fullrank_witness as H

ALL=(1<<2048)-1
SECTORS=H.SECTORS


def right_quadratic(terms):
    lin=0;const=0;adj=[0]*21
    for xr,xc,yr,yc in terms:
        const ^= xc&yc
        if xc:lin ^= yr
        if yc:lin ^= xr
        both=xr&yr;lin ^= both
        aa=[];m=xr
        while m:
            a=(m&-m).bit_length()-1;aa.append(a);m^=1<<a
        bb=[];m=yr
        while m:
            b=(m&-m).bit_length()-1;bb.append(b);m^=1<<b
        for a in aa:
            for b in bb:
                if a==b:continue
                lo,hi=(a,b) if a<b else (b,a)
                adj[lo] ^= 1<<hi
                adj[hi] ^= 1<<lo
    return lin,const,adj


def phase_setup(pos,z,input128):
    qleft,cross,terms=H.sector_phase_data(pos,z,input128)
    lin,const,adj=right_quadratic(terms)
    return qleft,cross,lin,const,adj


def support_table(eq):
    # eq list (leftmask,rightmask,rhs). table indexed by current right syndrome bits.
    out={}
    for syn in range(1<<len(eq)):
        z=ALL
        for i,(lm,rm,rhs) in enumerate(eq):
            b=rhs^((syn>>i)&1)
            w=H.WALSH[lm]
            z &= w if b else (w^ALL)
            if not z:break
        out[syn]=z
    return out


def add_basis(B,x):
    while x:
        p=x.bit_length()-1
        if p not in B:B[p]=x;return True
        x^=B[p]
    return False


def run(pos):
    can=N.residue_objects(pos)[0][-1]
    sol=T.rref(N.input_equations(can),n=128);assert sol is not None
    irank,input0,ibasis=sol
    eq=H.common_support_data(pos,input0)
    stable=support_table(eq)
    # Current right syndrome at y=0 is all zeros (table XORs stored rhs itself).
    syn=0
    phase=[phase_setup(pos,z,input0) for z in SECTORS]
    qR=[d[3] for d in phase]
    shift=[0]*4
    y=0;prevgray=0;B={};nonzero=0
    Nright=1<<21
    for step in range(Nright):
        if step:
            gray=step^(step>>1);diff=gray^prevgray;t=(diff&-diff).bit_length()-1
            oldy=y
            # update qR before y flip, using derivative at old y
            for i,(qleft,cross,lin,const,adj) in enumerate(phase):
                deriv=((lin>>t)&1)^((adj[t]&oldy).bit_count()&1)
                qR[i]^=deriv
                shift[i]^=cross[t]
            # update support right syndromes
            for j,(lm,rm,rhs) in enumerate(eq):
                if (rm>>t)&1:syn^=1<<j
            y^=1<<t;prevgray=gray
        sup=stable[syn]
        if not sup:continue
        qs=[]
        for i,(qleft,cross,lin,const,adj) in enumerate(phase):
            z=qleft^H.WALSH[shift[i]]
            if qR[i]:z^=ALL
            qs.append(z)
        col=sup & H.half_correction_bits(qs)
        if col:
            nonzero+=1;add_basis(B,col)
            if len(B)==2048:
                print('position',pos,'input_condition_rank',irank,'active_input',hex(input0),
                      'FULLRANK2048_at_gray_step',step,'right_assignment',hex(y),
                      'nonzero_columns_seen',nonzero,flush=True)
                return 2048,step
        if step and step%262144==0:
            print('position',pos,'step',step,'rank',len(B),'nonzero',nonzero,flush=True)
    print('position',pos,'COMPLETE_SCAN_rank',len(B),'nonzero',nonzero,flush=True)
    return len(B),Nright


def main():
    vals={p:run(p) for p in 'BC'}
    print('PASS PROBE V26_Q138_BC_HALF_CORRECTION_ACTIVE_FAST')
    print('results',vals)
    print('scope=exact GF2 rank for canonical active predecessor-input witness; rank2048 proves fixed-input Q-rank2048 for this correction component')

if __name__=='__main__':main()
