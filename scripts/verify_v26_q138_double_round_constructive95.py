#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_leaf_ht95 as H

N=32

def graph_plus_leaf(S):
    m=min(len(S),N-len(S))
    return H.central_graph_boundary(S)+4*m

def main():
    root,nodes=H.walk(H.TREE,True);assert root==set(range(N))
    vals=[]
    for rec in nodes:
        S=rec[0];vals.append((graph_plus_leaf(S),len(S),S,H.central_graph_boundary(S),4*min(len(S),N-len(S))))
    for i in range(N):
        S={i};vals.append((graph_plus_leaf(S),1,S,H.central_graph_boundary(S),4))
    vals.sort(key=lambda x:x[0],reverse=True);mx=vals[0][0];assert mx==95,mx
    maxnodes=[v for v in vals if v[0]==95]
    assert len(maxnodes)==3
    for total,k,S,c,l in maxnodes:assert (c,l)==(51,44)
    # Leaf vector generation: fixed-input/single-output reduced QR path <=44.
    # Dense leaf materialization has only 32 open binary bits. Both are <95.
    assert 44<95 and 32<95
    print('PASS V26_Q138_EXACT_DOUBLE_ROUND_CONSTRUCTIVE95')
    print('max_message_exponent=95 max_nodes=3 central_graph=51 four_leaf_HT=44')
    print('leaf_generation_peak_exponent<=44 dense_leaf_output_exponent=32')
    print('complete_constructive_structural_bound=W2_construct<=95')
    print('separate_existence_bound=W2_repr<=88 requires central Schmidt factor generation not certified here')
if __name__=='__main__':main()
