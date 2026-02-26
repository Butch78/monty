# === Three-argument pow (modular exponentiation) edge cases ===
# Modular pow with modulus = 1 always returns 0
assert pow(5, 3, 1) == 0, 'pow mod 1 always 0'
assert pow(100, 100, 1) == 0, 'pow large values mod 1'
assert pow(0, 0, 1) == 0, 'pow 0^0 mod 1'

# Modular pow with negative modulus
assert pow(2, 3, -5) == -2, 'pow with negative modulus'
assert pow(3, 2, -4) == -3, 'pow 3^2 mod -4'

# Modular pow with bool arguments
assert pow(True, True, True) == 0, 'pow bools modular'
assert pow(True, 2, 3) == 1, 'pow True^2 mod 3'
assert pow(2, True, 3) == 2, 'pow 2^True mod 3'

# Three-arg pow type errors
threw = False
try:
    pow(2, 3, 0)
except ValueError:
    threw = True
assert threw, 'pow mod 0 raises ValueError'

# Note: pow(2, -1, 5) computes modular inverse on CPython (returns 3),
# but Monty doesn't support modular inverse yet — skipping this case.

threw = False
try:
    pow(2.0, 3, 5)
except TypeError:
    threw = True
assert threw, 'pow float base with mod raises TypeError'

threw = False
try:
    pow(2, 3.0, 5)
except TypeError:
    threw = True
assert threw, 'pow float exp with mod raises TypeError'

threw = False
try:
    pow(2, 3, 5.0)
except TypeError:
    threw = True
assert threw, 'pow float mod raises TypeError'

# === pow() with mixed int/float ===
assert pow(2, 3.0) == 8.0, 'pow int base float exp'
assert pow(2.0, 3) == 8.0, 'pow float base int exp'
assert pow(0.5, 2) == 0.25, 'pow fractional base'

# pow with large int exponent (still fits in i64)
assert pow(2, 62) == 4611686018427387904, 'pow 2^62'
assert pow(-1, 100) == 1, 'pow -1^even'
assert pow(-1, 101) == -1, 'pow -1^odd'

# pow with 0 base
assert pow(0, 0) == 1, 'pow 0^0 is 1'
assert pow(0, 5) == 0, 'pow 0^positive'

# pow with float edge cases
assert pow(0, 0.0) == 1.0, 'pow int 0 float 0.0'

threw = False
try:
    pow(0, -2)
except ZeroDivisionError:
    threw = True
assert threw, 'pow 0^negative raises ZeroDivisionError'

threw = False
try:
    pow(0.0, -2.0)
except ZeroDivisionError:
    threw = True
assert threw, 'pow 0.0^negative float raises ZeroDivisionError'

threw = False
try:
    pow(0, -2.0)
except ZeroDivisionError:
    threw = True
assert threw, 'pow int 0^negative float raises ZeroDivisionError'

threw = False
try:
    pow(0.0, -2)
except ZeroDivisionError:
    threw = True
assert threw, 'pow float 0.0^negative int raises ZeroDivisionError'

# pow type errors with unsupported types
threw = False
try:
    pow('a', 2)
except TypeError:
    threw = True
assert threw, 'pow string base raises TypeError'

threw = False
try:
    pow(2, 'a')
except TypeError:
    threw = True
assert threw, 'pow string exp raises TypeError'

threw = False
try:
    pow(2, [1])
except TypeError:
    threw = True
assert threw, 'pow list exp raises TypeError'

# pow arg count errors
threw = False
try:
    pow(2)
except TypeError:
    threw = True
assert threw, 'pow with 1 arg raises TypeError'

threw = False
try:
    pow(2, 3, 5, 7)
except TypeError:
    threw = True
assert threw, 'pow with 4 args raises TypeError'
