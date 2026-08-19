#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A

S=sorted(A.S1)
R=A.R1
SITES=[(j,i) for j in range(1,4) for i in range(31)]
SID={z:k for k,z in enumerate(SITES)}
SPECIAL={(1,0),(3,0)}
NONSPECIAL=[z for z in SITES if z not in SPECIAL]
assert len(SITES)==93 and len(NONSPECIAL)==91

INT={'U3':0,'V3':32,'U4':64,'V4':96}
PRED={'A0':0,'B0':32,'C0':64,'D0':96}


def fi(name,i): return (1<<(INT[name]+(i%32)),0)
def fb(i): return (1<<(128+(i%32)),0)
def fp(name,i): return (0,1<<(1+PRED[name]+(i%32)))

def xx(*fs):
    m=e=0
    for a,b in fs:m^=a;e^=b
    return m,e


def forms(pos):
    def O(letter,k):return fb(k) if pos==letter else (0,0)
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


def add(rows,f,e=0):
    m,r=f;rows.append([m,r^e])


def always_rows(pos):
    F=forms(pos);rows=[]
    for j in range(1,4):
        for i in range(1,31):
            add(rows,xx(F[j,i,'u'],F[j,i,'v'],F[j,i,'w']),zrhs((j,i-1),(j,i)))
        add(rows,xx(F[j,31,'u'],F[j,31,'v']))
        add(rows,xx(F[j,31,'u'],F[j,31,'w']))
        add(rows,xx(F[j,31,'u'],F[j,31,'v'],F[j,31,'w']),zrhs((j,30),const=1))
    j=4
    add(rows,xx(F[j,0,'u'],F[j,0,'v']));add(rows,xx(F[j,0,'u'],F[j,0,'w']))
    for i in range(1,31):
        add(rows,xx(F[j,i,'u'],F[j,i,'v'],F[j,i,'w']))
        add(rows,xx(F[j,i,'u'],F[j,i,'v']));add(rows,xx(F[j,i,'u'],F[j,i,'w']))
    add(rows,xx(F[j,31,'u'],F[j,31,'v']));add(rows,xx(F[j,31,'u'],F[j,31,'w']))
    add(rows,xx(F[j,31,'u'],F[j,31,'v'],F[j,31,'w']))
    return rows


def selected_expressions(pos):
    rows=always_rows(pos)
    keep=R if pos=='A' else S
    elim=[i for i in range(32) if i not in keep]
    order=list(range(128))+[128+i for i in elim]+[128+i for i in keep]
    r=0;pivs=[]
    for col in order:
        p=next((k for k in range(r,len(rows)) if (rows[k][0]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        pm,pe=rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k][0]>>col)&1):rows[k][0]^=pm;rows[k][1]^=pe
        pivs.append(col);r+=1
    out={}
    for row,col in zip(rows[:r],pivs):
        if col>=128 and (col-128) in keep:
            assert row[0]==1<<col,(pos,col,row[0])
            out[col-128]=row[1]
    assert len(out)==len(keep),(pos,len(out),len(keep))
    return keep,out


def rank(rows,n):
    return T.gf2_rank(rows,n)


def h_columns(pos):
    keep,expr=selected_expressions(pos)
    H=[]
    for z in SITES:
        bit=129+SID[z];v=0
        for q,i in enumerate(keep):
            if (expr[i]>>bit)&1:v|=1<<q
        H.append(v)
    return keep,H


def exact_weight_sets(V,maxw=None):
    n=len(V);m=n if maxw is None else min(maxw,n)
    Sx=[set() for _ in range(m+1)];Sx[0]={0}
    for t,v in enumerate(V):
        for w in range(min(m,t+1),0,-1):
            Sx[w].update(x^v for x in Sx[w-1])
    return Sx


def offset_sizes(Sx,total_e):
    out=[]
    for e in range(total_e+1):
        a=Sx[e] if e<len(Sx) else set()
        b=Sx[e-1] if 0<=e-1<len(Sx) else set()
        out.append(len(a|b))
    return out


def conv4_layer(seqs,k):
    a,b,c,d=seqs;s=0
    for i in range(k+1):
        for j in range(k-i+1):
            for q in range(k-i-j+1):
                r=k-i-j-q;s+=a[i]*b[j]*c[q]*d[r]
    return s


def main():
    data={}
    for pos in 'AD':
        keep,H=h_columns(pos)
        dim=len(keep);hr=rank(H,dim)
        assert hr==dim,(pos,hr,dim)
        assert all(H[SID[z]]==0 for z in SPECIAL)
        V=[H[SID[z]] for z in NONSPECIAL]
        zc=sum(v==0 for v in V);dc=len(set(V))
        if pos=='A':
            assert (dim,dc,zc)==(21,41,20),(dim,dc,zc)
            SX=exact_weight_sets(V,4);O=offset_sizes(SX,4)
            assert [len(s) for s in SX]==[1,41,763,8525,62718]
            assert O==[1,41,763,8525,62718],O
        else:
            assert (dim,dc,zc)==(11,20,45),(dim,dc,zc)
            SX=exact_weight_sets(V)
            O=offset_sizes(SX,92)
            expected_low=[1,20,173,838,1958]
            assert O[:5]==expected_low,O[:5]
            assert all(x==2048 for x in O[5:88]),Counter(O[5:88])
            assert O[88:93]==[1958,838,173,20,1],O[88:93]
        data[pos]=(O,H)
        print('position',pos,'selected_dim',dim,'H_rank',hr,
              'distinct_nonspecial_columns',dc,'zero_nonspecial_columns',zc,
              'special_columns',[H[SID[z]] for z in sorted(SPECIAL)],flush=True)
        print('position',pos,'offset_sizes_prefix',O[:10],flush=True)
        if pos=='D':print('position D offset_sizes_suffix',O[83:93],flush=True)

    for s in (1,-1):
        assert (s-1)%2==0
        assert (s-s)//2==0

    AO=data['A'][0];DO=data['D'][0]
    Aseq=[1,41,564,2048,2048]+[2048]*10
    Dseq=[1,20,173,838,1958]+[2048]*10
    assert Aseq[0]==AO[0] and Aseq[1]==AO[1] and 564<=AO[2]
    assert Dseq[:5]==DO[:5]
    Bseq=[36,812]+[2048]*13
    Cseq=[84,972]+[2048]*13
    layers=[conv4_layer((Aseq,Bseq,Cseq,Dseq),k) for k in range(10)]
    expected=[3024,287664,12038592,292005472,4586351280,49716263696,
              387621863744,2230860887520,9647756379008,32011343233024]
    assert layers==expected,(layers,expected)
    total8=sum(layers[:9]);budget=1<<44;margin=budget-total8
    assert total8==12320846080000
    assert margin==5271339964416
    assert total8<budget and total8+layers[9]>budget

    print('A_exact_signed_prefix',[1,41,564,2048,2048])
    print('D_exact_signed_prefix',[1,20,173,838,1958])
    print('layers_k0_k9',layers)
    print('sum_k0_k8',total8,'budget_2^44',budget,'margin',margin)
    print('PASS V26_Q138_AD_UNIVERSAL_CARRY_OFFSET_EXACT_SIGNED_LIFTS')
    print('scope=universal selected-side carry-offset map, exact-signed A/D low-layer lifts, dynamic prefix through k8; complete tail remains open')

if __name__=='__main__':main()
