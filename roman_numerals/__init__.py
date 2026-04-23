import re

_TO_ROMAN = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100,  "C"), (90,  "XC"), (50,  "L"), (40,  "XL"),
    (10,   "X"), (9,   "IX"), (5,   "V"), (4,   "IV"),
    (1,    "I"),
]

_FROM_ROMAN = {"M": 1000, "D": 500, "C": 100, "L": 50, "X": 10, "V": 5, "I": 1}

_VALID_ROMAN = re.compile(
    r"^(?=.)M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
)


def to_roman(n: int) -> str:
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError(f"expected int, got {type(n).__name__}")
    if n < 1 or n > 3999:
        raise ValueError(f"integer must be 1..3999, got {n}")
    result = []
    for value, numeral in _TO_ROMAN:
        while n >= value:
            result.append(numeral)
            n -= value
    return "".join(result)


def from_roman(s: str) -> int:
    if not isinstance(s, str) or not s:
        raise ValueError("input must be a non-empty string")
    if not _VALID_ROMAN.match(s):
        raise ValueError(f"invalid Roman numeral: {s!r}")
    total = 0
    prev = 0
    for ch in reversed(s):
        val = _FROM_ROMAN.get(ch)
        if val is None:
            raise ValueError(f"unknown character: {ch!r}")
        if val < prev:
            total -= val
        else:
            total += val
        prev = val
    return total
