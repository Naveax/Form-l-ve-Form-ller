#!/usr/bin/env python3
import itertools,random,sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
import numpy as np
import opt_einsum as oe

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_leaf_ht95 as H

P=251
INV2=pow(2,P-2,P)
N=32

def bit(x,i):return (x>>i)&1

def tv(s,t,u,v,w):
    if t!=(s^u^v^w) or not(s or u==v==w):return 0
    z=INV2 if s else 1
    if ((u^w)&(v^w)):z=(-z)%P
    return z

def add_factor(j,i,words,pos,copy):
    A0,B0,C0,D0=words
    labs=[]
    if i>0:labs.append(f's{j}_{i-1}_{copy}')
    if i<31:labs.append(f's{j}_{i}_{copy}')
    def V(name,k):return f'{name}_{k%32}_{copy}'
    # Internal free masks.
    extra=[]
    if j==4:extra=[V('u4',i),V('v4',i)]
    elif j==3:extra=[V('u3',i),V('v3',i),V('v4',i+8)]
    elif j==2:extra=[V('u4',i),V('v3',i+12),V('v4',i+8)]
    else:extra=[V('u3',i),V('v3',i+12)]
    labs+=extra
    # Open output word occurrences use shared logical names before copy-normalization.
    def O(letter,k):return f'out_{k%32}' if pos==letter else None
    outs=[]
    if j==4:
        if pos=='C':outs.append(O('C',i))
        if pos=='B':outs.append(O('B',i+7))
    elif j==3:
        if pos=='A':outs.append(O('A',i))
        if pos=='D':outs.append(O('D',i+8))
    elif j==2:
        if pos=='B':outs.append(O('B',i+19))
        if pos=='D':outs.append(O('D',i+8))
    else:
        if pos=='B':outs.append(O('B',i+19))
    labs += [x for x in outs if x is not None]
    labs=list(dict.fromkeys(labs))
    arr=np.zeros((2,)*len(labs),dtype=np.int64);ix={x:k for k,x in enumerate(labs)}
    for a in itertools.product((0,1),repeat=len(labs)):
        get=lambda x:a[ix[x]] if x in ix else 0
        sprev=get(f's{j}_{i-1}_{copy}') if i>0 else None
        scur=get(f's{j}_{i}_{copy}') if i<31 else 0
        u4=get(V('u4',i));v4=get(V('v4',i));u3=get(V('u3',i));v3=get(V('v3',i))
        v4p8=get(V('v4',i+8));v3p12=get(V('v3',i+12))
        Af=get(O('A',i)) if pos=='A' else 0
        B7=get(O('B',i+7)) if pos=='B' else 0
        B19=get(O('B',i+19)) if pos=='B' else 0
        Cf=get(O('C',i)) if pos=='C' else 0
        D8=get(O('D',i+8)) if pos=='D' else 0
        if j==4:
            u,v,w=u4,v4,Cf^B7
        elif j==3:
            u,v,w=u3,v3,Af^v4p8^D8
        elif j==2:
            u=C0>>i&1;v=v4p8^D8^((D0>>((i+16)%32))&1);w=u4^v3p12^B19
        else:
            u=A0>>i&1;v=((B0>>i)&1)^v3p12^B19;w=u3^((D0>>i)&1)
        if i==0:
            val=(tv(scur,0,u,v,w)+tv(scur,1,u,v,w))%P
        else:val=tv(scur,sprev,u,v,w)
        arr[a]=val
    return arr,labs

def normalize_edges(factors,open_names):
    occ=Counter(x for _,ls in factors for x in ls);out=[];repl={}
    for name,c in occ.items():
        if name in open_names or c>2:
            legs=[f'{name}__e{k}' for k in range(c)];repl[name]=iter(legs)
            clabs=legs+([name] if name in open_names else [])
            A=np.zeros((2,)*len(clabs),dtype=np.int64);A[(0,)*len(clabs)]=1;A[(1,)*len(clabs)]=1
            out.append((A,clabs))
        elif c==1:
            # internal dangling variable is summed by an all-ones unary factor
            out.append((np.ones(2,dtype=np.int64),[name]))
    new=[]
    for A,ls in factors:
        nls=[]
        for x in ls:
            if x in repl:nls.append(next(repl[x]))
            else:nls.append(x)
        new.append((A,nls))
    return new+out

