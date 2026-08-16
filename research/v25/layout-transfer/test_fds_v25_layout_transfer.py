import fds_v25_chacha as ch
import fds_v25_boundary_syndrome as bs
from fds_v25_key_layout import Field,key_from_layout,state_from_layout
import fds_v25_layout_cache as lc
LAY={
 'W4_CONTROL':[Field(4,0,10,0)],'W5_SINGLE':[Field(5,0,10,0)],'W6_SINGLE':[Field(6,0,10,0)],'W7_SINGLE':[Field(7,0,10,0)],
 'W4_W8_SPLIT':[Field(4,0,5,0),Field(8,0,5,5)],'W4_W6_SPLIT':[Field(4,0,5,0),Field(6,0,5,5)]}
EXP={'W4_CONTROL':(15,3,18,3),'W5_SINGLE':(14,4,18,3),'W6_SINGLE':(14,4,18,3),'W7_SINGLE':(14,4,18,3),'W4_W8_SPLIT':(16,2,18,3),'W4_W6_SPLIT':(16,2,19,2)}
def test_mapping_and_frozen_costs():
 for lid,fs in LAY.items():
  for k in (0,1,511,1023):assert state_from_layout(k,10,fs,1)==ch.initial_state(key_from_layout(k,10,fs),1)
  z=ch.block_words(key_from_layout(813,10,fs),1,6);assert lc.cost_tuple(lc.prepare_layout_cache(z,fs))==EXP[lid]
def test_cached_exact_small_reference():
 cone=bs.select_min_cone();fc=bs.final_word_forward_cone(0)
 for fs in LAY.values():
  z=ch.block_words(key_from_layout(813,10,fs),1,6);c=lc.prepare_layout_cache(z,fs)
  for k in (0,1,17,410,813,1023):
   s=state_from_layout(k,10,fs,1);assert lc.cached_syndrome(k,c)==bs.boundary_syndrome(z,s,cone);assert lc.cached_direct_match(k,c)==bs.direct_output_word_matches(z,s,fc)
