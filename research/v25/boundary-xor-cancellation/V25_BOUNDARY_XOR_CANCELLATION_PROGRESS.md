# V25 Boundary-Word XOR Projection Cancellation Audit

Frozen Issue #14 family tested 5 splits × (16 single + 120 pairwise XOR) = **680 projection-splits** for `W4_W6_SPLIT` b16.

Forward exact half-independence produced **156 oriented candidates**.

On the first frozen fresh target `61681`, **0/156** candidates were exactly independent of the opposite half on the inverse/output side. Therefore no projection/orientation can satisfy the all-four-target gate; additional fresh-target computation cannot change the primary result.

Regression **2/2 PASS**: the independence detector is exact on planted grids and the true key's forward/backward internal states match on every split.

Decision: `NO_GO_SINGLE_PAIR_XOR_CANCELLATION`. No match/TOTAL stage opened.

Next, if linear XOR cancellation remains worth testing, exhaust the entire 65,535-mask GF(2) span of all 16 boundary words via nullspace intersection rather than manually adding triples/quadruples.
