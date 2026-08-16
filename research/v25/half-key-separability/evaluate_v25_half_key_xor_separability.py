from __future__ import annotations
import numpy as np
import fds_v25_chacha as ch
from fds_v25_key_layout import Field,key_from_layout
import fds_v25_layout_codegen as cg
TARGETS=[43051,21863,31754,45567];fs=[Field(5,0,16,0)];src,ns,_=cg.generate_module({'W5_SINGLE':fs});sf=ns['screen_W5_SINGLE']
def gf2_rank(M):
 rows=[]
 for r in np.asarray(M,dtype=np.uint8):
  x=sum((int(v)&1)<<j for j,v in enumerate(r))
  if x:rows.append(x)
 piv={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in piv:x^=piv[p]
   else:piv[p]=x;break
 return len(piv)
for t in TARGETS:
 z=ch.block_words(key_from_layout(t,16,fs),1,6);sp=cg.prepare_spec(z,fs,bits=16,need_screen=True)
 S=np.fromiter((sf(k,sp)&0xffff for k in range(65536)),dtype=np.uint16,count=65536).reshape(256,256).T
 R=S^S[:,[0]]^S[[0],:]^S[0,0]
 exact=[bit for bit in range(16) if not np.any((R>>bit)&1)]
 print(t,exact,[gf2_rank((S>>bit)&1) for bit in range(16)],[gf2_rank((R>>bit)&1) for bit in range(16)])