def doubled_network(words,pos,S):
    S=set(S);raw=[]
    for cp in ('a','b'):
        for j in (4,3,2,1):
            for i in range(N):
                A,ls=add_factor(j,i,words,pos,cp)
                # Internal names already carry copy suffix. Output logical names must
                # be shared on complement and separated on S.
                nls=[]
                for x in ls:
                    if x.startswith('out_'):
                        k=int(x.split('_')[1]);nls.append(f'out{cp}_{k}' if k in S else f'out_{k}')
                    else:nls.append(x)
                raw.append((A,nls))
    opens={f'outa_{i}' for i in S}|{f'outb_{i}' for i in S}
    return normalize_edges(raw,opens),opens

def execute(factors,opens):
    # Map labels to integer ids for opt_einsum path search.
    ids={};q=0
    for A,ls in factors:
        for x in ls:
            if x not in ids:ids[x]=q;q+=1
    outlabs=sorted(opens,key=lambda x:(x[3],int(x.split('_')[1])))
    args=[]
    for A,ls in factors:args.extend([A,[ids[x] for x in ls]])
    args.append([ids[x] for x in outlabs])
    path,info=oe.contract_path(*args,optimize='greedy')
    work=[(A,[ids[x] for x in ls]) for A,ls in factors]
    for step in path:
        assert len(step)==2,step
        i,j=sorted(step,reverse=True);B,lb=work.pop(i);A,la=work.pop(j)
        common=[x for x in la if x in set(lb)]
        axa=[la.index(x) for x in common];axb=[lb.index(x) for x in common]
        C=np.tensordot(A,B,axes=(axa,axb))%P
        lc=[x for x in la if x not in common]+[x for x in lb if x not in common]
        work.append((C,lc))
    assert len(work)==1
    A,ls=work[0];target=[ids[x] for x in outlabs];perm=[ls.index(x) for x in target];A=np.transpose(A,perm)%P
    m=1<<(len(outlabs)//2);return A.reshape(m,m),info

def rank_flint(M):
    from flint import nmod_mat
    return nmod_mat(M.tolist(),P).rank()

def critical_sets():
    root,nodes=H.walk(H.TREE,True);out=[]
    for rec in nodes:
        S=rec[0]
        if H.message_exponent(S)==88 and len(S)==11:out.append(set(S))
        elif H.message_exponent(S)==88 and len(S)==21:out.append(set(range(32))-set(S))
    uniq=[]
    for S in out:
        if S not in uniq:uniq.append(S)
    assert len(uniq)==3
    return uniq

def candidates():
    out=[]
    out.append((0,0,0,0))
    # deterministic sparse masks
    for w in range(4):
        for b in (0,1,7,10,12,16,19,31):
            z=[0,0,0,0];z[w]=1<<b;out.append(tuple(z))
    rng=random.Random(138)
    for _ in range(12):out.append(tuple(rng.getrandbits(32) for _ in range(4)))
    return out

def main():
    cases=[];crit=critical_sets();cands=candidates()
    for pos in 'ABCD':
        shift=7 if pos=='B' else 0
        for qi,S0 in enumerate(crit):
            S={(i+shift)%32 for i in S0}
            found=None
            for ci,words in enumerate(cands):
                fac,opens=doubled_network(words,pos,S);G,info=execute(fac,opens);r=rank_flint(G)
                print('case',pos,qi,'candidate',ci,'rank',r,'largest_intermediate',info.largest_intermediate,flush=True)
                if r==2048:found=(ci,words);break
            cases.append((pos,qi,found));assert found is not None,(pos,qi)
    print('PASS V26_Q138_LEAF_FULLRANK_WITNESS')
    for pos,qi,found in cases:print('fullrank_witness',pos,qi,'candidate',found[0],'words='+','.join(hex(x) for x in found[1]))
    print('consequence=no uniform fixed-input leaf Schmidt exponent<11 theorem can hold on any critical output-position/partition case')
    print('scope=mod251 full-rank witnesses imply rational full rank; source-specific masks can still have lower rank')
if __name__=='__main__':main()
