import pytest

from validador_bandeiras import detect_brand, is_luhn_valid


@pytest.mark.parametrize(
    "number,expected",
    [
        ("4111111111111111", "Visa"),
        ("5555555555554444", "MasterCard"),
        ("378282246310005", "American Express"),
        ("6011111111111117", "Discover"),
        ("3530111333300000", "JCB"),
        ("30569309025904", "Diners Club"),
        ("1234567890123456", "Unknown"),
    ],
)
def test_detect_brand(number, expected):
    assert detect_brand(number) == expected


def test_luhn_validity():
    assert is_luhn_valid("4111111111111111")
    assert is_luhn_valid("378282246310005")
    assert not is_luhn_valid("411111111111112")
