# nanoSQLite

`nanoSQLite` is a minimalistic SQLite wrapper tailored for those who feel JSON isn't quite right for data storage but
can't be bothered to dive deep into setting up a full-fledged ORM.

Sometimes, you just want a tiny step up without all the fuss.
With less than 300 lines of Python code, it provides an uncomplicated interface for managing SQLite databases.

Despite its simplicity, nanoSQLite offers a robust set of functionalities that enable you to interact with
SQLite databases seamlessly, without having to worry about managing cursors and connections manually.

It's designed to make working with SQLite in Python as straightforward and Pythonic as possible.

Ideal for small projects, prototypes, or when you just want a break from JSON but aren't ready for heavy ORM lifting.

## Features

- Easy Setup: Create connections to SQLite databases with a single function call.
- Intuitive Interface: Insert, update, and delete data using a simple syntax.
- Quick Prototyping: Manage data efficiently with a few lines of code, perfect for rapid prototyping and basic projects.
- Flexible: Execute custom SQL statements using the underlying `sqlite3.Cursor` and `sqlite3.Connection` objects.
- Robust: The `sqlite3` module is part of the Python standard library and has been extensively tested.
- Pythonic: The nanoSQLite API is designed to be as Pythonic as possible, which makes it intuitive and easy to use.
- Pure Python: nanoSQLite is written with no dependencies.
- Lightweight: nanoSQLite is a single-file module with less than 300 lines of code.
- Open Source: nanoSQLite is distributed under the MIT license.

## Examples

Most of database operations can be covered with the following examples:

1. Create a new SQLite database with a table:

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

2. Insert data:

    ```python
    db.insert("friends", {"name": "John", "age": 20, "height": 1.8, "is_cool": True})
    db.insert("friends", {"name": "Jane", "height": 1.7, "is_cool": False})
    db.insert("friends", {"name": "Bob"})
    ```

3. Update data:

    ```python
    db.update("friends", {"age": 21, "height": 1.9}, {"name": "John"})
    db.update("friends", {"age": 5}, {"name": "Bob"})
    ```

4. Delete data:

    ```python
    db.delete("friends", {"name": "Jane"})
    ```

5. Select data:

    ```python
    db.select("friends", ["name", "age", "height", "is_cool"], {"name": "Bob"})
    db.select_first("friends", ["name", "age", "height", "is_cool"], {"name": "Bob"})
    db.select_all("friends")
    ```

When more advanced functionality is required, you can still execute custom SQL statements,
using the underlying `sqlite3.Cursor` and `sqlite3.Connection` objects:

```python
data = [
    ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
    ("Monty Python's The Meaning of Life", 1983, 7.5),
    ("Monty Python's Life of Brian", 1979, 8.0),
]
db.cursor.executemany("INSERT INTO movie VALUES(?, ?, ?)", data)
db.connection.commit()
```

## Installation

You can install nanoSQLite from PyPI:

```bash
pip install nanoSQLite
```
