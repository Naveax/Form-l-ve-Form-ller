import fds_v26_single_column_qr_transform as q


def test_recovered_core_provenance():
    q.assert_recovered_core_provenance()


def test_cap2_all_columns_exact():
    q.assert_recovered_core_provenance()
    for ci in range(4):
        got = q.factorized_then_transform_column(column_index=ci, max_sigma_weight=2)
        ref = q.explicit_global_then_transform_column(column_index=ci, max_sigma_weight=2)
        cmp = q.compare_exact(got["coeffs"], ref["coeffs"])
        assert cmp["support_match"]
        assert cmp["max_coefficient_abs_error"] <= 1e-12
        assert cmp["energy_abs_error"] <= 1e-12
