#!/usr/bin/env python
import pytest

from devtools_shorthand_sql import core


def test_map_raw_field_data_type():
    # field type exists, upper
    result = core.map_raw_field_data_type('INT')
    assert result == 'INT'
    # field type exists, lower
    result = core.map_raw_field_data_type('int')
    assert result == 'INT'
    # field does not exist
    with pytest.raises(KeyError):
        result = core.map_raw_field_data_type('no')


def test_base_function():
    name, text = 'name', 'text'
    base = core.BaseFunction(name, text)
    assert base.name == name
    assert base.text == text
    assert base.__str__() == text
