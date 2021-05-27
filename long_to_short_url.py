import sqlite3

from settings import DB_FOLDER, DB_COMBINATIONS_NAME, DB_URLS_NAME, DOMAIN_NAME


# TODO сделать коннекты к БД в начале скрипта? Сделать их через контекстный менеджер в каждой функции?

def take_combination_from_db() -> tuple[int, str]:
    conn = sqlite3.connect(DB_FOLDER + DB_COMBINATIONS_NAME)
    cursor = conn.cursor()
    cursor.execute("""SELECT id, short_combination FROM combinations
    WHERE id = (SELECT MAX(id) FROM combinations)""")
    combination_id, short_combination = cursor.fetchall()[0]
    return combination_id, short_combination


def delete_last_combination_from_db(last_combination_id: int) -> None:
    conn = sqlite3.connect(DB_FOLDER + DB_COMBINATIONS_NAME)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM combinations
    WHERE id = (?)""", (last_combination_id,))
    conn.commit()


def get_combination() -> str:
    combination_id, short_combination = take_combination_from_db()
    delete_last_combination_from_db(combination_id)
    return short_combination


def add_combination_to_urls_db(long_url: str) -> str:
    """
    Связывает ссылку от пользователя и короткую комбинацию, кладя их в базу.
    """
    if type(long_url) == str:
        url = make_correct_url(long_url)
    else:
        raise long_url is None
    conn = sqlite3.connect(DB_FOLDER + DB_URLS_NAME)
    cursor = conn.cursor()
    combination = get_combination()
    cursor.execute("""INSERT INTO urls (long_url, short_combination)
    VALUES (?, ?)""", (url, combination,))
    conn.commit()
    return f'{DOMAIN_NAME}/{combination}'


def make_correct_url(url: str) -> str or None:
    """
    Если пользователь добавляет ссылку на протокол, отличный от HTTP, то в базу не будет добавлено http://
    Если пользователь не указал протокол совсем, то добавляется http://
    """
    if '://' in url[:10]:
        return url
    return 'http://' + url


def make_a_short_url(long_url: str) -> str:
    """
    Переименовывает функцию для удобного использования в другом контексте.
    """
    return add_combination_to_urls_db(long_url)
