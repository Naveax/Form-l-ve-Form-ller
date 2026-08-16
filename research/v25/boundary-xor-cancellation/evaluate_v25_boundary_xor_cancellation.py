from __future__ import annotations
import itertools
import numpy as np
from fds_v25_key_layout import Field
FIELDS=(Field(4,0,8,0),Field(6,0,8,8));TARGETS=[61681,7339,53820,8140]
PROJ=[(i,) for i in range(16)]+list(itertools.combinations(range(16),2))
def proj(X,p):return X[:,:,p[0]] if len(p)==1 else X[:,:,p[0]]^X[:,:,p[1]]
def indep(P):return bool(np.all(P==P[:,[0]])),bool(np.all(P==P[[0],:]))
