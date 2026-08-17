# V26 Q1.38 dyadic tail depth gate

## Scope

The clean five-layer prefix theorem leaves the exact four-leaf tail budget

`B_tail = 1,935,451,277,056`.

This note asks whether solving only the next one or two currently unresolved single-leaf residue levels could possibly make product layer `k=5` fit that entire budget.

The answer is no, even under unrealistically favorable zero-rank assumptions.

## Rank-series notation

Use single-leaf layer rank envelopes

A: `a0=3`, `a1=309`, `a2,a3,... unresolved`;

B: `b0=1052`, `b1,b2,... unresolved`;

C: `c0=1160`, `c1,c2,... unresolved`;

D: `d0=3`, `d1=310`, `d2,d3,... unresolved`.

Every unresolved layer has the universal fallback `<=2048`.

The four-leaf product layer `r5` is the coefficient of `x^5` in

`A(x)B(x)C(x)D(x)`.

## First unresolved depth set to zero

Pretend, much more strongly than any current theorem, that

`a2=d2=b1=c1=0`.

Keep every deeper unresolved rank at the generic2048 cap.

Exact convolution gives

`r5 = 2,067,939,590,144`.

This exceeds the entire remaining tail budget by

`132,488,313,088`.

Therefore even perfect elimination of the first unresolved residue in all four leaves cannot close the dyadic tail.

## First two unresolved depths set to zero

Now additionally pretend

`a3=d3=b2=c2=0`.

Again keep all deeper unresolved ranks at2048.

Exact convolution gives

`r5 = 2,004,408,467,456`.

This still exceeds the entire remaining tail budget by

`68,957,190,400`.

Thus even perfect elimination of the first two unresolved residue levels in all four leaves is insufficient for layer5 alone.

## Consequence

Any successful dyadic-tail proof must do at least one of the following:

1. reach a third unresolved depth (`a4/d4` or `b3/c3`) with coefficient-specific compression;
2. sharpen an already-certified earlier bound (`a1=309`, `d1=310`, `b0=1052`, `c0=1160`, or even the first A/D rank3 layers);
3. prove nontrivial cancellations directly at the four-leaf product level rather than bounding layers by subadditive tensor-rank convolution.

In particular, a program that computes only the B/C second residue and stops cannot establish the required full tail bound.

This is a search-depth theorem for the current dyadic-layer certificate method. It is not a lower bound on the true full leaf-product rank or on unrestricted arithmetic work.
