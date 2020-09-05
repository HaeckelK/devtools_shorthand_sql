"""Main module."""
import argparse
from typing import List


def load_instructions_file(filename: str) -> str:
    with open(filename, 'r') as f:
        contents = f.read()
    return contents


class Field():
    def __init__(self, name, field_type):
        self.name = name
        self.field_type = field_type
        return

    def lowercase(self):
        self.name = self.name.lower()
        return

    def uppercase(self):
        self.name = self.name.upper()
        return


class SQLBuilder():
    value_char = '?'
    def __init__(self, table_name: str, fields: List[Field]):
        self.table_name = table_name
        self.fields = fields
        return

    def create_table_statement(self) -> str:
        sql_lines = ''
        for field in self.fields:
            line = field.name + ' ' + field.field_type + ','
            sql_lines += line + '\n'
        sql_lines = sql_lines[:-2]
        sql = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (\n{sql_lines}\n);"""
        return sql

    def create_insert_statement(self) -> str:
        # TODO is this a valid def name?
        function_name = f'insert_{self.table_name.lower()}'
        field_names = ', '.join([field.name for field in self.fields])
        arguments = ', '.join([field.name for field in self.fields[1:]])
        values = ','.join([self.value_char]*len(self.fields))
        sql = f"""INSERT INTO {self.table_name} ({field_names}) VALUES({values});"""
        # TODO None is for the id field which might not be present
        params = '(None, ' + arguments + ')'
        definition = f'def {function_name}({arguments}):'
        return sql, params, definition, function_name


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
        fields = [Field('id', 'INTEGER PRIMARY KEY')]
        for raw_field in raw_fields:
            if len(raw_field) != 2:
                continue
            field = Field(raw_field[0], raw_field[1])
            fields.append(field)
        for field in fields:
            field.lowercase()
        
        if sql_type == 'postgres':
            builder = PostgresSQLBuilder(table_name, fields)
        else:
            builder = SQLBuilder(table_name, fields)

        table_sql = builder.create_table_statement()
        insert_sql, params, definition, function_name = builder.create_insert_statement()
        print('\n')
        print(table_sql)
        print('\n')
        print(definition)
        print(insert_sql)
        print(params)
    return
