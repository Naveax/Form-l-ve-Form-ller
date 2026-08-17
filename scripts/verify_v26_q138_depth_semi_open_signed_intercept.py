#!/usr/bin/env python3
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_depth_joint_sector_law as J
import verify_v26_q138_semi_open_s3_signed_ac as S

S3=J.A.S3
CENTER=24663038400
FULL=189*(2**56)
SEMI=S.SEMI_PRODUCT


def cost(Sset,d):
    m,c,s,f,v=J.A.caps(Sset);F=frozenset(Sset);C=frozenset(set(range(32))-set(F));special=(F==S3 or C==S3)
    ce=math.log2(CENTER) if special else float(c)
    se=math.log2(SEMI) if special else float(4*s)
    fe=math.log2(FULL) if special else float(f)
    return ce+se+(8*d-12)*fe+4*v

def main():
    root,sets=J.A.walk(J.A.TREE,True);assert root==set(range(32))
    vals={d:max(cost(X,d) for X in sets) for d in range(2,10)}
    semi_exp=math.log2(SEMI)
    for d,v in vals.items():
        target=math.log2(CENTER)+semi_exp+176+(8*d-12)*math.log2(FULL)
        assert abs(v-target)<1e-11,(d,v,target)
    slope=8*math.log2(FULL)
    intercept=math.log2(CENTER)+semi_exp+176-12*math.log2(FULL)
    assert abs(semi_exp-(203+math.log2(98415)))<1e-12
    print('PASS V26_Q138_DEPTH_SEMI_OPEN_SIGNED_INTERCEPT')
    print('semi_open_S3_product<=98415*2^203 log2=%.15f' % semi_exp)
    print('fully_open_S3_rank<=189*2^56 log2=%.15f' % math.log2(FULL))
    print('d>=2 W_repr(d)<=log2(24663038400)+379+log2(98415)+(8d-12)*log2(189*2^56)')
    print('affine_numeric_slope=%.15f intercept=%.15f' % (slope,intercept))
    print('verified='+','.join(f'{d}:{vals[d]:.12f}' for d in sorted(vals)))
    print('intercept_gain_vs_previous=%.15f bits' % (220-semi_exp))
    print('scope=exact representation/message upper bound; constructive/work/optimality not claimed')
if __name__=='__main__':main()
