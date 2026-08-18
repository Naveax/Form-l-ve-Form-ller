#!/usr/bin/env python3
from collections import Counter

S=[0,1,2,3,4,5,12,13,14,15,16]
R=[i for i in range(32) if i not in S]
SITES=[(j,i) for j in range(1,4) for i in range(31)]
SID={z:k for k,z in enumerate(SITES)}
SP1=(1,0);SP3=(3,0);SPECIAL={SP1,SP3}
NONSPECIAL=[z for z in SITES if z not in SPECIAL]
assert len(SITES)==93 and len(NONSPECIAL)==91

INT={'U3':0,'V3':32,'U4':64,'V4':96}
PRED={'A0':0,'B0':32,'C0':64,'D0':96}
MASK11=(1<<11)-1

# Unknown coordinates: internal0..127, beta128..159.
# Symbolic RHS bits: const0, predecessor1..128, zero indicators129..221.
def fi(name,i):return (1<<(INT[name]+(i%32)),0)
def fb(i):return (1<<(128+(i%32)),0)
def fp(name,i):return (0,1<<(1+PRED[name]+(i%32)))

def xx(*fs):
    m=e=0
    for a,b in fs:m^=a;e^=b
    return m,e


def forms_A():
    def O(letter,k):return fb(k) if letter=='A' else (0,0)
    F={}
    for i in range(32):
        F[4,i,'u']=fi('U4',i);F[4,i,'v']=fi('V4',i);F[4,i,'w']=xx(O('C',i),O('B',i+7))
        F[3,i,'u']=fi('U3',i);F[3,i,'v']=fi('V3',i);F[3,i,'w']=xx(O('A',i),fi('V4',i+8),O('D',i+8))
        F[2,i,'u']=fp('C0',i);F[2,i,'v']=xx(fi('V4',i+8),O('D',i+8),fp('D0',i+16));F[2,i,'w']=xx(fi('U4',i),fi('V3',i+12),O('B',i+19))
        F[1,i,'u']=fp('A0',i);F[1,i,'v']=xx(fp('B0',i),fi('V3',i+12),O('B',i+19));F[1,i,'w']=xx(fi('U3',i),fp('D0',i))
    return F


def zrhs(*zs,const=0):
    e=const&1
    for z in zs:e ^= 1<<(129+SID[z])
    return e


def always_rows():
    F=forms_A();rows=[]
    def add(f,e=0):
        m,r=f;rows.append([m,r^e])
    for j in range(1,4):
        for i in range(1,31):
            add(xx(F[j,i,'u'],F[j,i,'v'],F[j,i,'w']),zrhs((j,i-1),(j,i)))
        add(xx(F[j,31,'u'],F[j,31,'v']))
        add(xx(F[j,31,'u'],F[j,31,'w']))
        add(xx(F[j,31,'u'],F[j,31,'v'],F[j,31,'w']),zrhs((j,30),const=1))
    j=4
    add(xx(F[j,0,'u'],F[j,0,'v']));add(xx(F[j,0,'u'],F[j,0,'w']))
    for i in range(1,31):
        add(xx(F[j,i,'u'],F[j,i,'v'],F[j,i,'w']))
        add(xx(F[j,i,'u'],F[j,i,'v']));add(xx(F[j,i,'u'],F[j,i,'w']))
    add(xx(F[j,31,'u'],F[j,31,'v']))
    add(xx(F[j,31,'u'],F[j,31,'w']))
    add(xx(F[j,31,'u'],F[j,31,'v'],F[j,31,'w']))
    return F,rows


def derivative_pair(F,direction):
    m=e=0
    for j in range(1,5):
        for i in range(31):
            aa=xx(F[j,i,'u'],F[j,i,'w'])
            bb=xx(F[j,i,'v'],F[j,i,'w'])
            a=(aa[0]&direction).bit_count()&1
            b=(bb[0]&direction).bit_count()&1
            if a:m^=bb[0];e^=bb[1]
            if b:m^=aa[0];e^=aa[1]
            if a&b:e^=1
    return m,e


def special_eqs(F,z):
    j,i=z
    return [list(xx(F[j,i,'u'],F[j,i,'v'])),list(xx(F[j,i,'u'],F[j,i,'w']))]


