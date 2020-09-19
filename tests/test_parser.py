#!/usr/bin/env python
import pytest

from devtools_shorthand_sql import parser


def test_map_raw_field_data_type():
    # field type exists, upper
    result = parser.map_raw_field_data_type('INT')
    assert result == 'INT'
    # field type exists, lower
    result = parser.map_raw_field_data_type('int')
    assert result == 'INT'
    # field does not exist
    with pytest.raises(KeyError):
        result = parser.map_raw_field_data_type('no')


def test_parse_instructions_into_x():
    content = """# table photo
ID id
SIZE int
FILENAME text
date_taken int
is_DELeted boolean"""
    result = parser.parse_instructions_into_x(content)
