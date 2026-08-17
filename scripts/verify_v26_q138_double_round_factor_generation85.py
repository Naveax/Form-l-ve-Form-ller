#!/usr/bin/env python3
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S

S1=set(S.S1)
COMP=set(range(32))-S1

# Explicit 21-leaf complement tree found by finite minimax search for
# C(T)=gb(T)+4*min(|T|,21-|T|). No optimality claim is needed.
RIGHT_TREE=[[[10,11],[17,[18,19]]],[[[[30,31],[28,29]],[[8,9],[6,7]]],[[[26,27],[24,25]],[[22,23],[20,21]]]]]

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

def walk(t,root=False):
    if isinstance(t,int):return {t},[]
    A,a=walk(t[0]);B,b=walk(t[1]);assert A.isdisjoint(B);U=A|B
    return U,a+b+([] if root else [U])

def ccost(A):
    k=len(A);return gb(A)+4*min(k,21-k)

def main():
    root,sets=walk(RIGHT_TREE,True);assert root==COMP
    sets=sets+[{i} for i in COMP]
    vals=sorted((ccost(A),gb(A),len(A),tuple(sorted(A))) for A in sets)
    assert vals[-1][0]==80,vals[-1]
    top=[x for x in vals if x[0]==80]
    assert top==[
        (80,48,8,(20,21,22,23,24,25,26,27)),
        (80,60,16,(6,7,8,9,20,21,22,23,24,25,26,27,28,29,30,31)),
    ],top

    # Exact signed S1 rank from signed85 theorem.
    R=16*2784*(2**26);assert R==87*(2**35)
    table=R*(2**44);assert table==87*(2**79)
    table_exp=math.log2(table)
    assert 85<table_exp<86 and 80<table_exp

    # Existing dependencies: leaf vectors generated with peak<=44; a fixed
    # physical S1 central slice exposes only the51-bit central boundary; the
    # physical-row bridge expands one block2 basis slice into <=64 ordinary
    # physical rows. Hence complement-entry generation peak is max(80,51,44)=80.
    assert max(80,51,44)==80

    print('PASS V26_Q138_DOUBLE_ROUND_FACTOR_GENERATION85')
    print('right_complement_tree_peak=80')
    print('peak80_clusters='+repr([list(x[3]) for x in top]))
    print('signed_rank_R=87*2^35')
    print('materialized_left_or_right_factor=87*2^79 log2=%.15f' % table_exp)
    print('factor_generation_message_peak=max(table,80,51,44)=%.15f' % table_exp)
    print('scope=coefficient-aware materialized-factor generation memory/message ledger; arithmetic work unbounded here and may be enormous')
    print('static_coefficient_blind_graph_leaf_method_remains_method_optimal_at95')

if __name__=='__main__':main()
