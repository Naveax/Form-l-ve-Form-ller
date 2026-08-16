from __future__ import annotations
import json,time,statistics,resource
import fds_v25_chacha as ch
import fds_v25_boundary_syndrome as bs
PLAN=json.load(open('V25_INTERNAL_ROUND_BOUNDARY_SYNDROME_STAGE2_PLAN.json'))
B=10;K=1<<B;W=16;MASK=(1<<W)-1;cone=bs.select_min_cone();fc=bs.final_word_forward_cone(0)
assert cone.total_qr_count==18 and fc.qr_count==21

def prepare(target):
 key=ch.reduced_key_multiword(target,B);z=ch.block_words(key,1,6)
 states=[ch.initial_state(ch.reduced_key_multiword(k,B),1) for k in range(K)]
 return z,states

def screen(z,states):
 return [k for k,s in enumerate(states) if (bs.boundary_syndrome(z,s,cone)&MASK)==0]

def direct(z,states):
 return [k for k,s in enumerate(states) if bs.direct_output_word_matches(z,s,fc)]

def timed(fn,reps=31):
 vals=[]
 for _ in range(3):fn()
 for _ in range(reps):
  t=time.perf_counter();fn();vals.append(time.perf_counter()-t)
 return {'median_s':statistics.median(vals),'mean_s':statistics.fmean(vals),'min_s':min(vals),'max_s':max(vals),'reps':reps}

T=time.perf_counter();rows=[]
for target in PLAN['targets']:
 z,states=prepare(target);surv=screen(z,states);dm=direct(z,states);verified=[k for k in surv if bs.direct_output_word_matches(z,states[k],fc)]
 total=18*K+21*len(surv);ratio=total/(21*K)
 ts=timed(lambda:screen(z,states),31);td=timed(lambda:direct(z,states),31)
 row={'target':target,'survivors':surv,'survivor_count':len(surv),'true_survives':target in surv,'direct_matches':dm,'verified_survivors':verified,'total_qr':total,'ratio_vs_direct':ratio,'qr_speedup':(21*K)/total,'screen_timing':ts,'direct_timing':td,'wall_speedup_direct_over_screen_only':td['median_s']/ts['median_s']}
 rows.append(row);json.dump(row,open(f'v25_boundary_stage2_target{target}.json','w'),indent=2);print(target,len(surv),surv,'ratio',round(ratio,6),'wall screen/direct',round(ts['median_s'],6),round(td['median_s'],6),flush=True)
medsur=statistics.median(x['survivor_count'] for x in rows);medratio=statistics.median(x['ratio_vs_direct'] for x in rows)
gates={'true_key_survives_12_of_12':sum(x['true_survives'] for x in rows)==12,'median_survivors_max':medsur<=PLAN['primary_gate']['median_survivors_max'],'median_total_ratio_max':medratio<=PLAN['primary_gate']['median_total_ratio_max'],'positive_savings_targets_min':sum(x['ratio_vs_direct']<1 for x in rows)>=PLAN['primary_gate']['positive_savings_targets_min']}
out={'milestone':PLAN['milestone'],'stage':PLAN['stage'],'status':'PASS_CONFIRMED_CONSTANT_FACTOR_QR_WIN' if all(gates.values()) else 'NO_GO_STAGE2_CONFIRMATION','width':W,'targets':PLAN['targets'],'median_survivors':medsur,'survivor_counts':[x['survivor_count'] for x in rows],'median_total_ratio':medratio,'median_qr_speedup':statistics.median(x['qr_speedup'] for x in rows),'positive_savings_targets':sum(x['ratio_vs_direct']<1 for x in rows),'true_survival_targets':sum(x['true_survives'] for x in rows),'direct_unique_true_targets':sum(x['direct_matches']==[x['target']] for x in rows),'verified_exact_true_targets':sum(x['verified_survivors']==[x['target']] for x in rows),'median_screen_wall_s':statistics.median(x['screen_timing']['median_s'] for x in rows),'median_direct_wall_s':statistics.median(x['direct_timing']['median_s'] for x in rows),'median_wall_speedup_screen_only':statistics.median(x['wall_speedup_direct_over_screen_only'] for x in rows),'gates':gates,'all_gates_pass':all(gates.values()),'claim_limit':PLAN['claim_limit'],'wall_s':time.perf_counter()-T,'peak_rss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'target_results':rows}
json.dump(out,open('v25_boundary_syndrome_stage2_summary.json','w'),indent=2);print(json.dumps({k:v for k,v in out.items() if k!='target_results'},indent=2))
