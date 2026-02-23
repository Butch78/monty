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

# === math.sin() ===
assert math.sin(0) == 0.0, 'sin(0)'
assert math.sin(math.pi / 2) == 1.0, 'sin(pi/2)'
assert math.sin(math.pi) < 1e-15, 'sin(pi) near zero'
assert math.isnan(math.sin(float('nan'))), 'sin(nan) is nan'

threw = False
try:
    math.sin(float('inf'))
except ValueError:
    threw = True
assert threw, 'sin(inf) raises ValueError'

# === math.cos() ===
assert math.cos(0) == 1.0, 'cos(0)'
assert abs(math.cos(math.pi / 2)) < 1e-15, 'cos(pi/2) near zero'
assert math.cos(math.pi) == -1.0, 'cos(pi)'
assert math.isnan(math.cos(float('nan'))), 'cos(nan) is nan'

threw = False
try:
    math.cos(float('inf'))
except ValueError:
    threw = True
assert threw, 'cos(inf) raises ValueError'

# === math.tan() ===
assert math.tan(0) == 0.0, 'tan(0)'
assert abs(math.tan(math.pi / 4) - 1.0) < 1e-15, 'tan(pi/4) near 1'
assert math.isnan(math.tan(float('nan'))), 'tan(nan) is nan'

threw = False
try:
    math.tan(float('inf'))
except ValueError:
    threw = True
assert threw, 'tan(inf) raises ValueError'

# === math.asin() ===
assert math.asin(0) == 0.0, 'asin(0)'
assert math.asin(1) == math.pi / 2, 'asin(1)'
assert math.asin(-1) == -math.pi / 2, 'asin(-1)'

threw = False
try:
    math.asin(2)
except ValueError:
    threw = True
assert threw, 'asin(2) raises ValueError'

threw = False
try:
    math.asin(-2)
except ValueError:
    threw = True
assert threw, 'asin(-2) raises ValueError'

# === math.acos() ===
assert math.acos(1) == 0.0, 'acos(1)'
assert math.acos(0) == math.pi / 2, 'acos(0)'
assert math.acos(-1) == math.pi, 'acos(-1)'

threw = False
try:
    math.acos(2)
except ValueError:
    threw = True
assert threw, 'acos(2) raises ValueError'

# === math.atan() ===
assert math.atan(0) == 0.0, 'atan(0)'
assert math.atan(1) == math.pi / 4, 'atan(1)'
assert math.atan(float('inf')) == math.pi / 2, 'atan(inf)'
assert math.atan(float('-inf')) == -math.pi / 2, 'atan(-inf)'

# === math.atan2() ===
assert math.atan2(0, 1) == 0.0, 'atan2(0, 1)'
assert math.atan2(1, 0) == math.pi / 2, 'atan2(1, 0)'
assert math.atan2(0, -1) == math.pi, 'atan2(0, -1)'
assert math.atan2(0, 0) == 0.0, 'atan2(0, 0)'

# === math.sinh() ===
assert math.sinh(0) == 0.0, 'sinh(0)'
assert math.isclose(math.sinh(1), 1.1752011936438014), 'sinh(1)'
assert math.sinh(float('inf')) == float('inf'), 'sinh(inf)'

threw = False
try:
    math.sinh(1000)
except OverflowError:
    threw = True
assert threw, 'sinh(1000) raises OverflowError'

# === math.cosh() ===
assert math.cosh(0) == 1.0, 'cosh(0)'
assert math.isclose(math.cosh(1), 1.5430806348152437), 'cosh(1)'
assert math.cosh(float('inf')) == float('inf'), 'cosh(inf)'

# === math.tanh() ===
assert math.tanh(0) == 0.0, 'tanh(0)'
assert math.tanh(float('inf')) == 1.0, 'tanh(inf)'
assert math.tanh(float('-inf')) == -1.0, 'tanh(-inf)'
assert abs(math.tanh(1) - 0.7615941559557649) < 1e-10, 'tanh(1)'

# === math.asinh() ===
assert math.asinh(0) == 0.0, 'asinh(0)'
assert math.isclose(math.asinh(1), 0.881373587019543), 'asinh(1)'

