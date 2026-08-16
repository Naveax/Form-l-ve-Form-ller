import numpy as np
def residual_mod(S,m):
 mask=(1<<m)-1;X=np.asarray(S,dtype=np.int64);return (X-X[:,[0]]-X[[0],:]+int(X[0,0]))&mask
def test_exact_modular_model():
 a=np.arange(8,dtype=np.int64);b=np.arange(8,dtype=np.int64);S=(3*a[:,None]+5*b[None,:]+7)&255;assert not np.any(residual_mod(S,8))
def test_cross_term_breaks_exactness():
 a=np.arange(8,dtype=np.int64);b=np.arange(8,dtype=np.int64);S=(a[:,None]+b[None,:]+a[:,None]*b[None,:])&255;assert np.any(residual_mod(S,4))
