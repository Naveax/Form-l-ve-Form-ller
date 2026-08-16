import evaluate_v25_disjoint_half_dependency_mitm as e
def test_known_edge_supports():
 assert e.terminal_support(1,0)==([4],[4,6])
 assert e.terminal_support(5,3)==([4,6],[4])
def test_frozen_search_has_80_rows():
 assert len(e.rows)==80
 assert sum(r[-1] for r in e.rows)==0
