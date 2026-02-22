import sys

vi = sys.version_info

# === len() on namedtuple ===
assert len(vi) == 5, 'namedtuple len is 5'

# === bool() on namedtuple ===
assert bool(vi) == True, 'namedtuple is truthy'

# === indexing ===
assert vi[0] == vi.major, 'namedtuple index 0 matches .major'
assert vi[1] == vi.minor, 'namedtuple index 1 matches .minor'
assert vi[2] == vi.micro, 'namedtuple index 2 matches .micro'
assert vi[3] == vi.releaselevel, 'namedtuple index 3 matches .releaselevel'
assert vi[4] == vi.serial, 'namedtuple index 4 matches .serial'

# === negative indexing ===
assert vi[-1] == vi.serial, 'namedtuple index -1'
assert vi[-2] == vi.releaselevel, 'namedtuple index -2'
assert vi[-5] == vi.major, 'namedtuple index -5'

# === index out of bounds ===
threw = False
try:
    vi[5]
except IndexError:
    threw = True
assert threw, 'namedtuple index 5 out of bounds'

threw = False
try:
    vi[-6]
except IndexError:
    threw = True
assert threw, 'namedtuple index -6 out of bounds'

# === type error on non-int index ===
threw = False
try:
    vi['major']
except TypeError:
    threw = True
assert threw, 'namedtuple string index raises TypeError'

# === attribute access ===
assert isinstance(vi.major, int), 'major is int'
assert isinstance(vi.minor, int), 'minor is int'
assert isinstance(vi.releaselevel, str), 'releaselevel is str'

# === attribute error ===
threw = False
try:
    vi.nonexistent
except AttributeError:
    threw = True
assert threw, 'namedtuple nonexistent attr raises AttributeError'

# === equality comparisons ===
# namedtuple == tuple
t = (vi[0], vi[1], vi[2], vi[3], vi[4])
assert vi == t, 'namedtuple equals tuple'
assert t == vi, 'tuple equals namedtuple'

# different lengths
assert vi != (1, 2), 'namedtuple != shorter tuple'
assert vi != (1, 2, 3, 4, 5, 6), 'namedtuple != longer tuple'

# cross-type inequality
assert vi != 42, 'namedtuple != int'
assert vi != 'hello', 'namedtuple != str'
assert vi != [1, 2, 3, 4, 5], 'namedtuple != list'
assert vi != {1: 2}, 'namedtuple != dict'
assert vi != None, 'namedtuple != None'

# === repr ===
r = repr(vi)
assert 'sys.version_info' in r, f'namedtuple repr contains type name: {r!r}'
assert 'major=' in r, f'namedtuple repr contains field names: {r!r}'
