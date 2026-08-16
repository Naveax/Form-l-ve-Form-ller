from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import fds_v25_chacha as ch
import fds_v25_boundary_syndrome as bs
from fds_v25_key_layout import Field,state_from_layout,active_state_words

@dataclass(frozen=True)
class Op:
    round_index:int
    group_index:int
    inverse:bool

@dataclass
class CachedProgram:
    ops:tuple[Op,...]
    candidate_flags:tuple[bool,...]
    fixed_outputs:tuple[tuple[int,int,int,int] | None,...]
    candidate_qr_count:int
    fixed_qr_count:int


def screen_forward_ops():
    c=bs.select_min_cone()
    return tuple(Op(r,i,False) for r,ids in c.forward_groups for i in ids)

def screen_inverse_ops():
    c=bs.select_min_cone(); by={r:set(ids) for r,ids in c.backward_groups};o=[]
    for r in range(5,c.split-1,-1):
        for i in range(3,-1,-1):
            if i in by[r]:o.append(Op(r,i,True))
    return tuple(o)

def direct_ops():
    c=bs.final_word_forward_cone(0)
    return tuple(Op(r,i,False) for r,ids in c.groups for i in ids)

def apply_op(x:list[int],op:Op):
    q=bs.schedule(op.round_index)[op.group_index]
    if op.inverse: ch.inverse_quarter_round(x,*q)
    else: ch.quarter_round(x,*q)

def classify_ops(ops:Iterable[Op],active_words:Iterable[int]):
    dep=set(int(x) for x in active_words);flags=[]
    for op in tuple(ops):
        q=bs.schedule(op.round_index)[op.group_index]
        cand=bool(dep.intersection(q));flags.append(cand)
        if cand:dep.update(q)
    return tuple(flags)

def prepare_program(base_state:Iterable[int],ops:Iterable[Op],active_words:Iterable[int]):
    ops=tuple(ops);flags=classify_ops(ops,active_words);x=[int(v)&ch.MASK32 for v in base_state];fo=[]
    for op,cand in zip(ops,flags):
        apply_op(x,op);q=bs.schedule(op.round_index)[op.group_index]
        fo.append(None if cand else tuple(int(x[i]) for i in q))
    return CachedProgram(ops,flags,tuple(fo),sum(flags),len(flags)-sum(flags))

def execute_program(state:Iterable[int],p:CachedProgram):
    x=[int(v)&ch.MASK32 for v in state]
    for op,cand,vals in zip(p.ops,p.candidate_flags,p.fixed_outputs):
        q=bs.schedule(op.round_index)[op.group_index]
        if cand:apply_op(x,op)
        else:
            assert vals is not None
            for i,v in zip(q,vals):x[i]=v
    return x

@dataclass
class LayoutCache:
    fields:tuple[Field,...]
    bits:int
    counter:int
    output_words:tuple[int,...]
    active_words:tuple[int,...]
    forward:CachedProgram
    inverse:CachedProgram
    direct:CachedProgram


def prepare_layout_cache(output_words:Iterable[int],fields:Iterable[Field],bits:int=10,counter:int=1):
    fields=tuple(fields);z=tuple(int(v)&ch.MASK32 for v in output_words);a=active_state_words(fields)
    base=state_from_layout(0,bits,fields,counter)
    final=[(z[i]-base[i])&ch.MASK32 for i in range(16)]
    return LayoutCache(fields,bits,counter,z,a,
        prepare_program(base,screen_forward_ops(),a),
        prepare_program(final,screen_inverse_ops(),a),
        prepare_program(base,direct_ops(),a))

def candidate_initial(value:int,c:LayoutCache):return state_from_layout(value,c.bits,c.fields,c.counter)
def candidate_final(value:int,c:LayoutCache):
    s=candidate_initial(value,c);return [(c.output_words[i]-s[i])&ch.MASK32 for i in range(16)]
def cached_syndrome(value:int,c:LayoutCache):
    f=execute_program(candidate_initial(value,c),c.forward)
    inv=execute_program(candidate_final(value,c),c.inverse)
    return int(f[0])^int(inv[0])
def cached_direct_match(value:int,c:LayoutCache):
    s=candidate_initial(value,c);x=execute_program(s,c.direct)
    return ((int(x[0])+int(s[0]))&ch.MASK32)==c.output_words[0]
def cost_tuple(c:LayoutCache):
    return (c.forward.candidate_qr_count+c.inverse.candidate_qr_count,
            c.forward.fixed_qr_count+c.inverse.fixed_qr_count,
            c.direct.candidate_qr_count,c.direct.fixed_qr_count)
