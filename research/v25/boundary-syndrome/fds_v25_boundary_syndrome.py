from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import fds_v25_chacha as ch

R = 6


def schedule(round_index: int):
    return ch.COL_QR if int(round_index) % 2 == 0 else ch.DIAG_QR


@dataclass(frozen=True)
class Cone:
    split: int
    word: int
    forward_groups: tuple[tuple[int, tuple[int, ...]], ...]
    backward_groups: tuple[tuple[int, tuple[int, ...]], ...]
    forward_qr_count: int
    backward_qr_count: int

    @property
    def total_qr_count(self) -> int:
        return self.forward_qr_count + self.backward_qr_count


def _round_groups_touching(round_index: int, needed: set[int]) -> tuple[int, ...]:
    groups = schedule(round_index)
    return tuple(i for i, q in enumerate(groups) if needed.intersection(q))


def dependency_cone(split: int, word: int, rounds: int = R) -> Cone:
    split = int(split); word = int(word); rounds = int(rounds)
    if not (1 <= split < rounds):
        raise ValueError('split must be inside the permutation')
    if not (0 <= word < 16):
        raise ValueError('word must be 0..15')

    # Forward: boundary word -> initial words, walking rounds backward.
    needed = {word}
    f_rev: list[tuple[int, tuple[int, ...]]] = []
    for r in range(split - 1, -1, -1):
        ids = _round_groups_touching(r, needed)
        f_rev.append((r, ids))
        needed = {w for i in ids for w in schedule(r)[i]}
    f = tuple(reversed(f_rev))

    # Backward: boundary word -> final words.  Walking original rounds forward
    # gives the inverse dependency cone; execution later runs them in reverse.
    needed = {word}
    b: list[tuple[int, tuple[int, ...]]] = []
    for r in range(split, rounds):
        ids = _round_groups_touching(r, needed)
        b.append((r, ids))
        needed = {w for i in ids for w in schedule(r)[i]}

    return Cone(
        split=split,
        word=word,
        forward_groups=f,
        backward_groups=tuple(b),
        forward_qr_count=sum(len(ids) for _, ids in f),
        backward_qr_count=sum(len(ids) for _, ids in b),
    )


def apply_round_full(state: list[int], r: int) -> None:
    for q in schedule(r):
        ch.quarter_round(state, *q)


def inverse_round_full(state: list[int], r: int) -> None:
    for q in reversed(schedule(r)):
        ch.inverse_quarter_round(state, *q)


def state_after_rounds(state: Iterable[int], count: int) -> list[int]:
    x = [int(v) & ch.MASK32 for v in state]
    for r in range(int(count)):
        apply_round_full(x, r)
    return x


def partial_forward_word(state: Iterable[int], cone: Cone) -> int:
    x = [int(v) & ch.MASK32 for v in state]
    for r, ids in cone.forward_groups:
        groups = schedule(r)
        for i in ids:
            ch.quarter_round(x, *groups[i])
    return int(x[cone.word])


def partial_inverse_word(final_state: Iterable[int], cone: Cone, rounds: int = R) -> int:
    x = [int(v) & ch.MASK32 for v in final_state]
    by_round = {r: ids for r, ids in cone.backward_groups}
    for r in range(int(rounds) - 1, cone.split - 1, -1):
        groups = schedule(r)
        # Full inverse order is reversed group order.  The QRs in a round are
        # disjoint, but retain the exact reference ordering anyway.
        selected = set(by_round[r])
        for i in range(len(groups) - 1, -1, -1):
            if i in selected:
                ch.inverse_quarter_round(x, *groups[i])
    return int(x[cone.word])


def enumerate_cones(rounds: int = R):
    return [dependency_cone(s, w, rounds) for s in range(1, rounds) for w in range(16)]


def select_min_cone(rounds: int = R) -> Cone:
    return min(enumerate_cones(rounds), key=lambda c: (c.total_qr_count, c.split, c.word))

@dataclass(frozen=True)
class FinalWordCone:
    word: int
    groups: tuple[tuple[int, tuple[int, ...]], ...]
    qr_count: int


def final_word_forward_cone(word: int, rounds: int = R) -> FinalWordCone:
    """Exact dependency cone for one final permutation word from the initial state."""
    word=int(word); rounds=int(rounds)
    if not (0 <= word < 16): raise ValueError('word must be 0..15')
    needed={word}; rev=[]
    for r in range(rounds-1,-1,-1):
        ids=_round_groups_touching(r,needed)
        rev.append((r,ids))
        needed={w for i in ids for w in schedule(r)[i]}
    groups=tuple(reversed(rev))
    return FinalWordCone(word,groups,sum(len(ids) for _,ids in groups))


