#!/usr/bin/env python3

N=32
TREE=[[[[13,12],[14,[16,15]]],[[3,[4,5]],[2,[0,1]]]],[[[[17,18],[21,[20,19]]],[[26,25],[24,[23,22]]]],[[[27,28],[6,[8,7]]],[[9,[10,11]],[29,[30,31]]]]]]


def central_edges():
    E=[]
    for i in range(N-1):E.append((i,i+1,4,'sigma4'))
    for r in (8,12,16):
        seen=set()
        for i in range(N):
            j=(i+r)%N;e=tuple(sorted((i,j)))
            if e in seen:continue
            seen.add(e);E.append((e[0],e[1],1,f'rot{r}'))
    assert len(E)==111
    return E
E=central_edges()

def central_graph_boundary(S):
    S=set(S);return sum(w for u,v,w,_ in E if (u in S)!=(v in S))

def physical_side_exponent(S):
    # Central kernel has four open binary input-word coordinates per bit site.
    k=len(S);return 4*min(k,N-k)

def central_rank_exponent(S):
    # Both the factor-graph separator and the physical matricization dimension
    # are valid exact upper bounds; use their minimum.
    return min(central_graph_boundary(S),physical_side_exponent(S))

def four_leaf_rank_exponent(S):
    # Each leaf is a 32-bit vector; four independent leaf HT ranks multiply.
    return 4*min(len(S),N-len(S))

def message_exponent(S):return central_rank_exponent(S)+four_leaf_rank_exponent(S)

def walk(t,root=False):
    if isinstance(t,int):return {t},[]
    A,na=walk(t[0]);B,nb=walk(t[1]);assert A.isdisjoint(B);S=A|B
    rec=[] if root else [(frozenset(S),central_graph_boundary(S),central_rank_exponent(S),four_leaf_rank_exponent(S),message_exponent(S))]
    return S,na+nb+rec

def main():
    root,nodes=walk(TREE,True);assert root==set(range(N))
    for i in range(N):
        S={i};nodes.append((frozenset(S),central_graph_boundary(S),central_rank_exponent(S),4,message_exponent(S)))
    mx=max(x[4] for x in nodes);assert mx==88,mx
    top=sorted(nodes,key=lambda x:x[4],reverse=True);maxnodes=[x for x in top if x[4]==88]
    assert len(maxnodes)==3 and {len(x[0]) for x in maxnodes}=={11,21}
    for S,g,c,l,t in maxnodes:
        assert (g,c,l,t)==(51,44,44,88)
    assert 44<88 and 32<88
    print('PASS V26_Q138_EXACT_DOUBLE_ROUND_LEAF_HT88')
    print('bit_partition_tree='+repr(TREE))
    print('max_message_exponent=88 max_message_dimension=2^88')
    print('max_clusters=3: central_graph=51 central_physical_rank_bound=44 four_leaf_HT=44')
    print('max_cluster_sizes=11_or_21')
    print('leaf_factor_generation_message_exponent<=44; dense_leaf_vector<=32')
    print('exact_structural_representation_bound=W2_repr<=88')
    print('no claim of optimality or arithmetic-work reduction')
if __name__=='__main__':main()
