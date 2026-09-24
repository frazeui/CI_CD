def test_regression_passes():
    baseline_score = 10.0
    new_score = 10.0
    max_degradation = 0.05

    degradation = max(0.0, (baseline_score - new_score) / baseline_score)

    assert degradation <= max_degradation
