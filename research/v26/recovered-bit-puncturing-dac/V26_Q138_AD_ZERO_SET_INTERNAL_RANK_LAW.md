# V26 Q1.38 A/D arbitrary carry-zero internal rank law

## Statement

For positions A and D, let the93 variable carry sites be

`Zsites={(j,i): j in {1,2,3}, i in {0,...,30}}`.

The j4 carry string is forced zero and is already part of the A/D base system. Define the two special sites

`P={(1,0),(3,0)}`.

For any subset `Z subseteq Zsites`, impose carry zero at exactly the sites in Z and carry one at the other j1..j3 sites. Then the homogeneous internal system on the128 variables `(U3,V3,U4,V4)` has exact rank

- `127` if `Z intersect P` is empty;
- `128` if `Z intersect P` is nonempty.

Equivalently, every all-nonspecial zero pattern preserves the unique top null direction, while either special site kills it completely.

## Proof

At the all-one j1..j3 top pattern, the admitted A/D dyadic-descent theorem gives homogeneous internal rank127, hence a one-dimensional kernel N.

Changing a nonspecial carry site from1 to0 changes the homogeneous coefficient system only by adding the two equality rows `u+v=0` and `u+w=0` at that site; the always-present three-variable row has the same homogeneous coefficients. The clean single-zero classification says every nonspecial one-zero system still has rank127. Since it contains the top rank127 system, both newly added rows annihilate N.

Therefore every equality row contributed by every nonspecial site annihilates the same one-dimensional N. For an arbitrary set Z containing only nonspecial sites, all added rows annihilate N, so the augmented rank is at most127. It is at least127 because the top system is contained in it. Hence the rank is exactly127.

For either special site, the clean single-zero classification gives rank128. Any larger zero set containing that special site only adds rows, so rank cannot decrease and remains128.

This proves the law for all `2^93` carry-zero subsets without enumerating them.

## Combinatorial consequences

There are91 nonspecial sites and2 special sites. Thus among z-zero patterns:

- exactly `C(91,z)` have rank127/nullity1;
- exactly `C(93,z)-C(91,z)` have rank128.

For the next direct-e3 candidate families suggested by the already established e1/e2 valuation pattern:

- three nonspecial zeros: `C(91,3)=121,485` nullity-one candidates;
- four zeros containing at least one special:
  `C(93,4)-C(91,4)=2*C(91,3)+C(91,2)=247,065` full-rank candidates;
- total before external-consistency pruning: `368,550` candidates per A/D position.

The numerical e3 family count is a preparation result only. This theorem does not itself assert that every such candidate is externally reachable or that the valuation-e3 signed aggregate has a particular rank.

## Scope

This is an exact internal homogeneous rank theorem. It removes the need for repeated internal RREF over higher zero-set families. External consistency, singleton-map geometry, dyadic lift choice, higher-residue rank, complete tail, representation exponent, arithmetic work, alpha, and full-round relevance remain separate questions.
