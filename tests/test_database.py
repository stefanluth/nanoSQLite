import os

import pytest

from nanoSQLite import NanoSQLite, Types


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
            "name": Types.TEXT,
            "age": Types.INTEGER,
            "height": Types.REAL,
            "is_cool": Types.BOOLEAN,
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
            "name": Types.TEXT,
            "age": Types.INTEGER,
            "height": Types.REAL,
            "is_cool": Types.BOOLEAN,
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
            "name": Types.TEXT,
            "age": Types.INTEGER,
            "height": Types.REAL,
            "is_cool": Types.BOOLEAN,
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
            "name": Types.TEXT,
            "age": Types.INTEGER,
            "height": Types.REAL,
            "is_cool": Types.BOOLEAN,
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
            "name": Types.TEXT,
            "age": Types.INTEGER,
            "height": Types.REAL,
            "is_cool": Types.BOOLEAN,
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
            "name": Types.TEXT,
            "age": Types.INTEGER,
            "height": Types.REAL,
            "is_cool": Types.BOOLEAN,
        },
    )

    db.delete_table("test_table")

    assert db.tables == {}


def test_wrong_type_data_insertion(db: NanoSQLite):
    db.create_table(
        "test_table",
        {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": Types.TEXT,
            "age": Types.INTEGER,
            "height": Types.REAL,
            "is_cool": Types.BOOLEAN,
        },
    )

    with pytest.raises(TypeError):
        db.insert("test_table", {"name": "John", "age": 20, "height": 1.8, "is_cool": "bool"})

    with pytest.raises(TypeError):
        db.insert("test_table", {"name": "John", "age": 20, "height": "eighteen.three", "is_cool": True})

    with pytest.raises(TypeError):
        db.insert("test_table", {"name": "John", "age": "twelve", "height": 1, "is_cool": True})


def test_attempt_sql_injection(db: NanoSQLite):
    db.create_table(
        "test_table",
        {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": Types.TEXT,
            "age": Types.INTEGER,
            "height": Types.REAL,
            "is_cool": Types.BOOLEAN,
        },
    )

    with pytest.raises(TypeError):
        db.insert("test_table", {"name": "John", "age": 20, "height": 1.8, "is_cool": True, "is_cool": "1 OR 1=1"})

    db.insert(
        "test_table",
        {"name": "John; DROP TABLE test_table", "age": 20, "height": 1.8, "is_cool": True},
    )

    assert db.select_first("test_table", ["name", "age"], {"age": 20}) == {
        "name": "John; DROP TABLE test_table",
        "age": 20,
    }
