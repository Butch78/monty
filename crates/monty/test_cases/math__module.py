import math

# === Constants ===
assert math.pi == 3.141592653589793, 'math.pi value'
assert math.e == 2.718281828459045, 'math.e value'
assert math.tau == 6.283185307179586, 'math.tau value'
assert math.inf == float('inf'), 'math.inf is infinity'
assert math.nan != math.nan, 'math.nan is NaN (not equal to itself)'
assert math.isinf(math.inf), 'math.inf is recognized by isinf'
assert math.isnan(math.nan), 'math.nan is recognized by isnan'

# === math.floor() ===
assert math.floor(2.3) == 2, 'floor(2.3)'
assert math.floor(-2.3) == -3, 'floor(-2.3)'
assert math.floor(2.0) == 2, 'floor(2.0)'
assert math.floor(5) == 5, 'floor(int)'
assert math.floor(True) == 1, 'floor(True)'
assert math.floor(False) == 0, 'floor(False)'
assert math.floor(-0.5) == -1, 'floor(-0.5)'
assert math.floor(0.9) == 0, 'floor(0.9)'
assert math.floor(1e18) == 1000000000000000000, 'floor(1e18)'

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
assert math.ceil(False) == 0, 'ceil(False)'
assert math.ceil(0.1) == 1, 'ceil(0.1)'
assert math.ceil(-0.1) == 0, 'ceil(-0.1)'

threw = False
try:
    math.ceil(float('inf'))
except OverflowError:
    threw = True
assert threw, 'ceil(inf) raises OverflowError'

threw = False
try:
    math.ceil(float('nan'))
except ValueError:
    threw = True
assert threw, 'ceil(nan) raises ValueError'

threw = False
try:
    math.ceil('x')
except TypeError:
    threw = True
assert threw, 'ceil(str) raises TypeError'

# === math.trunc() ===
assert math.trunc(2.7) == 2, 'trunc(2.7)'
assert math.trunc(-2.7) == -2, 'trunc(-2.7)'
assert math.trunc(2.0) == 2, 'trunc(2.0)'
assert math.trunc(5) == 5, 'trunc(int)'
assert math.trunc(True) == 1, 'trunc(True)'
assert math.trunc(False) == 0, 'trunc(False)'

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

threw = False
try:
    math.trunc('x')
except TypeError:
    threw = True
assert threw, 'trunc(str) raises TypeError'

# === math.sqrt() ===
assert math.sqrt(4) == 2.0, 'sqrt(4)'
assert math.sqrt(2) == 1.4142135623730951, 'sqrt(2)'
assert math.sqrt(0) == 0.0, 'sqrt(0)'
assert math.sqrt(1) == 1.0, 'sqrt(1)'
assert math.sqrt(0.25) == 0.5, 'sqrt(0.25)'
assert isinstance(math.sqrt(4), float), 'sqrt returns float'
assert math.sqrt(True) == 1.0, 'sqrt(True)'
assert math.sqrt(False) == 0.0, 'sqrt(False)'

# sqrt with special float values
assert math.sqrt(float('inf')) == float('inf'), 'sqrt(inf) returns inf'
assert math.isnan(math.sqrt(float('nan'))), 'sqrt(nan) returns nan'

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
assert math.fabs(True) == 1.0, 'fabs(True)'
assert math.fabs(False) == 0.0, 'fabs(False)'

# fabs with special float values
assert math.fabs(float('inf')) == float('inf'), 'fabs(inf)'
assert math.fabs(float('-inf')) == float('inf'), 'fabs(-inf)'
assert math.isnan(math.fabs(float('nan'))), 'fabs(nan) returns nan'

threw = False
try:
    math.fabs('x')
except TypeError:
    threw = True
assert threw, 'fabs(str) raises TypeError'

# === math.isnan() ===
assert math.isnan(float('nan')) == True, 'isnan(nan)'
assert math.isnan(1.0) == False, 'isnan(1.0)'
assert math.isnan(0.0) == False, 'isnan(0.0)'
assert math.isnan(float('inf')) == False, 'isnan(inf)'
assert math.isnan(0) == False, 'isnan(int)'
assert math.isnan(True) == False, 'isnan(True)'
assert math.isnan(False) == False, 'isnan(False)'

threw = False
try:
    math.isnan('x')
except TypeError:
    threw = True
assert threw, 'isnan(str) raises TypeError'

# === math.isinf() ===
assert math.isinf(float('inf')) == True, 'isinf(inf)'
assert math.isinf(float('-inf')) == True, 'isinf(-inf)'
assert math.isinf(1.0) == False, 'isinf(1.0)'
assert math.isinf(float('nan')) == False, 'isinf(nan)'
assert math.isinf(0) == False, 'isinf(int)'
assert math.isinf(True) == False, 'isinf(True)'
assert math.isinf(False) == False, 'isinf(False)'

