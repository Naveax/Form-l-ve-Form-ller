# V26 Q1.38 C916 reachable-gauge half-induced third carry

## Status

Exact uniform upper-span certificate for the inherited third-bit carry of the relaxed half family under the same reachable-joint grouped-e0 basis that realizes the admitted C second-lift bound

`C1 <= 916`.

The clean exploratory run is `34218852396`, job `102036954962`.

This result is intentionally half-only. It does **not** prove `C2<=636` because grouped-e0's own lift carry, support-only carry, and cross-carries among the second-lift components remain outside scope.

`ALPHA_PASS=0`.

## Gauge compatibility

The C916 second lift uses

- support-only Walsh space dimension `788`;
- reachable-joint grouped-e0 displayed GF(2) basis dimension `388`;
- exact ZZ Walsh-complement quotient rank `128`;
- total `788+128=916`.

The relaxed half family is rebuilt independently by the same exact degree-two fiber interpolation used in the earlier half-carry work. Its GF(2) span dimension is `144`, and every half basis vector is solved exactly in the displayed reachable-joint basis. Adding the relaxed-half basis introduces no new GF(2) pivot.

For comparison, the canonical grouped-e0 basis has the same GF(2) dimension `388` but exact ZZ quotient `148`, giving the superseded C total `936`. The distinction is basis/gauge-sensitive integer geometry, not GF(2) dimension.

## Coarse all-coordinate carry hull

For reachable basis vectors `v_i`, the parity integer lift of a vector

`y = XOR_i a_i v_i`

has inherited carry

`carry(y) = XOR_{i<j, a_i=a_j=1} (v_i AND v_j)`.

The all-coordinate pairwise-intersection hull tests all `75,078` pairs and has

`dim_GF2 span{v_i AND v_j} <= 1848`.

This is subgeneric but far above the current repeated k9 arithmetic target `650`, so the coarse hull is not the useful endpoint.

## Exact realized relaxed-half carry span

On a fixed support-syndrome fiber and fixed four-bit scalar pattern, the relaxed half vector is degree at most two in the fiber coordinates. Coordinates in a fixed GF(2) basis are linear functions of that vector, hence each reachable-basis coordinate bit is degree at most two. The parity-lift carry is quadratic in those coordinate bits, so the complete realized carry is degree at most four.

Therefore the complete relaxed-half carry span on each fiber is recovered exactly by vector-valued ANF coefficients through degree four.

The clean run verifies:

- feasible support fibers: `8`;
- nonzero support fibers: `4`;
- scalar fibers: `64`;
- maximum fiber dimension: `15`;
- maximum interpolation subsets per scalar fiber: `1941`;
- carry evaluations: `124,480`;
- ANF coefficients inserted: `124,224`;
- unique half vectors / coordinate masks cached: `65,809`;
- deterministic higher-weight regression points reproduce the interpolated polynomial exactly.

The resulting uniform relaxed-family inherited carry span is

`dim_GF2 <= 636`.

Because the scalar phase was safely relaxed to all 16 patterns on every feasible linear state, the true half family is a subset. Thus `636` is a valid uniform upper span for the true half-induced carry in this C916 reachable gauge.

## Relation to the k9 target

PR #119 certifies that a repeated common higher-residue cap around

`650`

through the B/C residues relevant to k9 would make the present separated-leaf k0..k9 arithmetic pass.

The half-induced C916 carry span satisfies

`636 <= 650`.

This is the first authority-compatible C916 inherited-carry component to reach the current repeated arithmetic target.

It is **not** yet a complete C2 theorem. The remaining terms can enlarge the complete third-residue span.

## Comparison with historical gauges

Earlier half-carry authority found:

- compact alternate 144-basis diagnostic: C pairwise hull `<=825`;
- canonical C936 grouped-e0 gauge: all-coordinate half-carry hull `<=1834`.

The C916 reachable gauge has a coarse all-coordinate hull `<=1848`, slightly larger than the canonical one, but the exact realized relaxed-half family collapses to `<=636` after degree-four interpolation. This illustrates why the realized family must be measured rather than inferred from the ambient coordinate hull alone.

## Remaining route to complete C2

To turn this component theorem into a complete higher-residue statement, the next calculations must account for:

1. reachable grouped-e0's own lift carry;
2. support-only lift carry;
3. cross-carries between support-only, reachable grouped-e0, and relaxed-half components;
4. direct/inherited residue bookkeeping needed to form the full C2 lift.

The historical support-carry sumset probe can be reused as the starting point for item 2, but it must be attached to the current C916 gauge rather than treated as a complete C2 certificate.

## Claim discipline

Not included:

- complete `C2<=636`;
- complete B2/C2;
- complete dyadic tail;
- lower `W_repr(1)`;
- arithmetic-work theorem;
- `ALPHA_PASS=1`;
- ranking/search or full-round relevance.

`ALPHA_PASS=0`.
