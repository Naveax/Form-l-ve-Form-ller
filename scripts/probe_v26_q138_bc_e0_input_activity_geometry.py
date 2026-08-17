#!/usr/bin/env python3
import random,sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_bc_input_activity_no_gain as N
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H


def active(eq,x):
    return all(((m&x).bit_count()&1)==rhs for m,rhs in eq)


def main():
    e0,e1,half=H.classify_patterns()
    rng=random.Random(138120)
    samples=[0,(1<<128)-1]+[1<<i for i in range(128)]
    samples += [rng.getrandbits(128) for _ in range(2000)]
    for pos in 'BC':
        eqs=[]
        for k in range(4):
            for zs,cls in e0[k]:
                can=H.support_for(pos,zs,cls)
                if can is not None:eqs.append(N.input_equations(can))
        assert len(eqs)==(581 if pos=='B' else 577)
        flat=[e for q in eqs for e in q]
        sol=T.rref(flat,n=128)
        vals=[sum(active(eq,x) for eq in eqs) for x in samples]
        print('position',pos,'e0_supports',len(eqs),
              'all_simultaneously_active',sol is not None,
              'combined_rank_if_consistent',sol[0] if sol else None,
              'sample_max_active',max(vals),
              'nonzero_samples',sum(v>0 for v in vals),flush=True)
    print('PASS PROBE V26_Q138_BC_E0_INPUT_ACTIVITY_GEOMETRY')
    print('scope=raw e0 support predecessor-input mutual-exclusion geometry; sample maxima are exploratory unless all-active consistency succeeds')

if __name__=='__main__':main()
