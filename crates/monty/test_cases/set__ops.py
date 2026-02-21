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

# === String elements ===
assert {'a', 'b'} | {'b', 'c'} == {'a', 'b', 'c'}, 'string union'
assert {'a', 'b'} & {'b', 'c'} == {'b'}, 'string intersection'
assert {'a', 'b'} - {'b', 'c'} == {'a'}, 'string difference'
assert {'a', 'b'} ^ {'b', 'c'} == {'a', 'c'}, 'string symmetric difference'

# === None elements ===
assert {None, 1} | {None, 2} == {None, 1, 2}, 'none element union'
assert {None, 1} & {None, 2} == {None}, 'none element intersection'

# === Tuple elements ===
assert {(1, 2), (3, 4)} | {(1, 2), (5, 6)} == {(1, 2), (3, 4), (5, 6)}, 'tuple element union'

# === Self-operations (same set on both sides) ===
s = {1, 2, 3}
assert s | s == {1, 2, 3}, 'self union is identity'
assert s & s == {1, 2, 3}, 'self intersection is identity'
assert s - s == set(), 'self difference is empty'
assert s ^ s == set(), 'self symmetric difference is empty'

# === Operators do not modify originals ===
s1 = {1, 2, 3}
s2 = {2, 3, 4}
r = s1 | s2
assert s1 == {1, 2, 3}, 'union does not modify lhs'
assert s2 == {2, 3, 4}, 'union does not modify rhs'
r = s1 - s2
assert s1 == {1, 2, 3}, 'difference does not modify lhs'
assert s2 == {2, 3, 4}, 'difference does not modify rhs'

# === Chained operators ===
assert {1, 2} | {3, 4} | {5, 6} == {1, 2, 3, 4, 5, 6}, 'chained union'
assert {1, 2, 3} & {2, 3, 4} & {3, 4, 5} == {3}, 'chained intersection'

# === Single element sets ===
assert {1} | {2} == {1, 2}, 'single element union'
assert {1} & {1} == {1}, 'single element intersection same'
assert {1} & {2} == set(), 'single element intersection different'
assert {1} - {1} == set(), 'single element difference same'
assert {1} - {2} == {1}, 'single element difference different'
assert {1} ^ {1} == set(), 'single element xor same'
assert {1} ^ {2} == {1, 2}, 'single element xor different'

# === Larger sets ===
big1 = set(range(50))
big2 = set(range(25, 75))
assert len(big1 | big2) == 75, 'large set union len'
assert len(big1 & big2) == 25, 'large set intersection len'
assert len(big1 - big2) == 25, 'large set difference len'
assert len(big1 ^ big2) == 50, 'large set symmetric difference len'

# === Mixed set/frozenset — all operators ===
s = {1, 2, 3}
fs = frozenset({2, 3, 4})
assert s | fs == {1, 2, 3, 4}, 'set | frozenset value'
assert s & fs == {2, 3}, 'set & frozenset value'
assert s - fs == {1}, 'set - frozenset value'
assert s ^ fs == {1, 4}, 'set ^ frozenset value'
assert fs | s == frozenset({1, 2, 3, 4}), 'frozenset | set value'
assert fs & s == frozenset({2, 3}), 'frozenset & set value'
assert fs - s == frozenset({4}), 'frozenset - set value'
assert fs ^ s == frozenset({1, 4}), 'frozenset ^ set value'

# === Return type for all mixed operators ===
assert type(s | fs).__name__ == 'set', 'set | frozenset returns set'
assert type(s & fs).__name__ == 'set', 'set & frozenset returns set'
assert type(s - fs).__name__ == 'set', 'set - frozenset returns set'
assert type(s ^ fs).__name__ == 'set', 'set ^ frozenset returns set'
assert type(fs | s).__name__ == 'frozenset', 'frozenset | set returns frozenset'
assert type(fs & s).__name__ == 'frozenset', 'frozenset & set returns frozenset'
assert type(fs - s).__name__ == 'frozenset', 'frozenset - set returns frozenset'
assert type(fs ^ s).__name__ == 'frozenset', 'frozenset ^ set returns frozenset'

# === Augmented assignment with frozenset rhs ===
s = {1, 2}
s |= frozenset({3, 4})
assert s == {1, 2, 3, 4}, 'augmented union with frozenset rhs'
assert type(s).__name__ == 'set', 'augmented union preserves set type'

# === Type errors for invalid operands ===
try:
    {1, 2} | [3, 4]
    assert False, 'set | list should raise TypeError'
except TypeError as e:
    assert str(e) == "unsupported operand type(s) for |: 'set' and 'list'"

try:
    {1, 2} - [3, 4]
    assert False, 'set - list should raise TypeError'
except TypeError as e:
    assert str(e) == "unsupported operand type(s) for -: 'set' and 'list'"

try:
    {1, 2} & 'abc'
    assert False, 'set & str should raise TypeError'
except TypeError as e:
    assert str(e) == "unsupported operand type(s) for &: 'set' and 'str'"

try:
    {1, 2} ^ 42
    assert False, 'set ^ int should raise TypeError'
except TypeError as e:
    assert str(e) == "unsupported operand type(s) for ^: 'set' and 'int'"

