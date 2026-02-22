# === f-string extended edge cases ===

# Nested expressions
x = 10
assert f'{x + 5}' == '15', 'fstring arithmetic'
assert f'{x * 2 + 1}' == '21', 'fstring complex arithmetic'

# Boolean formatting
assert f'{True}' == 'True', 'fstring True'
assert f'{False}' == 'False', 'fstring False'

# None formatting
assert f'{None}' == 'None', 'fstring None'

# List in fstring
assert f'{[1, 2, 3]}' == '[1, 2, 3]', 'fstring list'
assert f'{[]}' == '[]', 'fstring empty list'

# Dict in fstring (use a variable to avoid parsing ambiguity)
d = {'a': 1}
assert f'{d}' == "{'a': 1}", 'fstring dict via variable'

# Tuple in fstring
assert f'{(1, 2)}' == '(1, 2)', 'fstring tuple'
# Note: single-element tuple formatting (1,) has a known issue in fstrings

# Multiple expressions
a, b = 'hello', 'world'
assert f'{a} {b}' == 'hello world', 'fstring multiple vars'
assert f'{a}{b}' == 'helloworld', 'fstring concatenated vars'

# Format spec with variable width
n = 42
assert f'{n:05d}' == '00042', 'fstring zero padded int'
assert f'{n:>10}' == '        42', 'fstring right aligned'
assert f'{n:<10}' == '42        ', 'fstring left aligned'
assert f'{n:^10}' == '    42    ', 'fstring center aligned'

# Float formatting
pi = 3.14159
assert f'{pi:.2f}' == '3.14', 'fstring float 2 decimals'
assert f'{pi:.0f}' == '3', 'fstring float 0 decimals'
assert f'{pi:10.3f}' == '     3.142', 'fstring float width and precision'

# String repr in fstring
s = 'hello'
assert f'{s!r}' == "'hello'", 'fstring repr conversion'
assert f'{s!s}' == 'hello', 'fstring str conversion'

# Nested quotes
name = 'world'
assert f'hello {name}!' == 'hello world!', 'fstring with punctuation'

# Empty fstring
assert f'' == '', 'empty fstring'

# fstring with only literal text
assert f'literal' == 'literal', 'fstring literal only'

# fstring with escaped braces
assert f'{{}}' == '{}', 'fstring escaped braces'
assert f'{{{x}}}' == '{10}', 'fstring mixed escaped and expression'

# Integer format types
assert f'{255:x}' == 'ff', 'fstring hex format'
assert f'{255:X}' == 'FF', 'fstring upper hex format'
assert f'{255:o}' == '377', 'fstring octal format'
assert f'{255:b}' == '11111111', 'fstring binary format'
assert f'{42:d}' == '42', 'fstring decimal format'

# Sign formatting
assert f'{42:+d}' == '+42', 'fstring positive sign'
assert f'{-42:+d}' == '-42', 'fstring negative sign'
assert f'{42: d}' == ' 42', 'fstring space for positive'
assert f'{-42: d}' == '-42', 'fstring negative with space flag'

# fstring with method call
assert f'{"hello".upper()}' == 'HELLO', 'fstring method call'
assert f'{len("test")}' == '4', 'fstring builtin call'

# fstring with conditional expression
x = 5
assert f'{x if x > 3 else 0}' == '5', 'fstring ternary true'
x = 1
assert f'{x if x > 3 else 0}' == '0', 'fstring ternary false'
