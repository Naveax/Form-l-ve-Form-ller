import importlib.util,pathlib,numpy as np
p=pathlib.Path(__file__).with_name('evaluate_v26_feedforward_cancel_anf.py');s=importlib.util.spec_from_file_location('v26',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def test_vector_matches_scalar():
 for bits in (8,10):
  for ctr in (1,257):
   for r in (4,6):
    v=m.block_words_vec(bits,ctr,r)
    for k in (0,1,(1<<bits)//3,(1<<bits)-1):assert tuple(map(int,v[k]))==m.block_words_scalar(k,ctr,r)
def test_mobius_known_polynomial():
 vals=np.array([((i>>0)&1)^(((i>>1)&1)&((i>>2)&1)) for i in range(8)],dtype=np.uint32);assert np.flatnonzero(m.mobius_u32(vals,3)&1).tolist()==[1,6]
def test_mobius_involution():
 rng=np.random.default_rng(26);a=rng.integers(0,2**32,size=256,dtype=np.uint32);assert np.array_equal(m.mobius_u32(m.mobius_u32(a,8),8),a)
