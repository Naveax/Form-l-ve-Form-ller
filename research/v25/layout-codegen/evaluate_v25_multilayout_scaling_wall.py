from __future__ import annotations
import sys,json,time,statistics,resource
import fds_v25_chacha as ch
from fds_v25_key_layout import Field,key_from_layout
import fds_v25_layout_codegen as cg
import fds_v25_layout_cache as lc
b=int(sys.argv[1]);lid=sys.argv[2];half=b//2;K=1<<b;MASK=(1<<16)-1
TARGETS={10:[128,828,1022],12:[2418,3039,241],14:[3682,2365,16104],16:[28124,21497,46696]}[b]
REPS={10:9,12:7,14:5,16:3}[b];WARM={10:2,12:2,14:1,16:1}[b]
fs=[Field(5,0,b,0)] if lid=='W5_SINGLE' else [Field(4,0,half,0),Field(6,0,half,half)]
LAY={lid:fs};src,ns,gen=cg.generate_module(LAY);sf=ns[f'screen_{lid}'];df=ns[f'direct_{lid}']
def z(t):return ch.block_words(key_from_layout(t,b,fs),1,6)
def alg(t):
 out=z(t);sp=cg.prepare_spec(out,fs,bits=b,need_screen=True);s=[k for k in range(K) if (sf(k,sp)&MASK)==0];v=[k for k in s if df(k,sp)];return s,v
def base(t):
 out=z(t);sp=cg.prepare_spec(out,fs,bits=b,need_screen=False);return [k for k in range(K) if df(k,sp)]
def bench(t):
 for _ in range(WARM):alg(t);base(t)
 A=[];D=[]
 for r in range(REPS):
  order=(('a',alg),('d',base)) if r%2==0 else (('d',base),('a',alg))
  for tag,fn in order:
   q=time.perf_counter();fn(t);dt=time.perf_counter()-q;(A if tag=='a' else D).append(dt)
 return {'alg_median_s':statistics.median(A),'base_median_s':statistics.median(D),'wall_speedup':statistics.median(D)/statistics.median(A),'alg_mean_s':statistics.fmean(A),'base_mean_s':statistics.fmean(D)}
T=time.perf_counter();rows=[]
for t in TARGETS:
 s,v=alg(t);d=base(t);tim=bench(t);c=lc.prepare_layout_cache(z(t),fs,bits=b);sc,sfix,dc,dfix=lc.cost_tuple(c);qr=(sfix+sc*K+dfix+dc*len(s))/(dfix+dc*K);rows.append({'target':t,'survivors':s,'verified':v,'baseline_matches':d,'qr_ratio':qr,**tim});print(b,lid,t,'N',len(s),'wallx',round(tim['wall_speedup'],4),flush=True)
speeds=[r['wall_speedup'] for r in rows];g={'true_unique_3_of_3':all(r['survivors']==[r['target']] and r['verified']==[r['target']] and r['baseline_matches']==[r['target']] for r in rows),'median_wall_speedup_min':statistics.median(speeds)>=1.05,'positive_wall_targets_min':sum(x>1 for x in speeds)>=2}
out={'b':b,'layout':lid,'targets':TARGETS,'reps':REPS,'warmups':WARM,'survivor_counts':[len(r['survivors']) for r in rows],'median_qr_ratio':statistics.median(r['qr_ratio'] for r in rows),'median_wall_speedup':statistics.median(speeds),'min_wall_speedup':min(speeds),'positive_wall_targets':sum(x>1 for x in speeds),'gates':g,'all_gates_pass':all(g.values()),'generator':gen,'rows':rows,'wall_s':time.perf_counter()-T,'peak_rss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};json.dump(out,open(f'v25_multilayout_scaling_wall_b{b}_{lid}.json','w'),indent=2);print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
