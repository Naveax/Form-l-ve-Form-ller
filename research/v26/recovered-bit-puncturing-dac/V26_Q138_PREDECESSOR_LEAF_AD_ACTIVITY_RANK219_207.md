# V26 Q1.38 predecessor-leaf A/D second-residue input-activity sharpening

## Scope

This theorem sharpens the uniform A/D second dyadic residue bounds across the frozen

`S1={0,1,2,3,4,5,12,13,14,15,16}`

11|21 split.

The previous exact theorem wrote

`2^92 L = M0 +2 M1`

with

`rank_F2(M1_A mod2)<=309`,

`rank_F2(M1_D mod2)<=310`.

Those bounds summed every symbolic sector as though all sectors could be nonzero for the same fixed128-bit predecessor input mask. They cannot.

This theorem is uniform over all fixed128-bit predecessor input masks. It is not a source-specific outer128 claim.

## Affine sector activity

The previous second-residue decomposition contains rank-one affine-support terms:

- A:181 reachable weight91 supports and90 reachable weight92 nullity-one derivative supports,271 total;
- D:183+91=274 total.

For each such support, eliminate the32 beta/output variables from its exact affine external consistency system. The remaining equations form an affine condition on the128 predecessor input bits. The support is identically zero for that fixed input whenever this input condition fails.

Thus for a fixed predecessor input, the rank-one affine contribution is bounded by the number of simultaneously satisfiable sector-activity conditions.

## Exact optimization model

For every sector t introduce a binary activity variable `z_t`. For every affine equation

`a.x = b (mod2)`

inside sector t introduce a binary violation bit v and an integer parity variable y satisfying exactly

`sum_i a_i x_i -2y = b +(1-2b)v`.

Then `v=0` iff that XOR equation is satisfied. Impose

`z_t + v <=1`

for every equation of sector t. Because the objective maximizes positive `sum_t z_t`, at optimum `z_t=1` exactly when all equations of sector t are satisfied.

All variables are integral and all coefficients are integers. HiGHS MILP is run with zero relative MIP gap; the admitted finite optimum requires matching primal objective and MIP dual bound.

Exact optima:

- A: maximum simultaneously active affine sectors =181;
- D: maximum simultaneously active affine sectors =171.

The A optimum equals the number of weight91 sectors, but still excludes90 of the271 affine pieces simultaneously. The D optimum excludes103 of274.

## Signed quadratic terms

The previous theorem has three remaining signed quadratic support terms.

Their uniform rank envelopes across S1 are:

- A cross ranks11,10,11; support intersection dimension0, hence bounds13,12,13, total38;
- D cross ranks10,10,10; hence12,12,12, total36.

We do not need any mutual-exclusion assumption between these signed terms and the affine optimum. Adding their full worst-case budgets gives a uniform bound.

Therefore

`rank_F2(M1_A mod2) <=181+38 =219`,

`rank_F2(M1_D mod2) <=171+36 =207`.

This strictly supersedes309/310.

## Dyadic meaning

For every fixed predecessor input mask there exists an integer second-layer lift with rational rank at most219 for A and207 for D, leaving an even residual for the next dyadic layer.

These are uniform coefficient bounds, so they may be used in the four-leaf dyadic convolution without freezing a source-specific outer128 mask.

This still does not bound the complete rational predecessor-leaf Schmidt rank or prove an arithmetic-work improvement. Higher dyadic residues remain.
