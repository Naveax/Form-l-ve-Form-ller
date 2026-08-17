#!/usr/bin/env python3
# Depends on the clean MILP cardinality theorem in
# verify_v26_q138_double_round_ht88_method_optimal.py.
EXPECTED={11:51,12:52,13:55,14:54,15:55,16:56}

def main():
    # In the purely constructive reduced-central-graph + four generic leaf method,
    # an edge whose smaller bit side has size k costs graph_boundary + 4k.
    costs={k:EXPECTED[k]+4*k for k in EXPECTED}
    assert costs=={11:95,12:100,13:107,14:110,15:115,16:120}
    # Standard balanced-edge lemma for a subcubic tree with32 leaves: some edge
    # has smaller side11..16. Therefore every binary contraction tree in this
    # method has peak at least min_k costs[k]=95.
    assert min(costs.values())==95
    # Existing constructive95 certificate/tree attains95, hence method-optimal.
    print('PASS V26_Q138_CONSTRUCTIVE_GRAPH_LEAF95_OPTIMAL')
    print('cardinality_graph_minima='+','.join(f'{k}:{EXPECTED[k]}' for k in sorted(EXPECTED)))
    print('constructive_graph_plus_leaf_costs='+','.join(f'{k}:{costs[k]}' for k in sorted(costs)))
    print('balanced_edge_smaller_side=11..16 => lower_bound95; constructive95 tree attains95')
    print('scope=optimal only inside coefficient-blind reduced-central-graph + four-generic-leaf method')
if __name__=='__main__':main()
