import evaluate_v25_all_two_word_dependency_mitm as e

def test_exhaustive_search_shape_and_no_candidate():
    assert len(e.cones)==80
    assert len(e.rows)==2240
    assert len(e.bylayout)==28
    assert len(e.cands)==0
    assert all(v['candidate_count']==0 for v in e.bylayout.values())

def test_w4_w6_reproduces_issue12_pattern_histogram():
    assert e.bylayout['4_6']['patterns']==[
      {'forward':[],'backward':[4,6],'count':8},
      {'forward':[4],'backward':[4,6],'count':4},
      {'forward':[4,6],'backward':[],'count':8},
      {'forward':[4,6],'backward':[4],'count':4},
      {'forward':[4,6],'backward':[4,6],'count':48},
      {'forward':[4,6],'backward':[6],'count':4},
      {'forward':[6],'backward':[4,6],'count':4}]
