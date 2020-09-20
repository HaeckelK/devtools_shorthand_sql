# devtools_shorthand_sql

[![image](https://img.shields.io/pypi/v/devtools_shorthand_sql.svg)](https://pypi.python.org/pypi/devtools_shorthand_sql/)
[![image](https://img.shields.io/pypi/l/devtools_shorthand_sql.svg)](https://pypi.python.org/pypi/devtools_shorthand_sql/)
[![image](https://img.shields.io/pypi/pyversions/devtools_shorthand_sql.svg)](https://pypi.python.org/pypi/devtools_shorthand_sql/)
[![Travis](https://img.shields.io/travis/HaeckelK/devtools_shorthand_sql/master.svg?logo=travis)](https://travis-ci.org/HaeckelK/devtools_shorthand_sql)
[![readthedocs](https://readthedocs.org/projects/devtools-shorthand-sql/badge/?version=latest)](https://devtools-shorthand-sql.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/HaeckelK/devtools_shorthand_sql/branch/master/graph/badge.svg)](https://codecov.io/gh/HaeckelK/devtools_shorthand_sql)

## Overview

Aid for writing boilerplate python code for SQL work, including creation of tables, insert functions, unit testing and SQL, dependent on relational database management system selected.

- Documentation: https://devtools-shorthand-sql.readthedocs.io.

## Quickstart

Install the latest version of this software from the Python package index (PyPI):
```bash
pip install --upgrade devtools_shorthand_sql
```

Create a shorthand sql file e.g. shorthand.txt.
```
# photo
id,id
size,int
filename,text
date_taken,int
```

Run
```bash
devtools_shorthand_sql shorthand.txt
```

Notification that file created:
```bash
Info: Output saved to: shorthand_sql_created_functions.txt
```

Created file contains:

SQL statement for table creation:
```SQL
CREATE TABLE IF NOT EXISTS photo (
id INTEGER PRIMARY KEY,
size INT,
filename TEXT,
date_taken INT
);
```

Python function for data insertion:
```python
def insert_photo(id: int, size: int, filename: str, date_taken: int) -> int:
    params = (id, size, filename, date_taken)
    id = YOUR_CONNECTOR_EXECUTOR("""INSERT INTO photo (id, size, filename, date_taken) VALUES(?,?,?,?);""",
                                 params)
    return id
```

Python function for unit testing (pytest only):
```python
def test_insert_photo(YOUR_CLEAN_DB_FIXTURE):
    expected = (1, 160, '3RWL0C6QSU', 374)
    new_id = YOUR_MODULE.insert_photo(size=160, filename="3RWL0C6QSU", date_taken=374)
    result = YOUR_CONNECTOR_QUERY('SELECT * FROM photo').fetchall()[0]
    assert result == expected
    assert new_id == 1
```

## Requirements

Python 3.6 or later is required to run devtools_shorthand_sql.

No other third party packages are required.
