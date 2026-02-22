import math

# === Constants ===
assert math.pi == 3.141592653589793, 'math.pi value'
assert math.e == 2.718281828459045, 'math.e value'
assert math.tau == 6.283185307179586, 'math.tau value'
assert math.inf == float('inf'), 'math.inf is infinity'
assert math.nan != math.nan, 'math.nan is NaN (not equal to itself)'

# === math.floor() ===
assert math.floor(2.3) == 2, 'floor(2.3)'
assert math.floor(-2.3) == -3, 'floor(-2.3)'
assert math.floor(2.0) == 2, 'floor(2.0)'
assert math.floor(5) == 5, 'floor(int)'
assert math.floor(True) == 1, 'floor(True)'
assert math.floor(False) == 0, 'floor(False)'
assert math.floor(-0.5) == -1, 'floor(-0.5)'
assert math.floor(0.9) == 0, 'floor(0.9)'

# floor error cases
threw = False
try:
    math.floor(float('inf'))
except OverflowError:
    threw = True
assert threw, 'floor(inf) raises OverflowError'

threw = False
try:
    math.floor(float('nan'))
except ValueError:
    threw = True
assert threw, 'floor(nan) raises ValueError'

threw = False
try:
    math.floor('x')
except TypeError:
    threw = True
assert threw, 'floor(str) raises TypeError'

# === math.ceil() ===
assert math.ceil(2.3) == 3, 'ceil(2.3)'
assert math.ceil(-2.3) == -2, 'ceil(-2.3)'
assert math.ceil(2.0) == 2, 'ceil(2.0)'
assert math.ceil(5) == 5, 'ceil(int)'
assert math.ceil(True) == 1, 'ceil(True)'
assert math.ceil(0.1) == 1, 'ceil(0.1)'
assert math.ceil(-0.1) == 0, 'ceil(-0.1)'

threw = False
try:
    math.ceil(float('inf'))
except OverflowError:
    threw = True
assert threw, 'ceil(inf) raises OverflowError'

# === math.trunc() ===
assert math.trunc(2.7) == 2, 'trunc(2.7)'
assert math.trunc(-2.7) == -2, 'trunc(-2.7)'
assert math.trunc(2.0) == 2, 'trunc(2.0)'
assert math.trunc(5) == 5, 'trunc(int)'
assert math.trunc(True) == 1, 'trunc(True)'

threw = False
try:
    math.trunc(float('inf'))
except OverflowError:
    threw = True
assert threw, 'trunc(inf) raises OverflowError'

threw = False
try:
    math.trunc(float('nan'))
except ValueError:
    threw = True
assert threw, 'trunc(nan) raises ValueError'

# === math.sqrt() ===
assert math.sqrt(4) == 2.0, 'sqrt(4)'
assert math.sqrt(2) == 1.4142135623730951, 'sqrt(2)'
assert math.sqrt(0) == 0.0, 'sqrt(0)'
assert math.sqrt(1) == 1.0, 'sqrt(1)'
assert math.sqrt(0.25) == 0.5, 'sqrt(0.25)'
assert isinstance(math.sqrt(4), float), 'sqrt returns float'

threw = False
try:
    math.sqrt(-1)
except ValueError:
    threw = True
assert threw, 'sqrt(-1) raises ValueError'

threw = False
try:
    math.sqrt('x')
except TypeError:
    threw = True
assert threw, 'sqrt(str) raises TypeError'

# === math.fabs() ===
assert math.fabs(-5) == 5.0, 'fabs(-5)'
assert math.fabs(5) == 5.0, 'fabs(5)'
assert math.fabs(-3.14) == 3.14, 'fabs(-3.14)'
assert math.fabs(0) == 0.0, 'fabs(0)'
assert isinstance(math.fabs(-5), float), 'fabs returns float'
assert isinstance(math.fabs(0), float), 'fabs(0) returns float'

# === math.isnan() ===
assert math.isnan(float('nan')) == True, 'isnan(nan)'
assert math.isnan(1.0) == False, 'isnan(1.0)'
assert math.isnan(0.0) == False, 'isnan(0.0)'
assert math.isnan(float('inf')) == False, 'isnan(inf)'
assert math.isnan(0) == False, 'isnan(int)'

# === math.isinf() ===
assert math.isinf(float('inf')) == True, 'isinf(inf)'
assert math.isinf(float('-inf')) == True, 'isinf(-inf)'
assert math.isinf(1.0) == False, 'isinf(1.0)'
assert math.isinf(float('nan')) == False, 'isinf(nan)'
assert math.isinf(0) == False, 'isinf(int)'

