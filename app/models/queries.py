import sqlite3
from app.models.db import db


def get_all(table: str) -> list[sqlite3.Row]:
    return execute_query(f"SELECT * FROM {table}")


def get_one(table: str, id: int | str) -> sqlite3.Row | None:
    query = f"SELECT * FROM {table} WHERE id=?"
    data = execute_query(query, (id,))
    return data[0] if data else None


def get_group() -> sqlite3.Row:
    query = f"SELECT * FROM GroupTable"
    data = execute_query(query)
    return data[0]


def update_group_bio(bio: str) -> None:
    query = f"UPDATE GroupTable SET bio=? WHERE name=?"
    execute_query(query, (bio, "The Grapefruits Duo"), is_update=True)


def execute_query(
    query: str, params: tuple | None = None, is_update=False
) -> list[sqlite3.Row]:
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)
    data = cursor.fetchall()
    if is_update:
        conn.commit()
    conn.close()
    return data
