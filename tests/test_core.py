#!/usr/bin/env python
import pytest

import random
import os
import filecmp

from devtools_shorthand_sql import core

random.seed(1234)

@pytest.fixture
def functionbuilder_basic():
    fields = [core.IDField('id', 'test'), core.TextField('COL2', 'test2'),
              core.IntegerField('col1', 'test')]
    sql_writer = core.SQLiteWriter()
    x = core.FunctionBuilder('my_table', fields, sql_writer)
    return x


def test_base_function():
    name, text = 'name', 'text'
    base = core.BaseFunction(name, text)
    assert base.name == name
    assert base.text == text
    assert base.__str__() == text


def test_sql_builder_properties():
    fields = [core.IntegerField('col1', 'test'), core.TextField('COL2', 'test2')]
    sql_writer = core.SQLiteWriter
    x = core.FunctionBuilder('my_table', fields, sql_writer)
    assert x.arguments == 'col1: int, col2: str'
    assert x.field_names == 'col1, COL2'
    assert x.params == 'col1, col2'
    assert x.function_name_stem == 'my_table'
    assert x.has_idfield is False
    assert x.kwargs == 'col1=902, col2="ED73BYDMA9"'


def test_sql_builder_create_table_statement(functionbuilder_basic):
    x = functionbuilder_basic
    result =  x.create_table_statement()
    assert result == 'CREATE TABLE IF NOT EXISTS my_table (\nid test,\nCOL2 test2,\ncol1 test\n);'


def test_sql_builder_create_insert_function_with_id(functionbuilder_basic):
    x = functionbuilder_basic
    result =  x.create_insert_function_with_id()
    assert result.text == '\ndef insert_my_table(id: int, col2: str, col1: int) -> int:\n    params = (id, col2, col1)\n    id = YOUR_CONNECTOR_EXECUTOR("""INSERT INTO my_table (id, COL2, col1) VALUES(?,?,?);""",\n                                 params)\n    return id\n'


def test_sql_builder_create_insert_function_without_id(functionbuilder_basic):
    x = functionbuilder_basic
    result =  x.create_insert_function_without_id()
    assert result.text == '\ndef insert_my_table(id: int, col2: str, col1: int) -> None:\n    params = (id, col2, col1)\n    YOUR_CONNECTOR_EXECUTOR("""INSERT INTO my_table (id, COL2, col1) VALUES(?,?,?);""",\n                            params)\n    return\n'


def test_sql_builder_create_insert_function_with_id_test(functionbuilder_basic):
    expected = """
def test_insert_my_table(YOUR_CLEAN_DB_FIXTURE):
    expected = (1, 'AXRQDZ4S5I', 954)
    new_id = YOUR_MODULE.insert_my_table(col2="AXRQDZ4S5I", col1=954)
    result = YOUR_CONNECTOR_QUERY('SELECT * FROM my_table').fetchall()[0]
    assert result == expected
    assert new_id == 1
"""
    x = functionbuilder_basic
    result =  x.create_insert_function_with_id_test()
    assert result.text == expected


def test_sql_builder_create_insert_function_without_id_test(functionbuilder_basic):
    expected = """
def test_insert_my_table(YOUR_CLEAN_DB_FIXTURE):
    expected = (1, 'CYSB3CK4JX', 409)
    YOUR_MODULE.insert_my_table(col2="CYSB3CK4JX", col1=409)
    result = YOUR_CONNECTOR_QUERY('SELECT * FROM my_table').fetchall()[0]
    assert result == expected
"""
    x = functionbuilder_basic
    result =  x.create_insert_function_without_id_test()
    assert result.text == expected


@pytest.mark.parametrize("source,sql_column_name_format,fixture_file",
[
("""# photo
id,id
SIZE,int
filename,text
date_taken,int""", 'none', 'basic_output.txt'),
("""# photo
id,id
size,int
filename,text
date_taken,int""", 'upper', 'basic_output_upper.txt'),
])
def test_main_pass(tmpdir, source, sql_column_name_format, fixture_file):
    expected = os.path.join('tests', 'fixtures', fixture_file)
    filename = os.path.join(tmpdir, 'shorthand.txt')
    with open(filename, 'w') as f:
        f.write(source)
    output_filename = os.path.join(tmpdir, 'output.txt')
    core.main(filename, 'sqlite', output_filename, sql_column_name_format)
    assert filecmp.cmp(expected, output_filename)
    
