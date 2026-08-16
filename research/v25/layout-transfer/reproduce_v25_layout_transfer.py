"""Canonical reduced-key layout-transfer reproduction.

Run correctness/QR L1 first. Wall L2 must use the frozen plan: warmup=3,
repeats=11, alternating algorithm/baseline order. This runner writes a compact
summary and intentionally keeps alpha/full-round claims out of scope.
"""
from __future__ import annotations
import json,time,statistics
import fds_v25_chacha as ch
import fds_v25_boundary_syndrome as bs
from fds_v25_key_layout import Field,key_from_layout,state_from_layout
import fds_v25_layout_cache as lc
B=10;K=1024;MASK=(1<<16)-1;TARGETS=[813,410,917,769,850,373,572,1000]
LAY={
 'W4_CONTROL':[Field(4,0,10,0)],'W5_SINGLE':[Field(5,0,10,0)],'W6_SINGLE':[Field(6,0,10,0)],'W7_SINGLE':[Field(7,0,10,0)],
 'W4_W8_SPLIT':[Field(4,0,5,0),Field(8,0,5,5)],'W4_W6_SPLIT':[Field(4,0,5,0),Field(6,0,5,5)]}
cone=bs.select_min_cone();fc=bs.final_word_forward_cone(0)
def z(t,fs):return ch.block_words(key_from_layout(t,B,fs),1,6)
def sets(t,fs):
 out=z(t,fs);c=lc.prepare_layout_cache(out,fs);surv=[k for k in range(K) if (lc.cached_syndrome(k,c)&MASK)==0];direct=[k for k in range(K) if lc.cached_direct_match(k,c)];return out,c,surv,direct
def alg(t,fs):
 out,c,s,_=sets(t,fs);return s,[k for k in s if lc.cached_direct_match(k,c)]
def baseline(t,fs):return sets(t,fs)[3]
def bench(t,fs):
 for _ in range(3):alg(t,fs);baseline(t,fs)
 a=[];d=[]
 for r in range(11):
  order=(('a',alg),('d',baseline)) if r%2==0 else (('d',baseline),('a',alg))
  for tag,fn in order:
   q=time.perf_counter();fn(t,fs);dt=time.perf_counter()-q;(a if tag=='a' else d).append(dt)
 return statistics.median(d)/statistics.median(a)
out={}
for lid,fs in LAY.items():
 c0=lc.prepare_layout_cache(z(TARGETS[0],fs),fs);sc,sf,dc,df=lc.cost_tuple(c0);rows=[]
 for t in TARGETS:
  outz,c,s,d=sets(t,fs);v=[k for k in s if lc.cached_direct_match(k,c)];total=sf+sc*K+df+dc*len(s);base=df+dc*K
  rows.append({'target':t,'survivors':s,'direct':d,'verified':v,'qr_ratio':total/base,'wall_speedup':bench(t,fs)})
 out[lid]={'cost':[sc,sf,dc,df],'rows':rows,'median_qr_ratio':statistics.median(r['qr_ratio'] for r in rows),'median_wall_speedup':statistics.median(r['wall_speedup'] for r in rows)}
json.dump(out,open('v25_layout_transfer_reproduction.json','w'),indent=2)
