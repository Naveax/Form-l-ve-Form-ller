from __future__ import annotations
from collections import defaultdict
from itertools import product
import time
import fds_v25_chacha as ch
import fds_v25_bit_puncturing as bp

Q138_MASKS = tuple((1<<10) if i==4 else 0 for i in range(16))

def first_layer_factors(*, n=32, max_sigma_weight=2, local_beam=None, min_abs=0.0):
    masks=Q138_MASKS
    active=[q for q in ch.COL_QR if any(masks[i] for i in q)]
    if len(active)!=1: raise AssertionError(active)
    q=active[0]; local=tuple(masks[i] for i in q)
    t0=time.perf_counter()
    col=bp.inverse_qr_linear_hull(local,n=n,beam=local_beam,max_sigma_weight=max_sigma_weight,min_abs=min_abs)
    cache={}; branches=[]; peak=0
    for cs in col:
        gm=list(masks)
        for j,i in enumerate(q):gm[i]=cs.masks[j]
        factors=[]
        for dq in ch.DIAG_QR:
            lm=tuple(gm[i] for i in dq)
            if not any(lm): d={(0,0,0,0):1.0}
            else:
                d=cache.get(lm)
                if d is None:
                    h=bp.inverse_qr_linear_hull(lm,n=n,beam=local_beam,max_sigma_weight=max_sigma_weight,min_abs=min_abs)
                    d={tuple(s.masks):float(s.coeff) for s in h if s.coeff};cache[lm]=d
            factors.append(d);peak=max(peak,len(d))
        branches.append((float(cs.coeff),tuple(factors)))
    return {'branches':branches,'cached_local_hulls':len(cache),'peak_local_hull':peak,'sec':time.perf_counter()-t0,'column_hull_count':len(col)}

def one_word_marginal(factor:dict, pos:int):
    out=defaultdict(float)
    for masks,c in factor.items():out[masks[pos]] += c
    return {k:v for k,v in out.items() if v}

def factorized_column_marginal(fdata, column_index:int, *, materialize=True):
    cq=ch.COL_QR[column_index]
    loc=[]
    for sw in cq:
        found=[]
        for di,dq in enumerate(ch.DIAG_QR):
            if sw in dq: found.append((di,dq.index(sw)))
        if len(found)!=1: raise AssertionError((sw,found))
        loc.append(found[0])
    merged=defaultdict(float) if materialize else None
    raw_cells=0; branch_rows=[]; union=[set() for _ in range(4)]
    t0=time.perf_counter()
    for coeff,factors in fdata['branches']:
        marg=[]
        for outpos,(di,pos) in enumerate(loc):
            d=one_word_marginal(factors[di],pos);marg.append(d);union[outpos].update(d)
        cnt=1
        for d in marg:cnt*=len(d)
        raw_cells+=cnt
        branch_rows.append(tuple(len(d) for d in marg))
        if materialize:
            items=[list(d.items()) for d in marg]
            for combo in product(*items):
                key=tuple(x[0] for x in combo);v=coeff
                for x in combo:v*=x[1]
                if v:merged[key]+=v
    if materialize:
        merged={k:v for k,v in merged.items() if v};energy=sum(v*v for v in merged.values());support=len(merged)
    else:energy=None;support=None
    return {'column_index':column_index,'column_words':tuple(cq),'raw_factorized_cells':raw_cells,'union_word_supports':[len(x) for x in union],'branch_support_products':branch_rows,'support':support,'energy':energy,'coeffs':merged,'sec':time.perf_counter()-t0}

def explicit_all_column_marginals(*, n=32, max_sigma_weight=2):
    t0=time.perf_counter();hull=bp.inverse_double_round_linear_hull(Q138_MASKS,n=n,beam=None,local_beam=None,max_sigma_weight=max_sigma_weight,min_abs=0.0);outs=[]
    for ci,cq in enumerate(ch.COL_QR):
        d=defaultdict(float)
        for s in hull:d[tuple(s.masks[i] for i in cq)] += float(s.coeff)
        d={k:v for k,v in d.items() if v};outs.append({'column_index':ci,'support':len(d),'energy':sum(v*v for v in d.values()),'coeffs':d})
    return {'global_unique_hulls':len(hull),'columns':outs,'sec':time.perf_counter()-t0}

def _marginal_arrays(d):
    if not d:return ([],[])
    import numpy as np
    return np.fromiter(d.keys(),dtype=np.uint32,count=len(d)),np.fromiter(d.values(),dtype=np.float64,count=len(d))

def factorized_column_marginal_packed(fdata,column_index:int,*,return_dict=False):
    import numpy as np
    cq=ch.COL_QR[column_index];loc=[]
    for sw in cq:
        found=[(di,dq.index(sw)) for di,dq in enumerate(ch.DIAG_QR) if sw in dq]
        if len(found)!=1:raise AssertionError((sw,found))
        loc.append(found[0])
    branch=[];total=0;union=[set() for _ in range(4)]
    for coeff,factors in fdata['branches']:
        ms=[];sizes=[]
        for outpos,(di,pos) in enumerate(loc):
            d=one_word_marginal(factors[di],pos);union[outpos].update(d);k,v=_marginal_arrays(d);ms.append((k,v));sizes.append(len(k))
        nprod=1
        for n in sizes:nprod*=n
        if nprod:branch.append((coeff,ms,sizes,nprod));total+=nprod
    t0=time.perf_counter();dt=np.dtype([('k0','<u4'),('k1','<u4'),('k2','<u4'),('k3','<u4'),('v','<f8')],align=False);arr=np.empty(total,dtype=dt);off=0
    for coeff,ms,sizes,nprod in branch:
        sl=slice(off,off+nprod);vals=np.full(nprod,float(coeff),dtype=np.float64)
        for d,(keys,coefs) in enumerate(ms):
            before=1
            for z in sizes[:d]:before*=z
            after=1
            for z in sizes[d+1:]:after*=z
            arr[f'k{d}'][sl]=np.tile(np.repeat(keys,after),before);vals*=np.tile(np.repeat(coefs,after),before)
        arr['v'][sl]=vals;off+=nprod
    arr.sort(order=['k0','k1','k2','k3'],kind='quicksort')
    if total:
        boundary=np.ones(total,dtype=np.bool_);boundary[1:]=(arr['k0'][1:]!=arr['k0'][:-1])|(arr['k1'][1:]!=arr['k1'][:-1])|(arr['k2'][1:]!=arr['k2'][:-1])|(arr['k3'][1:]!=arr['k3'][:-1]);starts=np.flatnonzero(boundary);sums=np.add.reduceat(arr['v'],starts);keep=sums!=0.0;support=int(np.count_nonzero(keep));energy=float(np.dot(sums[keep],sums[keep]));outdict=None
        if return_dict:
            ss=starts[keep];vv=sums[keep];outdict={(int(arr['k0'][i]),int(arr['k1'][i]),int(arr['k2'][i]),int(arr['k3'][i])):float(v) for i,v in zip(ss,vv)}
    else:support=0;energy=0.0;outdict={} if return_dict else None
    return {'column_index':column_index,'column_words':tuple(cq),'raw_factorized_cells':total,'union_word_supports':[len(x) for x in union],'support':support,'energy':energy,'coeffs':outdict,'compact_bytes_24':support*24,'sec':time.perf_counter()-t0}
