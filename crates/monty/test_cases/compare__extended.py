# === Cross-type comparisons ===

# int/float comparison
assert 1 == 1.0, 'int equals float'
assert 1.0 == 1, 'float equals int'
assert 2 > 1.5, 'int > float'
assert 1.5 < 2, 'float < int'
assert 2 >= 2.0, 'int >= float'
assert 2.0 <= 2, 'float <= int'

# bool/int comparison
assert True == 1, 'True == 1'
assert False == 0, 'False == 0'
assert True != 2, 'True != 2'
assert True < 2, 'True < 2'
assert False < 1, 'False < 1'

# bool/float comparison
assert True == 1.0, 'True == 1.0'
assert False == 0.0, 'False == 0.0'

# None comparisons
assert None == None, 'None equals None'
assert None is None, 'None is None'
assert None != 0, 'None != 0'
assert None != '', 'None != empty str'
assert None != False, 'None != False'
assert None != [], 'None != empty list'

# 'is' and 'is not' operators
a = [1, 2, 3]
b = a
c = [1, 2, 3]
assert a is b, 'is same reference'
assert a is not c, 'is not different reference'
assert a == c, '== same content'

# 'is' with None
assert None is None, 'None is None'
x = None
assert x is None, 'variable None is None'

# 'is' with small ints (interned)
assert 1 is 1, 'small int is same'
assert True is True, 'True is True'
assert False is False, 'False is False'

# 'in' and 'not in' operators
lst = [1, 2, 3, 4, 5]
assert 3 in lst, 'in list found'
assert 6 not in lst, 'not in list'
assert 1 in lst, 'in list first'
assert 5 in lst, 'in list last'

# 'in' with string
assert 'ell' in 'hello', 'substring in string'
assert 'xyz' not in 'hello', 'substring not in string'
assert '' in 'hello', 'empty string in string'
assert 'hello' in 'hello', 'string in itself'

# 'in' with tuple
assert 1 in (1, 2, 3), 'in tuple'
assert 4 not in (1, 2, 3), 'not in tuple'

# 'in' with set
assert 1 in {1, 2, 3}, 'in set'
assert 4 not in {1, 2, 3}, 'not in set'

# 'in' with dict (checks keys)
assert 'a' in {'a': 1, 'b': 2}, 'in dict checks keys'
assert 'c' not in {'a': 1, 'b': 2}, 'not in dict keys'

# Chained comparisons
x = 5
assert 1 < x < 10, 'chained comparison'
assert 0 < x <= 5, 'chained le'
assert 5 <= x < 10, 'chained ge lt'
assert not (1 < x < 3), 'chained comparison false'

# === Comparison with different types ===
assert 1 != 'one', 'int != str'
assert 'hello' != 42, 'str != int'
assert [] != {}, 'list != dict'
assert () != [], 'tuple != list'
assert set() != frozenset({1}), 'empty set != non-empty frozenset'

# === String comparisons ===
assert 'abc' < 'abd', 'string less than'
assert 'abc' > 'abb', 'string greater than'
assert 'abc' <= 'abc', 'string less equal'
assert 'abc' >= 'abc', 'string greater equal'
assert 'a' < 'b', 'single char compare'
assert 'abc' < 'abcd', 'shorter string is less'
assert '' < 'a', 'empty string is least'