# === math.acosh() ===
assert math.acosh(1) == 0.0, 'acosh(1)'
assert math.isclose(math.acosh(2), 1.3169578969248166), 'acosh(2)'

threw = False
try:
    math.acosh(0.5)
except ValueError:
    threw = True
assert threw, 'acosh(0.5) raises ValueError'

# === math.atanh() ===
assert math.atanh(0) == 0.0, 'atanh(0)'
assert math.isclose(math.atanh(0.5), 0.5493061443340549), 'atanh(0.5)'

threw = False
try:
    math.atanh(1)
except ValueError:
    threw = True
assert threw, 'atanh(1) raises ValueError'

threw = False
try:
    math.atanh(-1)
except ValueError:
    threw = True
assert threw, 'atanh(-1) raises ValueError'

# === math.exp() ===
assert math.exp(0) == 1.0, 'exp(0)'
assert math.exp(1) == math.e, 'exp(1)'
assert math.exp(float('-inf')) == 0.0, 'exp(-inf)'
assert math.exp(float('inf')) == float('inf'), 'exp(inf)'

threw = False
try:
    math.exp(1000)
except OverflowError:
    threw = True
assert threw, 'exp(1000) raises OverflowError'

# === math.exp2() ===
assert math.exp2(0) == 1.0, 'exp2(0)'
assert math.exp2(3) == 8.0, 'exp2(3)'
assert math.exp2(10) == 1024.0, 'exp2(10)'

# === math.expm1() ===
assert math.expm1(0) == 0.0, 'expm1(0)'
assert math.isclose(math.expm1(1), math.e - 1), 'expm1(1)'
# expm1 is more precise than exp(x)-1 for small x
assert math.expm1(1e-15) != 0.0, 'expm1(1e-15) is precise'

# === math.log1p() ===
assert math.log1p(0) == 0.0, 'log1p(0)'
assert math.isclose(math.log1p(math.e - 1), 1.0), 'log1p(e-1)'

threw = False
try:
    math.log1p(-1)
except ValueError:
    threw = True
assert threw, 'log1p(-1) raises ValueError'

threw = False
try:
    math.log1p(-2)
except ValueError:
    threw = True
assert threw, 'log1p(-2) raises ValueError'

# === math.pow() ===
assert math.pow(2, 3) == 8.0, 'pow(2, 3)'
assert math.pow(2.0, 0.5) == math.sqrt(2), 'pow(2, 0.5)'
assert math.pow(0, 0) == 1.0, 'pow(0, 0)'
assert isinstance(math.pow(2, 3), float), 'pow returns float'

# === math.isqrt() ===
assert math.isqrt(0) == 0, 'isqrt(0)'
assert math.isqrt(1) == 1, 'isqrt(1)'
assert math.isqrt(4) == 2, 'isqrt(4)'
assert math.isqrt(10) == 3, 'isqrt(10)'
assert math.isqrt(99) == 9, 'isqrt(99)'
assert math.isqrt(100) == 10, 'isqrt(100)'

threw = False
try:
    math.isqrt(-1)
except ValueError:
    threw = True
assert threw, 'isqrt(-1) raises ValueError'

# === math.cbrt() ===
assert math.cbrt(0) == 0.0, 'cbrt(0)'
assert math.cbrt(-8) == -2.0, 'cbrt(-8)'
assert math.cbrt(1) == 1.0, 'cbrt(1)'

# === math.fmod() ===
assert math.fmod(10, 3) == 1.0, 'fmod(10, 3)'
assert math.fmod(-10, 3) == -1.0, 'fmod(-10, 3)'
assert math.fmod(10.5, 3) == 1.5, 'fmod(10.5, 3)'

threw = False
try:
    math.fmod(10, 0)
except ValueError:
    threw = True
assert threw, 'fmod(10, 0) raises ValueError'

# === math.remainder() ===
assert math.remainder(10, 3) == 1.0, 'remainder(10, 3)'
assert math.remainder(10, 4) == 2.0, 'remainder(10, 4)'

