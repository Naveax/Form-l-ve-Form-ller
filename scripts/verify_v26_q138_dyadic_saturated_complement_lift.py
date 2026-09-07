#!/usr/bin/env python3

N=2048
BUDGET=1<<44


def conv(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j]+=x*y
    return out


def alt(prefix,d,start,length=12):
    out=list(prefix)
    assert len(out)==start
    for i in range(start,length):
        out.append(d if ((i-start)&1)==0 else N-d)
    return out


def four(A,B,C,D):
    return conv(conv(A,B),conv(C,D))


def cumulative9(b2,c2):
    # A/D use their latest admitted direct exact-signed bounds and then the
    # saturated-complement alternation. B/C are reset at a hypothetical
    # index2 bound b2/c2 and alternate from there.
    A=alt([1,41,564],1761,3,12)
    D=alt([1,20,173,838],1958,4,12)
    B=alt([36,812],b2,2,12)
    C=alt([84,972],c2,2,12)
    P=four(A,B,C,D)
    return sum(P[:10])


def main():
    # Immediate safe complements from the admitted previous layers.
    assert N-1761==287
    assert N-812==1236
    assert N-972==1076
    assert N-1958==90

    A=alt([1,41,564],1761,3,12)
    B=alt([36,812],1236,2,12)
    C=alt([84,972],1076,2,12)
    D=alt([1,20,173,838],1958,4,12)

    assert A[:10]==[1,41,564,1761,287,1761,287,1761,287,1761]
    assert B[:10]==[36,812,1236,812,1236,812,1236,812,1236,812]
    assert C[:10]==[84,972,1076,972,1076,972,1076,972,1076,972]
    assert D[:10]==[1,20,173,838,1958,90,1958,90,1958,90]

    P=four(A,B,C,D)
    expect=[
        3024,
        287664,
        11935392,
        283121296,
        4263338416,
        43221987824,
        305905291312,
        1534220327760,
        5424451203888,
        13519854417072,
    ]
    assert P[:10]==expect,(P[:10],expect)
    s8=sum(P[:9]);s9=sum(P[:10])
    assert s8==7312357496576
    assert s9==20832211913648
    assert s8<BUDGET<s9
    assert BUDGET-s8==10279828547840

    # The parametric k9 function is bilinear in b2,c2 because every B/C
    # alternating coefficient is affine in the corresponding reset rank.
    f00=cumulative9(0,0)
    f10=cumulative9(1,0)
    f01=cumulative9(0,1)
    f11=cumulative9(1,1)
    a=f00
    b=f10-f00
    c=f01-f00
    bc=f11-f10-f01+f00
    assert (a,b,c,bc)==(
        12425800334816,
        3537036576,
        2841485712,
        734769,
    )

    def formula(x,y):
        return a+b*x+c*y+bc*x*y

    # Independent grid checks against direct convolution.
    for x,y in [(0,0),(1,1),(745,745),(746,746),(1236,1076),(2048,2048),(731,509)]:
        assert cumulative9(x,y)==formula(x,y),(x,y,cumulative9(x,y),formula(x,y))

    v745=formula(745,745)
    v746=formula(746,746)
    assert v745==17585614603601
    assert v746==17593088666468
    assert v745<BUDGET<v746

    print('safe_sequences')
    print('A',A[:10])
    print('B',B[:10])
    print('C',C[:10])
    print('D',D[:10])
    print('layers_k0_k9',P[:10])
    print('sum_k0_k8',s8,'margin',BUDGET-s8)
    print('sum_k0_k9',s9,'over',s9-BUDGET)
    print('parametric_k9_coefficients',a,b,c,bc)
    print('equal_t745',v745,'margin',BUDGET-v745)
    print('equal_t746',v746,'over',v746-BUDGET)
    print('PASS V26_Q138_DYADIC_SATURATED_COMPLEMENT_LIFT')
    print('scope=exact integer-lift existence plus convolution arithmetic; complete dyadic tail remains open')

if __name__=='__main__':
    main()
