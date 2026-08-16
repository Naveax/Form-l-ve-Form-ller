import importlib.util,pathlib
p=pathlib.Path(__file__).with_name('evaluate_v26_rotational_applicability.py');s=importlib.util.spec_from_file_location('rot',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def test_rotation_group_inverse():
 for r in range(1,32):
  for x in (0,1,0x61707865,0xffffffff,0x12345678):assert m.rol(m.rol(x,r),32-r)==x
def test_no_nonzero_rotation_preserves_all_constants():
 assert all(not all(m.rol(x,r)==x for x in m.C) for r in range(1,32))
def test_arbitrary_same_key_and_rx_public_relation_fail():
 for r in range(1,32):
  assert m.rol(1,r)!=1
  assert (m.rol(0,r)^0)!=(m.rol(1,r)^1)
