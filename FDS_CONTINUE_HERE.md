# FDS_CONTINUE_HERE

**State:** V26 counter-derivative and cross-word XOR ANF families NO-GO.  
**Active:** `V26_SOURCE_ORBIT_COUNTER_CUBE_SUPERPOLY_ANF_AUDIT`.

1. Use frozen plan under `research/v26/source-orbit-counter-cube/`.
2. Source counters only: cubes 512..767 and 1024..1279; fixed nonce; no chosen-IV extension.
3. Low 8 counter bits are the cube variables; XOR all 256 outputs per cube.
4. b=`8,10,12,14,16`; R4 control/R6 primary; all 512 output bits.
5. Exact packed key-ANF for cube sums and same-base single-counter controls.
6. Each R6 base at b16 must show median per-bit degree reduction >=2 and support-exp reduction >=0.10.
7. >=16 identical bits must be sparse-useful at b14/b16 for both bases.
8. Only PASS opens fresh source-orbit superpoly solving/TOTAL scaling.
9. FAIL closes this cube dimension/base family; no retuning.
