# === List slicing ===
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Basic slicing
assert lst[2:5] == [2, 3, 4], 'list slice basic'
assert lst[:3] == [0, 1, 2], 'list slice from start'
assert lst[7:] == [7, 8, 9], 'list slice to end'
assert lst[:] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 'list slice full copy'

# Negative indices
assert lst[-3:] == [7, 8, 9], 'list slice negative start'
assert lst[:-3] == [0, 1, 2, 3, 4, 5, 6], 'list slice negative end'
assert lst[-5:-2] == [5, 6, 7], 'list slice both negative'

# Step slicing
assert lst[::2] == [0, 2, 4, 6, 8], 'list slice step 2'
assert lst[1::2] == [1, 3, 5, 7, 9], 'list slice odd indices'
assert lst[::-1] == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0], 'list slice reverse'
assert lst[::3] == [0, 3, 6, 9], 'list slice step 3'
assert lst[::-2] == [9, 7, 5, 3, 1], 'list slice reverse step 2'

# Out-of-bounds slicing (no error, just clamp)
assert lst[5:100] == [5, 6, 7, 8, 9], 'list slice beyond end'
assert lst[-100:3] == [0, 1, 2], 'list slice beyond start'
assert lst[100:200] == [], 'list slice completely out of range'

# Empty slices
assert lst[5:5] == [], 'list slice equal indices'
assert lst[5:3] == [], 'list slice start > end'

# === String slicing ===
s = 'hello world'
assert s[0:5] == 'hello', 'string slice word'
assert s[6:] == 'world', 'string slice from middle'
assert s[:5] == 'hello', 'string slice to middle'
assert s[::-1] == 'dlrow olleh', 'string reverse'
assert s[::2] == 'hlowrd', 'string step 2'
assert s[-5:] == 'world', 'string negative slice'

# === Tuple slicing ===
t = (0, 1, 2, 3, 4)
assert t[1:3] == (1, 2), 'tuple slice'
assert t[::-1] == (4, 3, 2, 1, 0), 'tuple reverse'
assert t[::2] == (0, 2, 4), 'tuple step'

# === Bytes slicing ===
b = b'hello'
assert b[1:3] == b'el', 'bytes slice'
assert b[::-1] == b'olleh', 'bytes reverse'

# === Slice edge cases ===
# Empty list slicing
empty = []
assert empty[:] == [], 'empty list slice'
assert empty[1:5] == [], 'empty list slice range'

# Single element
single = [42]
assert single[0:1] == [42], 'single element slice'
assert single[::-1] == [42], 'single element reverse'

# String empty slice
assert ''[:] == '', 'empty string slice'
assert 'a'[::-1] == 'a', 'single char reverse'
