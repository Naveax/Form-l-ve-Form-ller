from __future__ import annotations
import struct
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class Field:
    state_word: int
    bit_offset: int
    width: int
    logical_shift: int


def key_from_layout(value:int, bits:int, fields:Iterable[Field]) -> bytes:
    value=int(value); bits=int(bits); fields=tuple(fields)
    if not (1 <= bits <= 256): raise ValueError('bits')
    if not (0 <= value < (1<<bits)): raise ValueError('value')
    words=[0]*8
    covered=0
    logical_mask=0
    for f in fields:
        if not (4 <= f.state_word <= 11): raise ValueError('state_word must be key word state4..11')
        if not (1 <= f.width <= 32): raise ValueError('width')
        if not (0 <= f.bit_offset <= 32-f.width): raise ValueError('bit_offset')
        if not (0 <= f.logical_shift <= bits-f.width): raise ValueError('logical_shift')
        lm=((1<<f.width)-1)<<f.logical_shift
        if logical_mask & lm: raise ValueError('logical overlap')
        logical_mask |= lm
        widx=f.state_word-4
        wm=((1<<f.width)-1)<<f.bit_offset
        if words[widx] & wm: raise ValueError('physical overlap')
        chunk=(value>>f.logical_shift)&((1<<f.width)-1)
        words[widx] |= chunk<<f.bit_offset
    if logical_mask != (1<<bits)-1: raise ValueError('layout must cover every logical bit exactly once')
    return struct.pack('<8I',*words)


def active_state_words(fields:Iterable[Field]):
    return tuple(sorted({int(f.state_word) for f in fields}))

def state_from_layout(value:int,bits:int,fields:Iterable[Field],counter:int=1):
    import fds_v25_chacha as ch
    # Use the canonical ChaCha initial-state constructor for constants/counter,
    # then patch only the frozen active key/state words.
    s=ch.initial_state(bytes(32),int(counter))
    physical={}
    logical_mask=0
    for f in tuple(fields):
        if not (4 <= f.state_word <= 11): raise ValueError('state_word')
        lm=((1<<f.width)-1)<<f.logical_shift
        if logical_mask & lm: raise ValueError('logical overlap')
        logical_mask|=lm
        chunk=(int(value)>>f.logical_shift)&((1<<f.width)-1)
        pm=((1<<f.width)-1)<<f.bit_offset
        old=physical.get(f.state_word,0)
        if old & pm: raise ValueError('physical overlap')
        physical[f.state_word]=old | (chunk<<f.bit_offset)
    if logical_mask != (1<<int(bits))-1: raise ValueError('layout coverage')
    for sw,v in physical.items(): s[sw]=v & ch.MASK32
    return s
