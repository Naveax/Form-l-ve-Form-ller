import numpy as np
import evaluate_v25_full_linear_boundary_nullspace as e

def test_basis_detects_planted_low_only_mask():
    lo=np.arange(8,dtype=np.uint32)[:,None];hi=np.arange(8,dtype=np.uint32)[None,:];X=np.zeros((8,8,16),np.uint32);X[:,:,0]=lo;X[:,:,1]=hi;X[:,:,2]=lo^hi
    b=e.basis_from_grid(X,'low_only');m=e.null_masks(b);assert 1 in m;assert 2 not in m

def test_basis_merge_can_kill_all_masks():
    b={}
    for i in range(16):e.add_basis(b,1<<i)
    assert len(b)==16 and e.null_masks(b)==[]
