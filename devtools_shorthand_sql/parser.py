from devtools_shorthand_sql.fields import (
    Field,
    BlobField,
    IDField,
    IntegerField,
    RealField,
    TextField,
    BooleanIntField
)


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


# TODO rename
def parse_instructions_into_x(content: str):
    output = []
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
        output.append({'table_name': table_name, 'fields': fields})
    return output