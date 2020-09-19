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
    # This is just a high level test to check that the final output
    # still works after recfactoring.
    content = """# table photo
ID id
SIZE int
FILENAME text
date_taken int
is_DELeted boolean"""
    result = parser.parse_instructions_into_x(content)
    fields = result[0]['fields']
    assert result[0]['table_name'] == 'photo'
    assert fields[0].field_type == 'INTEGER PRIMARY KEY'
    assert fields[1].field_type == 'INT'
    assert fields[2].field_type == 'TEXT'
    assert fields[3].field_type == 'INT'