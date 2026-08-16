from __future__ import annotations

"""Small exact ChaCha research core used by the recovered V25 lab.

This is deliberately scoped to controlled reduced-key/reduced-round experiments.  The key
mapping follows the earlier V24 convention: the low ``b`` bits of key word 0 vary; all other
key words are zero.  Counter is explicit, nonce words are zero.
"""

import struct
from typing import Iterable

MASK32 = 0xFFFFFFFF
CONSTANTS = (0x61707865, 0x3320646E, 0x79622D32, 0x6B206574)
COL_QR = ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15))
DIAG_QR = ((0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14))


def rol32(x: int, n: int) -> int:
    return ((x << n) | (x >> (32 - n))) & MASK32


def ror32(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK32


def quarter_round(x: list[int], a: int, b: int, c: int, d: int) -> None:
    x[a] = (x[a] + x[b]) & MASK32
    x[d] = rol32(x[d] ^ x[a], 16)
    x[c] = (x[c] + x[d]) & MASK32
    x[b] = rol32(x[b] ^ x[c], 12)
    x[a] = (x[a] + x[b]) & MASK32
    x[d] = rol32(x[d] ^ x[a], 8)
    x[c] = (x[c] + x[d]) & MASK32
    x[b] = rol32(x[b] ^ x[c], 7)


def inverse_quarter_round(x: list[int], a: int, b: int, c: int, d: int) -> None:
    x[b] = ror32(x[b], 7) ^ x[c]
    x[c] = (x[c] - x[d]) & MASK32
    x[d] = ror32(x[d], 8) ^ x[a]
    x[a] = (x[a] - x[b]) & MASK32
    x[b] = ror32(x[b], 12) ^ x[c]
    x[c] = (x[c] - x[d]) & MASK32
    x[d] = ror32(x[d], 16) ^ x[a]
    x[a] = (x[a] - x[b]) & MASK32


def initial_state(key: bytes, counter: int = 1) -> list[int]:
    if len(key) != 32:
        raise ValueError("key must be 32 bytes")
    kw = struct.unpack("<8I", key)
    return [*CONSTANTS, *kw, counter & MASK32, 0, 0, 0]


def permute_state(state: Iterable[int], rounds: int) -> list[int]:
    if rounds <= 0 or rounds % 2:
        raise ValueError("rounds must be a positive even integer")
    x = [int(v) & MASK32 for v in state]
    if len(x) != 16:
        raise ValueError("state must have 16 words")
    for _ in range(rounds // 2):
        for q in COL_QR:
            quarter_round(x, *q)
        for q in DIAG_QR:
            quarter_round(x, *q)
    return x


def inverse_permute_state(state: Iterable[int], rounds: int) -> list[int]:
    if rounds <= 0 or rounds % 2:
        raise ValueError("rounds must be a positive even integer")
    x = [int(v) & MASK32 for v in state]
    if len(x) != 16:
        raise ValueError("state must have 16 words")
    for _ in range(rounds // 2):
        for q in reversed(DIAG_QR):
            inverse_quarter_round(x, *q)
        for q in reversed(COL_QR):
            inverse_quarter_round(x, *q)
    return x


def block_words(key: bytes, counter: int = 1, rounds: int = 20) -> tuple[int, ...]:
    s = initial_state(key, counter)
    p = permute_state(s, rounds)
    return tuple((a + b) & MASK32 for a, b in zip(p, s))


def block(key: bytes, counter: int = 1, rounds: int = 20) -> bytes:
    return struct.pack("<16I", *block_words(key, counter, rounds))


def reduced_key_layout(value: int, bits: int, *, offset: int = 0, fixed_word: int = 0) -> bytes:
    """Map a logical reduced key field into key word 0 for layout falsification.

    The active field has ``bits`` bits starting at ``offset``. ``fixed_word`` may set
    known inactive bits but may not overlap the active field.
    """
    bits = int(bits); offset = int(offset); fixed_word = int(fixed_word) & MASK32
    if not (1 <= bits <= 32):
        raise ValueError("reduced-key lab supports 1..32 key bits")
    if not (0 <= offset <= 32 - bits):
        raise ValueError("offset places active field outside key word")
    value = int(value)
    if not (0 <= value < (1 << bits)):
        raise ValueError("value outside reduced key space")
    active_mask = (((1 << bits) - 1) << offset) & MASK32 if bits < 32 else MASK32
    if fixed_word & active_mask:
        raise ValueError("fixed_word overlaps active reduced-key field")
    word = fixed_word | ((value << offset) & active_mask)
    return struct.pack("<I", word) + b"\0" * 28


def reduced_key(value: int, bits: int) -> bytes:
    return reduced_key_layout(value, bits)


def reduced_key_multiword(value: int, bits: int) -> bytes:
    """Map b active bits contiguously across the 256-bit ChaCha key words.

    Bit 0 is k0 bit0, bit 32 is k1 bit0, etc.  Intended only for controlled
    reduced-key scaling experiments.
    """
    bits=int(bits); value=int(value)
    if not (1 <= bits <= 256): raise ValueError('bits must be 1..256')
    if not (0 <= value < (1 << bits)): raise ValueError('value outside reduced key space')
    return value.to_bytes(32,'little')

from dataclasses import dataclass as _dataclass

@_dataclass(frozen=True)
class InverseSubTrace:
    op_index:int
    double_round_from_end:int
    phase:str
    qr:tuple[int,int,int,int]
    step:str
    lhs_word:int
    rhs_word:int
    lhs_before:int
    rhs_before:int
    result:int


def inverse_permute_state_trace(state: Iterable[int], rounds: int):
    """Inverse permutation plus an exact trace of every modular subtraction.

    The returned trace is observational instrumentation only; state semantics are identical
    to :func:`inverse_permute_state`.
    """
    if rounds <= 0 or rounds % 2:
        raise ValueError('rounds must be a positive even integer')
    x=[int(v)&MASK32 for v in state]
    if len(x)!=16: raise ValueError('state must have 16 words')
    traces=[]; op=0
    def iqr_trace(a,b,c,d,dr,phase,qr):
        nonlocal op
        x[b]=ror32(x[b],7)^x[c]
        L,R=x[c],x[d]; x[c]=(L-R)&MASK32; traces.append(InverseSubTrace(op,dr,phase,qr,'c_minus_d_after_r7',c,d,L,R,x[c]));op+=1
        x[d]=ror32(x[d],8)^x[a]
        L,R=x[a],x[b]; x[a]=(L-R)&MASK32; traces.append(InverseSubTrace(op,dr,phase,qr,'a_minus_b_after_r8',a,b,L,R,x[a]));op+=1
        x[b]=ror32(x[b],12)^x[c]
        L,R=x[c],x[d]; x[c]=(L-R)&MASK32; traces.append(InverseSubTrace(op,dr,phase,qr,'c_minus_d_after_r12',c,d,L,R,x[c]));op+=1
        x[d]=ror32(x[d],16)^x[a]
        L,R=x[a],x[b]; x[a]=(L-R)&MASK32; traces.append(InverseSubTrace(op,dr,phase,qr,'a_minus_b_after_r16',a,b,L,R,x[a]));op+=1
    for dr in range(rounds//2):
        for q in reversed(DIAG_QR): iqr_trace(*q,dr,'diag',q)
        for q in reversed(COL_QR): iqr_trace(*q,dr,'col',q)
    return x,traces
