# === int() from string ===
assert int('42') == 42, 'int from string'
assert int('-7') == -7, 'int from negative string'
assert int('  10  ') == 10, 'int from string with whitespace'
assert int('1_000') == 1000, 'int from string with underscores'
assert int('0') == 0, 'int from string zero'
assert int('+5') == 5, 'int from string with plus'

# int() from string error
threw = False
try:
    int('hello')
except ValueError as e:
    threw = True
    assert 'invalid literal' in str(e), f'wrong msg: {e}'
assert threw, 'int from invalid string raises ValueError'

threw = False
try:
    int('')
except ValueError:
    threw = True
assert threw, 'int from empty string raises ValueError'

threw = False
try:
    int('3.14')
except ValueError:
    threw = True
assert threw, 'int from float string raises ValueError'

# int() from wrong type
threw = False
try:
    int([1])
except TypeError as e:
    threw = True
    assert 'int' in str(e), f'wrong msg: {e}'
assert threw, 'int from list raises TypeError'

threw = False
try:
    int(None)
except TypeError:
    threw = True
assert threw, 'int from None raises TypeError'

# === float() from string ===
assert float('3.14') == 3.14, 'float from string'
assert float('-2.5') == -2.5, 'float from negative string'
assert float('  1.0  ') == 1.0, 'float from string with whitespace'
assert float('42') == 42.0, 'float from int string'
assert float('inf') == float('inf'), 'float from inf'
assert float('-inf') == float('-inf'), 'float from -inf'
assert float('infinity') == float('inf'), 'float from infinity'

# float nan
import math

assert math.isnan(float('nan')), 'float from nan'
assert math.isnan(float('NaN')), 'float from NaN'

# float() from string error
threw = False
try:
    float('hello')
except ValueError as e:
    threw = True
    assert 'could not convert' in str(e), f'wrong msg: {e}'
assert threw, 'float from invalid string raises ValueError'

threw = False
try:
    float('')
except ValueError:
    threw = True
assert threw, 'float from empty string raises ValueError'

# float() from wrong type
threw = False
try:
    float([1])
except TypeError:
    threw = True
assert threw, 'float from list raises TypeError'

threw = False
try:
    float(None)
except TypeError:
    threw = True
assert threw, 'float from None raises TypeError'

# === bool() comprehensive ===
assert bool(0) == False, 'bool 0'
assert bool(0.0) == False, 'bool 0.0'
assert bool('') == False, 'bool empty str'
assert bool(b'') == False, 'bool empty bytes'
assert bool([]) == False, 'bool empty list'
assert bool(()) == False, 'bool empty tuple'
assert bool({}) == False, 'bool empty dict'
assert bool(set()) == False, 'bool empty set'
assert bool(frozenset()) == False, 'bool empty frozenset'
assert bool(None) == False, 'bool None'
assert bool(range(0)) == False, 'bool empty range'

assert bool(1) == True, 'bool 1'
assert bool(-1) == True, 'bool -1'
assert bool(0.1) == True, 'bool 0.1'
assert bool('x') == True, 'bool non-empty str'
assert bool(b'x') == True, 'bool non-empty bytes'
assert bool([0]) == True, 'bool non-empty list'
assert bool((0,)) == True, 'bool non-empty tuple'
assert bool({0: 0}) == True, 'bool non-empty dict'
assert bool({0}) == True, 'bool non-empty set'
assert bool(range(1)) == True, 'bool non-empty range'

# === set() constructor ===
assert set() == set(), 'set empty'
assert set([1, 2, 3]) == {1, 2, 3}, 'set from list'
assert set((1, 2, 2, 3)) == {1, 2, 3}, 'set from tuple deduplicates'
assert set('hello') == {'h', 'e', 'l', 'o'}, 'set from string'
assert set(range(3)) == {0, 1, 2}, 'set from range'
assert set({1: 'a', 2: 'b'}) == {1, 2}, 'set from dict uses keys'
assert set(set([1, 2])) == {1, 2}, 'set from set is copy'

# === frozenset() constructor ===
assert frozenset() == frozenset(), 'frozenset empty'
assert frozenset([1, 2, 3]) == frozenset({1, 2, 3}), 'frozenset from list'
assert frozenset((1, 2, 2, 3)) == frozenset({1, 2, 3}), 'frozenset from tuple deduplicates'
assert frozenset('abc') == frozenset({'a', 'b', 'c'}), 'frozenset from string'

# === bytes() constructor edge cases ===
assert bytes(5) == b'\x00\x00\x00\x00\x00', 'bytes from int fills zeros'
assert bytes(0) == b'', 'bytes from 0 empty'
assert bytes(b'hello') == b'hello', 'bytes from bytes copy'

threw = False
try:
    bytes(-1)
except ValueError:
    threw = True
assert threw, 'bytes from negative int raises ValueError'

# === str() with various types ===
assert str(set()) == 'set()', 'str of empty set'
assert str(frozenset()) == 'frozenset()', 'str of empty frozenset'
assert str(range(5)) == 'range(0, 5)', 'str of range'
assert str(range(1, 10, 2)) == 'range(1, 10, 2)', 'str of range with step'
