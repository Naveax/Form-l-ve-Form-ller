# V25 Multi-Layout Codegen Scaling b10→b16

## Verdict

`NO_GO_STRICT_MULTI_LAYOUT_SCALING_GATE`

The frozen family gate required both W5_SINGLE and W4_W6_SPLIT to pass the strict per-b gate at b=10,12,14,16. That gate included raw syndrome-survivor uniqueness on all three targets. It fails without retuning.

Exact generated/generic equivalence completed over the full candidate spaces: **522,240 full syndrome values + 522,240 direct predicates PASS**.

W5 median wall speedups: b10 1.1178x, b12 1.2424x, b14 1.2272x, b16 1.2628x. Strict pass only b12/b14 because b10 and b16 each contain one two-survivor collision.

W4+W6 median wall speedups: b10 1.0557x, b12 1.1419x, b14 1.1756x, b16 1.1801x. Strict pass only b10/b14 because b12 and b16 contain two-survivor collisions.

Crucially, every extra syndrome collision is removed by the already-accounted exact direct verifier: verified candidate set equals the true key for every frozen target, baseline is unique true for every target, true key survives every screen, and wall savings are positive in every case.

This does **not** rescue the frozen strict milestone. It motivates a separate fresh collision-tolerant end-to-end verified-screen protocol whose success criterion is the verified set and TOTAL cost rather than raw syndrome uniqueness.

Leading enumeration remains 2^b; alpha=1.