threw = False
try:
    math.isinf('x')
except TypeError:
    threw = True
assert threw, 'isinf(str) raises TypeError'

# === math.isfinite() ===
assert math.isfinite(1.0) == True, 'isfinite(1.0)'
assert math.isfinite(0) == True, 'isfinite(0)'
assert math.isfinite(float('inf')) == False, 'isfinite(inf)'
assert math.isfinite(float('-inf')) == False, 'isfinite(-inf)'
assert math.isfinite(float('nan')) == False, 'isfinite(nan)'
assert math.isfinite(True) == True, 'isfinite(True)'
assert math.isfinite(False) == True, 'isfinite(False)'

threw = False
try:
    math.isfinite('x')
except TypeError:
    threw = True
assert threw, 'isfinite(str) raises TypeError'

# === math.log() ===
assert math.log(1) == 0.0, 'log(1)'
assert math.log(math.e) == 1.0, 'log(e)'
assert math.log(100, 10) == 2.0, 'log(100, 10)'
assert math.log(1, 10) == 0.0, 'log(1, 10)'
assert math.log(True) == 0.0, 'log(True)'

# log with special float values
assert math.log(float('inf')) == float('inf'), 'log(inf) returns inf'
assert math.isnan(math.log(float('nan'))), 'log(nan) returns nan'

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

# log with base=1 raises ZeroDivisionError (log(1)=0 causes division by zero)
threw = False
try:
    math.log(10, 1)
except ZeroDivisionError:
    threw = True
assert threw, 'log(10, 1) raises ZeroDivisionError'

# log with invalid base values
threw = False
try:
    math.log(10, 0)
except ValueError:
    threw = True
assert threw, 'log(10, 0) raises ValueError'

threw = False
try:
    math.log(10, -1)
except ValueError:
    threw = True
assert threw, 'log(10, -1) raises ValueError'

# === math.log2() ===
assert math.log2(1) == 0.0, 'log2(1)'
assert math.log2(8) == 3.0, 'log2(8)'
assert math.log2(1024) == 10.0, 'log2(1024)'
assert math.log2(True) == 0.0, 'log2(True)'

# log2 with special float values
assert math.log2(float('inf')) == float('inf'), 'log2(inf) returns inf'
assert math.isnan(math.log2(float('nan'))), 'log2(nan) returns nan'

threw = False
try:
    math.log2(0)
except ValueError:
    threw = True
assert threw, 'log2(0) raises ValueError'

threw = False
try:
    math.log2(-1)
except ValueError:
    threw = True
assert threw, 'log2(-1) raises ValueError'

threw = False
try:
    math.log2('x')
except TypeError:
    threw = True
assert threw, 'log2(str) raises TypeError'

# === math.log10() ===
assert math.log10(1) == 0.0, 'log10(1)'
assert math.log10(1000) == 3.0, 'log10(1000)'
assert math.log10(100) == 2.0, 'log10(100)'
assert math.log10(True) == 0.0, 'log10(True)'

# log10 with special float values
assert math.log10(float('inf')) == float('inf'), 'log10(inf) returns inf'
assert math.isnan(math.log10(float('nan'))), 'log10(nan) returns nan'

threw = False
try:
    math.log10(0)
except ValueError:
    threw = True
assert threw, 'log10(0) raises ValueError'

threw = False
try:
    math.log10(-1)
except ValueError:
    threw = True
assert threw, 'log10(-1) raises ValueError'

threw = False
try:
    math.log10('x')
except TypeError:
    threw = True
assert threw, 'log10(str) raises TypeError'

# === math.factorial() ===
assert math.factorial(0) == 1, 'factorial(0)'
assert math.factorial(1) == 1, 'factorial(1)'
assert math.factorial(5) == 120, 'factorial(5)'
assert math.factorial(10) == 3628800, 'factorial(10)'
assert math.factorial(20) == 2432902008176640000, 'factorial(20)'
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

threw = False
try:
    math.factorial('x')
except TypeError:
    threw = True
assert threw, 'factorial(str) raises TypeError'

# === math.gcd() ===
assert math.gcd(12, 8) == 4, 'gcd(12, 8)'
assert math.gcd(0, 5) == 5, 'gcd(0, 5)'
assert math.gcd(5, 0) == 5, 'gcd(5, 0)'
assert math.gcd(0, 0) == 0, 'gcd(0, 0)'
assert math.gcd(-12, 8) == 4, 'gcd(-12, 8)'
assert math.gcd(12, -8) == 4, 'gcd(12, -8)'
assert math.gcd(-12, -8) == 4, 'gcd(-12, -8)'
assert math.gcd(7, 13) == 1, 'gcd(7, 13) coprime'
assert math.gcd(True, 2) == 1, 'gcd(True, 2)'
assert math.gcd(False, 5) == 5, 'gcd(False, 5)'