def projected_regime(reg):
    F,base=always_rows();rows=[r[:] for r in base]
    if reg=='N':
        # The admitted arbitrary zero-set law gives the common top kernel U3_0
        # for every all-nonspecial family. Nonzero equal-sign Gauss summation
        # imposes this radical derivative constraint.
        rows.append(list(derivative_pair(F,1<<INT['U3'])))
    elif reg=='S1':rows+=special_eqs(F,SP1)
    elif reg=='S3':rows+=special_eqs(F,SP3)
    elif reg=='B':rows+=special_eqs(F,SP1)+special_eqs(F,SP3)
    else:raise ValueError(reg)

    # Eliminate internal variables and all right21 beta variables. Additional
    # nonspecial equality rows are intentionally omitted: this enlarges the
    # projected support and is therefore safe for an upper bound.
    elim=list(range(128))+[128+i for i in R]
    r=0
    for col in elim:
        p=next((k for k in range(r,len(rows)) if (rows[k][0]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        pm,pe=rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k][0]>>col)&1):rows[k][0]^=pm;rows[k][1]^=pe
        r+=1

    li={i:q for q,i in enumerate(S)};res=[];constraints=[]
    for m,e in rows[r:]:
        lm=0
        for i,q in li.items():
            if (m>>(128+i))&1:lm|=1<<q
        if lm:res.append([lm,e])
        elif e:constraints.append(e)

    # RREF on left11. Pure external-consistency rows are discarded; doing so
    # can only enlarge the support and keeps the rank upper uniform.
    q=0;pivs=[]
    for col in range(11):
        p=next((k for k in range(q,len(res)) if (res[k][0]>>col)&1),None)
        if p is None:continue
        res[q],res[p]=res[p],res[q]
        pm,pe=res[q]
        for k in range(len(res)):
            if k!=q and ((res[k][0]>>col)&1):res[k][0]^=pm;res[k][1]^=pe
        pivs.append(col);q+=1
    for m,e in res[q:]:
        assert m==0
        if e:constraints.append(e)
    rr=res[:q];free=[i for i in range(11) if i not in pivs]

    expr=[0]*11
    for (m,e),p in zip(rr,pivs):expr[p]=e
    U=[]
    for f in free:
        v=1<<f
        for (m,e),p in zip(rr,pivs):
            if (m>>f)&1:v|=1<<p
        U.append(v)

    c=0;P=[];H=[]
    for i,e in enumerate(expr):
        if e&1:c|=1<<i
    for b in range(128):
        v=0
        for i,e in enumerate(expr):
            if (e>>(1+b))&1:v|=1<<i
        P.append(v)
    for z in SITES:
        v=0;bit=129+SID[z]
        for i,e in enumerate(expr):
            if (e>>bit)&1:v|=1<<i
        H.append(v)
    return {'rank':q,'U':tuple(U),'c':c,'P':tuple(P),'H':tuple(H),'constraints':len(constraints)}


def span_set(vs):
    out={0}
    for v in vs:out|={x^v for x in list(out)}
    return out


def exact_weight(V,w):
    if w<0:return set()
    dp=[set() for _ in range(w+1)];dp[0]={0}
    for t,v in enumerate(V):
        for k in range(min(w,t+1),0,-1):dp[k].update(x^v for x in dp[k-1])
    return dp[w]


def category_rows(d,reg,e):
    w=e if reg!='B' else e-1
    V=[d['H'][SID[z]] for z in NONSPECIAL]
    base=d['c']
    if reg=='S1':base^=d['H'][SID[SP1]]
    elif reg=='S3':base^=d['H'][SID[SP3]]
    elif reg=='B':base^=d['H'][SID[SP1]]^d['H'][SID[SP3]]
    U=span_set(d['U']);out=set()
    for h in exact_weight(V,w):
        for u in U:out.add(base^h^u)
    return out


def basis(vals):
    B={}
    for x in vals:
        y=x
        while y:
            p=y.bit_length()-1
            if p in B:y^=B[p]
            else:B[p]=y;break
    return tuple(B.values())


def span_states(B):
    out=[0]
    for b in B:out += [x^b for x in out]
    return out


def main():
    D={reg:projected_regime(reg) for reg in ('N','S1','S3','B')}
    assert D['N']['rank']==10 and D['N']['U']==(65,)
    assert D['S1']['rank']==10 and D['S1']['U']==(1,)
    assert D['S3']['rank']==10 and D['S3']['U']==(64,)
    assert D['B']['rank']==11 and D['B']['U']==()

    e=3
    rows={reg:category_rows(D[reg],reg,e) for reg in D}
    sizes={reg:len(rows[reg]) for reg in rows}
    assert sizes=={'N':1168,'S1':1206,'S3':1206,'B':151},sizes

    PN=D['N']['P'];joint=[]
    for b in range(128):
        d1=D['S1']['P'][b]^PN[b]
        d3=D['S3']['P'][b]^PN[b]
        db=D['B']['P'][b]^PN[b]
        joint.append(d1|(d3<<11)|(db<<22))
    JB=basis(joint)
    assert len(JB)==4,len(JB)
    vals=[]
    for st in span_states(JB):
        d1=st&MASK11;d3=(st>>11)&MASK11;db=(st>>22)&MASK11
        U=set(rows['N'])
        U|={x^d1 for x in rows['S1']}
        U|={x^d3 for x in rows['S3']}
        U|={x^db for x in rows['B']}
        vals.append(len(U))
    dist=Counter(vals)
    assert dist==Counter({1742:8,1761:8}),dist
    assert max(vals)==1761

    print('A_e3_regime_left_fiber_ranks',{r:D[r]['rank'] for r in D})
    print('A_e3_regime_free_directions',{r:D[r]['U'] for r in D})
    print('A_e3_enlarged_category_row_sizes',sizes)
    print('A_e3_joint_relative_predecessor_shift_rank',len(JB),'states',len(vals))
    print('A_e3_row_union_size_distribution',dict(sorted(dist.items())))
    print('A_direct_e3_signed_aggregate_rank<=',max(vals))
    print('PASS V26_Q138_PREDECESSOR_LEAF_A_DIRECT_E3_ROW_UNION1761')
    print('scope=uniform direct valuation-e3 signed aggregate rank upper; external consistency and omitted nonspecial equality rows can only shrink support')

if __name__=='__main__':main()
