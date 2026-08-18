#!/usr/bin/env python3
import probe_v26_q138_ad_fast_external_consistency_e3 as P


def reduce_extra_full(B,row,e):
    y=row;ee=e
    # Reduce by every base pivot, not only until the first unmatched leading
    # coordinate. Otherwise XORs of two quotient rows can expose a lower base
    # pivot and create false consistency.
    for p in sorted(B,reverse=True):
        if (y>>p)&1:
            r,re=B[p]
            y^=r;ee^=re
    return y,ee


P.reduce_extra=reduce_extra_full

if __name__=='__main__':
    P.main()
