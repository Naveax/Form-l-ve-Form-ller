from __future__ import annotations
import importlib.util,pathlib,json,numpy as np,time,hashlib
root=pathlib.Path('/mnt/data/fds_v26');spec=importlib.util.spec_from_file_location('base',root/'evaluate_v26_feedforward_cancel_anf.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
B=[8,10,12,14,16];R=[4,6];BASES=[512,1024];DIM=8;SIZE=1<<DIM

def sparse(mm):return {i for i,(d,e) in enumerate(zip(mm['degree'],mm['support_exponent'])) if d<=6 and e<=0.75}
def main():
 t0=time.time();tests=m.selftest();res={};stable_sets={}
 for r in R:
  rr={};perbase_sparse={}
  for base in BASES:
   q=time.time();cube=np.zeros((1<<16,16),dtype=np.uint32);single=None
   for c in range(base,base+SIZE):
    z=m.block_words_vec(16,c,r)
    if c==base:single=z.copy()
    np.bitwise_xor(cube,z,out=cube)
   br={};sp_by_b={}
   for b in B:
    N=1<<b;a=m.map_metrics(single[:N],b);cs=m.map_metrics(cube[:N],b);sp=sparse(cs);sp_by_b[b]=sp
    br[str(b)]={'single_median_degree':float(np.median(a['degree'])),'cube_median_degree':float(np.median(cs['degree'])),'median_bitwise_degree_reduction':float(np.median(np.array(a['degree'])-np.array(cs['degree']))),'single_median_support_exponent':float(np.median(a['support_exponent'])),'cube_median_support_exponent':float(np.median(cs['support_exponent'])),'median_bitwise_support_exponent_reduction':float(np.median(np.array(a['support_exponent'])-np.array(cs['support_exponent']))),'cube_sparse_useful_bits':len(sp),'cube_sparse_positions':sorted(sp)}
   br['stable_sparse_b14_b16']=sorted(sp_by_b[14]&sp_by_b[16]);br['wall_s']=time.time()-q;perbase_sparse[base]=set(br['stable_sparse_b14_b16']);rr[str(base)]=br
   print('R',r,'base',base,'b16 deg',br['16']['median_bitwise_degree_reduction'],'exp',br['16']['median_bitwise_support_exponent_reduction'],'stable',len(br['stable_sparse_b14_b16']),'wall',round(br['wall_s'],2),flush=True)
  rr['stable_sparse_across_bases_b14_b16']=sorted(perbase_sparse[512]&perbase_sparse[1024]);res[str(r)]=rr
 r6=res['6'];g={'base512_b16_degree_reduction_ge_2':r6['512']['16']['median_bitwise_degree_reduction']>=2,'base512_b16_support_reduction_ge_0p10':r6['512']['16']['median_bitwise_support_exponent_reduction']>=0.10,'base1024_b16_degree_reduction_ge_2':r6['1024']['16']['median_bitwise_degree_reduction']>=2,'base1024_b16_support_reduction_ge_0p10':r6['1024']['16']['median_bitwise_support_exponent_reduction']>=0.10,'stable_sparse_bits_across_bases_b14_b16_ge_16':len(r6['stable_sparse_across_bases_b14_b16'])>=16}
 out={'milestone':'V26_SOURCE_ORBIT_COUNTER_CUBE_SUPERPOLY_ANF_AUDIT','selftest_checks':tests,'cube_dimension':8,'cube_bases':BASES,'cube_ranges':[[x,x+255] for x in BASES],'results':res,'primary_gate':g,'primary_pass':all(g.values()),'status':'PASS_STAGE0_OPEN_SUPERPOLY_SOLVING' if all(g.values()) else 'NO_GO_SOURCE_ORBIT_COUNTER_CUBE_ANF','wall_s':time.time()-t0}
 p=root/'V26_SOURCE_ORBIT_COUNTER_CUBE_SUPERPOLY_ANF_RESULT.json';p.write_text(json.dumps(out,indent=2));print(json.dumps({'status':out['status'],'gate':g,'r6_stable':len(r6['stable_sparse_across_bases_b14_b16']),'r6_base512_b16':r6['512']['16'],'r6_base1024_b16':r6['1024']['16'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'wall_s':out['wall_s']},indent=2))
if __name__=='__main__':main()