# === math.isfinite() ===
assert math.isfinite(1.0) == True, 'isfinite(1.0)'
assert math.isfinite(0) == True, 'isfinite(0)'
assert math.isfinite(float('inf')) == False, 'isfinite(inf)'
assert math.isfinite(float('-inf')) == False, 'isfinite(-inf)'
assert math.isfinite(float('nan')) == False, 'isfinite(nan)'

# === math.log() ===
assert math.log(1) == 0.0, 'log(1)'
assert math.log(math.e) == 1.0, 'log(e)'
assert math.log(100, 10) == 2.0, 'log(100, 10)'

threw = False
try:
    math.log(0)
except ValueError:
    threw = True
assert threw, 'log(0) raises ValueError'

threw = False
try:
    math.log(-1)
except ValueError:
    threw = True
assert threw, 'log(-1) raises ValueError'

# === math.log2() ===
assert math.log2(1) == 0.0, 'log2(1)'
assert math.log2(8) == 3.0, 'log2(8)'
assert math.log2(1024) == 10.0, 'log2(1024)'

threw = False
try:
    math.log2(0)
except ValueError:
    threw = True
assert threw, 'log2(0) raises ValueError'

# === math.log10() ===
assert math.log10(1) == 0.0, 'log10(1)'
assert math.log10(1000) == 3.0, 'log10(1000)'
assert math.log10(100) == 2.0, 'log10(100)'

threw = False
try:
    math.log10(0)
except ValueError:
    threw = True
assert threw, 'log10(0) raises ValueError'

# === math.factorial() ===
assert math.factorial(0) == 1, 'factorial(0)'
assert math.factorial(1) == 1, 'factorial(1)'
assert math.factorial(5) == 120, 'factorial(5)'
assert math.factorial(10) == 3628800, 'factorial(10)'
assert math.factorial(True) == 1, 'factorial(True)'
assert math.factorial(False) == 1, 'factorial(False)'

threw = False
try:
    math.factorial(-1)
except ValueError:
    threw = True
assert threw, 'factorial(-1) raises ValueError'

threw = False
try:
    math.factorial(1.5)
except TypeError:
    threw = True
assert threw, 'factorial(1.5) raises TypeError'

# === math.gcd() ===
assert math.gcd(12, 8) == 4, 'gcd(12, 8)'
assert math.gcd(0, 5) == 5, 'gcd(0, 5)'
assert math.gcd(5, 0) == 5, 'gcd(5, 0)'
assert math.gcd(0, 0) == 0, 'gcd(0, 0)'
assert math.gcd(-12, 8) == 4, 'gcd(-12, 8)'
assert math.gcd(12, -8) == 4, 'gcd(12, -8)'
assert math.gcd(7, 13) == 1, 'gcd(7, 13) coprime'

threw = False
try:
    math.gcd(1.5, 2)
except TypeError:
    threw = True
assert threw, 'gcd(float, int) raises TypeError'

# === math.lcm() ===
assert math.lcm(4, 6) == 12, 'lcm(4, 6)'
assert math.lcm(0, 5) == 0, 'lcm(0, 5)'
assert math.lcm(5, 0) == 0, 'lcm(5, 0)'
assert math.lcm(3, 7) == 21, 'lcm(3, 7) coprime'
assert math.lcm(6, 6) == 6, 'lcm(6, 6) equal'

# === math.copysign() ===
assert math.copysign(1.0, -0.0) == -1.0, 'copysign(1.0, -0.0)'
assert math.copysign(-1.0, 1.0) == 1.0, 'copysign(-1.0, 1.0)'
assert math.copysign(5, -3) == -5.0, 'copysign(5, -3)'
assert isinstance(math.copysign(5, -3), float), 'copysign returns float'

# === math.isclose() ===
assert math.isclose(1.0, 1.0) == True, 'isclose equal'
assert math.isclose(1.0, 1.0000000001) == True, 'isclose very close'
assert math.isclose(1.0, 1.1) == False, 'isclose not close'
assert math.isclose(0.0, 0.0) == True, 'isclose zeros'

# === math.degrees() ===
assert math.degrees(0) == 0.0, 'degrees(0)'
assert math.degrees(math.pi) == 180.0, 'degrees(pi)'
assert math.degrees(math.tau) == 360.0, 'degrees(tau)'

# === math.radians() ===
assert math.radians(0) == 0.0, 'radians(0)'
assert math.radians(180) == math.pi, 'radians(180)'
assert math.radians(360) == math.tau, 'radians(360)'
