from __future__ import annotations
import sys,json,time,statistics,resource
import fds_v25_chacha as ch
from fds_v25_key_layout import Field,key_from_layout
import fds_v25_layout_codegen as cg

P=json.load(open('V25_COLLISION_TOLERANT_VERIFIED_SCREEN_SCALING_PLAN.json'))
b=int(sys.argv[1]);lid=sys.argv[2];K=1<<b;MASK=(1<<16)-1;half=b//2
TARGS=P['fresh_targets_by_b'][str(b)]['targets'];REPS=P['wall_protocol']['repeats_by_b'][str(b)];WARM=P['wall_protocol']['warmups_by_b'][str(b)]
fs=[Field(5,0,b,0)] if lid=='W5_SINGLE' else [Field(4,0,half,0),Field(6,0,half,half)]
src,ns,gen=cg.generate_module({lid:fs});sf=ns[f'screen_{lid}'];df=ns[f'direct_{lid}']
def zout(t):return ch.block_words(key_from_layout(t,b,fs),1,6)
def alg(t):
 z=zout(t);sp=cg.prepare_spec(z,fs,bits=b,need_screen=True);s=[k for k in range(K) if (sf(k,sp)&MASK)==0];v=[k for k in s if df(k,sp)];return s,v
def base(t):
 z=zout(t);sp=cg.prepare_spec(z,fs,bits=b,need_screen=False);return [k for k in range(K) if df(k,sp)]
def bench(t):
 for _ in range(WARM):alg(t);base(t)
 A=[];D=[]
 for r in range(REPS):
  order=(('a',alg),('d',base)) if r%2==0 else (('d',base),('a',alg))
  for tag,fn in order:
   q=time.perf_counter();fn(t);dt=time.perf_counter()-q;(A if tag=='a' else D).append(dt)
 return statistics.median(A),statistics.median(D)
def qr_ratio(n):
 if lid=='W5_SINGLE':total=4+14*K+3+18*n;baseq=3+18*K
 else:total=2+16*K+2+19*n;baseq=2+19*K
 return total/baseq
rows=[]
for t in TARGS:
 s,v=alg(t);d=base(t);a,dd=bench(t);rows.append({'target':t,'survivors':s,'verified':v,'baseline_matches':d,'qr_ratio':qr_ratio(len(s)),'wall_speedup':dd/a})
print(json.dumps({'b':b,'layout':lid,'rows':rows,'generator':gen},indent=2))
