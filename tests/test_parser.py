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


@pytest.mark.parametrize("content",
[
# Cleanest possible
("""# photo
ID,id
SIZE,int
FILENAME,text
date_taken,int
is_DELeted,boolean"""),
# Drop data before first #
("""well what about this
# photo
ID,id
SIZE,int
FILENAME,text
date_taken,int
is_DELeted,boolean"""),
# Double spacing
# Double lines
("""# photo
ID, id
SIZE,  int
FILENAME,text
date_taken,int
is_DELeted,boolean"""),
# Double lines
("""# photo
ID,id
SIZE,int
FILENAME,text



date_taken,int
is_DELeted,boolean""")
]
)
def test_parse_instructions_into_x(content):
    # This is just a high level test to check that the final output
    # still works after recfactoring.
    result = parser.parse_instructions_into_x(content)
    fields = result[0]['fields']
    assert result[0]['table_name'] == 'photo'
    assert fields[0].field_type == 'INTEGER PRIMARY KEY'
    assert fields[1].field_type == 'INT'
    assert fields[2].field_type == 'TEXT'
    assert fields[3].field_type == 'INT'


@pytest.mark.parametrize("content", [(""), ("this is also notying\nyup yup\n")])
def test_parse_instructions_into_x_fail_empty_contents(content, capfd):
    with pytest.raises(SystemExit):
        parser.parse_instructions_into_x(content)
    out, err = capfd.readouterr()
    assert out == 'Error: No instructions found in file. See documentation for example.\n'


def test_parse_instructions_into_x_fail_not_enough_elements_in_row(capfd):
    content = "# photo\nid,id\nfail"
    with pytest.raises(SystemExit):
        parser.parse_instructions_into_x(content)
    out, err = capfd.readouterr()
    assert out == "Error: Instruction line 2 ['fail'] has 1 element(s). Expected at least 2.\n"