threw = False
try:
    math.gcd(1.5, 2)
except TypeError:
    threw = True
assert threw, 'gcd(float, int) raises TypeError'

threw = False
try:
    math.gcd(2, 1.5)
except TypeError:
    threw = True
assert threw, 'gcd(int, float) raises TypeError'

# === math.lcm() ===
assert math.lcm(4, 6) == 12, 'lcm(4, 6)'
assert math.lcm(0, 5) == 0, 'lcm(0, 5)'
assert math.lcm(5, 0) == 0, 'lcm(5, 0)'
assert math.lcm(0, 0) == 0, 'lcm(0, 0)'
assert math.lcm(3, 7) == 21, 'lcm(3, 7) coprime'
assert math.lcm(6, 6) == 6, 'lcm(6, 6) equal'
assert math.lcm(-4, 6) == 12, 'lcm(-4, 6) negative'
assert math.lcm(-4, -6) == 12, 'lcm(-4, -6) both negative'
assert math.lcm(True, 2) == 2, 'lcm(True, 2)'
assert math.lcm(False, 5) == 0, 'lcm(False, 5)'

threw = False
try:
    math.lcm(1.5, 2)
except TypeError:
    threw = True
assert threw, 'lcm(float, int) raises TypeError'

threw = False
try:
    math.lcm(2, 1.5)
except TypeError:
    threw = True
assert threw, 'lcm(int, float) raises TypeError'

# === math.copysign() ===
assert math.copysign(1.0, -0.0) == -1.0, 'copysign(1.0, -0.0)'
assert math.copysign(-1.0, 1.0) == 1.0, 'copysign(-1.0, 1.0)'
assert math.copysign(5, -3) == -5.0, 'copysign(5, -3)'
assert isinstance(math.copysign(5, -3), float), 'copysign returns float'

# copysign with special float values
assert math.copysign(float('inf'), -1.0) == float('-inf'), 'copysign(inf, -1.0)'
assert math.copysign(0.0, -1.0) == -0.0, 'copysign(0.0, -1.0)'
assert math.isnan(math.copysign(float('nan'), -1.0)), 'copysign(nan, -1.0) is nan'

threw = False
try:
    math.copysign('x', 1)
except TypeError:
    threw = True
assert threw, 'copysign(str, int) raises TypeError'

# === math.isclose() ===
assert math.isclose(1.0, 1.0) == True, 'isclose equal'
assert math.isclose(1.0, 1.0000000001) == True, 'isclose very close'
assert math.isclose(1.0, 1.1) == False, 'isclose not close'
assert math.isclose(0.0, 0.0) == True, 'isclose zeros'
assert math.isclose(-0.0, 0.0) == True, 'isclose neg zero and zero'

# isclose with special float values
assert math.isclose(float('inf'), float('inf')) == True, 'isclose(inf, inf)'
assert math.isclose(float('inf'), 1e308) == False, 'isclose(inf, large) is False'
assert math.isclose(float('nan'), float('nan')) == False, 'isclose(nan, nan) is False'

# isclose with small numbers near zero
assert math.isclose(1e-15, 0.0) == False, 'isclose(1e-15, 0.0) is False with default abs_tol'
assert math.isclose(0.0, 1e-15) == False, 'isclose(0.0, 1e-15) is False with default abs_tol'

threw = False
try:
    math.isclose('x', 1)
except TypeError:
    threw = True
assert threw, 'isclose(str, int) raises TypeError'

# === math.degrees() ===
assert math.degrees(0) == 0.0, 'degrees(0)'
assert math.degrees(math.pi) == 180.0, 'degrees(pi)'
assert math.degrees(math.tau) == 360.0, 'degrees(tau)'
assert math.degrees(True) == math.degrees(1), 'degrees(True)'

# degrees with special float values
assert math.degrees(float('inf')) == float('inf'), 'degrees(inf)'
assert math.isnan(math.degrees(float('nan'))), 'degrees(nan) is nan'

threw = False
try:
    math.degrees('x')
except TypeError:
    threw = True
assert threw, 'degrees(str) raises TypeError'

# === math.radians() ===
assert math.radians(0) == 0.0, 'radians(0)'
assert math.radians(180) == math.pi, 'radians(180)'
assert math.radians(360) == math.tau, 'radians(360)'
assert math.radians(True) == math.radians(1), 'radians(True)'

# radians with special float values
assert math.radians(float('inf')) == float('inf'), 'radians(inf)'
assert math.isnan(math.radians(float('nan'))), 'radians(nan) is nan'

threw = False
try:
    math.radians('x')
except TypeError:
    threw = True
assert threw, 'radians(str) raises TypeError'
