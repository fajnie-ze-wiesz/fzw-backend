import pytest

from fzw.util.common import smart_bool, smart_bool_or_none


@pytest.mark.parametrize(
    "value,expected_output",
    (
        (False, False),
        (True, True),
        (0, False),
        (1, True),
        (1.0, True),
        (0.1, True),
        ("", False),
        ("none", False),
        ("nil", False),
        ("0", False),
        ("false", False),
        ("False", False),
        ("f", False),
        ("1", True),
        ("true", True),
        ("True", True),
        ("t", True),
    ),
)
def test_smart_bool(value, expected_output):
    assert smart_bool(value) == expected_output


@pytest.mark.parametrize(
    "value,expected_output",
    (
        (False, False),
        (True, True),
        (0, False),
        (1, True),
        (1.0, True),
        (0.1, True),
        ("", None),
        ("none", None),
        ("nil", None),
        ("0", False),
        ("false", False),
        ("False", False),
        ("f", False),
        ("1", True),
        ("true", True),
        ("True", True),
        ("t", True),
    ),
)
def test_smart_bool_or_none(value, expected_output):
    assert smart_bool_or_none(value) == expected_output