def partial_final_word(state: Iterable[int], cone: FinalWordCone) -> int:
    x=[int(v)&ch.MASK32 for v in state]
    for r,ids in cone.groups:
        groups=schedule(r)
        for i in ids: ch.quarter_round(x,*groups[i])
    return int(x[cone.word])


def implied_final_state_from_output(output_words: Iterable[int], initial_state: Iterable[int]) -> list[int]:
    z=[int(v)&ch.MASK32 for v in output_words];s=[int(v)&ch.MASK32 for v in initial_state]
    if len(z)!=16 or len(s)!=16: raise ValueError('need 16 words')
    return [(a-b)&ch.MASK32 for a,b in zip(z,s)]


def boundary_syndrome(output_words: Iterable[int], initial_state: Iterable[int], cone: Cone) -> int:
    final=implied_final_state_from_output(output_words,initial_state)
    return partial_forward_word(initial_state,cone)^partial_inverse_word(final,cone)


def direct_output_word_matches(output_words: Iterable[int], initial_state: Iterable[int], cone: FinalWordCone) -> bool:
    z=[int(v)&ch.MASK32 for v in output_words];s=[int(v)&ch.MASK32 for v in initial_state]
    return ((partial_final_word(s,cone)+s[cone.word])&ch.MASK32)==z[cone.word]

@dataclass(frozen=True)
class Word4Cache:
    initial_base: tuple[int, ...]
    forward_fixed_round0: tuple[int, ...]
    inverse_fixed_round5: tuple[int, ...]
    output_words: tuple[int, ...]


def prepare_word4_cache(output_words: Iterable[int], counter: int = 1) -> Word4Cache:
    """Prepare candidate-independent work for a reduced key varying only state word4."""
    z=tuple(int(v)&ch.MASK32 for v in output_words)
    if len(z)!=16: raise ValueError('need 16 output words')
    base=ch.initial_state(ch.reduced_key_multiword(0,10),counter)
    # Direct-forward cache: round0 groups 1..3 never touch active word4.
    ff=base.copy()
    for i in (1,2,3): ch.quarter_round(ff,*schedule(0)[i])
    # Backward cache: implied final state at k=0, then the three round5
    # inverse groups that do not touch word4. Round groups are disjoint.
    fin=[(z[i]-base[i])&ch.MASK32 for i in range(16)]
    inv=fin.copy()
    for i in (2,1,0): ch.inverse_quarter_round(inv,*schedule(5)[i])
    return Word4Cache(tuple(base),tuple(ff),tuple(inv),z)


def fast_word4_syndrome_and_round0_group(k: int, cache: Word4Cache) -> tuple[int, tuple[int,int,int,int]]:
    """Exact split1/word0 syndrome with candidate-independent QR cache.

    Candidate QR count: 1 forward + 14 inverse = 15. The cache costs
    three inverse QRs per target.
    """
    k=int(k)&ch.MASK32
    # Candidate-dependent round0 group0, also retained for survivor verification.
    f=list(cache.initial_base);f[4]=k
    ch.quarter_round(f,*schedule(0)[0])
    q0=tuple(int(f[i]) for i in schedule(0)[0]);fw=int(f[0])
    # Cached inverse round5 groups0..2; group3 is the only one touching word4.
    x=list(cache.inverse_fixed_round5);x[4]=(cache.output_words[4]-k)&ch.MASK32
    ch.inverse_quarter_round(x,*schedule(5)[3])
    for r in (4,3,2):
        for q in reversed(schedule(r)): ch.inverse_quarter_round(x,*q)
    ch.inverse_quarter_round(x,*schedule(1)[0])
    return fw^int(x[0]), q0


def fast_word4_direct_match(k: int, cache: Word4Cache) -> bool:
    """Fair optimized direct output-word0 baseline: 18 QR/candidate + 3 fixed QR."""
    k=int(k)&ch.MASK32;x=list(cache.forward_fixed_round0);x[4]=k
    ch.quarter_round(x,*schedule(0)[0])
    for r in (1,2,3,4): apply_round_full(x,r)
    ch.quarter_round(x,*schedule(5)[0])
    return ((int(x[0])+int(cache.initial_base[0]))&ch.MASK32)==cache.output_words[0]


def fast_word4_verify_from_round0_group(q0_values: Iterable[int], cache: Word4Cache) -> bool:
    """Verify a screen survivor reusing its already-computed round0 group0: 17 QR."""
    vals=tuple(int(v)&ch.MASK32 for v in q0_values)
    if len(vals)!=4: raise ValueError('need four group0 words')
    x=list(cache.forward_fixed_round0)
    for i,v in zip(schedule(0)[0],vals):x[i]=v
    for r in (1,2,3,4): apply_round_full(x,r)
    ch.quarter_round(x,*schedule(5)[0])
    return ((int(x[0])+int(cache.initial_base[0]))&ch.MASK32)==cache.output_words[0]
