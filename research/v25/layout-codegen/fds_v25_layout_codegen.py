from __future__ import annotations
from dataclasses import dataclass
from types import SimpleNamespace
import time
import fds_v25_chacha as ch
import fds_v25_boundary_syndrome as bs
import fds_v25_layout_cache as lc
from fds_v25_key_layout import Field,active_state_words,state_from_layout

@dataclass
class Spec:
    z:tuple[int,...]
    base:tuple[int,...]
    final_base:tuple[int,...]
    ff:tuple[tuple[int,int,int,int] | None,...]
    fi:tuple[tuple[int,int,int,int] | None,...]
    fd:tuple[tuple[int,int,int,int] | None,...]

def _fixed_outputs_only(base_state,ops,active):
    flags=lc.classify_ops(ops,active);x=[int(v)&ch.MASK32 for v in base_state];out=[]
    for op,cand in zip(ops,flags):
        q=bs.schedule(op.round_index)[op.group_index]
        if cand:
            out.append(None)
            # Skip: dep words may be stale, but every future fixed QR is disjoint
            # from propagated dep and therefore does not consume these words.
        else:
            lc.apply_op(x,op);out.append(tuple(int(x[i]) for i in q))
    return tuple(out),flags

def prepare_spec(z,fields,bits=10,counter=1,need_screen=True):
    z=tuple(int(v)&ch.MASK32 for v in z);fields=tuple(fields);base=state_from_layout(0,bits,fields,counter);final=[(z[i]-base[i])&ch.MASK32 for i in range(16)];a=active_state_words(fields)
    if need_screen:
        ff,_=_fixed_outputs_only(base,lc.screen_forward_ops(),a);fi,_=_fixed_outputs_only(final,lc.screen_inverse_ops(),a)
    else:ff=fi=tuple()
    fd,_=_fixed_outputs_only(base,lc.direct_ops(),a)
    return Spec(z,tuple(base),tuple(final),ff,fi,fd)

def _word_expr(fields,sw):
    parts=[]
    for f in fields:
        if f.state_word==sw:
            mask=(1<<f.width)-1;parts.append(f'(((k>>{f.logical_shift})&{mask})<<{f.bit_offset})')
    return '|'.join(parts) if parts else '0'

def _patch_lines(var,fields,prefix=''):
    return [f'    {var}[{sw}]={_word_expr(fields,sw)}' for sw in sorted({f.state_word for f in fields})]

def _inverse_patch_lines(var,fields):
    return [f'    {var}[{sw}]=(sp.z[{sw}]-({_word_expr(fields,sw)}))&MASK' for sw in sorted({f.state_word for f in fields})]

def _emit_ops(var,ops,flags,fo_attr):
    lines=[]
    for idx,(op,cand) in enumerate(zip(ops,flags)):
        q=bs.schedule(op.round_index)[op.group_index]
        if cand:
            fn='inverse_quarter_round' if op.inverse else 'quarter_round';lines.append(f'    ch.{fn}({var},{q[0]},{q[1]},{q[2]},{q[3]})')
        else:
            lines.append(f'    v=sp.{fo_attr}[{idx}]')
            for j,sw in enumerate(q):lines.append(f'    {var}[{sw}]=v[{j}]')
    return lines

def generate_module(layouts:dict[str,list[Field]]):
    t0=time.perf_counter();lines=['import fds_v25_chacha as ch','MASK=ch.MASK32','']
    for lid,fields0 in layouts.items():
        fields=tuple(fields0);active=active_state_words(fields)
        fops=lc.screen_forward_ops();iops=lc.screen_inverse_ops();dops=lc.direct_ops();ff=lc.classify_ops(fops,active);fi=lc.classify_ops(iops,active);fd=lc.classify_ops(dops,active)
        # screen
        lines.append(f'def screen_{lid}(k,sp):');lines.append('    f=list(sp.base)');lines += _patch_lines('f',fields);lines += _emit_ops('f',fops,ff,'ff');lines.append('    x=list(sp.final_base)');lines += _inverse_patch_lines('x',fields);lines += _emit_ops('x',iops,fi,'fi');lines.append('    return int(f[0])^int(x[0])');lines.append('')
        # direct
        lines.append(f'def direct_{lid}(k,sp):');lines.append('    x=list(sp.base)');lines += _patch_lines('x',fields);lines += _emit_ops('x',dops,fd,'fd');lines.append('    return ((int(x[0])+int(sp.base[0]))&MASK)==sp.z[0]');lines.append('')
    src='\n'.join(lines)+'\n';ns={};t1=time.perf_counter();exec(compile(src,'<v25_layout_codegen>','exec'),ns);t2=time.perf_counter();return src,ns,{'generation_s':t1-t0,'compile_exec_s':t2-t1,'source_bytes':len(src.encode())}
