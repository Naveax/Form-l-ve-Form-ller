from __future__ import annotations
import sys,json,time,resource
import fds_v25_chacha as ch
import fds_v25_boundary_syndrome as bs
from fds_v25_key_layout import Field,key_from_layout,state_from_layout
import fds_v25_layout_codegen as cg
b=int(sys.argv[1]);half=b//2
TARGETS={10:[128,828,1022],12:[2418,3039,241],14:[3682,2365,16104],16:[28124,21497,46696]}[b]
LAY={'W5_SINGLE':[Field(5,0,b,0)],'W4_W6_SPLIT':[Field(4,0,half,0),Field(6,0,half,half)]}
cone=bs.select_min_cone();fc=bs.final_word_forward_cone(0);T=time.perf_counter();src,ns,gen=cg.generate_module(LAY);syn=direct=0
for lid,fs in LAY.items():
 for t in TARGETS:
  z=ch.block_words(key_from_layout(t,b,fs),1,6);sp=cg.prepare_spec(z,fs,bits=b,need_screen=True);sf=ns[f'screen_{lid}'];df=ns[f'direct_{lid}']
  for k in range(1<<b):
   s=state_from_layout(k,b,fs,1);a=sf(k,sp);g=bs.boundary_syndrome(z,s,cone)
   if a!=g:raise AssertionError(('syn',b,lid,t,k))
   syn+=1;ad=df(k,sp);gd=bs.direct_output_word_matches(z,s,fc)
   if ad!=gd:raise AssertionError(('direct',b,lid,t,k))
   direct+=1
out={'b':b,'targets':TARGETS,'status':'PASS','full_syndrome_equal':syn,'direct_predicate_equal':direct,'generator':gen,'wall_s':time.perf_counter()-T,'peak_rss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};json.dump(out,open(f'v25_multilayout_scaling_exact_b{b}.json','w'),indent=2);print(json.dumps(out,indent=2))
