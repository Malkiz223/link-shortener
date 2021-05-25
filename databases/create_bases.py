import sqlite3

from settings import DB_COMBINATIONS_NAME, DB_URLS_NAME


def create_combinations_database():
    """
    Создаём базу для хранения комбинаций коротких ссылок.
    id используется для доступа удобного к нижней комбинации.
    """
    connect = sqlite3.connect(DB_COMBINATIONS_NAME)
    cursor = connect.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS combinations (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           short_combination VARCHAR(5))""")


def create_urls_database():
    """
    База, в которой хранятся ссылки пользователей и короткие комбинации, к которым они привязаны.
    long_url - для ссылок пользователей, short_combinations - для коротких ссылок.
    """
    connect = sqlite3.connect(DB_URLS_NAME)
    cursor = connect.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS urls (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           long_url VARCHAR(2000),
           short_combination VARCHAR(5))""")


if __name__ == '__main__':
    create_combinations_database()
    create_urls_database()
