#!/usr/bin/env python3

N=32
TREE=[[[[27,13],[29,[21,4]]],[[28,[12,5]],[11,[20,19]]]],[[[[25,0],[2,[26,1]]],[[9,18],[17,[10,3]]]],[[[22,8],[24,[23,16]]],[[30,[31,6]],[14,[15,7]]]]]]


def edges(offsets):
    E=[]
    for i in range(N-1):E.append((i,i+1,4))
    for r in offsets:
        seen=set()
        for i in range(N):
            j=(i+r)%N;e=tuple(sorted((i,j)))
            if e in seen:continue
            seen.add(e);E.append((e[0],e[1],1))
    return E
EC=edges((8,12,16));EO=edges((7,8,12,16))

def bd(S,E):
    S=set(S);return sum(w for u,v,w in E if (u in S)!=(v in S))

def walk(t,root=False):
    if isinstance(t,int):return {t},[]
    A,a=walk(t[0]);B,b=walk(t[1]);assert A.isdisjoint(B);S=A|B
    return S,a+b+([] if root else [S])

def caps(S):
    m=min(len(S),N-len(S))
    return (
        m,
        min(bd(S,EC),4*m),
        min(bd(S,EC),5*m),
        min(bd(S,EO),8*m),
        4*m,
    )
def depth_cost(S,d):
    m,c,s,f,v=caps(S)
    return c+4*s+(8*d-12)*f+4*v

def main():
    root,sets=walk(TREE,True);assert root==set(range(N))
    fullmax=max(caps(S)[3] for S in sets);assert fullmax==65,fullmax
    vals={d:max(depth_cost(S,d) for S in sets) for d in range(2,10)}
    assert vals=={2:700,3:1220,4:1740,5:2260,6:2780,7:3300,8:3820,9:4340},vals
    for d,v in vals.items():assert v==520*d-340
    print('PASS V26_Q138_DEPTH_REPRESENTATION_LAW520')
    print('d=1 sharp_special_bound=88')
    print('d>=2 exact_common_tree_bound=W_repr(d)<=520*d-340')
    print('fully_open_per_QR_common_tree_bound=65')
    print('verified_d2_to_d9='+','.join(f'{d}:{vals[d]}' for d in sorted(vals)))
    print('tree='+repr(TREE))
    print('source_tree_search=clean heuristic search returned max65; this verifier exact-recounts the frozen tree')
    print('no optimality or arithmetic-work claim')
if __name__=='__main__':main()
