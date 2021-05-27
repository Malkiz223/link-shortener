import sqlite3

from settings import DB_URLS_NAME


def create_urls_database():
    """
    База, в которой хранятся ссылки пользователей и короткие комбинации, к которым они привязаны.
    long_url - для ссылок пользователей.
    short_combinations - для коротких ссылок.
    creation_time - для автоматической чистки старых ссылок, дабы снизить коллизии.
    """
    connect = sqlite3.connect(DB_URLS_NAME)
    cursor = connect.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS urls (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           long_url VARCHAR(2000) NOT NULL,
           short_combination VARCHAR(7) UNIQUE NOT NULL,
           creation_time INTEGER(10) NOT NULL)
           """)


if __name__ == '__main__':
    create_urls_database()
