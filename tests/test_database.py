import os

import pytest

from nanoSQLite import NanoSQLite


@pytest.fixture()
def db():
    db = NanoSQLite("tests/test")
    yield db
    db.close()
    if os.path.exists("tests/test.sqlite"):
        os.remove("tests/test.sqlite")


def test_create_empty_table(db: NanoSQLite):
    db.create_table(
        "test_table",
        {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT",
            "age": "INTEGER",
            "height": "REAL",
            "is_cool": "BOOLEAN",
        },
    )

    assert db.select_all("test_table") == None
    assert dict(
        db.cursor.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='test_table'").fetchone()
    ) == {
        "name": "test_table",
        "rootpage": 2,
        "sql": "CREATE TABLE test_table (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, height REAL, is_cool BOOLEAN)",
        "tbl_name": "test_table",
        "type": "table",
    }


def test_insert_data(db: NanoSQLite):
    db.create_table(
        "test_table",
        {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT",
            "age": "INTEGER",
            "height": "REAL",
            "is_cool": "BOOLEAN",
        },
    )

    db.insert("test_table", {"name": "John", "age": 20, "height": 1.8, "is_cool": True})
    db.insert("test_table", {"name": "Jane", "height": 1.7, "is_cool": False})
    db.insert("test_table", {"name": "Bob"})
    db.insert("test_table", {"name": "Bob"})

    assert db.select_all("test_table") == [
        {"id": 1, "name": "John", "age": 20, "height": 1.8, "is_cool": 1},
        {"id": 2, "name": "Jane", "age": None, "height": 1.7, "is_cool": 0},
        {"id": 3, "name": "Bob", "age": None, "height": None, "is_cool": None},
        {"id": 4, "name": "Bob", "age": None, "height": None, "is_cool": None},
    ]


def test_select_data(db: NanoSQLite):
    db.create_table(
        "test_table",
        {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT",
            "age": "INTEGER",
            "height": "REAL",
            "is_cool": "BOOLEAN",
        },
    )

    db.insert("test_table", {"name": "John", "age": 20, "height": 1.8, "is_cool": True})
    db.insert("test_table", {"name": "Jane", "height": 1.7, "is_cool": False})
    db.insert("test_table", {"name": "Bob"})
    db.insert("test_table", {"name": "Bob"})

    assert db.select("test_table", ["name", "age"], {"age": 20}) == [
        {"name": "John", "age": 20},
    ]


def test_update_data(db: NanoSQLite):
    db.create_table(
        "test_table",
        {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT",
            "age": "INTEGER",
            "height": "REAL",
            "is_cool": "BOOLEAN",
        },
    )

    db.insert("test_table", {"name": "John", "age": 20, "height": 1.8, "is_cool": True})
    db.insert("test_table", {"name": "Jane", "height": 1.7, "is_cool": False})
    db.insert("test_table", {"name": "Bob"})
    db.insert("test_table", {"name": "Bob"})

    db.update("test_table", {"age": 21, "height": 1.9}, {"name": "John"})
    db.update("test_table", {"age": 5}, {"name": "Bob"})

    assert db.select_all("test_table") == [
        {"id": 1, "name": "John", "age": 21, "height": 1.9, "is_cool": 1},
        {"id": 2, "name": "Jane", "age": None, "height": 1.7, "is_cool": 0},
        {"id": 3, "name": "Bob", "age": 5, "height": None, "is_cool": None},
        {"id": 4, "name": "Bob", "age": 5, "height": None, "is_cool": None},
    ]


def test_delete_data(db: NanoSQLite):
    db.create_table(
        "test_table",
        {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT",
            "age": "INTEGER",
            "height": "REAL",
            "is_cool": "BOOLEAN",
        },
    )

    db.insert("test_table", {"name": "John", "age": 20, "height": 1.8, "is_cool": True})
    db.insert("test_table", {"name": "Jane", "height": 1.7, "is_cool": False})
    db.insert("test_table", {"name": "Bob"})
    db.insert("test_table", {"name": "Bob"})

    db.delete("test_table", {"name": "Bob"})

    assert db.select_all("test_table") == [
        {"id": 1, "name": "John", "age": 20, "height": 1.8, "is_cool": 1},
        {"id": 2, "name": "Jane", "age": None, "height": 1.7, "is_cool": 0},
    ]


def test_drop_table(db: NanoSQLite):
    db.create_table(
        "test_table",
        {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT",
            "age": "INTEGER",
            "height": "REAL",
            "is_cool": "BOOLEAN",
        },
    )

    db.delete_table("test_table")

    assert db.tables == {}
