#!/usr/bin/env python3
import itertools,sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as B

RANK128=[((1,0),(2,0)),((1,0),(4,0)),((2,0),(3,0)),((3,0),(4,0))]


def correction_value(q):
    n=sum(q)
    return 1 if n in (0,3,4) else 0


def walsh_coeff(mask):
    s=0
    for q in itertools.product((0,1),repeat=4):
        parity=sum(q[i] for i in range(4) if (mask>>i)&1)&1
        s += correction_value(q) * (-1 if parity else 1)
    return Fraction(s,16)


def main():
    coeff={m:walsh_coeff(m) for m in range(16)}
    assert all(c for c in coeff.values())
    print('half_correction_walsh_coefficients',
          {format(m,'04b'):str(c) for m,c in coeff.items()},flush=True)

    for pos in 'BC':
        supports=[A.canonical_support(pos,D.carries(z),expect_internal=128) for z in RANK128]
        assert all(x==supports[0] for x in supports)
        sd=A.cut_intersection(supports[0]);assert sd==2
        qrows=[B.sign_cross_rows(pos,D.carries(z)) for z in RANK128]
        dist=Counter();ranks={}
        total=0
        for mask,c in coeff.items():
            rows=[0]*len(A.S1)
            for i in range(4):
                if (mask>>i)&1:rows=[a^b for a,b in zip(rows,qrows[i])]
            r=T.gf2_rank(rows,len(A.R1));ranks[mask]=r;dist[r]+=1
            total += (1<<sd)*(1<<r)
        bound=min(2048,total)
        print('position',pos,'subset_cross_rank_distribution',dict(sorted(dist.items())),
              'subset_cross_ranks',{format(m,'04b'):ranks[m] for m in range(16)},
              'support_rectangles',1<<sd,'fourier_sum_rank_bound',total,
              'row_cap_adjusted_bound',bound,flush=True)

    print('PASS PROBE V26_Q138_BC_HALF_GROUP_SECOND_CORRECTION')
    print('scope=uniform rank bound for weight122 four-half-sector second-bit correction via Boolean Walsh expansion')

if __name__=='__main__':main()
