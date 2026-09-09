# V26 q138 C916 e0 first-dyadic cross-frequency separator

## Construction

For every C grouped-e0 support group, begin with the exact existing support/frequency `combined_basis` on the 149 shared predecessor/right coordinates. Add all 149-bit linear forms that control the 11 common local-left frequency bits appearing in valid full-coordinate representatives of the singleton anchors, signed pair anchors, and pair equality differences.

This produces an exact refined linear skeleton sufficient to determine every shared-dependent local-frequency shift used by the first-dyadic representation.

## Exact local ranks

The global refined rank remains `149`.

Base-rank histogram:

`{11:24, 12:107, 13:15, 14:1, 19:4, 20:14, 21:85}`.

Anchor cross-control rank histogram:

`{10:8, 11:152, 13:1, 14:73, 15:14, 16:2}`.

Difference cross-control rank histogram:

`{0:103, 1:6, 2:11, 3:57, 4:26, 5:40, 6:3, 7:4}`.

Combined cross-control rank histogram:

`{10:7, 11:96, 12:6, 13:12, 14:25, 15:11, 16:36, 17:19, 18:31, 19:3, 20:1, 21:3}`.

The extra rank over the pre-existing support/frequency signature is

`{0:103, 10:9, 11:48, 12:2, 13:81, 14:7}`.

Exactly 103 groups require no extra rank; these are the singleton groups. The maximum per-group extra rank is 14.

The refined-rank histogram is

`{19:4, 20:14, 21:87, 22:16, 23:36, 24:10, 25:71, 26:11, 27:1}`.

## Exact displayed separator certificates

For deterministic orders, the recursive widths are:

- `base_multiplicity_then_rank`: `85`
- `multiplicity_then_refined`: `83`
- `refined_rank_ascending`: `83`
- `refined_rank_descending`: `80`

The best displayed tree therefore has width `80`, depth `11`, under `refined_rank_descending`.

Its root children both have coupling `lambda=48`:

- size 83: rank 127, complement rank 70
- size 167: rank 70, complement rank 127

The best sampled balanced cut has `lambda=57`, with 125 groups on each side and ranks 57 and 149.

## Interpretation

Decision:

`CROSS_FREQUENCY_LINEAR_SKELETON_WIDTH_80`

The common shared-to-left frequency controls can be integrated into an exact 149-rank linear skeleton with a displayed recursive width of 80. This is a meaningful precursor, but not a complete grouped-e0 carry state: the local-left quadratic blocks, shared-only phase components, possible support-gauge reductions, and exact signed integer residual arithmetic are not charged by this certificate.

## Scope

No complete grouped-e0 carry contraction, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work bound, alpha, ranking/search, or full-round theorem is claimed.

`ALPHA_PASS=0`
