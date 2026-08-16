import fds_v26_second_layer_separator as s

def _check_cap(cap):
    f=s.first_layer_factors(max_sigma_weight=cap);exp=s.explicit_all_column_marginals(max_sigma_weight=cap)
    for ci in range(4):
        p=s.factorized_column_marginal_packed(f,ci,return_dict=True);e=exp['columns'][ci]
        assert p['support']==e['support'];assert p['coeffs']==e['coeffs'];assert abs(p['energy']-e['energy'])<1e-12

def test_cap2_all_columns_exact():_check_cap(2)
def test_cap3_all_columns_exact():_check_cap(3)
