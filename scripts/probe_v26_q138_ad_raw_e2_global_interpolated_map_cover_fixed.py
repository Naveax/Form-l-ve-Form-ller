#!/usr/bin/env python3
import probe_v26_q138_ad_raw_e2_global_interpolated_map_cover as P

MASK=(1<<128)-1


def canonical_map_on_condition(B,M):
    out=[]
    piv=sorted(B,reverse=True)
    for m,b in M:
        y=m; bb=b
        for p in piv:
            if (y>>p)&1:
                rr=B[p]
                y ^= rr&MASK
                bb ^= (rr>>128)&1
        out.append((y,bb))
    return tuple(out)


P.canonical_map_on_condition=canonical_map_on_condition

if __name__=='__main__':
    P.main()
