from __future__ import annotations
import json,time,statistics,resource
import fds_v25_chacha as ch, fds_v25_boundary_syndrome as bs
P=json.load(open('V25_INTERNAL_ROUND_BOUNDARY_SYNDROME_STAGE2_PLAN.json'));K=1024;MASK=(1<<16)-1

def alg(target):
 z=ch.block_words(ch.reduced_key_multiword(target,10),1,6);cache=bs.prepare_word4_cache(z,1);surv=[]
 for k in range(K):
  syn,q0=bs.fast_word4_syndrome_and_round0_group(k,cache)
  if (syn&MASK)==0:surv.append((k,q0))
 verified=[k for k,q0 in surv if bs.fast_word4_verify_from_round0_group(q0,cache)]
 return [k for k,_ in surv],verified

def baseline(target):
 z=ch.block_words(ch.reduced_key_multiword(target,10),1,6);cache=bs.prepare_word4_cache(z,1)
 return [k for k in range(K) if bs.fast_word4_direct_match(k,cache)]

def bench(fn,target,reps=41):
 for _ in range(4):fn(target)
 a=[]
 for _ in range(reps):
  t=time.perf_counter();fn(target);a.append(time.perf_counter()-t)
 return {'median_s':statistics.median(a),'mean_s':statistics.fmean(a),'min_s':min(a),'max_s':max(a),'reps':reps}
rows=[];T=time.perf_counter()
for t in P['targets']:
 s,v=alg(t);b=baseline(t);ta=bench(alg,t);tb=bench(baseline,t)
 qr_alg=15*K+3+3+17*len(s);qr_base=18*K+3
 row={'target':t,'survivors':s,'verified':v,'baseline_matches':b,'alg_qr':qr_alg,'baseline_qr':qr_base,'qr_ratio':qr_alg/qr_base,'qr_speedup':qr_base/qr_alg,'alg_timing':ta,'baseline_timing':tb,'wall_speedup':tb['median_s']/ta['median_s']};rows.append(row)
 print(t,s,'qr',qr_alg,qr_base,'wall x',round(row['wall_speedup'],4),flush=True)
out={'stage':'STAGE2B_CANDIDATE_ENSEMBLE_CACHE_ENGINEERING','status':'PASS_ACTUAL_WALL_AND_QR_CONSTANT_FACTOR' if all(r['wall_speedup']>1 for r in rows) else 'QR_WIN_WALL_NOT_UNIVERSAL','targets':P['targets'],'survivor_counts':[len(r['survivors']) for r in rows],'exact_verified_targets':sum(r['verified']==[r['target']] for r in rows),'baseline_unique_targets':sum(r['baseline_matches']==[r['target']] for r in rows),'median_qr_ratio':statistics.median(r['qr_ratio'] for r in rows),'median_qr_speedup':statistics.median(r['qr_speedup'] for r in rows),'median_wall_speedup':statistics.median(r['wall_speedup'] for r in rows),'wall_speedup_min':min(r['wall_speedup'] for r in rows),'wall_speedup_positive_targets':sum(r['wall_speedup']>1 for r in rows),'qr_accounting':'screen cache 3 inverse QR/target + 15 QR/candidate; direct-survivor cache 3 forward QR/target + 17 QR/survivor; direct baseline 3 forward QR/target +18 QR/candidate','claim_limit':'constant-factor reduced b=10 only; leading candidate enumeration remains 2^b','wall_s':time.perf_counter()-T,'peak_rss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'rows':rows}
json.dump(out,open('v25_boundary_syndrome_cached_summary.json','w'),indent=2);print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
