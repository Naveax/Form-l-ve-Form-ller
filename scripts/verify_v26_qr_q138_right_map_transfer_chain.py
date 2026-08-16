#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_algebraic_width40 as V

def main():
 cert=Path(sys.argv[1] if len(sys.argv)>1 else 'research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json')
 C=json.loads(cert.read_text());E=V.build_modified(C);B=V.build_original()
 def bd(S):
  d=1
  for _,q,W in E:
   if any(v in S for v in W) and any(v not in S for v in W):d*=q
  return d
 node=[]
 def walk(x):
  if isinstance(x,int):return {x}
  A=walk(x[0]);D=walk(x[1]);S=A|D
  if bd(S)==2**40:node.append((S,A,D))
  return S
 walk(C['certificate']['tree']);assert len(node)==1
 S,A64,B107=node[0];removed=set(C['rank_compression']['removed_original_leaf_ids']);keep=[v for v in range(568) if v not in removed];new2old={i:v for i,v in enumerate(keep)}
 site={i:set() for i in range(3,8)}
 for v in B107:
  name=B.names[new2old[v]]
  if name.startswith('P_i'):
   i=int(name[3:]);assert 3<=i<=7;site[i].add(v);continue
  m=re.match(r'J([1-4])_i(\d+)_c',name);assert m,name;j,i=map(int,m.groups())
  if 3<=i<=7:site[i].add(v)
  elif j==4 and 11<=i<=15:site[i-8].add(v)
  elif i==31:site[7].add(v)
  elif j==4 and i==16:site[7].add(v)
  elif j==2 and i==8:site[7].add(v)
  else:raise AssertionError((v,name))
 assert {i:len(site[i]) for i in site}=={3:18,4:21,5:21,6:21,7:26}
 assert len(set().union(*site.values()))==107
 for k in range(3,7):
  P=set().union(*(site[i] for i in range(3,k+1)));Q=set(B107)-P
  cross=sorted(n for n,d,W in E if any(v in P for v in W) and any(v in Q for v in W))
  expected=sorted([f'sig4_{k}',f'sig4_{k+8}',f'sig3_{k}',f'sig2_{k}',f'sig1_{k}'])
  assert cross==expected,(k,cross,expected)
  print(f'cut_after_site_{k}: state_bits=5 edges={cross}')
 print('PASS V26_QR_Q138_RIGHT_MAP_TRANSFER_CHAIN')
 print('site_sizes=18,21,21,21,26 hidden_state_bits=5 doubled_Gram_state_bits=10')
if __name__=='__main__':main()
