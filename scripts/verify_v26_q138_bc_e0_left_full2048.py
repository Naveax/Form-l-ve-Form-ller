#!/usr/bin/env python3
import subprocess,sys
p=subprocess.run([sys.executable,'scripts/probe_v26_q138_predecessor_leaf_bc_e0_sign_qrank_minor.py'],capture_output=True,text=True,check=True)
print(p.stdout,end='')
assert 'position B deterministic_sign_vectors 2048 modulus 65521 minor_rank_mod_p 2048 full True' in p.stdout
assert 'position C deterministic_sign_vectors 2048 modulus 65521 minor_rank_mod_p 2048 full True' in p.stdout
print('PASS V26_Q138_BC_E0_LEFT_FULL2048')
print('scope=left-factor span only; assembled correction rank not claimed')
