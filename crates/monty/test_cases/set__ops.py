# === Construction ===
s = set()
assert len(s) == 0, 'empty set len'
assert s == set(), 'empty set equality'

s = set([1, 2, 3])
assert len(s) == 3, 'set from list len'

# === Basic Methods ===
s = set()
s.add(1)
s.add(2)
s.add(1)  # duplicate
assert len(s) == 2, 'add with duplicate'

# === Discard and Remove ===
s = set([1, 2, 3])
s.discard(2)
assert len(s) == 2, 'discard existing'
s.discard(99)  # should not raise
assert len(s) == 2, 'discard non-existing'

# === Pop ===
s = set([1])
v = s.pop()
assert v == 1, 'pop returns element'
assert len(s) == 0, 'pop removes element'

# === Clear ===
s = set([1, 2, 3])
s.clear()
assert len(s) == 0, 'clear'

# === Copy ===
s = set([1, 2, 3])
s2 = s.copy()
assert s == s2, 'copy equality'
s.add(4)
assert s != s2, 'copy is independent'

# === Update ===
s = set([1, 2])
s.update([2, 3, 4])
assert len(s) == 4, 'update with list'

# === Union ===
s1 = set([1, 2])
s2 = set([2, 3])
u = s1.union(s2)
assert len(u) == 3, 'union len'

# === Intersection ===
s1 = set([1, 2, 3])
s2 = set([2, 3, 4])
i = s1.intersection(s2)
assert len(i) == 2, 'intersection len'

# === Difference ===
s1 = set([1, 2, 3])
s2 = set([2, 3, 4])
d = s1.difference(s2)
assert len(d) == 1, 'difference len'

# === Symmetric Difference ===
s1 = set([1, 2, 3])
s2 = set([2, 3, 4])
sd = s1.symmetric_difference(s2)
assert len(sd) == 2, 'symmetric_difference len'

# === Issubset ===
s1 = set([1, 2])
s2 = set([1, 2, 3])
assert s1.issubset(s2) == True, 'issubset true'
assert s2.issubset(s1) == False, 'issubset false'

# === Issuperset ===
s1 = set([1, 2, 3])
s2 = set([1, 2])
assert s1.issuperset(s2) == True, 'issuperset true'
assert s2.issuperset(s1) == False, 'issuperset false'

# === Isdisjoint ===
s1 = set([1, 2])
s2 = set([3, 4])
s3 = set([2, 3])
assert s1.isdisjoint(s2) == True, 'isdisjoint true'
assert s1.isdisjoint(s3) == False, 'isdisjoint false'

# === Bool ===
assert bool(set()) == False, 'empty set is falsy'
assert bool(set([1])) == True, 'non-empty set is truthy'

# === repr ===
assert repr(set()) == 'set()', 'empty set repr'

# === Set literals ===
s = {1, 2, 3}
assert len(s) == 3, 'set literal len'

s = {1, 1, 2, 2, 3}
assert len(s) == 3, 'set literal deduplication'

# Set literal with expressions
x = 5
s = {x, x + 1, x + 2}
assert len(s) == 3, 'set literal with expressions'

# === Union operator (|) ===
s1 = {1, 2}
s2 = {3, 4}
assert s1 | s2 == {1, 2, 3, 4}, 'union operator basic'

s1 = {1, 2, 3}
s2 = {2, 3, 4}
assert s1 | s2 == {1, 2, 3, 4}, 'union operator with overlap'

assert set() | set() == set(), 'union of empty sets'
assert {1} | set() == {1}, 'union with empty rhs'
assert set() | {1} == {1}, 'union with empty lhs'

# === Intersection operator (&) ===
s1 = {1, 2, 3}
s2 = {2, 3, 4}
assert s1 & s2 == {2, 3}, 'intersection operator basic'

s1 = {1, 2}
s2 = {3, 4}
assert s1 & s2 == set(), 'intersection operator disjoint'

assert set() & set() == set(), 'intersection of empty sets'
assert {1, 2} & set() == set(), 'intersection with empty rhs'

# === Difference operator (-) ===
s1 = {1, 2, 3}
s2 = {2, 3}
assert s1 - s2 == {1}, 'difference operator basic'

s1 = {1, 2, 3}
s2 = {4, 5}
assert s1 - s2 == {1, 2, 3}, 'difference operator no overlap'

assert set() - set() == set(), 'difference of empty sets'
assert {1, 2} - set() == {1, 2}, 'difference with empty rhs'
assert set() - {1, 2} == set(), 'difference with empty lhs'

# === Symmetric difference operator (^) ===
s1 = {1, 2, 3}
s2 = {2, 3, 4}
assert s1 ^ s2 == {1, 4}, 'symmetric difference operator basic'

s1 = {1, 2}
s2 = {1, 2}
assert s1 ^ s2 == set(), 'symmetric difference same sets'

s1 = {1, 2}
s2 = {3, 4}
assert s1 ^ s2 == {1, 2, 3, 4}, 'symmetric difference disjoint'

# === Augmented assignment operators ===
s = {1, 2}
s |= {3, 4}
assert s == {1, 2, 3, 4}, 'augmented union'

s = {1, 2, 3}
s &= {2, 3, 4}
assert s == {2, 3}, 'augmented intersection'

s = {1, 2, 3}
s -= {2, 3}
assert s == {1}, 'augmented difference'

s = {1, 2, 3}
s ^= {2, 3, 4}
assert s == {1, 4}, 'augmented symmetric difference'

# === Frozenset operators ===
fs1 = frozenset({1, 2})
fs2 = frozenset({2, 3})
assert fs1 | fs2 == frozenset({1, 2, 3}), 'frozenset union'
assert fs1 & fs2 == frozenset({2}), 'frozenset intersection'
assert fs1 - fs2 == frozenset({1}), 'frozenset difference'
assert fs1 ^ fs2 == frozenset({1, 3}), 'frozenset symmetric difference'

# Return type matches left operand
result = {1, 2} | frozenset({3})
assert type(result).__name__ == 'set', 'set | frozenset returns set'

result = frozenset({1, 2}) | {3}
assert type(result).__name__ == 'frozenset', 'frozenset | set returns frozenset'

# === Type errors for invalid operands ===
try:
    {1, 2} | [3, 4]
    assert False, 'set | list should raise TypeError'
except TypeError as e:
    msg = str(e)
    assert 'set' in msg and 'list' in msg, f'error should mention types, got: {e}'

try:
    {1, 2} - [3, 4]
    assert False, 'set - list should raise TypeError'
except TypeError as e:
    msg = str(e)
    assert 'set' in msg and 'list' in msg, f'error should mention types, got: {e}'

try:
    {1, 2} & 'abc'
    assert False, 'set & str should raise TypeError'
except TypeError as e:
    msg = str(e)
    assert 'set' in msg and 'str' in msg, f'error should mention types, got: {e}'

try:
    {1, 2} ^ 42
    assert False, 'set ^ int should raise TypeError'
except TypeError as e:
    msg = str(e)
    assert 'set' in msg and 'int' in msg, f'error should mention types, got: {e}'
