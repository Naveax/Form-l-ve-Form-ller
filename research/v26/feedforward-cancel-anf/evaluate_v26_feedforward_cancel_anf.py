from __future__ import annotations
import json, math, time, hashlib
from pathlib import Path
import numpy as np

MASK32=np.uint32(0xffffffff)
CONSTANTS=(0x61707865,0x3320646e,0x79622d32,0x6b206574)
COL=((0,4,8,12),(1,5,9,13),(2,6,10,14),(3,7,11,15))
DIAG=((0,5,10,15),(1,6,11,12),(2,7,8,13),(3,4,9,14))
BVALS=[8,10,12,14,16];ROUNDS=[4,6];C1,C2=1,257

def rol32v(x,n): return ((x<<np.uint32(n))|(x>>np.uint32(32-n))).astype(np.uint32,copy=False)
def qr_v(x,a,b,c,d):
    x[a]=(x[a]+x[b]).astype(np.uint32,copy=False);x[d]=rol32v(np.bitwise_xor(x[d],x[a]),16)
    x[c]=(x[c]+x[d]).astype(np.uint32,copy=False);x[b]=rol32v(np.bitwise_xor(x[b],x[c]),12)
    x[a]=(x[a]+x[b]).astype(np.uint32,copy=False);x[d]=rol32v(np.bitwise_xor(x[d],x[a]),8)
    x[c]=(x[c]+x[d]).astype(np.uint32,copy=False);x[b]=rol32v(np.bitwise_xor(x[b],x[c]),7)
def block_words_vec(bits,counter,rounds):
    N=1<<bits;keys=np.arange(N,dtype=np.uint32);x=[np.full(N,np.uint32(v),dtype=np.uint32) for v in CONSTANTS];x.append(keys.copy())
    for _ in range(7):x.append(np.zeros(N,dtype=np.uint32))
    x.append(np.full(N,np.uint32(counter),dtype=np.uint32));x += [np.zeros(N,dtype=np.uint32) for _ in range(3)];s=[a.copy() for a in x]
    for _ in range(rounds//2):
        for q in COL:qr_v(x,*q)
        for q in DIAG:qr_v(x,*q)
    return np.stack([(x[i]+s[i]).astype(np.uint32,copy=False) for i in range(16)],axis=1)
def rol32s(x,n):return ((x<<n)|(x>>(32-n)))&0xffffffff
def qrs(x,a,b,c,d):
    x[a]=(x[a]+x[b])&0xffffffff;x[d]=rol32s(x[d]^x[a],16);x[c]=(x[c]+x[d])&0xffffffff;x[b]=rol32s(x[b]^x[c],12)
    x[a]=(x[a]+x[b])&0xffffffff;x[d]=rol32s(x[d]^x[a],8);x[c]=(x[c]+x[d])&0xffffffff;x[b]=rol32s(x[b]^x[c],7)
def block_words_scalar(k,counter,rounds):
    s=[*CONSTANTS,k,0,0,0,0,0,0,0,counter,0,0,0];x=s.copy()
    for _ in range(rounds//2):
        for q in COL:qrs(x,*q)
        for q in DIAG:qrs(x,*q)
    return tuple((x[i]+s[i])&0xffffffff for i in range(16))
def mobius_u32(values,bits):
    a=np.array(values,dtype=np.uint32,copy=True);step=1
    for _ in range(bits):
        v=a.reshape(-1,2*step);v[:,step:2*step]^=v[:,:step];step*=2
    return a
def popcount_indices(n):
    x=np.arange(n,dtype=np.uint32);x=x-((x>>1)&np.uint32(0x55555555));x=(x&np.uint32(0x33333333))+((x>>2)&np.uint32(0x33333333));x=(x+(x>>4))&np.uint32(0x0f0f0f0f);x=x+(x>>8);x=x+(x>>16);return (x&np.uint32(0x3f)).astype(np.uint8)
def map_metrics(arr,bits):
    degidx=popcount_indices(1<<bits);deg=[];sup=[]
    for w in range(16):
        c=mobius_u32(arr[:,w],bits)
        for bit in range(32):
            mask=((c>>np.uint32(bit))&np.uint32(1)).astype(bool,copy=False);n=int(np.count_nonzero(mask));sup.append(n);deg.append(int(degidx[mask].max()) if n else -1)
    exp=[math.log2(max(1,x))/bits for x in sup];return {'degree':deg,'support':sup,'support_exponent':exp}
def selftest():
    checks=0
    for bits in (8,10):
      for ctr in (1,257):
       for r in (4,6):
        v=block_words_vec(bits,ctr,r)
        for k in (0,1,(1<<bits)//3,(1<<bits)-1):assert tuple(map(int,v[k]))==block_words_scalar(k,ctr,r);checks+=16
    vals=np.array([((i>>0)&1)^(((i>>1)&1)&((i>>2)&1)) for i in range(8)],dtype=np.uint32);assert np.flatnonzero(mobius_u32(vals,3)&1).tolist()==[1,6];return checks+1
def main():
    out={};selftest()
    for r in ROUNDS:
      rr={};sparse={}
      for b in BVALS:
        z1=block_words_vec(b,C1,r);z2=block_words_vec(b,C2,r);d=(z2-z1).astype(np.uint32,copy=False);d[:,12]=(d[:,12]-np.uint32(256)).astype(np.uint32,copy=False)
        a=map_metrics(z1,b);c=map_metrics(d,b);sp={i for i,(de,se) in enumerate(zip(c['degree'],c['support_exponent'])) if de<=6 and se<=0.75};sparse[b]=sp
        rr[str(b)]={'median_bitwise_degree_reduction':float(np.median(np.array(a['degree'])-np.array(c['degree']))),'median_bitwise_support_exponent_reduction':float(np.median(np.array(a['support_exponent'])-np.array(c['support_exponent']))),'sparse_useful_bits':len(sp)}
      rr['stable_sparse_b14_b16']=sorted(sparse[14]&sparse[16]);out[str(r)]=rr
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
