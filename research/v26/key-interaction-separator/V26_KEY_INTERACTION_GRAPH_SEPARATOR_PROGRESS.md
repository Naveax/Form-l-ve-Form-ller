# V26 Key Interaction Graph Separator Audit

Frozen Issue #21 exact Stage0 completed.

For b=8/10/12/14/16, both R4 and R6, the union primal graph from all 512 exact output ANFs is complete: density **1.0** at every width. A full-support degree-b monomial is active at every tested width.

R6 b14 has all `2^14-1 = 16,383` nonconstant monomial masks active; R6 b16 has all `2^16-1 = 65,535` active. Exact separator proxy is **1.0** at b14 and b16.

Primary gates: **0/3 PASS**. Toy graph/separator regressions: **3/3 PASS**.

Decision: `NO_GO_ANF_PRIMAL_GRAPH_FACTORIZATION`. Do not sparsify/delete monomials or cherry-pick outputs to rescue this graph definition. No variable-elimination Stage1 opens.
