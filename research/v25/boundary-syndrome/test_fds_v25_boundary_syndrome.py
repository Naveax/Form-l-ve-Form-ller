import random
import fds_v25_boundary_syndrome as bs


def test_all_cones_have_valid_group_indices():
    cs=bs.enumerate_cones()
    assert len(cs)==80
    for c in cs:
        assert 1<=c.split<=5 and 0<=c.word<16
        for r,ids in c.forward_groups+c.backward_groups:
            assert all(0<=i<4 for i in ids)


def test_partial_forward_inverse_exact_all_80_cones():
    rng=random.Random(0xB0A7D)
    for rep in range(12):
        s=[rng.getrandbits(32) for _ in range(16)]
        full=[x for x in s]
        states=[full.copy()]
        for r in range(6):
            bs.apply_round_full(full,r); states.append(full.copy())
        final=states[6]
        for c in bs.enumerate_cones():
            assert bs.partial_forward_word(s,c)==states[c.split][c.word]
            assert bs.partial_inverse_word(final,c)==states[c.split][c.word]


def test_selected_cone_is_structural_minimum():
    cs=bs.enumerate_cones();m=bs.select_min_cone()
    assert (m.total_qr_count,m.split,m.word)==min((c.total_qr_count,c.split,c.word) for c in cs)


def test_final_word_cone_exact_and_cost21():
    import random, fds_v25_chacha as ch
    c=bs.final_word_forward_cone(0)
    assert c.qr_count==21
    rng=random.Random(0xF1A1)
    for _ in range(32):
        s=[rng.getrandbits(32) for _ in range(16)]
        assert bs.partial_final_word(s,c)==ch.permute_state(s,6)[0]


def test_boundary_syndrome_zero_for_true_reduced_key():
    import fds_v25_chacha as ch
    c=bs.select_min_cone()
    for target in (1,17,511,1023):
        key=ch.reduced_key_multiword(target,10);s=ch.initial_state(key,1);z=ch.block_words(key,1,6)
        assert bs.boundary_syndrome(z,s,c)==0
        assert bs.direct_output_word_matches(z,s,bs.final_word_forward_cone(0))


def test_fast_word4_cached_paths_exact_against_generic():
    import random, fds_v25_chacha as ch
    rng=random.Random(0xCA6E)
    cone=bs.select_min_cone();fc=bs.final_word_forward_cone(0)
    for target in (73,385,893,1021):
        key=ch.reduced_key_multiword(target,10);z=ch.block_words(key,1,6);cache=bs.prepare_word4_cache(z,1)
        for k in [0,target,1023]+[rng.randrange(1024) for _ in range(8)]:
            s=ch.initial_state(ch.reduced_key_multiword(k,10),1)
            syn,q0=bs.fast_word4_syndrome_and_round0_group(k,cache)
            assert syn==bs.boundary_syndrome(z,s,cone)
            assert bs.fast_word4_direct_match(k,cache)==bs.direct_output_word_matches(z,s,fc)
            assert bs.fast_word4_verify_from_round0_group(q0,cache)==bs.direct_output_word_matches(z,s,fc)
