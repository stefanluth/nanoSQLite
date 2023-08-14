import sqlite3
import threading


def convert_to_bool(value) -> bool:
    """
    Convert a value to a boolean without Python's weirdness.
    """
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        if value.lower() in ["true", "1"]:
            return True
        elif value.lower() in ["false", "0"]:
            return False

    if isinstance(value, int) or isinstance(value, float):
        if value == 1:
            return True
        elif value == 0:
            return False

    raise TypeError(f"Cannot convert {type(value)} to boolean.")


def convert(func, value, typename):
    try:
        return func(value)
    except Exception as e:
        raise TypeError(f"Conversion of {value} to {typename} failed.") from e


TYPE_CONVERSIONS = {
    "BOOLEAN": convert_to_bool,
    "INTEGER": int,
    "REAL": float,
    "BLOB": lambda x: f"'{x}'",
    "TEXT": lambda x: f"'{x}'",
}


class Types:
    BOOLEAN = "BOOLEAN"
    INTEGER = "INTEGER"
    REAL = "REAL"
    BLOB = "BLOB"
    TEXT = "TEXT"


class NanoSQLite:
    """
    A simple database wrapper for SQLite3.
    """

    _lock = threading.Lock()
    tables = {}

    def __init__(self, name):
        """
        Create a new database.
        :param name: The name of the database.
        :type name: str
        """
        name = name if name.endswith(".sqlite") or name.endswith(".db") else f"{name}.sqlite"
        self.connection = sqlite3.connect(name, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def close(self):
        """
        Close the database connection.
        """
        self.connection.close()

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        with self._lock:
            with self.connection:
                return self.cursor.execute(query, params)

    def create_table(self, name: str, columns: dict[str, str]) -> None:
        """
        Create a table in the database.
        :param name: The name of the table.
        :type name: str
        :param columns: The columns of the table. Each column is a tuple of the column name and the column type.
        :type columns: dict[str, str]
        """

        if len(columns) == 0:
            raise ValueError("At least one column must be specified.")

        self.execute(f"CREATE TABLE {name} ({', '.join([f'{col} {columns[col]}' for col in columns])})")
        self.tables[name] = columns

    def delete_table(self, name: str) -> None:
        """
        Delete a table from the database.
        :param name: The name of the table.
        :type name: str
        """
        self.execute(f"DROP TABLE {name}")
        self.tables.pop(name)

    def insert(self, table: str, data: dict[str, str]) -> None:
        """
        Insert values into a table.
        :param table: The name of the table.
        :type table: str
        :param data: The data to insert into the table. The keys are the column names and the values are the values to insert.
        :type data: dict[str, str]
        """

        if len(data) == 0:
            raise ValueError("At least one column must be specified.")

        self._type_check(table, data)

        columns = ", ".join(data.keys())
        values = tuple(data.values())

        self.execute(f"INSERT INTO {table} ({columns}) VALUES ({', '.join(['?' for _ in values])})", values)

    def update(self, table: str, data: dict[str, str], where: dict[str, str] = {}) -> None:
        """
        Update values in a table.
        :param table: The name of the table.
        :type table: str
        :param data: The data to update in the table. The keys are the column names and the values are the values to update.
        :type data: dict[str, str]
        :param where: The WHERE clause of the query.
        :type where: str
        """

        if len(data) == 0:
            raise ValueError("At least one column must be specified.")

        self._type_check(table, data)

        converted_where = self._convert_where(table, where)
        new_data = ", ".join([f"{col} = ?" for col in data])
        values = tuple(data.values())

        self.execute(f"UPDATE {table} SET {new_data}{converted_where}", values)

    def delete(self, table: str, where: dict[str, str] = {}) -> None:
        """
        Delete values from a table.
        :param table: The name of the table.
        :type table: str
        :param where: The WHERE clause of the query.
        :type where: str
        """

        if len(where) == 0:
            raise ValueError("At least one column must be specified.")

        converted_where = self._convert_where(table, where)

        self.execute(f"DELETE FROM {table}{converted_where}")

    def select(self, table: str, columns: list[str], where: dict[str, str] = None) -> list[dict] | None:
        """
        Select values from a table.
        :param table: The name of the table.
        :type table: str
        :param columns: The columns to select.
        :type columns: list[str]
        :param where: The WHERE clause of the query.
        :type where: str
        :return: The selected values.
        :rtype: list[dict]
        """

        if len(columns) == 0:
            raise ValueError("At least one column must be specified.")

        converted_where = self._convert_where(table, where)
        rows = self.cursor.execute(f"SELECT {', '.join(columns)} FROM {table}{converted_where}")
        result = [dict(row) for row in rows]

        return result if len(result) > 0 else None

    def select_first(self, table: str, columns: list[str], where: dict[str, str] = {}) -> dict | None:
        """
        Select the first value from a table.
        :param table: The name of the table.
        :type table: str
        :param columns: The columns to select.
        :type columns: list[str]
        :param where: The WHERE clause of the query.
        :type where: str
        :return: The selected values.
        :rtype: dict
        """

        if len(columns) == 0:
            raise ValueError("At least one column must be specified.")

        converted_where = self._convert_where(table, where)
        rows = self.cursor.execute(f"SELECT {', '.join(columns)} FROM {table}{converted_where}").fetchone()

        return dict(rows) if rows is not None else None

    def select_all(self, table: str) -> list[dict] | None:
        """
        Select all values from a table.
        :param table: The name of the table.
        :type table: str
        :return: The selected values.
        :rtype: list[dict]
        """

        rows = self.cursor.execute(f"SELECT * FROM {table}")
        result = [dict(row) for row in rows]

        return result if len(result) > 0 else None

    def _type_check(self, table, data):
        for col in data:
            convert(TYPE_CONVERSIONS.get(self.tables[table][col], lambda x: x), data[col], self.tables[table][col])

    def _convert_where(self, table: str, where: dict[str, str] = {}) -> str:
        if len(where) == 0:
            return ""

        converted_where = [
            f"{col} = {convert(TYPE_CONVERSIONS.get(self.tables[table][col], lambda x: x), where[col], self.tables[table][col])}"
            for col in where
        ]

        return f" WHERE {', '.join(converted_where)}"
