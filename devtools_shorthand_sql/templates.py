from devtools_shorthand_sql.fields import IDField, BooleanIntField


def insert_with_id(function_name: str, arguments: str, params: str, table_name: str, values: str,
                   field_names: str) -> str:
    text = f'''
def {function_name}({arguments}) -> int:
    params = ({params})
    id = YOUR_CONNECTOR_EXECUTOR("""INSERT INTO {table_name} ({field_names}) VALUES({values});""",
                                 params)
    return id
'''
    return text


def insert_without_id(function_name: str, arguments: str, params: str, table_name: str, values: str,
                      field_names: str) -> str:
    text = f'''
def {function_name}({arguments}) -> None:
    params = ({params})
    YOUR_CONNECTOR_EXECUTOR("""INSERT INTO {table_name} ({field_names}) VALUES({values});""",
                            params)
    return
'''
    return text


def insert_with_id_test(function_name: str, expected: str, table_name: str, kwargs: str) -> str:
    text = f'''
def test_{function_name}(YOUR_CLEAN_DB_FIXTURE):
    expected = {expected}
    new_id = YOUR_MODULE.{function_name}({kwargs})
    result = YOUR_CONNECTOR_QUERY('SELECT * FROM {table_name}').fetchall()[0]
    assert result == expected
    assert new_id == 1
'''
    return text


def insert_without_id_test(function_name: str, expected: str, table_name: str, kwargs: str) -> str:
    text = f'''
def test_{function_name}(YOUR_CLEAN_DB_FIXTURE):
    expected = {expected}
    YOUR_MODULE.{function_name}({kwargs})
    result = YOUR_CONNECTOR_QUERY('SELECT * FROM {table_name}').fetchall()[0]
    assert result == expected
'''
    return text


def create_get_status_function(table_name: str, boolean_field: BooleanIntField, idfield: IDField) -> str:
    text = f'''
def {table_name}_get_{boolean_field.variable_name}_status({idfield.variable_name}: {idfield.type_hint}) -> {boolean_field.type_hint}:
    result = YOUR_CONNECTOR_EXECUTOR("""SELECT {idfield.sql_column_name} FROM {table_name} WHERE {idfield.sql_column_name}=?;""",
                            {idfield.sql_query_param}).fetchall()[0]
    return result
    '''
    return text


# create table statement
'''
CREATE TABLE IF NOT EXISTS photo (
id INTEGER PRIMARY KEY,
size int,
filename text,
date_taken int
);
'''

# get boolean status
'''
CREATE TABLE IF NOT EXISTS photo (
playerid INTEGER PRIMARY KEY,
active boolean
goals int
);
'''

# unit test get boolean status
# update boolean status True
# update boolean status False
# update boolean status
