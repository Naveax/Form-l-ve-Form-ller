import fds_v25_chacha as ch
from fds_v25_key_layout import Field,key_from_layout
import fds_v25_layout_cache as lc
import fds_v25_layout_codegen as cg
LAY={'W4_CONTROL':[Field(4,0,10,0)],'W5_SINGLE':[Field(5,0,10,0)],'W6_SINGLE':[Field(6,0,10,0)],'W7_SINGLE':[Field(7,0,10,0)],'W4_W8_SPLIT':[Field(4,0,5,0),Field(8,0,5,5)],'W4_W6_SPLIT':[Field(4,0,5,0),Field(6,0,5,5)]}
def test_generated_matches_generic_reference():
 src,ns,meta=cg.generate_module(LAY);assert meta['source_bytes']>1000
 for lid,fs in LAY.items():
  z=ch.block_words(key_from_layout(404,10,fs),1,6);sp=cg.prepare_spec(z,fs,need_screen=True);g=lc.prepare_layout_cache(z,fs)
  for k in (0,1,17,404,813,1023):
   assert ns[f'screen_{lid}'](k,sp)==lc.cached_syndrome(k,g)
   assert ns[f'direct_{lid}'](k,sp)==lc.cached_direct_match(k,g)
