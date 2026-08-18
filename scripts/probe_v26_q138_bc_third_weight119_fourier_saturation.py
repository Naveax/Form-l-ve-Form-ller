#!/usr/bin/env python3
import itertools,sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_predecessor_leaf_fast_nullspace_fourier as Q

MAX_TEST=2_000_000


def main():
    sites=[(j,i) for j in range(1,5) for i in range(31)]
    for pos in 'BC':
        F,res,free,extra=Q.setup(pos,False)
        U=set();full=0;growth=[];sat_at=None
        for tested,zs in enumerate(itertools.combinations(sites,5),1):
            B=Q.left_space(res,free,extra,zs)
            if B is not None:
                full+=1
                before=len(U);U |= Q.enumerate_space(B)
                if len(U)>before and len(growth)<40:growth.append((tested,zs,len(B),len(U)))
                if len(U)==2048:
                    sat_at=tested;break
            if tested>=MAX_TEST:break
        print('position',pos,'weight119_tested',tested,'fullrank_seen',full,
              'left_frequency_union',len(U),'saturated',sat_at is not None,
              'saturation_at',sat_at,'growth',repr(growth),flush=True)
    print('PASS PROBE V26_Q138_BC_THIRD_WEIGHT119_FOURIER_SATURATION')
    print('scope=deterministic saturation witness search; if saturated, exact union=2048; if not saturated before cap, no upper-bound claim')

if __name__=='__main__':main()
