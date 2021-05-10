import sqlite3
import settings


def take_combination_from_db() -> tuple[int, str]:
    conn = sqlite3.connect('databases/' + settings.DB_COMBINATIONS_NAME)
    cursor = conn.cursor()
    cursor.execute("""SELECT id, short_combination FROM combinations
    WHERE id = (SELECT MAX(id) FROM combinations)""")
    combination_id, short_combination = cursor.fetchall()[0]
    return combination_id, short_combination


def delete_last_combination_from_db(last_combination_id: int) -> None:
    conn = sqlite3.connect('databases/' + settings.DB_COMBINATIONS_NAME)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM combinations
    WHERE id = (?)""", (last_combination_id, ))
    conn.commit()


def get_combination():
    combination_id, short_combination = take_combination_from_db()
    delete_last_combination_from_db(combination_id)
    return short_combination


def add_combination_to_urls_db(long_url: str) -> str:
    conn = sqlite3.connect('databases/' + settings.DB_URLS_NAME)
    cursor = conn.cursor()
    if type(long_url) == str:
        url = make_correct_url(long_url)
    else:
        raise long_url is None
    combination = get_combination()
    cursor.execute("""INSERT INTO urls (long_url, short_combination)
    VALUES (?, ?)""", (url, combination, ))
    conn.commit()
    return f'{settings.DOMAIN_NAME}/{combination}'


def make_correct_url(url: str) -> str or None:
    if url.startswith('http://') or url.startswith('https://'):
        return url
    return 'http://' + url


def make_a_short_url(long_url: str) -> str:
    return add_combination_to_urls_db(long_url)
