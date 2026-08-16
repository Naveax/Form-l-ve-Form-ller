#!/usr/bin/env python3
import itertools,json,re,sys
from fractions import Fraction
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_algebraic_width40 as V
import verify_v26_qr_q138_width40_left_rank48 as Q

def setup(cert):
 C=json.loads(Path(cert).read_text());E=V.build_modified(C);B=V.build_original();id2={eid:n for n,eid in B.e.items()};dims={n:B.d[eid] for n,eid in B.e.items()}
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
 pext={n for n,d,W in E if any(v in S for v in W) and any(v not in S for v in W)};na={n for n,d,W in E if any(v in A64 for v in W) and any(v not in A64 for v in W)}
 extA=sorted(pext&na);inter=sorted(na-pext);extB=sorted(pext-set(extA));return C,E,B,id2,dims,new2old,A64,B107,extA,inter,extB

def left_rows(ctx,u1,u2):
 C,E,B,id2,dims,new2old,A64,B107,extA,inter,extB=ctx
 c4=Q.tt(('t','s','v','u'),{'w':0},[2,3,2]);c3=Q.tt(('u','t','s','v','w'),{},[2,3,3,2]);c2={b:Q.tt(('t','w','v','s'),{'u':b},[2,3,2]) for b in(0,1)};c1={b:Q.tt(('w','v','s','t'),{'u':b},[2,3,2]) for b in(0,1)}
 fs=[]
 for nv in sorted(A64):
  ov=new2old[nv];name=B.names[ov];labs=[id2[e] for e in B.ops[ov] if B.d[e]>1]
  if name.startswith('P_i'):
   fs.append([labs,{z:Fraction(1) for z in itertools.product((0,1),repeat=3) if z[0]^z[1]^z[2]==0}]);continue
  m=re.match(r'J([1-4])_i(\d+)_c(\d+)_',name);j,i,k=map(int,m.groups())
  co=c4[k] if j==4 else c3[k] if j==3 else c2[u2[i-8]][k] if j==2 else c1[u1[i-8]][k];fs.append(Q.cf(co,labs))
 H=Q.contract(fs,set(extA+inter),dims);pos={x:i for i,x in enumerate(H[0])};rows=defaultdict(dict)
 def lin(bs):
  z=0
  for b in bs:z=(z<<1)|b
  return z
 for a,v in H[1].items():
  r=lin([a[pos[x]] for x in extA]);c=lin([a[pos[x]] for x in inter]);rows[r][c]=rows[r].get(c,Fraction(0))+v
 return list(rows.values())

def right_gram(ctx,u1bits,u2bits):
 C,E,B,id2,dims,new2old,A64,B107,extA,inter,extB=ctx
 c3=Q.tt(('u','t','s','v','w'),{},[2,3,3,2]);c331=Q.tt(('u','t','v','w'),{'s':0},[2,2,2]);c4={w:Q.tt(('t','s','v','u'),{'w':w},[2,3,2]) for w in(0,1)};c2={u:Q.tt(('t','w','v','s'),{'u':u},[2,3,2]) for u in(0,1)};c231={u:Q.tt(('t','w','v'),{'u':u,'s':0},[1,1]) for u in(0,1)};c1={u:Q.tt(('w','v','s','t'),{'u':u},[2,3,2]) for u in(0,1)}
 fs=[];u1={i:u1bits[i-3] for i in range(3,8)};keys=list(range(3,9))+[31];u2={i:u2bits[k] for k,i in enumerate(keys)}
 for nv in sorted(B107):
  ov=new2old[nv];name=B.names[ov];labs=[id2[e] for e in B.ops[ov] if B.d[e]>1]
  if name.startswith('P_i'):
   fs.append([labs,{z:Fraction(1) for z in itertools.product((0,1),repeat=3) if z[0]^z[1]^z[2]==0}]);continue
  m=re.match(r'J([1-4])_i(\d+)_c(\d+)_',name);j,i,k=map(int,m.groups())
  if j==4:co=c4[1 if i==3 else 0][k]
  elif j==3:co=(c331 if i==31 else c3)[k]
  elif j==2:co=(c231[u2[i]] if i==31 else c2[u2[i]])[k]
  else:co=c1[u1[i]][k]
  fs.append(Q.cf(co,labs))
 ext=set(extB);F=[[list(l),dict(d)] for l,d in fs]+[[[x if x in ext else x+'__b' for x in l],dict(d)] for l,d in fs];dims2=dict(dims)
 for k,v in list(dims.items()):dims2[k+'__b']=v
 H=Q.contract(F,set(inter+[x+'__b' for x in inter]),dims2);pos={x:i for i,x in enumerate(H[0])};M=[[Fraction(0) for _ in range(64)] for __ in range(64)]
 def lin(bs):
  z=0
  for b in bs:z=(z<<1)|b
  return z
 for a,v in H[1].items():
  i=lin([a[pos[x]] for x in inter]);j=lin([a[pos[x+'__b']] for x in inter]);M[i][j]+=v
 return M

def dense_rank(M):return Q.rank_rows([{j:v for j,v in enumerate(r) if v} for r in M])
def parent_rank(L,G):
 rows=[]
 for lr in L:
  y={}
  for k,a in lr.items():
   for j,g in enumerate(G[k]):
    if g:y[j]=y.get(j,Fraction(0))+a*g
  rows.append(y)
 return Q.rank_rows(rows)

def main():
 cert=sys.argv[1] if len(sys.argv)>1 else 'research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json';ctx=setup(cert)
 cases=[('zero',(0,0,0),(0,0,0),(0,0,0,0,0),(0,0,0,0,0,0,0),34,23),('ones',(1,1,1),(1,1,1),(1,1,1,1,1),(1,1,1,1,1,1,1),19,8),('high',(0,1,0),(0,0,0),(0,1,1,0,1),(1,1,0,0,1,0,0),37,26)]
 for name,au1,au2,bu1,bu2,rr,pr in cases:
  L=left_rows(ctx,au1,au2);G=right_gram(ctx,bu1,bu2);rR=dense_rank(G);rP=parent_rank(L,G);assert Q.rank_rows(L)==48;assert (rR,rP)==(rr,pr),(name,rR,rP);print(name,'left=48 right=',rR,'parent=',rP)
 print('PASS V26_QR_Q138_RIGHT_MAP_RANK_CONDITIONING')
if __name__=='__main__':main()
