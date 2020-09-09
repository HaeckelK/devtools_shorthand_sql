"""Main module."""
import argparse
from typing import List

from devtools_shorthand_sql.fields import (
    Field,
    BlobField,
    IDField,
    IntegerField,
    RealField,
    TextField,
    BooleanIntField
)
import devtools_shorthand_sql.templates as templates


def load_instructions_file(filename: str) -> str:
    with open(filename, 'r') as f:
        contents = f.read()
    return contents


def map_raw_field_data_type(raw_field_data_type):
    # TODO mapping non sqlite to sqlite
    value = raw_field_data_type.upper()
    mapping = {'INT': 'INT',
               'INTEGER': 'INT',
               'INTEGER': 'INT',
               'TINYINT': 'INT',
               'SMALLINT': 'INT',
               'MEDIUMINT': 'INT',
               'BIGINT': 'INT',
               'UNSIGNED BIG INT': 'INT',
               'INT2': 'INT',
               'INT8': 'INT',
               'ID': 'INTEGER PRIMARY KEY',
               'INTEGER PRIMARY KEY': 'INTEGER PRIMARY KEY',
               'TEXT': 'TEXT',
               'BOOLEAN': 'BOOLEAN',
               'BOOL': 'BOOLEAN'}
    mapped = mapping[value]
    return mapped


# TODO rename
def get_field(field_name, field_data_type):
    mapping = {'INT': IntegerField,
               'TEXT': TextField,
               'INTEGER PRIMARY KEY': IDField,
               'BOOLEAN': BooleanIntField}
    f = mapping.get(field_data_type, Field)
    field = f(field_name, field_data_type)
    return field


# TODO this is a function builder, which has a SQL generator attached.
# TODO some way to decide on which methods to use e.g. with it or without. Builder pattern maybe.
# TODO sort of dependency with templates
class SQLBuilder():
    value_char = '?'
    def __init__(self, table_name: str, fields: List[Field]):
        self.table_name = table_name
        self.fields = fields

        self.creation_statement = None
        self.insert_function = None
        self.insert_function_test = None
        return

    @property
    def arguments(self):
        return ', '.join([field.arg for field in self.fields if field.arg != ''])

    @property
    def field_names(self):
        return ', '.join([field.name for field in self.fields])

    @property
    def params(self):
        return ', '.join([field.param for field in self.fields])

    @property
    def values(self):
        return ','.join([self.value_char]*len(self.fields))

    @property
    def function_name_stem(self):
        return self.table_name.lower()

    @property
    def kwargs(self):
        kwargs = []
        for field in self.fields:
            if isinstance(field, IDField):
                continue
            kwarg = field.name + '=' + str(field.kwarg)
            kwargs.append(kwarg)
        return ', '.join(kwargs)

    @property
    def has_idfield(self):
        for field in self.fields:
            if isinstance(field, IDField):
                return True
        return False

    def create_table_statement(self) -> str:
        sql_lines = ''
        for field in self.fields:
            line = field.name + ' ' + field.field_type + ','
            sql_lines += line + '\n'
        sql_lines = sql_lines[:-2]
        sql = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (\n{sql_lines}\n);"""
        self.creation_statement = sql
        return sql

    def create_insert_function_with_id(self) -> str:
        function_name = f'insert_{self.function_name_stem}'
        insert_function = templates.insert_with_id(function_name, self.arguments,
                                                   self.params, self.table_name,
                                                   self.values, self.field_names)
        self.insert_function = insert_function
        return insert_function

    def create_insert_function_without_id(self) -> str:
        function_name = f'insert_{self.function_name_stem}'
        insert_function = templates.insert_without_id(function_name, self.arguments,
                                                      self.params, self.table_name,
                                                      self.values, self.field_names)
        self.insert_function = insert_function
        return insert_function

    def create_insert_function_with_id_test(self) -> str:
        function_name = f'insert_{self.function_name_stem}'
        expected = tuple(field.test_default for field in self.fields)
        function = templates.insert_with_id_test(function_name, expected, self.table_name, self.kwargs)
        self.insert_function_test = function
        return function

    def create_insert_function_without_id_test(self) -> str:
        function_name = f'insert_{self.function_name_stem}'
        expected = tuple(field.test_default for field in self.fields)
        function = templates.insert_without_id_test(function_name, expected, self.table_name, self.kwargs)
        self.insert_function_test = function
        return function


class PostgresSQLBuilder(SQLBuilder):
    value_char = '%s' 


def main(filename: str, sql_type: str):
    content = load_instructions_file(filename)

    # get separate instructions
    raw_instructions = content.split('#')
    for raw_instruction in raw_instructions:
        # Tiny pre process
        raw_instruction.replace('  ', ' ')
        #print(raw_instruction)
        # Individual elements
        raw_lines = raw_instruction.split('\n')
        # basic pre process
        lines = [x.strip() for x in raw_lines]
        #print(lines)
        # TODO assumed its a table instruction
        if not lines[0].lower().startswith('table'):
            continue
        table_name = lines[0].replace('table', '').strip()
        raw_fields = [x.split(' ') for x in lines[1:]]
        fields = []
        for raw_field in raw_fields:
            if len(raw_field) != 2:
                continue
            raw_field_data_type = raw_field[1]
            field_name = raw_field[0]
            field_data_type = map_raw_field_data_type(raw_field_data_type)
            field = get_field(field_name, field_data_type)
            fields.append(field)
        for field in fields:
            field.lowercase()
        
        if sql_type == 'postgres':
            builder = PostgresSQLBuilder(table_name, fields)
        else:
            builder = SQLBuilder(table_name, fields)

        builder.create_table_statement()
        if builder.has_idfield:
            builder.create_insert_function_with_id()
            builder.create_insert_function_with_id_test()
        else:
            builder.create_insert_function_without_id()
            builder.create_insert_function_without_id_test()

        print('\n')
        print(builder.creation_statement)
        print('\n')
        print(builder.insert_function)
        print('\n')
        print(builder.insert_function_test)
    return
