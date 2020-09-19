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
from devtools_shorthand_sql.utils import fatal_error


def map_raw_field_data_type(raw_field_data_type):
    """
    Map a raw input field to an sql field type.

    Raises
    ------
    KeyError:
        If raw field not in mapping.
    """
    # TODO mapping non sqlite to sqlite
    value = raw_field_data_type.upper()
    mapping = {'INT': 'INT',
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


def _clean_raw_content(content: str) -> str:
    content = content.strip()
    content = content.replace('  ', ' ')
    content = content.replace(', ', ',')
    content = content.replace('\n\n', '\n')
    content = content.replace('\n \n', '\n')
    return content


def _split_content_into_instruction_sections(content: str) -> List[str]:
    marker = '#'
    if not marker in content:
        fatal_error('No instructions found in file. See documentation for example.')
    # instruction sections start with marker, anything before should be dropped
    content = content[content.find(marker):]
    sections = [x for x in content.split(marker) if (len(x) != 0 and x != '')]
    return sections


def _process_raw_instruction(raw_instruction: str):
    raw_lines = raw_instruction.split('\n')
    lines = [x.strip() for x in raw_lines]
    table_name = lines[0].strip()
    raw_fields = [x.split(',') for x in lines[1:]]
    fields = []
    for i, raw_field in enumerate(raw_fields):
        if len(raw_field) < 2:
            fatal_error(f'Instruction line {i + 1} {raw_field} has {len(raw_field)} elements. Expected at least 2.')
        raw_field_data_type = raw_field[1]
        field_name = raw_field[0]
        field_data_type = map_raw_field_data_type(raw_field_data_type)
        field = get_field(field_name, field_data_type)
        fields.append(field)
    return {'table_name': table_name, 'fields': fields}


# TODO rename
def parse_instructions_into_x(content: str):
    output = []
    clean_content = _clean_raw_content(content)
    raw_instructions = _split_content_into_instruction_sections(content)
    for i, raw_instruction in enumerate(raw_instructions):
        instruction_data = _process_raw_instruction(raw_instruction)
        output.append(instruction_data)
    return output