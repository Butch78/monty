# === min/max with two positional args ===
assert min(3, 5) == 3, 'min two args'
assert max(3, 5) == 5, 'max two args'
assert min(5, 3) == 3, 'min two args reversed'
assert max(5, 3) == 5, 'max two args reversed'

# min/max with equal values
assert min(5, 5) == 5, 'min equal values'
assert max(5, 5) == 5, 'max equal values'

# min/max with mixed int/float
assert min(1, 2.5) == 1, 'min int and float'
assert max(1, 2.5) == 2.5, 'max int and float'

# min/max with many args
assert min(5, 3, 1, 4, 2) == 1, 'min many args'
assert max(5, 3, 1, 4, 2) == 5, 'max many args'

# min/max with negative numbers
assert min(-10, -20, -5) == -20, 'min negatives'
assert max(-10, -20, -5) == -5, 'max negatives'

# min/max error: empty iterable
threw = False
try:
    min([])
except ValueError:
    threw = True
assert threw, 'min empty list raises ValueError'

threw = False
try:
    max([])
except ValueError:
    threw = True
assert threw, 'max empty list raises ValueError'

# min/max error: no args
threw = False
try:
    min()
except TypeError:
    threw = True
assert threw, 'min no args raises TypeError'

threw = False
try:
    max()
except TypeError:
    threw = True
assert threw, 'max no args raises TypeError'

# min/max with set
assert min({3, 1, 2}) == 1, 'min of set'
assert max({3, 1, 2}) == 3, 'max of set'

# min/max with range
assert min(range(5, 0, -1)) == 1, 'min of range'
assert max(range(5, 0, -1)) == 5, 'max of range'

# min/max with generator
assert min(x * 2 for x in [3, 1, 2]) == 2, 'min of generator'
assert max(x * 2 for x in [3, 1, 2]) == 6, 'max of generator'

# min/max with strings in list
assert min(['c', 'a', 'b']) == 'a', 'min string list'
assert max(['c', 'a', 'b']) == 'c', 'max string list'

# min/max with string args
assert min('b', 'a', 'c') == 'a', 'min string args'
assert max('b', 'a', 'c') == 'c', 'max string args'

# min/max with float list
assert min([1.5, 0.5, 2.5]) == 0.5, 'min float list'
assert max([1.5, 0.5, 2.5]) == 2.5, 'max float list'

# min/max with tuples
assert min((1, 3), (1, 2)) == (1, 2), 'min tuples'
assert max((1, 3), (1, 2)) == (1, 3), 'max tuples'
assert min((0,), (1,), (2,)) == (0,), 'min three tuples'
assert max((0,), (1,), (2,)) == (2,), 'max three tuples'

# min/max with lists
assert min([1, 3], [1, 2]) == [1, 2], 'min lists'
assert max([1, 3], [1, 2]) == [1, 3], 'max lists'
