"""
Test our two JSON serializers (orjson, and Python's built-in json module).

Need to ensure that we get the same output regardless of the serializer used.
"""

import sys
from datetime import date, datetime

import numpy as np
import pytest

try:
    # try to import module, only run test if succeeded
    import orjson  # noqa: F401
except ImportError:
    pass


@pytest.mark.skipif('orjson' not in sys.modules, reason='requires the orjson library.')
def test_json():
    # only run test if orjson is available to not break it on 32 bit systems
    # or architectures where orjson is not supported.

    # pylint: disable=import-outside-toplevel
    from nicegui.json.builtin_wrapper import dumps as builtin_dumps
    from nicegui.json.orjson_wrapper import dumps as orjson_dumps

    # test different scalar and array types
    tests = [
        None,
        'text',
        True,
        1.0,
        1,
        [],
        dict(),
        dict(key1='value1', key2=1),
        date(2020, 1, 31),
        datetime(2020, 1, 31, 12, 59, 59, 123456),
        [1.0, -3, 0],
        ['test', '€'],
        [0, None, False, np.pi, 'text', date(2020, 1, 31), datetime(2020, 1, 31, 12, 59, 59, 123456), np.array([1.0])],
        np.array([1.0, 0]),
        np.array([0, False, np.pi]),
        np.array(['2010-10-17 07:15:30', '2011-05-13 08:20:35', '2013-01-15 09:09:09'], dtype=np.datetime64),
        np.array([1.0, None, 'test'], dtype=np.object_)
    ]

    for test in tests:
        orjson_str = orjson_dumps(test)
        builtin_str = builtin_dumps(test)
        assert orjson_str == builtin_str, f'json serializer implementations do not match: orjson={orjson_str}, built-in={builtin_str}'
