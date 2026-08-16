from __future__ import annotations
import sys,json,time,statistics,resource
import fds_v25_chacha as ch, fds_v25_boundary_syndrome as bs
P=json.load(open('V25_INTERNAL_ROUND_BOUNDARY_SYNDROME_STAGE3_SCALING_PLAN.json'));MASK=(1<<16)-1;b=int(sys.argv[1]);K=1<<b;reps=P['wall_benchmark_reps'][str(b)]
def setup_direct(z):
 base=ch.initial_state(ch.reduced_key_multiword(0,10),1);ff=base.copy()
 for i in (1,2,3):ch.quarter_round(ff,*bs.schedule(0)[i])
 return tuple(base),tuple(ff),tuple(int(x) for x in z)
def direct(z):
 base,ff,z=setup_direct(z);out=[]
 for k in range(K):
  x=list(ff);x[4]=k;ch.quarter_round(x,*bs.schedule(0)[0])
  for r in (1,2,3,4):bs.apply_round_full(x,r)
  ch.quarter_round(x,*bs.schedule(5)[0])
  if ((x[0]+base[0])&ch.MASK32)==z[0]:out.append(k)
 return out
def alg(z):
 cache=bs.prepare_word4_cache(z,1);sv=[];q0s=[]
 for k in range(K):
  syn,q0=bs.fast_word4_syndrome_and_round0_group(k,cache)
  if (syn&MASK)==0:sv.append(k);q0s.append(q0)
 return sv,[k for k,q0 in zip(sv,q0s) if bs.fast_word4_verify_from_round0_group(q0,cache)]
def bench(fn):
 fn();a=[]
 for _ in range(reps):
  t=time.perf_counter();fn();a.append(time.perf_counter()-t)
 return {'median_s':statistics.median(a),'mean_s':statistics.fmean(a),'min_s':min(a),'max_s':max(a),'reps':reps}
rows=[];T=time.perf_counter()
targets=P['targets_by_b'][str(b)]['targets'] if len(sys.argv)<3 else [int(sys.argv[2])]
for target in targets:
 z=ch.block_words(ch.reduced_key_multiword(target,b),1,6);sv,ver=alg(z);dm=direct(z);ta=bench(lambda:alg(z));td=bench(lambda:direct(z));aq=15*K+6+17*len(sv);bq=18*K+3
 r={'b':b,'target':target,'survivors':sv,'survivor_count':len(sv),'true_survives':target in sv,'verified':ver,'direct_matches':dm,'alg_qr':aq,'baseline_qr':bq,'qr_ratio':aq/bq,'qr_speedup':bq/aq,'alg_timing':ta,'baseline_timing':td,'wall_speedup':td['median_s']/ta['median_s']};rows.append(r);json.dump(r,open(f'v25_boundary_stage3_b{b}_target{target}.json','w'),indent=2);print(target,'N',len(sv),'ratio',r['qr_ratio'],'wallx',r['wall_speedup'],flush=True)
out={'b':b,'rows':rows,'median_survivors':statistics.median(r['survivor_count'] for r in rows),'median_qr_ratio':statistics.median(r['qr_ratio'] for r in rows),'median_qr_speedup':statistics.median(r['qr_speedup'] for r in rows),'median_wall_speedup':statistics.median(r['wall_speedup'] for r in rows),'wall_positive_targets':sum(r['wall_speedup']>1 for r in rows),'true_survival_targets':sum(r['true_survives'] for r in rows),'verified_unique_true_targets':sum(r['verified']==[r['target']] for r in rows),'direct_unique_true_targets':sum(r['direct_matches']==[r['target']] for r in rows),'wall_s':time.perf_counter()-T,'peak_rss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
json.dump(out,open(f'v25_boundary_stage3_b{b}.json','w'),indent=2);print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
