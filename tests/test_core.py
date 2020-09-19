#!/usr/bin/env python
import pytest

import random

from devtools_shorthand_sql import core

random.seed(1234)

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


def test_sql_builder():
    fields = [core.IntegerField('col1', 'test'), core.TextField('COL2', 'test2')]
    x = core.SQLBuilder('my_table', fields)
    assert x.arguments == 'col1: int, col2: str'
    assert x.field_names == 'col1, COL2'
    assert x.params == 'col1, col2'
    assert x.values == '?,?'
    assert x.function_name_stem == 'my_table'
    assert x.has_idfield is False
    assert x.kwargs == 'col1=902, col2="ED73BYDMA9"'