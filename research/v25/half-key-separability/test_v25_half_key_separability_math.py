import numpy as np
def residual_xor(S):return S^S[:,[0]]^S[[0],:]^S[0,0]
def exact_bits(S,width=16):
 R=residual_xor(S);return [b for b in range(width) if not np.any((R>>b)&1)]
def test_exact_xor_model():
 a=np.arange(8,dtype=np.uint16);b=np.arange(8,dtype=np.uint16);S=(a[:,None]^((b[None,:]<<3)&0xffff)^0x55).astype(np.uint16);assert exact_bits(S,8)==list(range(8))
def test_cross_term_breaks_bits():
 a=np.arange(8,dtype=np.uint16);b=np.arange(8,dtype=np.uint16);S=(a[:,None]^b[None,:]).astype(np.uint16);S[3,5]^=1;assert 0 not in exact_bits(S,8)
