from __future__ import annotations
import numpy as np

def add_basis(basis,x):
    x=int(x)&0xffff
    while x:
        p=x.bit_length()-1
        if p in basis:x^=basis[p]
        else:
            basis[p]=x
            for q in list(basis):
                if q!=p and ((basis[q]>>p)&1):basis[q]^=x
            return True
    return False

def merge_basis(*bases):
    out={}
    for b in bases:
        for x in b.values():add_basis(out,x)
    return out

def basis_from_grid(X,mode):
    if mode=='low_only':D=X^X[:,[0],:]
    elif mode=='high_only':D=X^X[[0],:,:]
    else:raise ValueError(mode)
    A=D.reshape(-1,16);basis={};weights=(np.uint32(1)<<np.arange(16,dtype=np.uint32))
    for bit in range(32):
        rows=(((A>>np.uint32(bit))&np.uint32(1))*weights).sum(axis=1,dtype=np.uint32)
        for x in np.unique(rows):
            if x:add_basis(basis,int(x))
            if len(basis)==16:return basis
    return basis

def null_masks(basis):
    rows=list(basis.values());return [m for m in range(1,1<<16) if all(((m&r).bit_count()&1)==0 for r in rows)]
