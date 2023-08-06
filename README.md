# nanoSQLite

`nanoSQLite` is a lightweight Python wrapper for SQLite.
With around 200 lines of Python code, it provides an uncomplicated interface for managing SQLite databases.

Despite its simplicity, nanoSQLite offers a robust set of functionalities that enable you to interact with
SQLite databases seamlessly, without having to worry about managing cursors and connections manually.

It's designed to make working with SQLite in Python as straightforward and Pythonic as possible.

## Features

- Easy Setup: Create connections to SQLite databases with a single function call.
- Simple Query Execution:
Execute your SQL commands easily, without having to manage cursors and connections manually.
- Transaction Management:
Handle transactions effectively with commit and rollback operations.
- Pythonic Interface:
The nanoSQLite API is designed to be as Pythonic as possible, which makes it intuitive and easy to use.

## Examples

Create a new SQLite database with a table:

```python
from nanoSQLite import NanoSQLite

db = NanoSQLite("people")
db.create_table(
    "friends",
    {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT",
        "age": "INTEGER",
        "height": "REAL",
        "is_cool": "BOOLEAN",
    },
)
```

Insert data:

```python
db.insert("friends", {"name": "John", "age": 20, "height": 1.8, "is_cool": True})
db.insert("friends", {"name": "Jane", "height": 1.7, "is_cool": False})
db.insert("friends", {"name": "Bob"})
```

Update data:

```python
db.update("friends", {"age": 21, "height": 1.9}, {"name": "John"})
db.update("friends", {"age": 5}, {"name": "Bob"})
```

Delete data:

```python
db.delete("friends", {"name": "Jane"})
```

Select data:

```python
db.select("friends", ["name", "age", "height", "is_cool"], {"name": "Bob"})
db.select_first("friends", ["name", "age", "height", "is_cool"], {"name": "Bob"})
db.select_all("friends")
```

## Installation

You can install nanoSQLite from PyPI:

```bash
pip install nanoSQLite
```
