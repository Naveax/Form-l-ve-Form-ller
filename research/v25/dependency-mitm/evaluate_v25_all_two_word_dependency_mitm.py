from __future__ import annotations
import itertools,collections
import fds_v25_boundary_syndrome as bs

def terminal_word_sets(split,word):
    needed={word}
    for r in range(split-1,-1,-1):
        ids=tuple(i for i,q in enumerate(bs.schedule(r)) if needed.intersection(q));needed={w for i in ids for w in bs.schedule(r)[i]}
    f=frozenset(needed);needed={word}
    for r in range(split,6):
        ids=tuple(i for i,q in enumerate(bs.schedule(r)) if needed.intersection(q));needed={w for i in ids for w in bs.schedule(r)[i]}
    return f,frozenset(needed)

cones=[]
for s in range(1,6):
    for w in range(16):
        f,b=terminal_word_sets(s,w);c=bs.dependency_cone(s,w);cones.append({'split':s,'word':w,'fset':f,'bset':b,'total_qr':c.total_qr_count})
rows=[];cands=[];bylayout={}
for A,B in itertools.combinations(range(4,12),2):
    active={A,B};patterns=collections.Counter();n=0
    for c in cones:
        f=set(c['fset'])&active;b=set(c['bset'])&active;ok=bool(f and b and f.isdisjoint(b) and f|b==active);patterns[(tuple(sorted(f)),tuple(sorted(b)))]+=1
        row={'active_words':[A,B],'split':c['split'],'word':c['word'],'forward_active':sorted(f),'backward_active':sorted(b),'total_qr':c['total_qr'],'disjoint_cover':ok};rows.append(row)
        if ok:cands.append(row);n+=int(ok)
    bylayout[f'{A}_{B}']={'candidate_count':n,'patterns':[{'forward':list(k[0]),'backward':list(k[1]),'count':v} for k,v in sorted(patterns.items())]}
