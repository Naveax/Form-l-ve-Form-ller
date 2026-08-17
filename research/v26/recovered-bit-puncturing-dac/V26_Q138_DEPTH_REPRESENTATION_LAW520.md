# V26 q138 Improved Multi-Double-Round Representation Law

## Result

For fixed outer input masks, the current exact structural representation bounds are

- one inverse double round: `W_repr(1)<=88`;
- for `d>=2`: `W_repr(d)<=520d-340`.

The earlier common-tree slope `536d-364` is superseded.

## Improved fully-open common tree

A deterministic heuristic label search on the frozen 32-bit binary tree shape found the explicit bit tree

`[[[[27,13],[29,[21,4]]],[[28,[12,5]],[11,[20,19]]]],[[[[25,0],[2,[26,1]]],[[9,18],[17,[10,3]]]],[[[22,8],[24,[23,16]]],[[30,[31,6]],[14,[15,7]]]]]]`.

For a fully-open QR, use the exact reduced graph with

- four sigma path bonds;
- cyclic offset families 7,8,12,16;

and cap every site cluster by the physical eight-open-bit-per-site matricization dimension.

The returned tree has exact fully-open QR maximum exponent

`65`.

The heuristic search does not prove 65 optimal; it only supplies the tree. A separate verifier recomputes every cluster cost exactly.

## Depth accounting

For `d>=2`, the backward dependency cone contains

- one final fixed-output/open-four-input central QR;
- four semi-open input/open-one-output QRs;
- `8d-12` fully-open interior QRs;
- four earliest fixed-input/all-four-output vector kernels.

On the same bit tree, inter-layer equality wires are local to clusters. Direct exact evaluation of the layer formula gives

- d=2: 700;
- d=3: 1220;
- d=4: 1740;
- d=5: 2260;
- d=6: 2780;
- d=7: 3300;
- d=8: 3820;
- d=9: 4340.

Each additional double round adds eight fully-open QRs and therefore at most

`8*65=520`

exponent units on this common tree. Hence

`W_repr(d)<=520d-340`, `d>=2`.

## Verification

Tree-search evidence:

- `scripts/search_v26_q138_fully_open_common_tree.py`;
- clean Actions run `32012186410`, exact returned-tree maximum 65.

Frozen exact verifier:

- `scripts/verify_v26_q138_depth_representation_law520.py`;
- clean Actions run `32012790656` passes.

## Scope

The law is a representation/message upper bound for fixed outer input masks. It is not an arithmetic-work law, not an optimal tree theorem, and not a cryptanalytic attack exponent.
