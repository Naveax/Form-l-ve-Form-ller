#!/usr/bin/env python3
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_depth_joint_sector_law as J

S3=J.A.S3
CENTER=24663038400
FULL=189*(2**56)


def cost(S,d):
    m,c,s,f,v=J.A.caps(S);F=frozenset(S);C=frozenset(set(range(32))-set(F));special=(F==S3 or C==S3)
    ce=math.log2(CENTER) if special else float(c)
    fe=math.log2(FULL) if special else float(f)
    return ce+4*s+(8*d-12)*fe+4*v

def main():
    root,sets=J.A.walk(J.A.TREE,True);assert root==set(range(32))
    # Generic fully-open common-tree maximum was 65 only on S3 and complement;
    # next generic fully-open cap is 62.
    fs=sorted((J.A.caps(S)[3],frozenset(S)) for S in sets)
    assert fs[-1][0]==65 and fs[-2][0]==65 and fs[-3][0]==62
    vals={d:max(cost(S,d) for S in sets) for d in range(2,10)}
    for d,v in vals.items():
        target=math.log2(CENTER)+396+(8*d-12)*math.log2(FULL)
        assert abs(v-target)<1e-11,(d,v,target)
    slope=8*math.log2(FULL)
    intercept=math.log2(CENTER)+396-12*math.log2(FULL)
    print('PASS V26_Q138_DEPTH_FULLY_OPEN_SIGNED_SLOPE')
    print('fully_open_S3_rank<=189*2^56 log2=%.15f' % math.log2(FULL))
    print('next_generic_fully_open_common_tree_cap=62')
    print('d>=2 W_repr(d)<=log2(24663038400)+396+(8d-12)*log2(189*2^56)')
    print('affine_numeric_slope=%.15f intercept=%.15f' % (slope,intercept))
    print('verified='+','.join(f'{d}:{vals[d]:.12f}' for d in sorted(vals)))
    print('slope_gain_vs_520=%.15f bits_per_double_round' % (520-slope))
    print('scope=exact representation/message upper bound; constructive/work/optimality not claimed')
if __name__=='__main__':main()
