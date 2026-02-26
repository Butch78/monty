# === print() with sep keyword ===
# print returns None
result = print('a', 'b', sep='-')
assert result is None, 'print with sep returns None'

# print with custom end
result = print('hello', end='')
assert result is None, 'print with end returns None'

# print with both sep and end
result = print('x', 'y', 'z', sep=', ', end='!\n')
assert result is None, 'print with sep and end returns None'

# print with sep=None (should use default space)
result = print('a', 'b', sep=None)
assert result is None, 'print with sep=None returns None'

# print with end=None (should use default newline)
result = print('hello', end=None)
assert result is None, 'print with end=None returns None'

# print with flush (accepted but ignored)
result = print('test', flush=True)
assert result is None, 'print with flush returns None'

result = print('test', flush=False)
assert result is None, 'print with flush=False returns None'

# print with no args
result = print()
assert result is None, 'print no args returns None'

# print with various types
result = print(1, 2.5, True, None, [1, 2], (3,), {'a': 1})
assert result is None, 'print various types returns None'

# print with empty sep
result = print('a', 'b', 'c', sep='')
assert result is None, 'print empty sep returns None'

# print with empty end
result = print('line', end='')
assert result is None, 'print empty end returns None'

# === print() error cases ===

# print with non-string sep
threw = False
try:
    print('a', 'b', sep=42)
except TypeError as e:
    threw = True
    assert 'sep must be None or a string' in str(e), f'wrong error msg: {e}'
assert threw, 'print non-string sep raises TypeError'

# print with non-string end
threw = False
try:
    print('a', end=42)
except TypeError as e:
    threw = True
    assert 'end must be None or a string' in str(e), f'wrong error msg: {e}'
assert threw, 'print non-string end raises TypeError'
