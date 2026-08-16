from __future__ import annotations
import fds_v25_boundary_syndrome as bs
ACTIVE={4:'low',6:'high'}
def terminal_support(split,word):
 needed={word}
 for r in range(split-1,-1,-1):
  ids=tuple(i for i,q in enumerate(bs.schedule(r)) if needed.intersection(q));needed={w for i in ids for w in bs.schedule(r)[i]}
 f=set(needed)&set(ACTIVE);needed={word}
 for r in range(split,6):
  ids=tuple(i for i,q in enumerate(bs.schedule(r)) if needed.intersection(q));needed={w for i in ids for w in bs.schedule(r)[i]}
 return sorted(f),sorted(set(needed)&set(ACTIVE))
rows=[]
for split in range(1,6):
 for word in range(16):
  f,b=terminal_support(split,word);rows.append((split,word,f,b,bool(f and b and set(f).isdisjoint(b) and set(f)|set(b)=={4,6})))
print('candidates',sum(x[-1] for x in rows),'of',len(rows))
