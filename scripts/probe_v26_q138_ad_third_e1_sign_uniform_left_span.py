#!/usr/bin/env python3
"""Superseded exploratory entrypoint.

The original version eliminated predecessor-input variables while forming left
support masks and therefore could undercount affine coset shifts.  It is not an
authority source.  The safe replacement is the field-independent left-row
support theorem verified below.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_ad_third_e1_correction_rank362_171 as V

if __name__=='__main__':
    print('SUPERSEDED unsafe global-span construction; using exact left-row support bound instead')
    V.main()
