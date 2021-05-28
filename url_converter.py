import contextlib
import sqlite3
import time
from random import choice
from string import ascii_letters, digits

from settings import DB_FOLDER, DB_URLS_NAME, DOMAIN_NAME


def create_combination(count_characters=5) -> str:
    """
    Возвращает случайную комбинацию вида 'Qa5Lz', длиной в count_characters.
    """
    return ''.join(choice(ascii_letters + digits) for _ in range(count_characters))


def make_correct_url(long_url: str) -> str or None:
    """
    Дабы редирект происходил по правильным ссылкам, в базу кладётся их предполагаемый протокол.
    Если юзер передаёт протокол самостоятельно - он и кладётся, в противном случае делаем http://
    """
    if type(long_url) != str:
        raise long_url is None
    if '://' in long_url[:10]:
        return long_url
    return 'http://' + long_url


def convert_to_short_url(long_url: str) -> str:
    """
    Циклично генерируем комбинацию до тех пор, в базе её не окажется.
    Если комбинация в базе есть - cursor.rowcount вернёт 0.
    Если успешно вставил - вернёт количество вставленных строк.
    """
    with contextlib.closing(sqlite3.connect(DB_FOLDER + DB_URLS_NAME)) as conn:
        with conn:
            with contextlib.closing(conn.cursor()) as cursor:
                long_url = make_correct_url(long_url)
                while cursor.rowcount < 1:
                    combination = create_combination()
                    cursor.execute("""INSERT OR IGNORE INTO urls (long_url, short_combination, creation_time)
                    VALUES (?, ?, ?)""", (long_url, combination, int(time.time()),))
                return f'{DOMAIN_NAME}/{combination}'


def convert_to_long_url(short_url: str) -> str:
    """
    Идёт в базу, ищет там короткую комбинацию.
    Если она имеется - возвращает длинную ссылку.
    Если комбинации нет - возвращает None.
    """
    with contextlib.closing(sqlite3.connect(DB_FOLDER + DB_URLS_NAME)) as conn:
        with conn:
            with contextlib.closing(conn.cursor()) as cursor:
                cursor.execute("""SELECT long_url FROM urls
                WHERE short_combination = (?)""", (short_url,))
                original_url = cursor.fetchall()
                return original_url[0][0] if original_url else None
