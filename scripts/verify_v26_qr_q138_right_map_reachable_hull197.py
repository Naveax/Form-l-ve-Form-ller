#!/usr/bin/env python3
import itertools,json,re,sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_algebraic_width40 as V
import verify_v26_qr_q138_width40_left_rank48 as Q

TAUS=list(itertools.product((0,1),repeat=3))

def setup(cert):
    C=json.loads(Path(cert).read_text());E=V.build_modified(C);B=V.build_original()
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
    S,A64,B107=node[0]
    removed=set(C['rank_compression']['removed_original_leaf_ids']);keep=[v for v in range(568) if v not in removed];new2old={i:v for i,v in enumerate(keep)}
    pext={n for n,d,W in E if any(v in S for v in W) and any(v not in S for v in W)}
    na={n for n,d,W in E if any(v in A64 for v in W) and any(v not in A64 for v in W)}
    intA=sorted(na-pext);extB=set(pext-(pext&na));assert len(intA)==6 and len(extB)==24
    id2={eid:n for n,eid in B.e.items()};dims={n:B.d[eid] for n,eid in B.e.items()}
    site={i:set() for i in range(3,8)}
    for nv in B107:
        name=B.names[new2old[nv]]
        if name.startswith('P_i'):
            i=int(name[3:]);site[i].add(nv);continue
        m=re.match(r'J([1-4])_i(\d+)_c',name);assert m,name;j,i=map(int,m.groups())
        if 3<=i<=7:site[i].add(nv)
        elif j==4 and 11<=i<=15:site[i-8].add(nv)
        elif i==31:site[7].add(nv)
        elif j==4 and i==16:site[7].add(nv)
        elif j==2 and i==8:site[7].add(nv)
        else:raise AssertionError((nv,name))
    assert {i:len(site[i]) for i in site}=={3:18,4:21,5:21,6:21,7:26}
    return C,E,B,new2old,id2,dims,intA,extB,site

def core_cache():
    return {
        'T4_0':Q.tt(('t','s','v','u'),{'w':0},[2,3,2]),
        'T4_1':Q.tt(('t','s','v','u'),{'w':1},[2,3,2]),
        'T3':Q.tt(('u','t','s','v','w'),{},[2,3,3,2]),
        'T2_0':Q.tt(('t','w','v','s'),{'u':0},[2,3,2]),
        'T2_1':Q.tt(('t','w','v','s'),{'u':1},[2,3,2]),
        'T1_0':Q.tt(('w','v','s','t'),{'u':0},[2,3,2]),
        'T1_1':Q.tt(('w','v','s','t'),{'u':1},[2,3,2]),
    }

def site_factors(ctx,site_i,tau):
    C,E,B,new2old,id2,dims,intA,extB,site=ctx;u1,u2,p=tau;K=core_cache();out=[]
    for nv in sorted(site[site_i]):
        ov=new2old[nv];name=B.names[ov];labs=[id2[e] for e in B.ops[ov] if B.d[e]>1]
        if name.startswith('P_i'):
            data={z:Fraction(1) for z in itertools.product((0,1),repeat=3) if z[0]^z[1]^z[2]==p};out.append([labs,data]);continue
        m=re.match(r'J([1-4])_i(\d+)_c(\d+)_',name);assert m,name;j,i,k=map(int,m.groups())
        if j==4:cores=K['T4_1' if i==3 else 'T4_0']
        elif j==3:cores=K['T3']
        elif j==2:cores=K[f'T2_{u2}']
        else:cores=K[f'T1_{u1}']
        out.append(Q.cf(cores[k],labs))
    return out

def states(i):
    left=[f'sig4_{i-1}',f'sig4_{i+7}',f'sig3_{i-1}',f'sig2_{i-1}',f'sig1_{i-1}']
    right=[f'sig4_{i}',f'sig4_{i+8}',f'sig3_{i}',f'sig2_{i}',f'sig1_{i}']
    return left,right

def enc(names,a,pos):
    z=0
    for x in names:z=(z<<1)|a[pos[x]]
    return z

def doubled(ctx,F,open1):
    C,E,B,new2old,id2,dims,intA,extB,site=ctx
    factors=[[list(l),dict(d)] for l,d in F]
    for labs,d in F:factors.append([[x if x in extB else x+'__b' for x in labs],dict(d)])
    dims2=dict(dims)
    for k,v in list(dims.items()):dims2[k+'__b']=v
    opens=set(open1+[x+'__b' for x in open1])
    return Q.contract(factors,opens,dims2)