threw = False
try:
    math.remainder(10, 0)
except ValueError:
    threw = True
assert threw, 'remainder(10, 0) raises ValueError'

# === math.modf() ===
r = math.modf(3.5)
assert r == (0.5, 3.0), 'modf(3.5)'
r = math.modf(-3.5)
assert r == (-0.5, -3.0), 'modf(-3.5)'
r = math.modf(0.0)
assert r == (0.0, 0.0), 'modf(0.0)'

# === math.frexp() ===
r = math.frexp(0.0)
assert r == (0.0, 0), 'frexp(0.0)'
r = math.frexp(3.5)
assert r == (0.875, 2), 'frexp(3.5)'

# === math.ldexp() ===
assert math.ldexp(0.875, 2) == 3.5, 'ldexp(0.875, 2)'
assert math.ldexp(1.0, 0) == 1.0, 'ldexp(1.0, 0)'
assert math.ldexp(0.5, 1) == 1.0, 'ldexp(0.5, 1)'

# === math.comb() ===
assert math.comb(5, 2) == 10, 'comb(5, 2)'
assert math.comb(10, 0) == 1, 'comb(10, 0)'
assert math.comb(10, 10) == 1, 'comb(10, 10)'
assert math.comb(0, 0) == 1, 'comb(0, 0)'
assert math.comb(5, 6) == 0, 'comb(5, 6) k > n'

threw = False
try:
    math.comb(5, -1)
except ValueError:
    threw = True
assert threw, 'comb(5, -1) raises ValueError'

# === math.perm() ===
assert math.perm(5, 2) == 20, 'perm(5, 2)'
assert math.perm(5, 0) == 1, 'perm(5, 0)'
assert math.perm(5, 5) == 120, 'perm(5, 5)'
assert math.perm(5, 6) == 0, 'perm(5, 6) k > n'

threw = False
try:
    math.perm(5, -1)
except ValueError:
    threw = True
assert threw, 'perm(5, -1) raises ValueError'

# === math.gamma() ===
assert math.gamma(1) == 1.0, 'gamma(1)'
assert math.gamma(5) == 24.0, 'gamma(5)'
assert math.isclose(math.gamma(0.5), math.sqrt(math.pi)), 'gamma(0.5)'

threw = False
try:
    math.gamma(0)
except ValueError:
    threw = True
assert threw, 'gamma(0) raises ValueError'

threw = False
try:
    math.gamma(-1)
except ValueError:
    threw = True
assert threw, 'gamma(-1) raises ValueError'

# === math.lgamma() ===
assert math.lgamma(1) == 0.0, 'lgamma(1)'
assert math.isclose(math.lgamma(5), math.log(24)), 'lgamma(5)'

threw = False
try:
    math.lgamma(0)
except ValueError:
    threw = True
assert threw, 'lgamma(0) raises ValueError'

# === math.erf() ===
assert math.erf(0) == 0.0, 'erf(0)'
assert abs(math.erf(1) - 0.8427007929497149) < 1e-6, 'erf(1)'
assert math.erf(float('inf')) == 1.0, 'erf(inf)'
assert math.erf(float('-inf')) == -1.0, 'erf(-inf)'

# === math.erfc() ===
assert math.erfc(0) == 1.0, 'erfc(0)'
assert math.isclose(math.erfc(1), 1.0 - math.erf(1)), 'erfc(1)'

# === math.nextafter() ===
r = math.nextafter(1.0, 2.0)
assert r > 1.0, 'nextafter(1.0, 2.0) > 1.0'
assert r == 1.0000000000000002, 'nextafter(1.0, 2.0) value'
r = math.nextafter(1.0, 0.0)
assert r < 1.0, 'nextafter(1.0, 0.0) < 1.0'

# === math.ulp() ===
assert math.ulp(1.0) == 2.220446049250313e-16, 'ulp(1.0)'
assert math.ulp(0.0) > 0, 'ulp(0.0) > 0'
assert math.isinf(math.ulp(float('inf'))), 'ulp(inf) is inf'
assert math.isnan(math.ulp(float('nan'))), 'ulp(nan) is nan'
