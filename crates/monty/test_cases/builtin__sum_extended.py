# === sum() extended coverage ===

# sum with floats
assert sum([1.5, 2.5, 3.0]) == 7.0, 'sum of pure floats'
assert sum([0.1, 0.2]) == 0.30000000000000004, 'sum float precision'

# sum with generators/iterators
assert sum(x for x in [1, 2, 3]) == 6, 'sum of generator'
assert sum(x * 2 for x in range(4)) == 12, 'sum of generator with transform'

# sum with custom start
assert sum([1, 2], 100) == 103, 'sum with large start'
assert sum([], 42) == 42, 'sum empty with start returns start'
assert sum([1], -1) == 0, 'sum with negative start'

# sum with string start raises error
threw = False
try:
    sum(['a', 'b'], '')
except TypeError:
    threw = True
assert threw, 'sum with string start raises TypeError'

# sum with nested lists
assert sum([[1, 2], [3]], []) == [1, 2, 3], 'sum nested lists'
assert sum([[], [1], [2, 3]], []) == [1, 2, 3], 'sum with empty inner list'

# sum of range
assert sum(range(1, 11)) == 55, 'sum 1 to 10'
assert sum(range(100)) == 4950, 'sum 0 to 99'
assert sum(range(0)) == 0, 'sum empty range'

# sum of single element
assert sum([42]) == 42, 'sum single element'
assert sum([42], 8) == 50, 'sum single element with start'

# sum of set and dict keys
assert sum({1, 2, 3}) == 6, 'sum of set'
assert sum({10: 'a', 20: 'b'}) == 30, 'sum of dict keys'

# sum with float start and int values
assert sum([1, 2, 3], 0.0) == 6.0, 'sum int list with float start'

# sum with bools (True=1, False=0)
assert sum([True, True, False]) == 2, 'sum of bools'
assert sum([True, True, True]) == 3, 'sum all True'
assert sum([False, False]) == 0, 'sum all False'
assert sum([True, 1, 2]) == 4, 'sum mixed bool and int'
