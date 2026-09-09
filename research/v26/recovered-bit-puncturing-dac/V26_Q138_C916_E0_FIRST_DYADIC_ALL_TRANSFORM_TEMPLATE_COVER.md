# V26 Q138 C916 e0 all-transform phase template coverage

## Purpose

Freeze the full-physical-support coverage test of the 340-anchor support-maximal template universe against all 577 transformed C e0 sectors, including the 237 frozen pair mates.

This gate exists because the merged pair-compatibility authority only controls anchor/mate sign differences on their support intersection. It does not justify using an anchor phase on mate-only support regions.

## Exact universe

- transformed sectors: **577**;
- term anchors: **340** = 237 pair anchors + 103 singleton anchors;
- pair mates: **237**;
- physical shared dimension: **149**;
- support-maximal anchor templates: **52**;
- maximal anchor support classes: **15**, class-size histogram `{1:13,18:1,21:1}`.

## Full-support containment result

Exactly **574/577** transforms are contained in one and only one maximal anchor-template support.

Exactly three transforms have no containing maximal anchor-template support:

- `(group_id=61, sector_index=1)`;
- `(group_id=61, sector_index=3)`;
- `(group_id=227, sector_index=1)`.

All three are pair mates.

Owner-class count histogram: `{0:3,1:574}`. There are no transforms with multiple maximal anchor support classes.

Decision: `ANCHOR_MAXIMAL_TEMPLATE_SUPPORT_DOES_NOT_COVER_ALL_577_TRANSFORMS`.

## Frozen 33-template / R=2 anchor optimum on all sectors

The merged anchor-optimal 33-template set covers the physical supports of 574 transforms. The same three pair mates have no containing selected template.

Among the covered 574 transforms, minimum direct residual polar-rank histogram is:

`{0:355,2:213,4:6}`.

The six rank-4 exceptions are all pair mates. Therefore the 33-template anchor optimum is neither support-complete nor R=2-complete on the full 577-transform universe.

## Frozen 19-template / R=4 anchor optimum on all sectors

The 19-template anchor-optimal set again covers only 574 transform supports, missing exactly the same three pair mates.

Among the covered 574 transforms, minimum residual rank histogram is:

`{0:256,2:267,4:51}`.

There are no over-R=4 residuals among the covered transforms. Thus its only full-sector failure is physical-support coverage of the three pair mates.

## Consequence

The 340-anchor maximal-template universe is not a complete phase-template universe for the actual 577 transformed sectors. Separator-state attachment must not proceed from #154/#155 alone.

The next exact target is to rebuild support-maximal templates over **all 577 transforms**, determine whether the three uncovered pair mates create new maximal supports/classes, and recompute exact R=0/R=2/R=4 template covers on that complete universe.

## Scope

No separator-width attachment, no template common high-rank sign cost, no complete grouped-e0 separator theorem, no support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work, alpha, ranking/search, or full-round claim is made.

`ALPHA_PASS=0`.
