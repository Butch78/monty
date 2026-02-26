# === ord() error cases ===

# ord with empty string
threw = False
try:
    ord('')
except TypeError as e:
    threw = True
    assert str(e) == 'ord() expected a character, but string of length 0 found', f'wrong msg: {e}'
assert threw, 'ord empty string raises TypeError'

# ord with multi-char string
threw = False
try:
    ord('ab')
except TypeError as e:
    threw = True
    assert str(e) == 'ord() expected a character, but string of length 2 found', f'wrong msg: {e}'
assert threw, 'ord multi-char raises TypeError'

# ord with long string
threw = False
try:
    ord('hello')
except TypeError as e:
    threw = True
    assert str(e) == 'ord() expected a character, but string of length 5 found', f'wrong msg: {e}'
assert threw, 'ord long string raises TypeError'

# ord with wrong type - int
threw = False
try:
    ord(42)
except TypeError as e:
    threw = True
    assert 'ord() expected string of length 1' in str(e), f'wrong msg: {e}'
assert threw, 'ord int raises TypeError'

# ord with wrong type - list
threw = False
try:
    ord([1])
except TypeError as e:
    threw = True
    assert 'ord() expected string of length 1' in str(e), f'wrong msg: {e}'
assert threw, 'ord list raises TypeError'

# ord with wrong type - None
threw = False
try:
    ord(None)
except TypeError as e:
    threw = True
    assert 'ord() expected string of length 1' in str(e), f'wrong msg: {e}'
assert threw, 'ord None raises TypeError'

# ord with heap-allocated string (dynamic string)
s = 'h' + 'i'
threw = False
try:
    ord(s)
except TypeError as e:
    threw = True
    assert str(e) == 'ord() expected a character, but string of length 2 found', f'wrong msg: {e}'
assert threw, 'ord heap-allocated multi-char raises TypeError'

# ord with heap-allocated single char
s = chr(65)
assert ord(s) == 65, 'ord of heap-allocated single char'
