def clean_rut(rut: str) -> str:
    return ''.join(ch for ch in rut if ch.isalnum()).upper()

def valid_rut(rut: str) -> bool:
    r = clean_rut(r)
    if len(r) < 2: return False
    body, dv = r[:-1], r[-1]
    try:
        reversed_digits = map(int, reversed(body))
    except ValueError:
        return False
    factors = [2,3,4,5,6,7]
    s = 0
    factor_index = 0
    for d in reversed_digits:
        s += d * factors[factor_index]
        factor_index = (factor_index + 1) % len(factors)
    mod = 11 - (s % 11)
    expected = 'K' if mod == 10 else '0' if mod == 11 else str(mod)
    return expected == dv
