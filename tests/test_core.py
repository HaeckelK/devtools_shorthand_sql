#!/usr/bin/env python
import pytest

import random
import os

from devtools_shorthand_sql import core

random.seed(1234)

@pytest.fixture
def sqlbuilder_basic():
    fields = [core.IDField('id', 'test'), core.TextField('COL2', 'test2'),
              core.IntegerField('col1', 'test')]
    x = core.SQLBuilder('my_table', fields)
    return x


def test_load_instructions_file(tmpdir):
    text = '123\n456'
    filename = os.path.join(tmpdir, 'test.txt')
    with open(filename, 'w') as f:
        f.write(text)
    assert core.load_instructions_file(filename) == text


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


def test_sql_builder_properties():
    fields = [core.IntegerField('col1', 'test'), core.TextField('COL2', 'test2')]
    x = core.SQLBuilder('my_table', fields)
    assert x.arguments == 'col1: int, col2: str'
    assert x.field_names == 'col1, COL2'
    assert x.params == 'col1, col2'
    assert x.values == '?,?'
    assert x.function_name_stem == 'my_table'
    assert x.has_idfield is False
    assert x.kwargs == 'col1=902, col2="ED73BYDMA9"'


def test_sql_builder_create_table_statement(sqlbuilder_basic):
    x = sqlbuilder_basic
    result =  x.create_table_statement()
    assert result == 'CREATE TABLE IF NOT EXISTS my_table (\nid test,\nCOL2 test2,\ncol1 test\n);'


def test_sql_builder_create_insert_function_with_id(sqlbuilder_basic):
    x = sqlbuilder_basic
    result =  x.create_insert_function_with_id()
    assert result.text == '\ndef insert_my_table(id: int, col2: str, col1: int) -> int:\n    params = (id, col2, col1)\n    id = YOUR_CONNECTOR_EXECUTOR("""INSERT INTO my_table (id, COL2, col1) VALUES(?,?,?);""",\n                                 params)\n    return id\n'


def test_sql_builder_create_insert_function_without_id(sqlbuilder_basic):
    x = sqlbuilder_basic
    result =  x.create_insert_function_without_id()
    assert result.text == '\ndef insert_my_table(id: int, col2: str, col1: int) -> None:\n    params = (id, col2, col1)\n    YOUR_CONNECTOR_EXECUTOR("""INSERT INTO my_table (id, COL2, col1) VALUES(?,?,?);""",\n                            params)\n    return\n'


def test_sql_builder_create_insert_function_with_id_test(sqlbuilder_basic):
    expected = """
def test_insert_my_table(YOUR_CLEAN_DB_FIXTURE):
    expected = (1, 'AXRQDZ4S5I', 954)
    new_id = YOUR_MODULE.insert_my_table(col2="AXRQDZ4S5I", col1=954)
    result = YOUR_CONNECTOR_QUERY('SELECT * FROM my_table').fetchall()[0]
    assert result == expected
    assert new_id == 1
"""
    x = sqlbuilder_basic
    result =  x.create_insert_function_with_id_test()
    assert result.text == expected


def test_sql_builder_create_insert_function_without_id_test(sqlbuilder_basic):
    expected = """
def test_insert_my_table(YOUR_CLEAN_DB_FIXTURE):
    expected = (1, 'CYSB3CK4JX', 409)
    YOUR_MODULE.insert_my_table(col2="CYSB3CK4JX", col1=409)
    result = YOUR_CONNECTOR_QUERY('SELECT * FROM my_table').fetchall()[0]
    assert result == expected
"""
    x = sqlbuilder_basic
    result =  x.create_insert_function_without_id_test()
    assert result.text == expected
