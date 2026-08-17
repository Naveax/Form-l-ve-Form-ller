#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_leaf_ht95 as H

N=32
class Vars:
    def __init__(self):self.d={}
    def id(self,n):
        if n not in self.d:self.d[n]=len(self.d)
        return self.d[n]

def rank(rows):
    B={}
    for z in rows:
        x=z
        while x:
            c=x.bit_length()-1
            if c not in B:B[c]=x;break
            x^=B[c]
    return len(B)

def build():
    V=Vars();eq=[]
    def var(n):return V.id(n)
    def add(names):
        z=0
        for n in names:z^=1<<var(n)
        eq.append(z)
    # q138 has fixed output Bf bit10; constants alter RHS only and do not affect
    # projected linear dimension, so omit affine constants.
    for j in (4,3,2,1):
        for i in range(1,N):
            names=[f's{j}_{i-1}']
            if i<31:names.append(f's{j}_{i}')
            if j==4:names += [f'u4_{i}',f'v4_{i}'] # w4 is fixed constant
            elif j==3:names += [f'u3_{i}',f'v3_{i}',f'v4_{(i+8)%N}']
            elif j==2:names += [f'C_{i}',f'v4_{(i+8)%N}',f'D_{(i+16)%N}',f'u4_{i}',f'v3_{(i+12)%N}']
            else:names += [f'A_{i}',f'B_{i}',f'v3_{(i+12)%N}',f'u3_{i}',f'D_{i}']
            add(names)
    # Ensure all physical and internal variables exist even if bit0 recurrence
    # does not impose a linear equation after summing sigma_-1.
    for i in range(N):
        for w in 'ABCD':var(f'{w}_{i}')
        for x in ('u4','v4','u3','v3'):var(f'{x}_{i}')
        for j in (1,2,3,4):
            if i<31:var(f's{j}_{i}')
    return V,eq

def critical_sets():
    root,nodes=H.walk(H.TREE,True);out=[]
    for rec in nodes:
        S=set(rec[0])
        if H.message_exponent(S)==88:
            if len(S)>16:S=set(range(N))-S
            if S not in out:out.append(S)
    assert len(out)==3 and all(len(S)==11 for S in out)
    return out

def projected_codim(V,eq,S):
    X={V.d[f'{w}_{i}'] for i in S for w in 'ABCD'};assert len(X)==44
    # B consists of all non-X columns. Codim of projection onto X is
    # rank([B A])-rank(B) = rank(full)-rank(B).
    full=rank(eq);brows=[]
    maskX=sum(1<<i for i in X)
    for r in eq:brows.append(r & ~maskX)
    rb=rank(brows);return full-rb,full,rb

def main():
    V,eq=build();vals=[]
    for q,S in enumerate(critical_sets(),1):
        c,rf,rb=projected_codim(V,eq,S);vals.append(c)
        print('partition',q,'sites',sorted(S),'boundary_bits=44','full_eq_rank',rf,'other_column_rank',rb,'pure_boundary_parity_codim',c)
    assert vals==[0,0,0],vals
    print('PASS V26_Q138_CENTRAL_BOUNDARY_GF2_CONSTRAINTS')
    print('critical_partitions_pure_linear_boundary_constraints=0,0,0')
    print('scope=sigma recurrence plus exact XOR/rotation linear relations; nonlinear sigma=0 equality support not included')
    print('consequence=no free GF2 parity reduction below central exponent44 on critical HT88 cuts')
if __name__=='__main__':main()