def transfer(ctx,i,tau):
    left,right=states(i);H=doubled(ctx,site_factors(ctx,i,tau),left+right);pos={x:j for j,x in enumerate(H[0])};rows=defaultdict(dict)
    for a,v in H[1].items():
        r=(enc(left,a,pos)<<5)|enc([x+'__b' for x in left],a,pos);c=(enc(right,a,pos)<<5)|enc([x+'__b' for x in right],a,pos)
        rows[r][c]=rows[r].get(c,Fraction(0))+v
    return rows

def boundary(ctx,tau):
    F=site_factors(ctx,3,tau);_,right=states(3);intA=ctx[6];iface=[x for x in intA if any(x in f[0] for f in F)];assert iface==['aux_j4_i11_k0']
    H=doubled(ctx,F,iface+right);pos={x:j for j,x in enumerate(H[0])};vecs={}
    for a,v in H[1].items():
        z=(a[pos[iface[0]]]<<1)|a[pos[iface[0]+'__b']];st=(enc(right,a,pos)<<5)|enc([x+'__b' for x in right],a,pos)
        vecs.setdefault(z,{})[st]=vecs.setdefault(z,{}).get(st,Fraction(0))+v
    return vecs

def add_basis(B,r):
    r={j:Fraction(v) for j,v in r.items() if v}
    while r:
        c=min(r)
        if c not in B:
            q=1/r[c];B[c]={j:x*q for j,x in r.items()};return True
        q=r[c];b=B[c]
        for j,x in b.items():
            r[j]=r.get(j,Fraction(0))-q*x
            if not r[j]:r.pop(j,None)
    return False

def image(v,K):
    out={}
    for i,a in v.items():
        for j,k in K.get(i,{}).items():
            out[j]=out.get(j,Fraction(0))+a*k
            if not out[j]:out.pop(j,None)
    return out

def rank_vectors(vecs):
    B={}
    for v in vecs:add_basis(B,v)
    return len(B)

def swap(v):
    out={}
    for i,a in v.items():
        j=((i&31)<<5)|(i>>5);out[j]=out.get(j,Fraction(0))+a
    return out

def main():
    cert=sys.argv[1] if len(sys.argv)>1 else 'research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json';ctx=setup(cert)
    Ks={tau:transfer(ctx,4,tau) for tau in TAUS}
    for tau in TAUS:
        assert Ks[tau]==transfer(ctx,5,tau)==transfer(ctx,6,tau)
    ambient=[rank_vectors([row for _,row in sorted(K.items())]) for K in Ks.values()]
    assert ambient==[1016,575,384,397,454,537,431,315],ambient
    H={}
    for tau in TAUS:
        vecs=boundary(ctx,tau);assert rank_vectors(vecs.values())==4
        for v in vecs.values():add_basis(H,v)
    dims=[len(H)];assert dims==[28]
    for _ in range(4):
        old=list(H.values());added=0
        for K in Ks.values():
            for v in old:added+=add_basis(H,image(v,K))
        dims.append(len(H))
        if not added:break
    assert dims==[28,150,193,197,197],dims
    restricted=[]
    for K in Ks.values():restricted.append(rank_vectors(image(v,K) for v in H.values()))
    assert restricted==[194,126,89,94,112,122,100,80],restricted
    U={}
    for v in H.values():add_basis(U,v)
    for v in H.values():add_basis(U,swap(v))
    assert len(U)==197
    Sym={};Anti={}
    for v in H.values():
        s=swap(v);keys=set(v)|set(s)
        add_basis(Sym,{j:v.get(j,0)+s.get(j,0) for j in keys});add_basis(Anti,{j:v.get(j,0)-s.get(j,0) for j in keys})
    assert (len(Sym),len(Anti))==(138,59)
    print('PASS V26_QR_Q138_RIGHT_MAP_REACHABLE_HULL197')
    print('ambient_K_ranks='+','.join(map(str,ambient)))
    print('cumulative_hull_dims=28,150,193,197,197 invariant_hull=197')
    print('restricted_K_ranks='+','.join(map(str,restricted)))
    print('copy_swap_sectors=symmetric:138 antisymmetric:59')
if __name__=='__main__':main()
