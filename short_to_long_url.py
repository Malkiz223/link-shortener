import sqlite3
import settings


def return_original_url_from_short(short_url: str) -> str:
    conn = sqlite3.connect('databases/' + settings.DB_URLS_NAME)
    cursor = conn.cursor()
    cursor.execute("""SELECT long_url FROM urls
    WHERE short_combination = (?)""", (short_url,))
    original_url = cursor.fetchall()
    return original_url[0][0] if original_url else None
