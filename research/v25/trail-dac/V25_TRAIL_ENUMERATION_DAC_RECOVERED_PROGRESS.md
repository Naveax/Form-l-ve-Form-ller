# Recovered V25 Trail Enumeration / D&C Authority

Historical snapshot `FDS_V25_TRAIL_ENUMERATION_DAC_SNAPSHOT.zip` was recovered and revalidated after Issue #16.

Status: `PASS_WITH_LIMITS`, next=`CONTINUE_TO_SECOND_LAYER_TENSOR_CONTRACTION`.

Measured results:
- exact punctured spectra have small dominant support: b10 top4 median energy 0.94693 and exact rank 6/6; b12 top8 median 0.95924; b14 top8 median 0.93542;
- verified inverse-QR trail engine reproduces toy exact Walsh spectra;
- one inverse double-round factorized exact signed energies: cap2 0.0205078125, cap3 0.1812324524, cap4 0.4534969479, cap5 0.6959718947;
- cap5 naive global trails 43,071,961,472 vs 3,438,542 factorized nonzero entries; compact-memory estimate ~1.034 TB vs ~82.5 MB, reduction ~12,526x;
- four-inverse-round low-weight global beam collapses; this is truncation/representation failure, not proof of zero true correlation.

Recovered source/test suite: **19/19 PASS** with dependencies restored. Cert status: `PASS_WITH_LIMITS`.

No end-to-end work reduction, alpha reduction or full-round relevance was admitted.