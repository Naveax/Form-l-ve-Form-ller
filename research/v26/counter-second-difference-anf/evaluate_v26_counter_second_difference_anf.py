from __future__ import annotations
import importlib.util,pathlib,json,numpy as np,time
root=pathlib.Path(__file__).parents[1]/'feedforward-cancel-anf';p=root/'evaluate_v26_feedforward_cancel_anf.py';s=importlib.util.spec_from_file_location('base',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
B=[8,10,12,14,16];R=[4,6]
def sparse(mm):return {i for i,(d,e) in enumerate(zip(mm['degree'],mm['support_exponent'])) if d<=6 and e<=0.75}
def main():
 out={}
 for r in R:
  rr={};ss={}
  for b in B:
   z1=m.block_words_vec(b,1,r);z2=m.block_words_vec(b,257,r);z3=m.block_words_vec(b,513,r);d2=(z3-(z2*np.uint32(2))+z1).astype(np.uint32,copy=False);a=m.map_metrics(z1,b);c=m.map_metrics(d2,b);q=sparse(c);ss[b]=q
   rr[str(b)]={'median_bitwise_degree_reduction':float(np.median(np.array(a['degree'])-np.array(c['degree']))),'median_bitwise_support_exponent_reduction':float(np.median(np.array(a['support_exponent'])-np.array(c['support_exponent']))),'sparse_useful_bits':len(q)}
  rr['stable_sparse_b14_b16']=sorted(ss[14]&ss[16]);out[str(r)]=rr
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
