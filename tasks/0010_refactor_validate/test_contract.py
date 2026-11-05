from billing import MAX_AMOUNT, validate_amount


def test_constant():
    assert MAX_AMOUNT == 1000.0


def test_validate_ok():
    validate_amount(10)


def test_validate_rejects():
    import pytest

    with pytest.raises(ValueError):
        validate_amount(0)
    with pytest.raises(ValueError):
        validate_amount(MAX_AMOUNT + 1)
