import contextlib
import sqlite3
from functools import wraps

from settings import DB_FOLDER, DB_COMBINATIONS_NAME, DB_URLS_NAME, DOMAIN_NAME


def connect_db(db_name):
    @wraps(db_name)
    def outer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with contextlib.closing(sqlite3.connect(DB_FOLDER + db_name)) as conn:
                with conn:
                    with contextlib.closing(conn.cursor()) as cursor:
                        result = func(cursor, *args, **kwargs)
                        conn.commit()
            return result
        return wrapper
    return outer


@connect_db(DB_COMBINATIONS_NAME)
def take_combination_from_db(cursor) -> tuple[int, str]:
    cursor.execute("""SELECT id, short_combination FROM combinations
    WHERE id = (SELECT MAX(id) FROM combinations)""")
    combination_id, short_combination = cursor.fetchall()[0]
    return combination_id, short_combination


@connect_db(DB_COMBINATIONS_NAME)
def delete_last_combination_from_db(cursor, last_combination_id: int) -> None:
    cursor.execute("""DELETE FROM combinations
    WHERE id = (?)""", (last_combination_id,))


def get_combination():
    combination_id, short_combination = take_combination_from_db()
    delete_last_combination_from_db(combination_id)
    return short_combination


@connect_db(DB_URLS_NAME)
def add_combination_to_urls_db(cursor, long_url: str) -> str:
    long_url = make_correct_url(long_url)
    combination = get_combination()
    cursor.execute("""INSERT INTO urls (long_url, short_combination)
    VALUES (?, ?)""", (long_url, combination,))
    return f'{DOMAIN_NAME}/{combination}'


def make_correct_url(long_url: str) -> str or None:
    if type(long_url) != str:
        raise long_url is None
    if '://' in long_url[:10]:
        return long_url
    return 'http://' + long_url


def make_a_short_url(long_url: str) -> str:
    return add_combination_to_urls_db(long_url)