try:
    {1, 2} | 42
    assert False, 'set | int should raise TypeError'
except TypeError as e:
    assert str(e) == "unsupported operand type(s) for |: 'set' and 'int'"

try:
    {1, 2} & [1]
    assert False, 'set & list should raise TypeError'
except TypeError as e:
    assert str(e) == "unsupported operand type(s) for &: 'set' and 'list'"

try:
    {1, 2} - 'x'
    assert False, 'set - str should raise TypeError'
except TypeError as e:
    assert str(e) == "unsupported operand type(s) for -: 'set' and 'str'"

try:
    {1, 2} ^ (1, 2)
    assert False, 'set ^ tuple should raise TypeError'
except TypeError as e:
    assert str(e) == "unsupported operand type(s) for ^: 'set' and 'tuple'"

# === Containment (in / not in) ===
assert 1 in {1, 2, 3}, 'in operator positive'
assert 4 not in {1, 2, 3}, 'not in operator'
assert 'a' in {'a', 'b'}, 'in with strings'
assert None in {None, 1}, 'in with None'
assert (1, 2) in {(1, 2), (3, 4)}, 'in with tuples'

# === Inequality (!=) ===
assert {1, 2} != {1, 3}, 'ne different'
assert not ({1, 2} != {1, 2}), 'ne same'
assert {1} != set(), 'ne non-empty vs empty'

# === Iteration ===
result = []
for x in {1, 2, 3}:
    result.append(x)
assert len(result) == 3, 'iteration length'
assert set(result) == {1, 2, 3}, 'iteration elements'

# iterating empty set
result = []
for x in set():
    result.append(x)
assert result == [], 'empty set iteration'

# === Construction from various iterables ===
s = set('abc')
assert len(s) == 3, 'set from string len'
assert 'a' in s and 'b' in s and 'c' in s, 'set from string elements'

s = set((1, 2, 3))
assert s == {1, 2, 3}, 'set from tuple'

s = set(range(5))
assert s == {0, 1, 2, 3, 4}, 'set from range'

# === Cross-construction (set <-> frozenset) ===
fs = frozenset({1, 2, 3})
s = set(fs)
assert s == {1, 2, 3}, 'set from frozenset'
assert type(s).__name__ == 'set', 'set from frozenset type'

s2 = {4, 5, 6}
fs2 = frozenset(s2)
assert fs2 == frozenset({4, 5, 6}), 'frozenset from set'
assert type(fs2).__name__ == 'frozenset', 'frozenset from set type'

# === Set comprehension ===
s = {x * 2 for x in range(5)}
assert s == {0, 2, 4, 6, 8}, 'set comprehension'

# === Remove (success and KeyError) ===
s = {1, 2, 3}
s.remove(2)
assert 2 not in s, 'remove existing element'
assert len(s) == 2, 'remove existing len'

try:
    s.remove(99)
    assert False, 'remove non-existing should raise KeyError'
except KeyError:
    pass

# === Pop from empty set (KeyError) ===
try:
    set().pop()
    assert False, 'pop empty should raise KeyError'
except KeyError:
    pass

# === Methods accepting iterables (not just sets) ===
assert {1, 2}.union([3, 4]) == {1, 2, 3, 4}, 'union with list arg'
assert {1, 2, 3}.intersection([2, 3, 4]) == {2, 3}, 'intersection with list arg'
assert {1, 2, 3}.difference([2, 3]) == {1}, 'difference with list arg'
assert {1, 2, 3}.symmetric_difference([2, 3, 4]) == {1, 4}, 'symmetric_difference with list arg'
assert {1, 2}.union(range(3)) == {0, 1, 2}, 'union with range arg'
assert {1, 2}.union((3, 4)) == {1, 2, 3, 4}, 'union with tuple arg'

# === Update with various iterables ===
s = {1}
s.update((2, 3))
assert s == {1, 2, 3}, 'update with tuple'
s.update(range(4, 6))
assert s == {1, 2, 3, 4, 5}, 'update with range'

# === Frozenset: containment ===
assert 1 in frozenset({1, 2, 3}), 'in frozenset positive'
assert 4 not in frozenset({1, 2, 3}), 'not in frozenset'

# === Frozenset: iteration ===
result = []
for x in frozenset({1, 2, 3}):
    result.append(x)
assert len(result) == 3, 'frozenset iteration length'
assert set(result) == {1, 2, 3}, 'frozenset iteration elements'

# === Frozenset: methods accepting iterables ===
assert frozenset({1, 2}).union([3]) == frozenset({1, 2, 3}), 'frozenset union with list'
assert frozenset({1, 2, 3}).intersection([2, 3]) == frozenset({2, 3}), 'frozenset intersection with list'
assert frozenset({1, 2, 3}).difference([2]) == frozenset({1, 3}), 'frozenset difference with list'
assert frozenset({1, 2}).symmetric_difference([2, 3]) == frozenset({1, 3}), 'frozenset symmetric_difference with list'

# === Nested frozensets as set elements ===
s = {frozenset({1}), frozenset({2})}
assert frozenset({1}) in s, 'frozenset in set positive'
assert frozenset({3}) not in s, 'frozenset in set negative'
assert len(s) == 2, 'set of frozensets len'
