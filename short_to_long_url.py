import sqlite3

from settings import DB_FOLDER, DB_URLS_NAME


def original_url_from_short(short_url: str) -> str:
    """
    Идёт в базу urls.db, ищем там короткую комбинацию. Если таковая имеется - возвращает длинную ссылку.
    Если такой комбинации нет - возвращает None.
    """
    conn = sqlite3.connect(DB_FOLDER + DB_URLS_NAME)
    cursor = conn.cursor()
    cursor.execute("""SELECT long_url FROM urls
    WHERE short_combination = (?)""", (short_url,))
    original_url = cursor.fetchall()
    return original_url[0][0] if original_url else None
