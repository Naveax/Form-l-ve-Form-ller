import importlib.util,pathlib,numpy as np
p=pathlib.Path(__file__).with_name('evaluate_v26_key_interaction_graph_separator.py');s=importlib.util.spec_from_file_location('g',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def test_separator_complete_graph_is_one():
 b=6;adj=[((1<<b)-1)^(1<<i) for i in range(b)];assert m.separator_proxy(adj,b)['alpha_sep_proxy']==1.0
def test_separator_disconnected_halves_is_half():
 b=6;adj=[0]*b
 for grp in ((0,1,2),(3,4,5)):
  mask=sum(1<<i for i in grp)
  for i in grp:adj[i]=mask^(1<<i)
 q=m.separator_proxy(adj,b);assert q['alpha_sep_proxy']==0.5 and q['separator_size']==0 and q['max_component']==3
def test_graph_from_single_cross_monomial():
 b=3;z=np.zeros((8,16),dtype=np.uint32);z[:,0]=[1 if ((k&1) and (k&4)) else 0 for k in range(8)];_,adj,g=m.graph_from_output(z,b);assert g['edges']==1 and (adj[0]&(1<<2)) and (adj[2]&(1<<0)) and not adj[1]
