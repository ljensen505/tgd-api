import sqlite3
from app.models.db import DB
from app.models.models import CarouselImage, Headshot, Musician, Event


def get_headshots_by_musician(musician_id: int) -> list[sqlite3.Row]:
    return execute_query("SELECT * FROM Headshots WHERE musician_id=?", (musician_id,))


def update_musician(m: Musician):
    query = "UPDATE Musicians SET bio=?, headshot_id=? WHERE id=?"
    execute_query(query, (m.bio, m.headshot_id, m.id), is_update=True)


def insert_event(event: Event):
    query = "INSERT INTO Events (name, date, description, image_url, location, ticket_url) VALUES(?, ?, ?, ?, ?, ?)"
    params = (
        event.name,
        event.date,
        event.description,
        event.image_url,
        event.location,
        event.ticket_url,
    )
    execute_query(query, params, is_update=True, get_id=True, modal_obj=event)


def insert_carousel_img(img: CarouselImage):
    query = "INSERT INTO CarouselImages (id, url) VALUES (?,?)"
    params = (img.id, img.url)
    execute_query(query, params, is_update=True)


def insert_headshot(img: Headshot) -> None:
    query = "INSERT INTO Headshots (id, url, musician_id) VALUES (?,?,?)"
    params = (img.id, img.url, img.musician_id)
    execute_query(query, params, is_update=True)


def delete(table: str, id: int | str) -> None:
    query = f"DELETE FROM {table} WHERE id=?"
    execute_query(query, (id,), is_update=True)


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
    query: str,
    params: tuple | None = None,
    is_update=False,
    get_id=False,
    modal_obj=None,
) -> list[sqlite3.Row]:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)
    if get_id and modal_obj is not None:
        last_row_id = cursor.lastrowid
        modal_obj.id = last_row_id
    data = cursor.fetchall()
    if is_update:
        conn.commit()
    conn.close()
    return data
