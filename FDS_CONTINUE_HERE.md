# FDS_CONTINUE_HERE

**State:** rotational branch source-model inapplicable; prior V26 exact families NO-GO.  
**Active:** `V26_KEY_INTERACTION_GRAPH_SEPARATOR_AUDIT`.

1. Use frozen plan under `research/v26/key-interaction-separator/`.
2. b=`8,10,12,14,16`, counter1, R4 control/R6 primary, all 512 block-output bits.
3. Compute exact ANFs and union key-bit primal graph from every active monomial.
4. Enumerate all separators exactly and compute `alpha_sep_proxy=min_S(|S|+max_component(G-S))/b`.
5. R6 PASS requires proxy<=0.75 at b14 and b16 plus b16 graph density<=0.75.
6. Full-support monomial/max degree are diagnostics; no monomial deletion or output cherry-picking.
7. Only PASS opens a concrete variable-elimination/TOTAL scaling stage.
8. FAIL closes straightforward ANF graph factorization; no second graph definition.
9. No alpha/full-round claim from Stage0 alone.
