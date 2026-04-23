import pytest
from roman_numerals import to_roman, from_roman

known = [
    (1,    "I"),
    (4,    "IV"),
    (9,    "IX"),
    (40,   "XL"),
    (90,   "XC"),
    (400,  "CD"),
    (900,  "CM"),
    (1994, "MCMXCIV"),
    (3999, "MMMCMXCIX"),
]


@pytest.mark.parametrize("n, s", known)
def test_to_roman_known(n, s):
    assert to_roman(n) == s


@pytest.mark.parametrize("n, s", known)
def test_from_roman_known(n, s):
    assert from_roman(s) == n


@pytest.mark.parametrize("n, s", known)
def test_round_trip(n, s):
    assert to_roman(from_roman(s)) == s
    assert from_roman(to_roman(n)) == n


@pytest.mark.parametrize("bad", [0, 4000, -1])
def test_to_roman_out_of_range(bad):
    with pytest.raises(ValueError):
        to_roman(bad)


def test_to_roman_non_int():
    with pytest.raises(ValueError):
        to_roman(3.5)
    with pytest.raises(ValueError):
        to_roman("X")


@pytest.mark.parametrize("bad", ["IIII", "VV", "IC", "", "iv", "ABC"])
def test_from_roman_invalid(bad):
    with pytest.raises(ValueError):
        from_roman(bad)


def test_to_roman_bool():
    with pytest.raises(ValueError):
        to_roman(True)
    with pytest.raises(ValueError):
        to_roman(False)
