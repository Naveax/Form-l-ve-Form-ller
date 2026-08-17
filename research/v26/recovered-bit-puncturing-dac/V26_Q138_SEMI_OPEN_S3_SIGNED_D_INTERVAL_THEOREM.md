# V26 q138 semi-open S3 signed D-interval theorem

Scope: the frozen S3/complement cut in the exact one-output/open-four-input fused QR representation, for predecessor orientation D. This is an exact representation-rank statement, not a constructive/work claim and not a lower bound.

Let the S3 interval `[4,5]` expose its full twelve fused crossing channels: at site4 the incoming four carry channels plus `K0,K1`, and at site5 the outgoing four carry channels plus `K0,K1`. Contract the four carry channels internal to the two-site interval exactly.

Using the exact dyadic local Walsh tensor scaled by16, the resulting 4096-row interval map has exact rational rank

`rank_D[4,5] = 1016`.

Certificate structure in `scripts/verify_v26_q138_semi_open_s3_signed_d_interval.py`:

- the exact integer Gram matrix has 1520 zero rows;
- modulo row equality/sign, 1760 representatives remain;
- sparse Gaussian elimination modulo the odd prime1000003 gives rank1016 and744 independent dependencies;
- every one of those modular dependencies, after centered lifting, is verified as an exact integer relation on the Gram rows;
- hence `rank_Q Gram<=1016`, while the odd-prime rank gives `rank_Q Gram>=1016`;
- over Q/R, `rank(M M^T)=rank(M)`, so the interval map rank is exactly1016.

The three disjoint remaining D entry blocks on sites11,19,27 each have exact rational rank96 by signed-row-class upper bounds plus matching odd-prime ranks. The four compressed groups cover 33 of the57 fused EC crossing channels; the remaining24 channels are passed as binary.

Therefore

`rank_D(S3) <= 1016 * 96^3 * 2^24 = 3429 * 2^42`,

and

`F_D <= 42 + log2(3429) = 53.74357218893564... <55`.

This improves the previous generic D cap55 by

`1.25642781106436...` bits.

No claim is made that 1016 or the global D bound is optimal. The theorem only supplies a safe exact factorization upper bound for the frozen S3 cut.
