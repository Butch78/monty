from typing import Literal

import pytest
from inline_snapshot import snapshot

import pydantic_monty

PythonVersionStr = Literal['3.10', '3.11', '3.12', '3.13', '3.14']


@pytest.mark.parametrize(
    'version,expected_minor',
    [
        ('3.10', 10),
        ('3.11', 11),
        ('3.12', 12),
        ('3.13', 13),
        ('3.14', 14),
    ],
)
def test_version_info_minor(version: PythonVersionStr, expected_minor: int):
    code = 'import sys\nsys.version_info[1]'
    m = pydantic_monty.Monty(code, python_version=version)
    assert m.run() == expected_minor


@pytest.mark.parametrize(
    'version,expected_version_str',
    [
        ('3.10', '3.10.0 (Monty)'),
        ('3.11', '3.11.0 (Monty)'),
        ('3.12', '3.12.0 (Monty)'),
        ('3.13', '3.13.0 (Monty)'),
        ('3.14', '3.14.0 (Monty)'),
    ],
)
def test_version_string(version: PythonVersionStr, expected_version_str: str):
    code = 'import sys\nsys.version'
    m = pydantic_monty.Monty(code, python_version=version)
    assert m.run() == expected_version_str


def test_default_version_is_3_14():
    code = 'import sys\n(sys.version_info[0], sys.version_info[1])'
    m = pydantic_monty.Monty(code)
    assert m.run() == snapshot((3, 14))


def test_version_info_full_tuple():
    code = """\
import sys
v = sys.version_info
(v[0], v[1], v[2], v[3], v[4])
"""
    m = pydantic_monty.Monty(code, python_version='3.12')
    assert m.run() == snapshot((3, 12, 0, 'final', 0))


def test_version_info_named_attributes():
    code = """\
import sys
v = sys.version_info
(v.major, v.minor, v.micro, v.releaselevel, v.serial)
"""
    m = pydantic_monty.Monty(code, python_version='3.11')
    assert m.run() == snapshot((3, 11, 0, 'final', 0))


def test_invalid_version_raises_value_error():
    with pytest.raises(ValueError) as exc_info:
        pydantic_monty.Monty('1 + 1', python_version='3.9')  # pyright: ignore[reportArgumentType]
    assert exc_info.value.args[0] == snapshot(
        "unsupported python_version '3.9', expected one of: '3.10', '3.11', '3.12', '3.13', '3.14'"
    )


def test_invalid_version_format_raises_value_error():
    with pytest.raises(ValueError) as exc_info:
        pydantic_monty.Monty('1 + 1', python_version='invalid')  # pyright: ignore[reportArgumentType]
    assert exc_info.value.args[0] == snapshot(
        "unsupported python_version 'invalid', expected one of: '3.10', '3.11', '3.12', '3.13', '3.14'"
    )


def test_none_version_uses_default():
    code = 'import sys\nsys.version_info[1]'
    m = pydantic_monty.Monty(code, python_version=None)
    assert m.run() == snapshot(14)
