from __future__ import annotations
import importlib.util,pathlib,json,numpy as np,math,itertools
root=pathlib.Path(__file__).parents[1]/'feedforward-cancel-anf';p=root/'evaluate_v26_feedforward_cancel_anf.py';s=importlib.util.spec_from_file_location('base',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
B=[8,10,12,14,16];R=[4,6];PAIRS=list(itertools.combinations(range(16),2))
def pm(v,b,di):
 c=m.mobius_u32(v,b);d=[];e=[]
 for bit in range(32):
  q=((c>>np.uint32(bit))&1).astype(bool);n=int(np.count_nonzero(q));d.append(int(di[q].max()) if n else -1);e.append(math.log2(max(1,n))/b)
 return d,e
def main():
 out={}
 for r in R:
  rr={};detail={}
  for b in B:
   z=m.block_words_vec(b,1,r);di=m.popcount_indices(1<<b);sp=[]
   for i,j in PAIRS:
    d,e=pm(np.bitwise_xor(z[:,i],z[:,j]),b,di)
    for bit,(dd,ee) in enumerate(zip(d,e)):
     if dd<=6 and ee<=0.75:sp.append((i,j,bit))
     if r==6 and b in (14,16):detail.setdefault(b,{})[(i,j,bit)]=(dd,ee)
   rr[str(b)]={'sparse_projected_count':len(sp),'distinct_sparse_pairs':len({(i,j) for i,j,_ in sp})}
  if r==6:
   stable=[c for c in detail[14] if detail[14][c][0]<=6 and detail[14][c][1]<=0.75 and detail[16][c][0]<=6 and detail[16][c][1]<=0.75];rr['stable_sparse_b14_b16']=[list(x) for x in stable]
  out[str(r)]=rr
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
