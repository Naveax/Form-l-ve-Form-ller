# V25 Reduced-Key Layout Transfer Falsifier

## Verdict

`ADMIT_BROAD_QR_LAYOUT_TRANSFER_NO_GENERIC_WALL_TRANSFER`

The split1/word0/width16 algorithm and six layouts were frozen before survivor measurement. On eight fresh paired logical targets, all 48 layout-target cases produced exactly one syndrome survivor, equal to the true logical key; direct word0 verification was unique in all 48 cases.

Conservative median TOTAL QR ratios: word4 control 0.83450; word5/6/7 0.77901; word4+word8 0.88999; word4+word6 0.84320. All 5/5 non-control layouts passed every frozen L1 gate, so broad mathematical QR transfer across the tested layouts is admitted.

The exact generic cache engine then matched the generic reference on 49,152 full syndrome values, 49,152 low16 predicates and 49,152 direct predicates. Frozen wall gates nevertheless failed on 5/5 non-control layouts. Median Python wall speedups: W5 1.0441x, W6 1.0394x, W7 1.0412x, W4+W8 0.9626x, W4+W6 0.9918x. Generic interpreter/copy overhead consumes the QR advantage.

Thus broad QR transfer is admitted but broad generic Python wall-time transfer is not. The prior hand-specialized word4 wall win remains valid only in its prior scope. Leading enumeration remains 2^b and alpha=1.

## Next

Freeze layout-specialized straight-line code generation and test real wall realization on fresh targets without changing split/word/width/layouts.
