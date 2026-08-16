from __future__ import annotations
import importlib.util,pathlib,json,time
import numpy as np
basep=pathlib.Path('/mnt/data/fds_v26/evaluate_v26_feedforward_cancel_anf.py');s=importlib.util.spec_from_file_location('base',basep);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
B=[8,10,12,14,16];ROUNDS=[4,6]
def graph_from_output(z,b):
 n=1<<b;active=np.zeros(n,dtype=bool)
 for w in range(16):active |= (m.mobius_u32(z[:,w],b)!=0)
 active[0]=False;idx=np.flatnonzero(active);deg=m.popcount_indices(n);maxdeg=int(deg[idx].max()) if len(idx) else 0;full=bool(active[n-1]);adj=[0]*b
 if full:
  allm=(1<<b)-1
  for i in range(b):adj[i]=allm^(1<<i)
 else:
  for mask in idx:
   mask=int(mask)
   if mask & (mask-1)==0:continue
   bits=[i for i in range(b) if (mask>>i)&1]
   for i in bits:adj[i]|=mask^(1<<i)
 edges=sum(x.bit_count() for x in adj)//2;density=edges/(b*(b-1)/2)
 return active,adj,{'active_monomials':int(active.sum()),'max_active_monomial_degree':maxdeg,'full_support_monomial':full,'edges':edges,'density':density}
def max_component(adj,remain,b):
 best=0;left=remain
 while left:
  seed=left&-left;front=seed;comp=0
  while front:
   comp|=front;neigh=0;f=front
   while f:
    bit=f&-f;i=bit.bit_length()-1;neigh|=adj[i];f^=bit
   front=(neigh&remain)&~comp
  best=max(best,comp.bit_count());left&=~comp
 return best
def separator_proxy(adj,b):
 allm=(1<<b)-1;best_num=b+1;best_s=0;best_mc=b
 for S in range(1<<b):
  s=S.bit_count()
  if s>=best_num:continue
  mc=max_component(adj,allm^S,b);num=s+mc
  if num<best_num or (num==best_num and s<best_s.bit_count()):best_num=num;best_s=S;best_mc=mc
 return {'alpha_sep_proxy':best_num/b,'best_numerator':best_num,'separator_size':best_s.bit_count(),'max_component':best_mc,'separator_bits':[i for i in range(b) if (best_s>>i)&1]}
