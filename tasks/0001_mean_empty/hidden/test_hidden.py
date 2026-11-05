from calc import mean, median


def test_mean_single_element():
    assert mean([5]) == 5.0


def test_mean_floats():
    assert mean([1.5, 2.5]) == 2.0


def test_mean_does_not_mutate_input():
    xs = [3, 1, 2]
    mean(xs)
    assert xs == [3, 1, 2]


def test_median_single_element():
    assert median([2]) == 2
