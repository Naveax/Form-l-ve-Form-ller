#!/usr/bin/env python3
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_leaf_ht95 as H
import verify_v26_q138_double_round_signed85 as S

TREE=H.TREE
S1=set(S.S1)
COMP=set(range(32))-S1


def edges():
    E=[]
    for i in range(31):E.append((i,i+1,4))
    for d in (8,12,16):
        seen=set()
        for i in range(32):
            j=(i+d)%32;e=tuple(sorted((i,j)))
            if e in seen:continue
            seen.add(e);E.append((e[0],e[1],1))
    return E
E=edges()

def gb(A):
    A=set(A);return sum(w for u,v,w in E if (u in A)!=(v in A))

def nodes(t,include_root=False):
    out=[]
    def walk(q,root=False):
        if isinstance(q,int):return {q}
        A=walk(q[0]);B=walk(q[1]);U=A|B
        if include_root or not root:out.append(U)
        return U
    root=walk(t,True)
    out.extend({i} for i in root)
    return root,out

def main():
    # Frozen constructive tree root split is S1 | complement(S1).
    left,right=TREE
    RL,NL=nodes(left);RR,NR=nodes(right)
    assert RL==S1 and RR==COMP and len(COMP)==21

    # Signed central rank channel. The clean physical-row bridge proves the
    # block2 rank2784 basis can be generated from <=64 physical block2 rows;
    # block1 contributes rank16 and remaining26 row bits are identity channels.
    R=16*2784*(2**26);assert R==87*(2**35)
    table=R*(2**44);assert table==87*(2**79)
    assert math.log2(table)<86

    # For one physical S1 basis row, central S1 inputs are fixed. Contracting
    # the exact reduced central graph on the left subtree has internal peak34
    # and leaves only the 51-bit S1/complement graph boundary.
    assert max(gb(A) for A in NL)==34
    assert gb(S1)==51

    # For a fixed leaf-left assignment alpha (44 bits total), each predecessor
    # leaf becomes an arbitrary exact vector on the21 complement bit positions.
    # Its Hilbert exponent across T|COMP\T is min(k,21-k); four leaves contribute
    # 4*min(k,21-k). Use the existing exact reduced central graph for gb(T).
    costs={frozenset(A):gb(A)+4*min(len(A),21-len(A)) for A in NR}
    mx=max(costs.values());assert mx==94,mx
    witnesses=[sorted(A) for A,v in costs.items() if v==94]
    assert witnesses==[[17,18,19,20,21,22,23,24,25,26]],witnesses

    # The complement root itself carries only the 51 central boundary bits;
    # the four 21-bit leaf slices are fully contracted there, after which the
    # stored fixed-row S1 boundary factor closes the scalar.
    assert gb(COMP)==51

    # Factor-generation ledger:
    # - old exact leaf vectors can be generated with peak<=44 (constructive95 dependency);
    # - left signed table U(alpha,r) has exponent85.443;
    # - each right-table entry N(r,alpha) is a sum of <=64 physical-slice contractions
    #   (physical-row bridge dependency), each with peak94 above;
    # - dense N table has the same exponent85.443;
    # - final dot product can stream over the two tables.
    assert 44<94 and math.log2(table)<94 and 51<94
    print('PASS V26_Q138_DOUBLE_ROUND_CONSTRUCTIVE94')
    print('signed_rank_R=87*2^35')
    print('left_and_right_factor_table=87*2^79 log2=%.15f' % math.log2(table))
    print('fixed_physical_S1_central_boundary=51; left_internal_central_peak=34')
    print('fixed_alpha_complement_graph_plus_four_21bit_leaf_peak=94')
    print('unique_94_witness='+str(witnesses[0]))
    print('right_basis_slice_expansion<=64 physical S1 slices (verified by physical-row bridge dependency)')
    print('W2_construct<=94')
    print('scope=explicit exact factor-generation/contraction structural-message bound; arithmetic work may be enormous and is not reduced')
if __name__=='__main__':main()
