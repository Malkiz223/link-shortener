import sqlite3
import settings


def create_combinations_database():
    connect = sqlite3.connect(settings.DB_COMBINATIONS_NAME)
    cursor = connect.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS combinations (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           short_combination VARCHAR(5))""")


def create_urls_database():
    connect = sqlite3.connect(settings.DB_URLS_NAME)
    cursor = connect.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS urls (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           long_url VARCHAR(2000),
           short_combination VARCHAR(5))""")


if __name__ == '__main__':
    create_combinations_database()
    create_urls_database()
