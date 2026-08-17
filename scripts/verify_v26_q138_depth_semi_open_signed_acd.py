#!/usr/bin/env python3
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_depth_joint_sector_law as J

S3=J.A.S3
CENTER=24663038400
FULL=189*(2**56)
A=405*(2**46)
B=2**55
C=243*(2**47)
D=3429*(2**42)
SEMI=A*B*C*D

def cost(S,d):
    m,c,s,f,v=J.A.caps(S);F=frozenset(S);C0=frozenset(set(range(32))-set(F));special=(F==S3 or C0==S3)
    ce=math.log2(CENTER) if special else float(c)
    if special:
        se=math.log2(SEMI)
        fe=math.log2(FULL)
        return ce+se+(8*d-12)*fe+4*v
    return float(c)+4*float(s)+(8*d-12)*float(f)+4*float(v)

def main():
    root,sets=J.A.walk(J.A.TREE,True);assert root==set(range(32))
    assert D==3429*(2**42)
    assert abs(math.log2(SEMI)-218.3301627903134)<1e-12
    vals={d:max(cost(S,d) for S in sets) for d in range(2,10)}
    for d,v in vals.items():
        target=math.log2(CENTER)+math.log2(SEMI)+(8*d-12)*math.log2(FULL)+176
        assert abs(v-target)<1e-10,(d,v,target)
    slope=8*math.log2(FULL)
    intercept=math.log2(CENTER)+math.log2(SEMI)-12*math.log2(FULL)+176
    print('PASS V26_Q138_DEPTH_SEMI_OPEN_SIGNED_ACD')
    print('semi_A_log2=%.15f semi_B=55 semi_C_log2=%.15f semi_D_log2=%.15f' % (math.log2(A),math.log2(C),math.log2(D)))
    print('four_semi_total_log2=%.15f' % math.log2(SEMI))
    print('d>=2 affine_slope=%.15f intercept=%.15f' % (slope,intercept))
    print('verified='+','.join(f'{d}:{vals[d]:.12f}' for d in sorted(vals)))
    print('scope=exact representation/message upper bound; constructive/work/optimality not claimed')
if __name__=='__main__':main()
