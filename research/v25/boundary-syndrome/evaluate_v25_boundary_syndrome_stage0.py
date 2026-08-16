from __future__ import annotations
import json, time, resource, random
from collections import Counter
import fds_v25_boundary_syndrome as bs

T=time.perf_counter(); cones=bs.enumerate_cones(); selected=bs.select_min_cone()
# Independent equivalence run, separate from pytest.
rng=random.Random(0x51A6E0)
checks=0
for rep in range(64):
    s=[rng.getrandbits(32) for _ in range(16)]
    states=[s.copy()];x=s.copy()
    for r in range(6):
        bs.apply_round_full(x,r);states.append(x.copy())
    for c in cones:
        if bs.partial_forward_word(s,c)!=states[c.split][c.word]: raise AssertionError(('fwd',rep,c))
        if bs.partial_inverse_word(states[6],c)!=states[c.split][c.word]: raise AssertionError(('inv',rep,c))
        checks+=2
rows=[]
for c in cones:
    rows.append({'split':c.split,'word':c.word,'forward_qr':c.forward_qr_count,'backward_qr':c.backward_qr_count,'total_qr':c.total_qr_count,
                 'forward_groups':[{'round':r,'groups':list(ids)} for r,ids in c.forward_groups],
                 'backward_groups':[{'round':r,'groups':list(ids)} for r,ids in c.backward_groups]})
hist=Counter(r['total_qr'] for r in rows)
out={'milestone':'V25_INTERNAL_ROUND_BOUNDARY_CANDIDATE_TRAJECTORY_SYNDROME_AUDIT','stage':'STAGE0_DEPENDENCY_CONE_FEASIBILITY',
     'status':'PASS_CONSTANT_FACTOR_ONLY' if selected.total_qr_count<24 else 'NO_GO_NO_QR_REDUCTION',
     'baseline_full_qr':24,'selected':{'split':selected.split,'word':selected.word,'forward_qr':selected.forward_qr_count,'backward_qr':selected.backward_qr_count,'total_qr':selected.total_qr_count},
     'qr_reduction_fraction':1.0-selected.total_qr_count/24.0,'histogram_total_qr':{str(k):v for k,v in sorted(hist.items())},
     'all_80':rows,'equivalence_random_states':64,'equivalence_checks':checks,'equivalence':'PASS','claim_limit':'constant-factor only; candidate enumeration remains 2^b; alpha reduction not demonstrated',
     'wall_s':time.perf_counter()-T,'peak_rss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
json.dump(out,open('v25_boundary_syndrome_stage0_summary.json','w'),indent=2);print(json.dumps({k:v for k,v in out.items() if k!='all_80'},indent=2))
