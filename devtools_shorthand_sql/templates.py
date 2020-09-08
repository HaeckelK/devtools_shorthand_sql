

def insert_with_id(function_name: str, arguments: str, params: str, table_name: str, values: str,
                   field_names: str):
    text = f'''
def {function_name}({arguments}) -> int:
    params = ({params})
    id = YOUR_CONNECTOR_EXECUTOR("""INSERT INTO {table_name} ({field_names}) VALUES({values});""",
                                 params)
    return id
'''
    return text


def insert_without_id(function_name: str, arguments: str, params: str, table_name: str, values: str,
                      field_names: str):
    text = f'''
def {function_name}({arguments}) -> None:
    params = ({params})
    YOUR_CONNECTOR_EXECUTOR("""INSERT INTO {table_name} ({field_names}) VALUES({values});""",
                            params)
    return
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

# unit test insert template with id
'''
def test_insert_photo(YOUR_CLEAN_DB_FIXTURE):
    expected = (1, 999, '123fakestreet', 999)
    new_id = YOUR_MODULE.insert_photo(size=999, filename="123fakestreet", date_taken=999)
    result = YOUR_CONNECTOR_QUERY('SELECT * FROM photo').fetchall()[0]
    assert result == expected
    assert new_id == 1
'''

# insert template without id
'''
def insert_photo(size: int, filename: str, date_taken: int) -> int:
    params = (size, filename, date_taken)
    YOUR_CONNECTOR_EXECUTOR("""INSERT INTO photo (size, filename, date_taken) VALUES(?,?,?,?);""",
                            params)
    return
'''

# unit test insert template without id
'''
def test_insert_photo(YOUR_CLEAN_DB_FIXTURE):
    expected = (999, '123fakestreet', 999)
    YOUR_MODULE.insert_photo(size=999, filename="123fakestreet", date_taken=999)
    result = YOUR_CONNECTOR_QUERY('SELECT * FROM photo').fetchall()[0]
    assert result == expected
'''

# get boolean status
'''
CREATE TABLE IF NOT EXISTS photo (
playerid INTEGER PRIMARY KEY,
active boolean
goals int
);
'''
'''
def player_get_active_status(playerid: int) -> None:
    YOUR_CONNECTOR_EXECUTOR("""SELECT active FROM player WHERE playerid=?;""",
                            playerid)
    result = YOUR_CONNECTOR_QUERY('SELECT * FROM photo').fetchall()[0]
    return    
'''
# unit test get boolean status
# update boolean status True
# update boolean status False
# update boolean status