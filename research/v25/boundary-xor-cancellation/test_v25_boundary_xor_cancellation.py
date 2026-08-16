import numpy as np
import fds_v25_chacha as ch
import fds_v25_boundary_syndrome as bs
from fds_v25_key_layout import state_from_layout,key_from_layout
import evaluate_v25_boundary_xor_cancellation as e

def test_projection_family_and_independence_detector():
    assert len(e.PROJ)==136
    lo=np.broadcast_to(np.arange(256,dtype=np.uint32)[:,None],(256,256));hi=np.broadcast_to(np.arange(256,dtype=np.uint32)[None,:],(256,256))
    assert e.indep(lo)==(True,False);assert e.indep(hi)==(False,True);assert e.indep(np.zeros((256,256),np.uint32))==(True,True)

def test_true_key_forward_backward_boundary_equality():
    target=61681;z=ch.block_words(key_from_layout(target,16,e.FIELDS),1,6);s=state_from_layout(target,16,e.FIELDS,1)
    f=s.copy();forward=[]
    for r in range(5):bs.apply_round_full(f,r);forward.append(f.copy())
    x=[(int(z[i])-int(s[i]))&ch.MASK32 for i in range(16)];backward={}
    for r in range(5,0,-1):
        for q in reversed(bs.schedule(r)):ch.inverse_quarter_round(x,*q)
        backward[r]=x.copy()
    for split in range(1,6):assert backward[split]==forward[split-1]
