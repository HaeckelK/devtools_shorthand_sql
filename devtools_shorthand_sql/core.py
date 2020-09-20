"""Main module."""
from typing import List, Optional

from devtools_shorthand_sql.fields import (  # noqa: F401
    Field,
    BlobField,
    IDField,
    IntegerField,
    RealField,
    TextField,
    BooleanIntField
)
import devtools_shorthand_sql.templates as templates
from devtools_shorthand_sql.parser import parse_instructions_into_x
from devtools_shorthand_sql.utils import fatal_error, info_message


def load_instructions_file(filename: str) -> str:
    try:
        with open(filename, 'r') as f:
            contents = f.read()
    except FileNotFoundError:
        fatal_error(f'File does not exist {filename}.')
    return contents


# Generated functions
class BaseFunction():
    function_type = 'base_class_none'

    def __init__(self, name: str, text: str):
        self.name = name
        self.text = text

    def __str__(self) -> str:
        return self.text


class UnitTest(BaseFunction):
    function_type = 'unit_test'


class Function(BaseFunction):
    function_type = 'function'


# TODO this is a function builder, which has a SQL generator attached.
# TODO some way to decide on which methods to use e.g. with it or without. Builder pattern maybe.
# TODO sort of dependency with templates
class SQLBuilder():
    value_char = '?'

    def __init__(self, table_name: str, fields: List[Field]):
        self.table_name = table_name
        self.fields = fields

        self.creation_statement: Optional[str] = None
        self.insert_function: Optional[Function] = None
        self.insert_function_test: Optional[UnitTest] = None
        # boolean_functions will include function and unit test
        self.boolean_functions: List[Function] = []
        return

    @property
    def arguments(self) -> str:
        return ', '.join([field.function_arg for field in self.fields if field.function_arg != ''])

    @property
    def field_names(self) -> str:
        return ', '.join([field.sql_column_name for field in self.fields])

    @property
    def params(self) -> str:
        return ', '.join([field.sql_query_param for field in self.fields])

    @property
    def values(self) -> str:
        return ','.join([self.value_char]*len(self.fields))

    @property
    def function_name_stem(self) -> str:
        return self.table_name.lower()

    @property
    def kwargs(self) -> str:
        kwargs = []
        for field in self.fields:
            if isinstance(field, IDField):
                continue
            # TODO move this into Field
            kwarg = field.variable_name + '=' + str(field.function_kwarg)
            kwargs.append(kwarg)
        return ', '.join(kwargs)

    @property
    def has_idfield(self) -> bool:
        for field in self.fields:
            if isinstance(field, IDField):
                return True
        return False

    # TODO this needs to check a more general BooleanField
    @property
    def boolean_fields(self) -> List[BooleanIntField]:
        return [f for f in self.fields if isinstance(f, BooleanIntField)]

    def create_table_statement(self) -> str:
        sql_lines = ''
        for field in self.fields:
            line = field.sql_column_name + ' ' + field.field_type + ','
            sql_lines += line + '\n'
        sql_lines = sql_lines[:-2]
        sql = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (\n{sql_lines}\n);"""
        self.creation_statement = sql
        return sql

    def create_insert_function_with_id(self) -> Function:
        function_name = f'insert_{self.function_name_stem}'
        insert_function = templates.insert_with_id(function_name, self.arguments,
                                                   self.params, self.table_name,
                                                   self.values, self.field_names)
        function = Function(function_name, insert_function)
        self.insert_function = function
        return function

    def create_insert_function_without_id(self) -> Function:
        function_name = f'insert_{self.function_name_stem}'
        insert_function = templates.insert_without_id(function_name, self.arguments,
                                                      self.params, self.table_name,
                                                      self.values, self.field_names)
        function = Function(function_name, insert_function)
        self.insert_function = function
        return function

    def create_insert_function_with_id_test(self) -> UnitTest:
        function_name = f'insert_{self.function_name_stem}'
        expected = tuple(field.test_default for field in self.fields)
        function_text = templates.insert_with_id_test(function_name, expected, self.table_name, self.kwargs)
        function = UnitTest(function_name, function_text)
        self.insert_function_test = function
        return function

    def create_insert_function_without_id_test(self) -> UnitTest:
        function_name = f'insert_{self.function_name_stem}'
        expected = tuple(field.test_default for field in self.fields)
        function_text = templates.insert_without_id_test(function_name, expected, self.table_name, self.kwargs)
        function = UnitTest(function_name, function_text)
        self.insert_function_test = function
        return function

    # TODO this should just be BooleanField as type
    def create_get_status_function(self, field: BooleanIntField, idfield: IDField) -> Function:
        function = templates.create_get_status_function(self.table_name, field, idfield)
        self.boolean_functions.append(function)
        return function


class PostgresSQLBuilder(SQLBuilder):
    value_char = '%s'


def save_builders_to_file(builders: List[SQLBuilder], filename: str) -> None:
    with open(filename, 'w') as f:
        for builder in builders:
            f.write(f'# Table Name: {builder.table_name}')
            f.write('\n\n## Creation Statement\n')
            f.write(builder.creation_statement)
            f.write('\n\n## Insert Function\n')
            f.write(str(builder.insert_function))
            f.write('\n\n## Insert Function Unit Test\n')
            f.write(str(builder.insert_function_test))
            f.write('\n\n## Boolean Fields\n')
            for function in builder.boolean_functions:
                f.write(str(function))
    info_message(f'Output saved to: {filename}')
    return


def main(filename: str, sql_type: str, output_filename: str):
    content = load_instructions_file(filename)
    # TODO rename
    packet = parse_instructions_into_x(content)
    builders: List[SQLBuilder] = []
    for item in packet:
        table_name = item['table_name']
        fields = item['fields']

        if sql_type == 'postgres':
            builder = PostgresSQLBuilder(table_name, fields)
        else:
            builder = SQLBuilder(table_name, fields)

        builders.append(builder)

        builder.create_table_statement()
        if builder.has_idfield:
            builder.create_insert_function_with_id()
            builder.create_insert_function_with_id_test()
        else:
            builder.create_insert_function_without_id()
            builder.create_insert_function_without_id_test()

        for boolean_field in builder.boolean_fields:
            # TODO this is not generic, how to get idfield normally? may not exist.
            idfield = builder.fields[0]
            builder.create_get_status_function(boolean_field, idfield)
            # unit test
            # builder.create update
            # no unit test make it a private functino
            # builder.create update true
            # unit test
            # builder.create update False
            # unit test
    save_builders_to_file(builders, output_filename)
    return
