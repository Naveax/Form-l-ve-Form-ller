from __future__ import annotations
import json,time,resource,statistics
import fds_v25_chacha as ch
import fds_v25_boundary_syndrome as bs

PLAN=json.load(open('V25_INTERNAL_ROUND_BOUNDARY_SYNDROME_STAGE1_PLAN.json'))
B=PLAN['reduced_model']['b'];K=1<<B;COUNTER=PLAN['reduced_model']['counter'];WIDTHS=PLAN['widths']
cone=bs.select_min_cone();final_cone=bs.final_word_forward_cone(cone.word)
assert (cone.split,cone.word,cone.total_qr_count)==(1,0,18)
assert final_cone.qr_count==21

def run_target(target:int):
    t0=time.perf_counter();key=ch.reduced_key_multiword(target,B);z=ch.block_words(key,COUNTER,6)
    synd=[];direct=[]
    for k in range(K):
        s=ch.initial_state(ch.reduced_key_multiword(k,B),COUNTER)
        synd.append(bs.boundary_syndrome(z,s,cone))
        direct.append(bs.direct_output_word_matches(z,s,final_cone))
    rows={}
    for m in WIDTHS:
        mask=(1<<m)-1 if m<32 else 0xffffffff
        survivors=[k for k,x in enumerate(synd) if (x&mask)==0]
        total=18*K+21*len(survivors)
        rows[str(m)]={'survivors':len(survivors),'true_survives':target in survivors,'total_qr':total,'ratio_vs_direct':total/(21*K),'speedup_vs_direct':(21*K)/total}
    direct_matches=[k for k,x in enumerate(direct) if x]
    return {'target':target,'widths':rows,'direct_word_matches':direct_matches,'direct_true_matches':target in direct_matches,'wall_s':time.perf_counter()-t0}

T=time.perf_counter();results=[]
for target in PLAN['targets']:
    r=run_target(int(target));results.append(r);json.dump(r,open(f'v25_boundary_stage1_target{target}.json','w'),indent=2);print(target,{m:r['widths'][str(m)]['survivors'] for m in WIDTHS},'direct',r['direct_word_matches'],'wall',round(r['wall_s'],3),flush=True)
summary={}
for m in WIDTHS:
    rr=[x['widths'][str(m)]['ratio_vs_direct'] for x in results];tt=[x['widths'][str(m)]['total_qr'] for x in results];ss=[x['widths'][str(m)]['survivors'] for x in results]
    summary[str(m)]={'survivors':ss,'median_survivors':statistics.median(ss),'median_total_qr':statistics.median(tt),'median_ratio':statistics.median(rr),'mean_ratio':statistics.fmean(rr),'positive_savings_targets':sum(x<1 for x in rr),'true_survival_targets':sum(x['widths'][str(m)]['true_survives'] for x in results)}
selected=min(WIDTHS,key=lambda m:(summary[str(m)]['median_total_qr'],m));s=summary[str(selected)]
gate={'true_key_survives_all_widths_all_targets':all(x['widths'][str(m)]['true_survives'] for x in results for m in WIDTHS),'selected_width_median_total_ratio_max':s['median_ratio']<=PLAN['stage1_gate']['selected_width_median_total_ratio_max'],'selected_width_positive_savings_targets_min':s['positive_savings_targets']>=PLAN['stage1_gate']['selected_width_positive_savings_targets_min']}
out={'milestone':PLAN['milestone'],'stage':PLAN['stage'],'status':'PASS_STAGE1_CONSTANT_FACTOR_SCREEN' if all(gate.values()) else 'NO_GO_STAGE1_TOTAL_COST','selected_width':selected,'selected':s,'by_width':summary,'gates':gate,'all_gates_pass':all(gate.values()),'direct_unique_true_targets':sum(x['direct_word_matches']==[x['target']] for x in results),'target_results':results,'wall_s':time.perf_counter()-T,'peak_rss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'claim_limit':PLAN['claim_limit']}
json.dump(out,open('v25_boundary_syndrome_stage1_summary.json','w'),indent=2)
print(json.dumps({k:v for k,v in out.items() if k not in ('target_results','by_width')},indent=2));print(json.dumps(out['by_width'],indent=2))
