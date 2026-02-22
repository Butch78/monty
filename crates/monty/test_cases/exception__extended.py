# === Exception chaining and handling ===

# Basic try/except
threw = False
try:
    1 / 0
except ZeroDivisionError:
    threw = True
assert threw, 'basic try/except'

# Multiple except clauses
threw_type = None
try:
    int('abc')
except TypeError:
    threw_type = 'type'
except ValueError:
    threw_type = 'value'
assert threw_type == 'value', 'multiple except clauses'

# Except with tuple of types
threw = False
try:
    1 / 0
except (ValueError, ZeroDivisionError):
    threw = True
assert threw, 'except with tuple of types'

# try/except/else
ran_else = False
try:
    x = 42
except ValueError:
    pass
else:
    ran_else = True
assert ran_else, 'else runs when no exception'

# try/except/else - else does NOT run on exception
ran_else = False
try:
    int('bad')
except ValueError:
    pass
else:
    ran_else = True
assert not ran_else, 'else does not run on exception'

# try/except/finally
finally_ran = False
try:
    x = 1
except ValueError:
    pass
finally:
    finally_ran = True
assert finally_ran, 'finally runs after try'

# finally runs even with exception
finally_ran = False
threw = False
try:
    try:
        1 / 0
    except ZeroDivisionError:
        threw = True
    finally:
        finally_ran = True
except:
    pass
assert threw, 'exception caught'
assert finally_ran, 'finally runs after exception'

# Nested try/except
result = None
try:
    try:
        int('bad')
    except TypeError:
        result = 'wrong'
    except ValueError:
        result = 'inner'
except ValueError:
    result = 'outer'
assert result == 'inner', 'nested try catches inner'

# Exception attributes
try:
    raise ValueError('test message')
except ValueError as e:
    assert str(e) == 'test message', 'exception message'
    assert type(e).__name__ == 'ValueError', 'exception type name'

# Raise without message
try:
    raise TypeError()
except TypeError as e:
    assert str(e) == '', 'exception empty message'

# Bare raise (reraise)
caught = False
try:
    try:
        raise ValueError('original')
    except ValueError:
        raise
except ValueError as e:
    caught = True
    assert str(e) == 'original', 'bare raise preserves exception'
assert caught, 'reraised exception caught'

# === Exception hierarchy ===
# All exceptions should be instances of Exception
assert isinstance(ValueError('x'), Exception), 'ValueError is Exception'
assert isinstance(TypeError('x'), Exception), 'TypeError is Exception'
assert isinstance(KeyError('x'), Exception), 'KeyError is Exception'
assert isinstance(IndexError('x'), Exception), 'IndexError is Exception'
assert isinstance(ZeroDivisionError('x'), Exception), 'ZeroDivisionError is Exception'
assert isinstance(OverflowError('x'), Exception), 'OverflowError is Exception'
assert isinstance(RuntimeError('x'), Exception), 'RuntimeError is Exception'
assert isinstance(StopIteration(), Exception), 'StopIteration is Exception'
assert isinstance(AttributeError('x'), Exception), 'AttributeError is Exception'
assert isinstance(NameError('x'), Exception), 'NameError is Exception'
