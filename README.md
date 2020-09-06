# devtools_shorthand_sql

[![image](https://img.shields.io/pypi/v/devtools_shorthand_sql.svg)](https://pypi.python.org/pypi/devtools_shorthand_sql/)
[![image](https://img.shields.io/pypi/l/devtools_shorthand_sql.svg)](https://pypi.python.org/pypi/devtools_shorthand_sql/)
[![image](https://img.shields.io/pypi/pyversions/devtools_shorthand_sql.svg)](https://pypi.python.org/pypi/devtools_shorthand_sql/)
[![Travis](https://img.shields.io/travis/HaeckelK/devtools_shorthand_sql/master.svg?logo=travis)](https://travis-ci.org/HaeckelK/devtools_shorthand_sql)
[![readthedocs](https://readthedocs.org/projects/devtools-shorthand-sql/badge/?version=latest)](https://devtools-shorthand-sql.readthedocs.io/en/latest/?badge=latest)


## Overview

Aid for writing boilerplate python code for SQL work, including creation of tables, insert functions, unit testing and SQL, dependent on relational database management system selected.

- Documentation: https://devtools-shorthand-sql.readthedocs.io.


## Features

- TODO

## Requirements

You need Python 3.6 or later to run devtools_shorthand_sql.

No other third party packages are required.

## Quickstart

Install the latest version of this software from the Python package index (PyPI):
```bash
pip install --upgrade devtools_shorthand_sql
```

Create a shorthand sql file e.g. shorthand.txt.
```
# table photo
size int
filename text
date_taken int
```

Run
```bash
devtools_shorthand_sql shorthand.txt
```

SQL statement for table creation:
```SQL
CREATE TABLE IF NOT EXISTS photo (
id INTEGER PRIMARY KEY,
size int,
filename text,
date_taken int
);
```

Python function for data insertion:
```python
def insert_photo(size: int, filename: str, date_taken: int) -> int:
    params = (None, size, filename, date_taken)
    id = YOUR_CONNECTOR_EXECUTOR("""INSERT INTO photo (id, size, filename, date_taken) VALUES(?,?,?,?);""",
                                 params)
    return id
```

Python function for unit testing:
```python
def test_insert_photo(YOUR_CLEAN_DB_FIXTURE):
    expected = (1, 999, '123fakestreet', 999)
    YOUR_MODULE.insert_photo(size=999, filename="123fakestreet", date_taken=999)
    result = YOUR_CONNECTOR_QUERY('SELECT * FROM photo').fetchall()[0]
    assert result == expected
```
