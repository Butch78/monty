# === Tuple ordering comparison ===
# Basic less-than
assert (1, 2) < (1, 3), 'tuple lt differing element'
assert (1, 2) < (2, 0), 'tuple lt first element differs'
assert () < (1,), 'tuple lt empty vs non-empty'
assert (1,) < (1, 2), 'tuple lt prefix shorter'

# Basic greater-than
assert (1, 3) > (1, 2), 'tuple gt differing element'
assert (2, 0) > (1, 9), 'tuple gt first element differs'
assert (1,) > (), 'tuple gt non-empty vs empty'
assert (1, 2) > (1,), 'tuple gt longer prefix'

# Less-than-or-equal
assert (1, 2) <= (1, 3), 'tuple le less'
assert (1, 2) <= (1, 2), 'tuple le equal'
assert () <= (), 'tuple le both empty'
assert (1,) <= (1, 2), 'tuple le prefix'

# Greater-than-or-equal
assert (1, 3) >= (1, 2), 'tuple ge greater'
assert (1, 2) >= (1, 2), 'tuple ge equal'
assert () >= (), 'tuple ge both empty'
assert (1, 2) >= (1,), 'tuple ge longer prefix'

# NOT comparisons (False results)
assert not (1, 3) < (1, 2), 'tuple not lt'
assert not (1, 2) > (1, 3), 'tuple not gt'
assert not (1, 3) <= (1, 2), 'tuple not le'
assert not (1, 2) >= (1, 3), 'tuple not ge'

# Multi-element tuples
assert (1, 2, 3) < (1, 2, 4), 'tuple lt 3 elements'
assert (1, 2, 3, 4) < (1, 2, 3, 5), 'tuple lt 4 elements'
assert (0, 0, 0) < (0, 0, 1), 'tuple lt last element differs'

# Mixed types in tuple elements
assert (1, 2.0) < (1, 3.0), 'tuple lt with floats'
assert (1, 2) < (1, 2.5), 'tuple lt int vs float element'
assert (True, 2) < (True, 3), 'tuple lt with bools'
assert (False,) < (True,), 'tuple lt False vs True'

# String elements in tuples
assert ('a', 1) < ('b', 1), 'tuple lt string elements'
assert ('hello', 1) < ('hello', 2), 'tuple lt equal strings'
assert ('abc',) < ('abd',), 'tuple lt string comparison'

# Nested tuples
assert ((1, 2), 3) < ((1, 3), 0), 'tuple lt nested inner differs'
assert ((1, 2), 3) < ((1, 2), 4), 'tuple lt nested equal inner'

# === List ordering comparison ===
assert [1, 2] < [1, 3], 'list lt'
assert [1, 3] > [1, 2], 'list gt'
assert [1, 2] <= [1, 2], 'list le equal'
assert [1, 2] >= [1, 2], 'list ge equal'
assert [] < [1], 'list lt empty vs non-empty'
assert [1] < [1, 2], 'list lt prefix shorter'
assert [1, 2, 3] < [1, 2, 4], 'list lt 3 elements'

# List NOT comparisons
assert not [1, 3] < [1, 2], 'list not lt'
assert not [1, 2] > [1, 3], 'list not gt'

# === min/max with tuples ===
assert min((1, 3), (1, 2)) == (1, 2), 'min of two tuples'
assert max((1, 3), (1, 2)) == (1, 3), 'max of two tuples'
assert min((0,), (1,), (2,)) == (0,), 'min of three tuples'
assert max((0,), (1,), (2,)) == (2,), 'max of three tuples'

# min/max with lists
assert min([1, 3], [1, 2]) == [1, 2], 'min of two lists'
assert max([1, 3], [1, 2]) == [1, 3], 'max of two lists'

# === sorted with tuples ===
items = [(3, 'c'), (1, 'a'), (2, 'b')]
items.sort()
assert items == [(1, 'a'), (2, 'b'), (3, 'c')], 'sort list of tuples'

# Sort stability with equal first elements
items2 = [(1, 'b'), (1, 'a'), (2, 'x')]
items2.sort()
assert items2 == [(1, 'a'), (1, 'b'), (2, 'x')], 'sort tuples stable on second element'

# === sorted dict.items() ===
d = {'c': 3, 'a': 1, 'b': 2}
items = list(d.items())
items.sort()
assert items == [('a', 1), ('b', 2), ('c', 3)], 'sorted dict items'

# === Edge cases ===
# Single element tuples
assert (0,) < (1,), 'single element tuple lt'
assert (1,) > (0,), 'single element tuple gt'
assert (1,) <= (1,), 'single element tuple le'
assert (1,) >= (1,), 'single element tuple ge'

# Empty tuples
assert not () < (), 'empty tuples not lt'
assert not () > (), 'empty tuples not gt'
assert () <= (), 'empty tuples le'
assert () >= (), 'empty tuples ge'

# Empty lists
assert not [] < [], 'empty lists not lt'
assert [] <= [], 'empty lists le'

# Very different lengths
assert (1,) < (1, 2, 3, 4, 5), 'tuple prefix much shorter'
assert (1, 2, 3, 4, 5) > (1,), 'tuple much longer than prefix'
