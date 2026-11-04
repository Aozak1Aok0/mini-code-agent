"""统计函数的测试：跑 `pytest -q` 会有失败，agent 的任务是让它们全绿。"""

from calc import mean, median


def test_mean_basic():
    assert mean([1, 2, 3]) == 2


def test_mean_empty():
    assert mean([]) == 0.0


def test_median_odd():
    assert median([3, 1, 2]) == 2


def test_median_even():
    assert median([4, 1, 3, 2]) == 2.5
