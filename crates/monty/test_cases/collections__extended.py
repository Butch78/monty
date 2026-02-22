# === Dict comprehension ===
d = {k: v for k, v in [('a', 1), ('b', 2), ('c', 3)]}
assert d == {'a': 1, 'b': 2, 'c': 3}, 'dict comprehension from list of tuples'

d2 = {i: i**2 for i in range(5)}
assert d2 == {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}, 'dict comprehension from range'

# Empty dict comprehension
d3 = {k: v for k, v in []}
assert d3 == {}, 'empty dict comprehension'

# Dict comprehension with filter
d4 = {k: v for k, v in [('a', 1), ('b', 2), ('c', 3)] if v > 1}
assert d4 == {'b': 2, 'c': 3}, 'dict comprehension with filter'

# === Set comprehension ===
s = {x * 2 for x in [1, 2, 3]}
assert s == {2, 4, 6}, 'set comprehension'

# Set comprehension with filter
s2 = {x for x in range(10) if x % 2 == 0}
assert s2 == {0, 2, 4, 6, 8}, 'set comprehension with filter'

# Empty set comprehension
s3 = {x for x in []}
assert s3 == set(), 'empty set comprehension'

# === List comprehension edge cases ===
# Nested list comprehension (flat)
flat = [x for row in [[1, 2], [3, 4], [5, 6]] for x in row]
assert flat == [1, 2, 3, 4, 5, 6], 'nested list comprehension flat'

# List comprehension with multiple conditions
result = [x for x in range(20) if x % 2 == 0 if x % 3 == 0]
assert result == [0, 6, 12, 18], 'list comp multiple conditions'

# === Dict operations ===
d = {'a': 1, 'b': 2, 'c': 3}

# .get() with default
assert d.get('a') == 1, 'dict get existing'
assert d.get('z') is None, 'dict get missing returns None'
assert d.get('z', 42) == 42, 'dict get missing with default'

# .keys(), .values()
assert sorted(d.keys()) == ['a', 'b', 'c'], 'dict keys sorted'
assert sorted(d.values()) == [1, 2, 3], 'dict values sorted'

# .items() - check len and membership
items = list(d.items())
assert len(items) == 3, 'dict items length'

# .pop()
d2 = {'x': 10, 'y': 20}
v = d2.pop('x')
assert v == 10, 'dict pop returns value'
assert d2 == {'y': 20}, 'dict pop removes key'

# .pop() with default
v2 = d2.pop('z', 99)
assert v2 == 99, 'dict pop missing with default'

# .update()
d3 = {'a': 1}
d3.update({'b': 2, 'c': 3})
assert d3 == {'a': 1, 'b': 2, 'c': 3}, 'dict update'

# .setdefault()
d4 = {'a': 1}
v = d4.setdefault('a', 99)
assert v == 1, 'setdefault existing returns existing'
assert d4 == {'a': 1}, 'setdefault existing does not modify'

v = d4.setdefault('b', 42)
assert v == 42, 'setdefault missing returns default'
assert d4 == {'a': 1, 'b': 42}, 'setdefault missing inserts'

# 'in' operator for dict
assert 'a' in d, 'in operator dict key exists'
assert 'z' not in d, 'not in operator dict key missing'

# === List operations ===
lst = [1, 2, 3, 4, 5]

# .index()
assert lst.index(3) == 2, 'list index'
assert lst.index(1) == 0, 'list index first'
assert lst.index(5) == 4, 'list index last'

# .count()
lst2 = [1, 2, 2, 3, 2, 4]
assert lst2.count(2) == 3, 'list count'
assert lst2.count(5) == 0, 'list count missing'
assert lst2.count(1) == 1, 'list count single'

# .remove()
lst3 = [1, 2, 3, 2, 4]
lst3.remove(2)
assert lst3 == [1, 3, 2, 4], 'list remove first occurrence'

# .insert()
lst4 = [1, 3, 4]
lst4.insert(1, 2)
assert lst4 == [1, 2, 3, 4], 'list insert middle'
lst4.insert(0, 0)
assert lst4 == [0, 1, 2, 3, 4], 'list insert beginning'

# .extend()
lst5 = [1, 2]
lst5.extend([3, 4, 5])
assert lst5 == [1, 2, 3, 4, 5], 'list extend'
lst5.extend([])
assert lst5 == [1, 2, 3, 4, 5], 'list extend empty'

# .clear()
lst6 = [1, 2, 3]
lst6.clear()
assert lst6 == [], 'list clear'

# .copy()
lst7 = [1, 2, 3]
lst8 = lst7.copy()
lst8.append(4)
assert lst7 == [1, 2, 3], 'list copy independent'
assert lst8 == [1, 2, 3, 4], 'list copy modified'

# .reverse()
lst9 = [3, 1, 2]
lst9.reverse()
assert lst9 == [2, 1, 3], 'list reverse in place'

# .sort()
lst10 = [3, 1, 4, 1, 5]
lst10.sort()
assert lst10 == [1, 1, 3, 4, 5], 'list sort in place'

# === Set operations ===
s1 = {1, 2, 3}
s2 = {2, 3, 4}

# .union() / |
assert s1 | s2 == {1, 2, 3, 4}, 'set union operator'
assert s1.union(s2) == {1, 2, 3, 4}, 'set union method'

# .intersection() / &
assert s1 & s2 == {2, 3}, 'set intersection operator'
assert s1.intersection(s2) == {2, 3}, 'set intersection method'

# .difference() / -
assert s1 - s2 == {1}, 'set difference operator'
assert s1.difference(s2) == {1}, 'set difference method'

# .symmetric_difference() / ^
assert s1 ^ s2 == {1, 4}, 'set symmetric difference operator'
assert s1.symmetric_difference(s2) == {1, 4}, 'set symmetric_difference method'

# .issubset() / <=
assert {1, 2}.issubset({1, 2, 3}), 'set issubset'
assert not {1, 4}.issubset({1, 2, 3}), 'set not issubset'

# .issuperset() / >=
assert {1, 2, 3}.issuperset({1, 2}), 'set issuperset'

# .add() and .discard()
s3 = {1, 2}
s3.add(3)
assert s3 == {1, 2, 3}, 'set add'
s3.discard(2)
assert s3 == {1, 3}, 'set discard'
s3.discard(99)  # should not raise
assert s3 == {1, 3}, 'set discard missing is no-op'

# 'in' operator for set
assert 1 in s1, 'in operator set member'
assert 5 not in s1, 'not in operator set non-member'
